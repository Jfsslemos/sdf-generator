"""Isolated Python 3.10 + Torch environment, without modifying the host kernel."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[2]

def run(*cmd):
    subprocess.run([str(x) for x in cmd], check=True)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--cpu', action='store_true')
    p.add_argument('--lock', type=Path, help='Resolved environment from an earlier run')
    a = p.parse_args()
    work = a.work.resolve(); work.mkdir(parents=True, exist_ok=True)
    uv = shutil.which('uv')
    if not uv:
        target = work / 'bootstrap-tools'
        run(sys.executable, '-m', 'pip', 'install', '--target', target, 'uv==0.6.17')
        uv = str(target / 'bin/uv')
    os.environ['UV_PYTHON_INSTALL_DIR'] = str(work / 'python')
    env = work / 'env'; python = env / 'bin/python'
    if not python.exists():
        run(uv, 'python', 'install', '3.10.16')
        run(uv, 'venv', '--python', '3.10.16', env)
    run(python, '-c', 'import sys; assert sys.version_info[:3] == (3,10,16), "Use a new work directory"')
    flavor = 'cpu' if a.cpu else 'cu118'
    run(uv, 'pip', 'install', '--python', python, 'torch==2.2.2', 'torchvision==0.17.2',
        '--index-url', f'https://download.pytorch.org/whl/{flavor}')
    requirements = ROOT / 'configs/dmnerf/requirements.txt'
    if a.lock:
        requirements = work / 'resume-requirements.txt'
        lines = [line for line in a.lock.read_text().splitlines()
                 if not line.lower().startswith(('torch==', 'torchvision=='))]
        requirements.write_text('\n'.join(lines) + '\n')
    run(uv, 'pip', 'install', '--python', python, '-r', requirements)
    freeze = subprocess.check_output([uv, 'pip', 'freeze', '--python', str(python)], text=True)
    (work / 'environment.freeze.txt').write_text(freeze)
    (work / 'environment.json').write_text(json.dumps({'python':str(python),'torch_flavor':flavor}, indent=2))
    run(python, '-c', 'import torch, torchvision, open3d, cv2, lpips, h5py, skimage; print(torch.__version__, torch.cuda.is_available())')
    print('READY:', python)
if __name__ == '__main__':
    main()
