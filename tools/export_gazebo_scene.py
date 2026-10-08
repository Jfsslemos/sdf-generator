#!/usr/bin/env python3
"""Export traceable A0/A1/A2 static Gazebo Classic assets (CPU/XML gate only)."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
import numpy as np
import trimesh
from postprocess_instances import split_instances


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_world(path):
    """Check portable local asset references and the explicitly scoped G0 contract."""
    path = Path(path)
    root = ET.parse(path).getroot()
    if root.tag != 'sdf' or root.find('world') is None:
        raise ValueError('Expected sdf/world')
    models = root.findall('./world/model')
    if not models:
        raise ValueError('No models')
    names = [m.get('name') for m in models]
    if any(not n or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',n) for n in names) or len(set(names)) != len(names):
        raise ValueError('Model names must be nonempty and unique')
    for model in models:
        links = model.findall('link')
        if not links:
            raise ValueError('Missing link')
        for link in links:
            references = {}
            for kind in ('visual', 'collision'):
                elements = link.findall(kind)
                if not elements:
                    raise ValueError('Missing ' + kind)
                for item in elements:
                    mesh = item.find('geometry/mesh')
                    if mesh is None:
                        raise ValueError('Missing mesh geometry')
                    uri = mesh.findtext('uri', '')
                    relative = Path(uri)
                    if '\\' in uri:
                        raise ValueError('Nonportable mesh URI')
                    if not uri or relative.is_absolute() or '..' in relative.parts or ':' in uri:
                        raise ValueError('Nonportable mesh URI')
                    target = (path.parent / relative).resolve()
                    if not target.is_relative_to(path.parent.resolve()) or not target.is_file():
                        raise ValueError('Unresolved mesh URI')
                    scale = np.asarray([float(v) for v in mesh.findtext('scale', '').split()])
                    if scale.shape != (3,) or not np.all(np.isfinite(scale)) or np.any(scale <= 0):
                        raise ValueError('Invalid mesh scale')
                    references.setdefault(kind, []).append((uri,tuple(scale)))
            if sorted(references['visual']) != sorted(references['collision']):
                raise ValueError('Visual/collision mesh references differ')
    return {'status': 'PASS', 'models': len(models), 'scope': 'static XML and local references; not libsdformat or Gazebo runtime'}


def export_scene(mesh_file, labels_file, output, condition, up_axis, floor_provenance=None):
    mesh_file, labels_file, output = Path(mesh_file), Path(labels_file), Path(output)
    if condition not in ('A0', 'A1', 'A2') or up_axis not in ('x', 'y', 'z'):
        raise ValueError('Invalid condition or up axis')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output must be empty; preserve previous evidence in a separate directory')
    if condition == 'A2' and floor_provenance is None:
        raise ValueError('A2 requires explicit floor provenance')
    provenance = None
    if floor_provenance is not None:
        provenance = json.loads(Path(floor_provenance).read_text())
        if not isinstance(provenance, dict) or not provenance:
            raise ValueError('Floor provenance must be a nonempty JSON object')
        floor_id = provenance.get('instance_id')
        if type(floor_id) is not int or floor_id < 0:
            raise ValueError('Floor provenance needs a selected nonnegative instance_id')
        if provenance.get('status') != 'selected':
            raise ValueError('Floor selection was not successful')
        if provenance.get('evidence_type') != 'geometric_heuristic':
            raise ValueError('Floor provenance must declare evidence_type=geometric_heuristic')
        if provenance.get('semantic_ground_truth') is not False:
            raise ValueError('Floor provenance must explicitly declare semantic_ground_truth=false')
        if provenance.get('source_sha256') != digest(labels_file):
            raise ValueError('Floor provenance must identify these exact labels by source_sha256')
    output.mkdir(parents=True, exist_ok=True)
    meshes = output / 'meshes'
    # Even A0 validates the pair. A2 permits vertex displacement, never topology changes.
    split = split_instances(labels_file, meshes, mesh_file=mesh_file,
                            allow_vertex_change=condition == 'A2')
    if provenance is not None and provenance['instance_id'] not in [r['instance_id'] for r in split['instances']]:
        raise ValueError('Selected floor has no homogeneous exported faces')
    mesh = trimesh.load(mesh_file, process=False, force='mesh')
    warnings = []
    if condition == 'A0':
        mesh.export(meshes / 'scene_raw.obj')
        records = [{'instance_id': None, 'obj': 'scene_raw.obj', 'name': 'scene_raw'}]
    else:
        records = [dict(r, name=Path(r['obj']).stem) for r in split['instances']]
        if split['boundary_faces']:
            warnings.append(f"{split['boundary_faces']} mixed-label boundary faces omitted by the registered homogeneous-face split")
    if not records:
        raise ValueError('No exportable faces')
    # Active rotations: x-up -> z-up about y by -pi/2; y-up -> z-up about x by pi/2.
    rpy = {'x': (0., -math.pi/2, 0.), 'y': (math.pi/2, 0., 0.), 'z': (0., 0., 0.)}[up_axis]
    pose = '0 0 0 ' + ' '.join(format(v, '.17g') for v in rpy)
    root = ET.Element('sdf', version='1.6')
    world = ET.SubElement(root, 'world', name='study_' + condition.lower())
    ET.SubElement(world, 'gravity').text = '0 0 -9.81'
    physics = ET.SubElement(world, 'physics', name='ode', type='ode')
    ET.SubElement(physics, 'max_step_size').text = '0.001'
    light = ET.SubElement(world, 'light', name='scene_light', type='directional')
    ET.SubElement(light, 'direction').text = '-0.5 -0.5 -1'
    ET.SubElement(light, 'diffuse').text = '0.8 0.8 0.8 1'
    for record in records:
        asset = meshes / record['obj']
        obj = trimesh.load(asset, process=False, force='mesh')
        if not obj.is_watertight:
            warnings.append(record['name'] + ': non-watertight triangle collision; support/contact requires G3 runtime validation')
        model = ET.SubElement(world, 'model', name=record['name'])
        ET.SubElement(model, 'static').text = 'true'
        ET.SubElement(model, 'pose').text = pose
        link = ET.SubElement(model, 'link', name='geometry')
        for kind in ('visual', 'collision'):
            item = ET.SubElement(link, kind, name=kind)
            geom = ET.SubElement(item, 'geometry')
            shape = ET.SubElement(geom, 'mesh')
            ET.SubElement(shape, 'uri').text = 'meshes/' + record['obj']
            ET.SubElement(shape, 'scale').text = '1 1 1'
        record['sha256'] = digest(asset)
        record['uri'] = 'meshes/' + record['obj']
        record['model_name'] = record['name']
    ET.indent(root)
    world_path = output / 'scene.world'
    ET.ElementTree(root).write(world_path, encoding='utf-8', xml_declaration=True)
    g0 = validate_world(world_path)
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=Path(__file__).resolve().parents[1], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = None
    validation = {
        'schema_version': 1, 'run_id': 'study_' + condition.lower() + '_' + digest(mesh_file)[:12],
        'condition': condition, 'code_commit': commit, 'gazebo_version': None,
        'input_mesh': {'name': mesh_file.name, 'sha256': digest(mesh_file)},
        'labels': {'name': labels_file.name, 'sha256': digest(labels_file)},
        'sdf': {'path': 'scene.world', 'sha256': digest(world_path)},
        'input_up_axis': up_axis, 'model_pose': pose, 'scale': [1, 1, 1],
        'objects': records, 'floor_provenance': provenance,
        'floor_provenance_sha256': digest(floor_provenance) if floor_provenance else None,
        'instance_ids_tested': [], 'warnings': warnings,
        'gates': {'G0': g0, **{g: {'status': 'NOT_EXECUTED'} for g in ('G1', 'G2', 'G3', 'G4')}},
        'logs': ['export.log'],
    }
    validation['generated_files'] = [
        {'path': p.relative_to(output).as_posix(), 'sha256': digest(p)}
        for p in sorted(output.rglob('*'))
        if p.is_file()
    ]
    (output / 'manifest.json').write_text(json.dumps(validation, indent=2) + '\n')
    (output / 'gazebo_validation.json').write_text(json.dumps(validation, indent=2) + '\n')
    (output / 'export.log').write_text('G0 PASS: XML and local asset references validated.\nGazebo runtime not executed.\n' + '\n'.join(warnings) + '\n')
    return validation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mesh', type=Path)
    parser.add_argument('labels', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--condition', choices=['A0', 'A1', 'A2'], required=True)
    parser.add_argument('--up-axis', choices=['x', 'y', 'z'], required=True)
    parser.add_argument('--floor-provenance', type=Path)
    args = parser.parse_args()
    print(json.dumps(export_scene(args.mesh, args.labels, args.output, args.condition,
                                  args.up_axis, args.floor_provenance), indent=2))


if __name__ == '__main__':
    main()
