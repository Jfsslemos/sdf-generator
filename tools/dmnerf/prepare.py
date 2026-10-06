"""Recover and validate the pinned code and one DM-SR scene."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import zipfile
from patch_upstream import apply
ROOT = Path(__file__).resolve().parents[2]
SOURCE = json.loads((ROOT / 'configs/dmnerf/source.json').read_text())

def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def extract_scene(archive, destination):
    destination = Path(destination).resolve()
    with zipfile.ZipFile(archive) as z:
        selected = [x for x in z.infolist() if x.filename.startswith('dmsr/study/')]
        if not selected:
            raise ValueError('Missing dmsr/study in ZIP')
        for info in selected:
            path = PurePosixPath(info.filename)
            target = destination.joinpath(*path.parts)
            if '..' in path.parts or not target.resolve().is_relative_to(destination) or ((info.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError('Unsafe archive member: ' + info.filename)
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(info) as src, target.open('wb') as dst:
                    shutil.copyfileobj(src, dst)

def validate_scene(scene):
    import h5py
    import numpy as np
    from PIL import Image
    scene = Path(scene)
    with h5py.File(scene / 'ins_rgb.hdf5', 'r') as f:
        colors = f['datasets'][:]
    if colors.ndim != 2 or colors.shape[1] != 3:
        raise ValueError('Invalid instance palette')
    info = {'scene':'study', 'instances':len(colors), 'splits':{}, 'files':[]}
    shape = None
    for split in ('train','test'):
        folder = scene / split
        rgbs = sorted((folder/'rgbs').iterdir()); masks = sorted((folder/'semantic_instance').iterdir())
        poses = json.loads((folder/'transforms.json').read_text())
        if not rgbs or len(rgbs) != len(masks) or len(rgbs) != len(poses['frames']):
            raise ValueError('RGB/mask/pose count mismatch: ' + split)
        if not 0 < float(poses['camera_angle_x']) < np.pi:
            raise ValueError('Invalid camera angle')
        for rgb, mask, pose in zip(rgbs, masks, poses['frames']):
            with Image.open(rgb) as im, Image.open(mask) as lab:
                shape = shape or im.size
                values = np.asarray(lab)
                if im.size != shape or lab.size != shape or values.ndim != 2 or values.min() < 0 or values.max() >= len(colors):
                    raise ValueError('Image or instance mask invalid: ' + str(mask))
            matrix = np.asarray(pose['transform_matrix']).reshape(4,4)
            if not np.isfinite(matrix).all() or not np.allclose(matrix[3], [0,0,0,1]):
                raise ValueError('Invalid pose')
        info['splits'][split] = {'frames':len(rgbs),'width':shape[0],'height':shape[1]}
    if not (scene/'study.ply').is_file():
        raise FileNotFoundError('Missing study.ply required by official meshing')
    objects = json.loads((scene/'mani/objs_info_rigid.json').read_text())
    if not all(k in objects for k in ('objects','view_id','ins_map')):
        raise ValueError('Missing meshing metadata')
    for f in sorted(scene.rglob('*')):
        if f.is_file():
            info['files'].append({'path':str(f.relative_to(scene)),'bytes':f.stat().st_size,'sha256':sha256(f)})
    return info

def prepare(work, archive=None):
    work = Path(work).resolve(); work.mkdir(parents=True, exist_ok=True)
    upstream = work/'DM-NeRF'
    if not upstream.exists():
        subprocess.run(['git','clone','--filter=blob:none','--no-checkout',SOURCE['repository'],str(upstream)], check=True)
        subprocess.run(['git','checkout','--detach',SOURCE['commit']],cwd=upstream,check=True)
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=upstream,text=True).strip()
    if commit != SOURCE['commit']:
        raise RuntimeError('Unexpected upstream commit; use a new work directory')
    apply(upstream)
    scene = upstream/'data/dmsr/study'
    if not scene.exists():
        archive = Path(archive) if archive else work/'dmsr.zip'
        if not archive.exists():
            temp = archive.with_suffix('.partial')
            subprocess.run(['curl','--fail','--location','--retry','3','--connect-timeout','30','--max-time','1800',
                            '--output',str(temp),SOURCE['dataset_url']],check=True)
            if not zipfile.is_zipfile(temp):
                raise ValueError('Official download is not a ZIP')
            temp.replace(archive)
        if sha256(archive) != SOURCE['dataset_sha256']:
            raise ValueError('DM-SR checksum mismatch')
        staging = work/'extracting'; extract_scene(archive, staging)
        scene.parent.mkdir(parents=True,exist_ok=True)
        shutil.move(str(staging/'dmsr/study'),scene)
    manifest = validate_scene(scene)
    manifest.update(upstream_commit=commit, source=SOURCE, patch_sha256=sha256(upstream/'session.patch'))
    (work/'dataset_manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps({k:v for k,v in manifest.items() if k!='files'},indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work',type=Path,required=True); p.add_argument('--archive',type=Path)
    a = p.parse_args(); prepare(a.work,a.archive)
