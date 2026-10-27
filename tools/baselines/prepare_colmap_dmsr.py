#!/usr/bin/env python3
"""Create a COLMAP text model for DM-SR from the dataset-provided poses.

DM-SR stores NeRF/OpenGL camera-to-world transforms. COLMAP expects
world-to-camera transforms in a pinhole frame (+x right, +y down, +z forward).
The explicit conversion used here is:

    c2w_colmap = c2w_dmsr @ diag(1, -1, -1, 1)
    w2c_colmap = inv(c2w_colmap)

No pose estimation or bundle adjustment is performed by this script.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import numpy as np
from PIL import Image

OPENGL_TO_COLMAP = np.diag([1.0, -1.0, -1.0, 1.0])


def rotmat_to_qvec(R: np.ndarray) -> np.ndarray:
    """Return COLMAP quaternion [qw, qx, qy, qz] from a rotation matrix."""
    R = np.asarray(R, dtype=np.float64)
    K = np.array([
        [R[0,0]-R[1,1]-R[2,2], R[1,0]+R[0,1], R[2,0]+R[0,2], R[1,2]-R[2,1]],
        [R[1,0]+R[0,1], R[1,1]-R[0,0]-R[2,2], R[2,1]+R[1,2], R[2,0]-R[0,2]],
        [R[2,0]+R[0,2], R[2,1]+R[1,2], R[2,2]-R[0,0]-R[1,1], R[0,1]-R[1,0]],
        [R[1,2]-R[2,1], R[2,0]-R[0,2], R[0,1]-R[1,0], R[0,0]+R[1,1]+R[2,2]],
    ], dtype=np.float64) / 3.0
    values, vectors = np.linalg.eigh(K)
    q = vectors[:, np.argmax(values)][[3,0,1,2]]
    if q[0] < 0:
        q = -q
    return q / np.linalg.norm(q)


def load_scene(scene: Path, split: str):
    folder = scene / split
    images = sorted(p for p in (folder/'rgbs').iterdir() if p.is_file())
    meta = json.loads((folder/'transforms.json').read_text())
    frames = meta['frames']
    if not images or len(images) != len(frames):
        raise ValueError(f'RGB/pose count mismatch: {len(images)} vs {len(frames)}')
    with Image.open(images[0]) as im:
        width, height = im.size
    angle_x = float(meta['camera_angle_x'])
    if not 0.0 < angle_x < math.pi:
        raise ValueError('camera_angle_x outside (0, pi)')
    focal = 0.5 * width / math.tan(0.5 * angle_x)
    poses = []
    for frame in frames:
        c2w = np.asarray(frame['transform_matrix'], dtype=np.float64).reshape(4,4)
        if not np.isfinite(c2w).all() or not np.allclose(c2w[3], [0,0,0,1], atol=1e-6):
            raise ValueError('invalid homogeneous pose')
        c2w_colmap = c2w @ OPENGL_TO_COLMAP
        w2c = np.linalg.inv(c2w_colmap)
        if not np.allclose(w2c[:3,:3] @ w2c[:3,:3].T, np.eye(3), atol=1e-4):
            raise ValueError('camera rotation is not orthonormal')
        if not np.isclose(np.linalg.det(w2c[:3,:3]), 1.0, atol=1e-4):
            raise ValueError('camera rotation determinant is not +1')
        poses.append((w2c, c2w_colmap[:3,3].copy()))
    return images, poses, width, height, focal, angle_x


def nearest_sources(centers: np.ndarray, count: int):
    result = []
    for i, center in enumerate(centers):
        distance = np.linalg.norm(centers-center, axis=1)
        order = np.argsort(distance)
        result.append([int(j) for j in order if int(j) != i][:count])
    return result


def prepare(scene: Path, out: Path, split='train', source_count=10, near=4.0, far=15.0):
    scene, out = Path(scene).resolve(), Path(out).resolve()
    images, poses, width, height, focal, angle_x = load_scene(scene, split)
    sparse = out/'sparse'
    sparse.mkdir(parents=True, exist_ok=True)
    (sparse/'cameras.txt').write_text(
        '# Camera list with one line of data per camera:\n'
        '# CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]\n'
        f'1 PINHOLE {width} {height} {focal:.17g} {focal:.17g} {width/2:.17g} {height/2:.17g}\n'
    )
    image_lines = [
        '# Image list with two lines of data per image:',
        '# IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME',
        '# POINTS2D[] as (X, Y, POINT3D_ID)',
    ]
    centers, records = [], []
    for image_id, (image, (w2c, center)) in enumerate(zip(images, poses), start=1):
        q = rotmat_to_qvec(w2c[:3,:3])
        t = w2c[:3,3]
        image_lines.append(
            f'{image_id} ' + ' '.join(f'{x:.17g}' for x in [*q,*t]) + f' 1 {image.name}'
        )
        image_lines.append('')
        centers.append(center)
        records.append({
            'image_id':image_id, 'name':image.name, 'center':center.tolist(),
            'qvec':q.tolist(), 'tvec':t.tolist(),
        })
    (sparse/'images.txt').write_text('\n'.join(image_lines)+'\n')
    (sparse/'points3D.txt').write_text(
        '# 3D point list with one line of data per point:\n'
        '# POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK[] as (IMAGE_ID, POINT2D_IDX)\n'
    )
    centers = np.asarray(centers)
    source_count = min(source_count, max(0, len(images)-1))
    sources = nearest_sources(centers, source_count)
    pairs = [
        {'reference':images[i].name, 'sources':[images[j].name for j in sources[i]]}
        for i in range(len(images))
    ]
    manifest = {
        'scene':str(scene), 'split':split, 'images':len(images),
        'width':width, 'height':height, 'camera_model':'PINHOLE',
        'fx':focal, 'fy':focal, 'cx':width/2, 'cy':height/2,
        'camera_angle_x':angle_x,
        'pose_conversion':'c2w_colmap = c2w_dmsr @ diag(1,-1,-1,1); w2c = inv(c2w_colmap)',
        'source_count':source_count, 'depth_min':near, 'depth_max':far,
        'image_path':str(scene/split/'rgbs'),
        'records':records, 'source_pairs':pairs,
    }
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2))
    return manifest


def write_patch_match_cfg(manifest_path: Path, dense_workspace: Path):
    manifest = json.loads(Path(manifest_path).read_text())
    stereo = Path(dense_workspace)/'stereo'
    stereo.mkdir(parents=True, exist_ok=True)
    lines = []
    for pair in manifest['source_pairs']:
        lines += [pair['reference'], ', '.join(pair['sources'])]
    cfg = stereo/'patch-match.cfg'
    cfg.write_text('\n'.join(lines)+'\n')
    return cfg


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('scene', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--split', choices=['train','test'], default='train')
    ap.add_argument('--source-count', type=int, default=10)
    ap.add_argument('--near', type=float, default=4.0)
    ap.add_argument('--far', type=float, default=15.0)
    ap.add_argument('--write-patch-match-cfg', type=Path)
    args = ap.parse_args()
    manifest = prepare(args.scene, args.output, args.split, args.source_count, args.near, args.far)
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('records','source_pairs')}, indent=2))
    if args.write_patch_match_cfg:
        print('PATCH_MATCH_CFG:', write_patch_match_cfg(args.output/'manifest.json', args.write_patch_match_cfg))


if __name__ == '__main__':
    main()
