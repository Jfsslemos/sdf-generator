#!/usr/bin/env python3
"""Split a DM-NeRF instance-labelled mesh into independent instance meshes.

Uses the explicit vertex_instance_id array exported by the current DM-NeRF
runner; RGB colors are never interpreted as semantic identities.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import trimesh


def split_instances(labels_file: Path, output: Path, exclude=()):
    data = np.load(labels_file)
    vertices = np.asarray(data['vertices'], dtype=float)
    triangles = np.asarray(data['triangles'], dtype=np.int64)
    labels = np.asarray(data['vertex_instance_id']).reshape(-1)
    if len(vertices) != len(labels):
        raise ValueError('vertex/label count mismatch')
    if triangles.ndim != 2 or triangles.shape[1] != 3:
        raise ValueError('triangles must be Nx3')

    output.mkdir(parents=True, exist_ok=True)
    face_labels = labels[triangles]
    homogeneous = np.all(face_labels == face_labels[:, :1], axis=1)
    boundary_faces = int((~homogeneous).sum())
    records = []
    for instance_id in sorted(int(x) for x in np.unique(labels) if int(x) not in set(exclude)):
        face_mask = homogeneous & (face_labels[:,0] == instance_id)
        faces = triangles[face_mask]
        if not len(faces):
            continue
        used = np.unique(faces.reshape(-1))
        remap = np.full(len(vertices), -1, dtype=np.int64)
        remap[used] = np.arange(len(used))
        mesh = trimesh.Trimesh(vertices=vertices[used], faces=remap[faces], process=False)
        stem = f'instance_{instance_id:03d}'
        ply = output/(stem+'.ply')
        obj = output/(stem+'.obj')
        mesh.export(ply)
        mesh.export(obj)
        records.append({
            'instance_id':instance_id, 'vertices':int(len(mesh.vertices)),
            'faces':int(len(mesh.faces)), 'surface_area':float(mesh.area),
            'bounds':np.asarray(mesh.bounds).tolist(), 'centroid':np.asarray(mesh.centroid).tolist(),
            'ply':ply.name, 'obj':obj.name,
        })
    manifest = {
        'source':str(labels_file), 'instances':records,
        'source_vertices':int(len(vertices)), 'source_faces':int(len(triangles)),
        'homogeneous_faces':int(homogeneous.sum()), 'boundary_faces':boundary_faces,
        'face_coverage':float(homogeneous.mean()) if len(homogeneous) else 0.0,
        'excluded_instance_ids':[int(x) for x in exclude],
    }
    (output/'instances.json').write_text(json.dumps(manifest, indent=2))
    return manifest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('labels', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--exclude-id', type=int, action='append', default=[])
    args = ap.parse_args()
    result = split_instances(args.labels, args.output, args.exclude_id)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
