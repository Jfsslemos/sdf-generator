#!/usr/bin/env python3
"""Regularize a floor subset in a triangle mesh.

Preferred selection uses the explicit instance id exported by the DM-NeRF
runner. RGB selection is retained only for legacy artifacts. The script fits a
plane using RANSAC, projects only selected floor vertices onto it and,
optionally, aligns the whole scene so the plane becomes coordinate zero.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import trimesh


def parse_rgb(value: str):
    vals = tuple(int(v) for v in value.split(','))
    if len(vals) != 3 or any(v < 0 or v > 255 for v in vals):
        raise argparse.ArgumentTypeError('RGB deve ser R,G,B com valores em 0..255')
    return vals


def fit_plane_svd(points: np.ndarray):
    center = points.mean(axis=0)
    _, _, vh = np.linalg.svd(points - center, full_matrices=False)
    normal = vh[-1]
    normal = normal / np.linalg.norm(normal)
    d = -float(np.dot(normal, center))
    return normal, d


def ransac_plane(points: np.ndarray, threshold: float, iterations: int, seed: int):
    if len(points) < 3:
        raise ValueError('São necessários ao menos 3 vértices para estimar um plano.')
    rng = np.random.default_rng(seed)
    best_mask = None
    best_count = -1
    for _ in range(iterations):
        sample = points[rng.choice(len(points), 3, replace=False)]
        normal = np.cross(sample[1] - sample[0], sample[2] - sample[0])
        norm = np.linalg.norm(normal)
        if norm < 1e-10:
            continue
        normal /= norm
        d = -float(np.dot(normal, sample[0]))
        mask = np.abs(points @ normal + d) <= threshold
        count = int(mask.sum())
        if count > best_count:
            best_count = count
            best_mask = mask
    if best_mask is None or best_mask.sum() < 3:
        raise RuntimeError('RANSAC não encontrou plano válido.')
    normal, d = fit_plane_svd(points[best_mask])
    return normal, d, best_mask


def rotation_from_a_to_b(a: np.ndarray, b: np.ndarray):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    v = np.cross(a, b)
    c = float(np.dot(a, b))
    if c < -0.999999:
        axis = np.array([1.0, 0.0, 0.0])
        if abs(a[0]) > 0.9:
            axis = np.array([0.0, 1.0, 0.0])
        v = np.cross(a, axis)
        v /= np.linalg.norm(v)
        return -np.eye(3) + 2.0 * np.outer(v, v)
    s = np.linalg.norm(v)
    if s < 1e-12:
        return np.eye(3)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * ((1 - c) / (s * s))


def selection_mask(mesh, rgb=None, labels=None, instance_id=None):
    if labels is not None:
        data=np.load(labels)
        ids=np.asarray(data['vertex_instance_id']).reshape(-1)
        if len(ids)!=len(mesh.vertices):
            raise ValueError('labels/mesh vertex count mismatch')
        return ids==instance_id, {'instance_id':int(instance_id),'labels':str(labels)}
    colors=np.asarray(mesh.visual.vertex_colors)
    if colors.ndim!=2 or colors.shape[1]<3:
        raise ValueError('A mesh não possui cores por vértice.')
    return np.all(colors[:,:3].astype(np.uint8)==np.array(rgb,dtype=np.uint8),axis=1), {'rgb':list(rgb)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mesh', type=Path)
    ap.add_argument('output', type=Path)
    sel=ap.add_mutually_exclusive_group(required=True)
    sel.add_argument('--rgb', type=parse_rgb, help='seletor legado R,G,B')
    sel.add_argument('--instance-id', type=int, help='seletor preferido: ID explícito da instância do piso')
    ap.add_argument('--labels', type=Path, help='instance_labels.npz; obrigatório com --instance-id')
    ap.add_argument('--threshold', type=float, default=0.02)
    ap.add_argument('--iterations', type=int, default=2000)
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--align-scene', action='store_true')
    ap.add_argument('--up-axis', choices=['x','y','z'], default='z')
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    if (args.instance_id is None)!=(args.labels is None):
        ap.error('--instance-id and --labels devem ser fornecidos juntos')

    mesh = trimesh.load(args.mesh, process=False)
    if not isinstance(mesh, trimesh.Trimesh):
        raise TypeError('Esperada uma única TriangleMesh.')
    mask,selector = selection_mask(mesh,args.rgb,args.labels,args.instance_id)
    if mask.sum() < 3:
        raise ValueError(f'A seleção contém apenas {int(mask.sum())} vértices.')

    vertices = np.asarray(mesh.vertices).copy()
    floor = vertices[mask]
    normal, d, inliers = ransac_plane(floor, args.threshold, args.iterations, args.seed)
    axis_index = {'x':0,'y':1,'z':2}[args.up_axis]
    target = np.zeros(3); target[axis_index] = 1.0
    if np.dot(normal, target) < 0:
        normal = -normal; d = -d

    before = np.abs(floor @ normal + d)
    signed = floor @ normal + d
    vertices[mask] = floor - signed[:, None] * normal[None, :]

    transform = np.eye(4)
    if args.align_scene:
        point_on_plane = -d * normal
        R = rotation_from_a_to_b(normal, target)
        vertices = (R @ vertices.T).T
        rotated_plane_point = R @ point_on_plane
        translation = np.zeros(3)
        translation[axis_index] = -rotated_plane_point[axis_index]
        vertices += translation
        transform[:3,:3] = R
        transform[:3,3] = translation

    out_mesh = mesh.copy()
    out_mesh.vertices = vertices
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out_mesh.export(args.output)

    after_floor = vertices[mask]
    after_residual = np.abs(after_floor[:, axis_index]) if args.align_scene else np.abs(after_floor @ normal + d)
    report = {
        'input':str(args.mesh),'output':str(args.output),'selector':selector,
        'selected_vertices':int(mask.sum()),'plane_normal':normal.tolist(),'plane_d':float(d),
        'ransac_threshold':args.threshold,'ransac_inlier_fraction':float(inliers.mean()),
        'before_mean_abs_distance':float(before.mean()),
        'before_rmse_distance':float(np.sqrt(np.mean(before**2))),
        'before_p95_abs_distance':float(np.percentile(before,95)),
        'after_mean_abs_distance':float(after_residual.mean()),
        'after_rmse_distance':float(np.sqrt(np.mean(after_residual**2))),
        'after_p95_abs_distance':float(np.percentile(after_residual,95)),
        'align_scene':bool(args.align_scene),'up_axis':args.up_axis,
        'scene_transform':transform.tolist(),
    }
    print(json.dumps(report, indent=2))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
