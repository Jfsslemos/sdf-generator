#!/usr/bin/env python3
"""Inventory official DM-SR evidence; never infer semantic names from colors."""
import argparse
import json
import hashlib
import subprocess
import zipfile
from pathlib import Path
import numpy as np
from mesh_contract import sha256

def audit(scene, upstream, archive):
    import h5py
    from PIL import Image
    scene=Path(scene);upstream=Path(upstream)
    source=json.loads((Path(__file__).resolve().parents[1]/'configs/dmnerf/source.json').read_text())
    if sha256(archive)!=source['dataset_sha256']:raise ValueError('Official archive checksum mismatch')
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=upstream,text=True).strip()
    if commit!=source['commit'] or subprocess.check_output(['git','diff','HEAD'],cwd=upstream):
        raise ValueError('Expected clean pinned upstream')
    with zipfile.ZipFile(archive) as z:
        expected={Path(n).relative_to('dmsr/study').as_posix():hashlib.sha256(z.read(n)).hexdigest()
                  for n in z.namelist() if n.startswith('dmsr/study/') and not n.endswith('/')}
    actual={p.relative_to(scene).as_posix():sha256(p) for p in scene.rglob('*') if p.is_file()}
    if actual!=expected:raise ValueError('Scene differs from verified official archive')
    report={'archive_sha256':source['dataset_sha256'],'upstream_commit':commit,'scene':'study','semantic_floor_id':None,'semantic_ground_truth_available':False,
            'scope':'Inspected DM-SR study release and pinned upstream only; not a claim about unpublished author data.',
            'files':[], 'metadata':{},'splits':{}}
    for path in sorted(scene.rglob('*')):
        if path.is_file():report['files'].append({'path':path.relative_to(scene).as_posix(),'bytes':path.stat().st_size,'sha256':sha256(path)})
    report['inventory_file_count']=len(report['files'])
    report['inventory_sha256']=hashlib.sha256(json.dumps(report['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    report['files']=[r for r in report['files'] if Path(r['path']).suffix in ('.json','.hdf5','.ply')]
    for path in sorted(scene.rglob('*.json')):
        d=json.loads(path.read_text());rel=path.relative_to(scene).as_posix()
        if 'frames' in d:
            report['metadata'][rel]={'keys':list(d),'frame_count':len(d['frames']),
                'frame_keys':sorted({k for f in d['frames'] for k in f}), 'camera_angle_x':d.get('camera_angle_x')}
        else: report['metadata'][rel]=d
    with h5py.File(scene/'ins_rgb.hdf5') as f:
        info={}
        def visit(name,obj):
            info[name]={'attributes':{k:np.asarray(v).tolist() for k,v in obj.attrs.items()}}
            if isinstance(obj,h5py.Dataset):info[name].update(shape=list(obj.shape),dtype=str(obj.dtype),values=obj[:].tolist())
        f.visititems(visit)
        report['hdf5']={'root_attributes':{k:np.asarray(v).tolist() for k,v in f.attrs.items()},'objects':info}
    for split in ('train','test'):
        counts={};files=sorted((scene/split/'semantic_instance').glob('*'));shapes=set()
        for p in files:
            with Image.open(p) as im:a=np.asarray(im)
            if a.ndim!=2:raise ValueError('Mask must contain scalar IDs, not RGB colors')
            shapes.add(tuple(a.shape));unique,n=np.unique(a,return_counts=True)
            for k,v in zip(unique,n):counts[str(int(k))]=counts.get(str(int(k)),0)+int(v)
        report['splits'][split]={'mask_count':len(files),'shapes':[list(x) for x in sorted(shapes)],'pixels_by_instance_id':counts}
    with (scene/'study.ply').open('rb') as f:
        lines=[]
        while True:
            line=f.readline().decode('ascii').strip();lines.append(line)
            if line=='end_header':break
            if len(lines)>1000:raise ValueError('Invalid PLY header')
    report['gt_ply_header']=lines
    import trimesh
    mesh=trimesh.load(scene/'study.ply',process=False)
    report['gt_geometry']={'vertices':len(mesh.vertices),'faces':len(mesh.faces),'bounds':mesh.bounds.tolist()}
    color=upstream/'data/color_dict.json';d=json.loads(color.read_text())
    report['upstream_color_mapping']={'sha256':sha256(color),'study':d['dmsr']['study']}
    report['upstream_sources']={name:sha256(upstream/name) for name in ('datasets/loader_dmsr.py','tools/mesh_generator.py','tools/visualizer.py','networks/tester.py')}
    report['conclusion']='No explicit floor class/name-to-ID mapping found. Instance masks and palette are not semantic class annotations; ins_map belongs to the supplied model/manipulation example, not to a new training run.'
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('scene',type=Path);p.add_argument('--archive',type=Path,required=True);p.add_argument('--upstream',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();r=audit(a.scene,a.upstream,a.archive);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['conclusion'])
if __name__=='__main__':main()
