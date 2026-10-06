#!/usr/bin/env python3
"""Run the geometry-only COLMAP baseline on a prepared DM-SR scene.

This baseline uses the DM-SR camera intrinsics and poses as fixed inputs.
It compares multi-view stereo geometry, not semantic/instance decomposition.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import time
from prepare_colmap_dmsr import prepare, write_patch_match_cfg


def execute(command, records, cwd=None):
    start = time.monotonic()
    result = subprocess.run(command, cwd=cwd, text=True)
    row = {'command':[str(x) for x in command], 'returncode':result.returncode,
           'elapsed_seconds':time.monotonic()-start}
    records.append(row)
    if result.returncode:
        raise RuntimeError('Command failed: ' + ' '.join(map(str,command)))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('scene', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--colmap', default='colmap')
    ap.add_argument('--source-count', type=int, default=10)
    ap.add_argument('--near', type=float, default=4.0)
    ap.add_argument('--far', type=float, default=15.0)
    args = ap.parse_args()

    exe = shutil.which(args.colmap)
    if not exe:
        raise SystemExit('COLMAP executable not found')
    scene, output = args.scene.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    manifest = prepare(scene, output/'model', 'train', args.source_count, args.near, args.far)
    dense = output/'dense'
    records = []
    execute([
        exe,'image_undistorter',
        '--image_path',manifest['image_path'],
        '--input_path',str(output/'model/sparse'),
        '--output_path',str(dense),
        '--output_type','COLMAP',
    ], records)
    cfg = write_patch_match_cfg(output/'model/manifest.json', dense)
    execute([
        exe,'patch_match_stereo',
        '--workspace_path',str(dense),
        '--workspace_format','COLMAP',
        '--PatchMatchStereo.geom_consistency','1',
        '--PatchMatchStereo.depth_min',str(args.near),
        '--PatchMatchStereo.depth_max',str(args.far),
    ], records)
    fused = dense/'fused.ply'
    execute([
        exe,'stereo_fusion',
        '--workspace_path',str(dense),
        '--workspace_format','COLMAP',
        '--input_type','geometric',
        '--StereoFusion.min_num_pixels','1',
        '--output_path',str(fused),
    ], records)
    if not fused.is_file() or fused.stat().st_size == 0:
        raise RuntimeError('COLMAP did not produce a non-empty fused.ply')
    report = {
        'status':'ok', 'scene':str(scene), 'fused':str(fused),
        'source_count':args.source_count, 'depth_min':args.near, 'depth_max':args.far,
        'patch_match_cfg':str(cfg), 'stages':records,
    }
    (output/'baseline_run.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
