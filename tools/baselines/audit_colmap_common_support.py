#!/usr/bin/env python3
"""Audit COLMAP against DM-NeRF A0 on the same DM-SR scene support.

COLMAP operates in the DM-SR/OpenGL world coordinates used by the camera
poses. The upstream DM-NeRF mesher queries the neural field after mapping
scene coordinates to [x, -z, y], while exporting the mesh back in scene
coordinates. Therefore the inverse map used here is:

    scene = [colmap_x, colmap_z, -colmap_y]

For a fair geometry comparison, the COLMAP cloud is clipped to the same
oriented support used by the pinned upstream mesher and then deterministically
subsampled to 200,000 points, matching the A0/GT evaluation cardinality.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import trimesh
from scipy.spatial import cKDTree


SCENE_EXTENTS = np.array([1.9, 7.0, 7.0], dtype=np.float64)


def sample_surface(mesh: trimesh.Trimesh, n: int, seed: int) -> np.ndarray:
    state = np.random.get_state()
    np.random.seed(seed)
    try:
        pts, _ = trimesh.sample.sample_surface(mesh, n)
    finally:
        np.random.set_state(state)
    return np.asarray(pts)


def dmnerf_scene_support(gt_mesh: trimesh.Trimesh):
    to_origin, _ = trimesh.bounds.oriented_bounds(gt_mesh)
    scene_transform = np.linalg.inv(to_origin)
    center = scene_transform[:3, 3]
    rotation = scene_transform[:3, :3]
    return center, rotation


def colmap_to_scene(points: np.ndarray) -> np.ndarray:
    out = np.empty_like(points, dtype=np.float64)
    out[:, 0] = points[:, 0]
    out[:, 1] = points[:, 2]
    out[:, 2] = -points[:, 1]
    return out


def crop_common_support(points: np.ndarray, center: np.ndarray, rotation: np.ndarray):
    local = (points - center) @ rotation
    half = SCENE_EXTENTS / 2.0
    mask = np.all(np.abs(local) <= half + 1e-9, axis=1)
    return points[mask], mask


def metrics(pred: np.ndarray, gt: np.ndarray, thresholds):
    gt_tree = cKDTree(gt)
    pred_tree = cKDTree(pred)
    d_pred, _ = gt_tree.query(pred, k=1)
    d_gt, _ = pred_tree.query(gt, k=1)
    out = {
        "mean_pred_to_gt": float(d_pred.mean()),
        "mean_gt_to_pred": float(d_gt.mean()),
        "chamfer_l1_symmetric": float(d_pred.mean() + d_gt.mean()),
        "rmse_pred_to_gt": float(np.sqrt(np.mean(d_pred**2))),
        "rmse_gt_to_pred": float(np.sqrt(np.mean(d_gt**2))),
    }
    for th in thresholds:
        precision = float(np.mean(d_pred <= th))
        completeness = float(np.mean(d_gt <= th))
        fscore = 0.0 if precision + completeness == 0 else (
            2 * precision * completeness / (precision + completeness)
        )
        out[f"precision@{th:g}"] = precision
        out[f"completeness@{th:g}"] = completeness
        out[f"fscore@{th:g}"] = fscore
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("colmap", type=Path, help="COLMAP fused.ply")
    ap.add_argument("ground_truth", type=Path, help="DM-SR study.ply")
    ap.add_argument("a0", type=Path, help="DM-NeRF A0 mesh_geometry.ply")
    ap.add_argument("--samples", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--thresholds", type=float, nargs="+", default=[0.01, 0.02, 0.05])
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--sample-out", type=Path)
    args = ap.parse_args()

    gt_mesh = trimesh.load(args.ground_truth, process=False)
    a0_mesh = trimesh.load(args.a0, process=False)
    colmap = trimesh.load(args.colmap, process=False)
    if not isinstance(gt_mesh, trimesh.Trimesh) or not isinstance(a0_mesh, trimesh.Trimesh):
        raise TypeError("GT and A0 must be triangle meshes")
    if not isinstance(colmap, trimesh.points.PointCloud):
        raise TypeError("COLMAP fused.ply must be a point cloud")

    center, rotation = dmnerf_scene_support(gt_mesh)
    colmap_scene = colmap_to_scene(np.asarray(colmap.vertices))
    colmap_common, mask = crop_common_support(colmap_scene, center, rotation)
    if len(colmap_common) < args.samples:
        raise RuntimeError("Not enough COLMAP points inside common support")

    rng = np.random.default_rng(args.seed)
    idx = rng.choice(len(colmap_common), size=args.samples, replace=False)
    colmap_sample = colmap_common[idx]
    gt_sample = sample_surface(gt_mesh, args.samples, args.seed)
    a0_sample = sample_surface(a0_mesh, args.samples, args.seed)

    out = {
        "protocol": {
            "samples_per_set": args.samples,
            "seed": args.seed,
            "thresholds_m": args.thresholds,
            "scene_extents_m": SCENE_EXTENTS.tolist(),
            "coordinate_map": "scene=[colmap_x,colmap_z,-colmap_y]",
        },
        "colmap_points_raw": int(len(colmap_scene)),
        "colmap_points_in_common_support": int(len(colmap_common)),
        "colmap_fraction_in_common_support": float(mask.mean()),
        "a0": metrics(a0_sample, gt_sample, args.thresholds),
        "colmap": metrics(colmap_sample, gt_sample, args.thresholds),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    if args.sample_out:
        cloud = trimesh.points.PointCloud(colmap_sample)
        cloud.export(args.sample_out)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
