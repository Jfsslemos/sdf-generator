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
from mesh_contract import load_labels, sha256


def split_instances(labels_file: Path, output: Path, exclude=(), mesh_file=None, allow_vertex_change=False):
    vertices, triangles, labels = load_labels(labels_file, mesh_file, allow_vertex_change)
    output = Path(output)

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
        'source':Path(labels_file).name, 'source_sha256':sha256(labels_file), 'instances':records,
        'mesh_sha256':sha256(mesh_file) if mesh_file else None,
        'allow_vertex_change':bool(allow_vertex_change),
        'exported_faces':sum(x['faces'] for x in records),
        'source_vertices':int(len(vertices)), 'source_faces':int(len(triangles)),
        'homogeneous_faces':int(homogeneous.sum()), 'boundary_faces':boundary_faces,
        'face_coverage':float(homogeneous.mean()) if len(homogeneous) else 0.0,
        'excluded_instance_ids':[int(x) for x in exclude],
    }
    if boundary_faces:
        trimesh.Trimesh(vertices=vertices, faces=triangles[~homogeneous], process=False).export(output/'boundary_faces.obj')
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
