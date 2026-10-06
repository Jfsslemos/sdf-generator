"""Instrumented one-scene runner; smoke checkpoints never enter the experiment."""
import argparse
import csv
import datetime as dt
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
from prepare import ROOT, SOURCE, sha256
from patch_upstream import apply

def run_stage(command, cwd, env, output, stage, timeout):
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    logfile = output/f'{stamp}-{stage}.log'
    record = {'stage':stage,'command':command,'cwd':str(cwd),'started_utc':stamp,'log':logfile.name,'status':'running'}
    start = time.monotonic(); telemetry = None
    print('Starting',stage,'log:',logfile,flush=True)
    with logfile.open('w') as log, (output/f'{stamp}-gpu.csv').open('w') as gpu:
        if shutil.which('nvidia-smi'):
            telemetry = subprocess.Popen(['nvidia-smi','--query-gpu=timestamp,name,memory.used,utilization.gpu',
                                         '--format=csv','-l','5'],stdout=gpu,stderr=subprocess.DEVNULL)
        try:
            result = subprocess.run(command,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=timeout)
            record.update(returncode=result.returncode,status='ok' if result.returncode == 0 else 'failed')
        except subprocess.TimeoutExpired:
            record.update(returncode=None,status='timeout')
        finally:
            if telemetry:
                telemetry.terminate(); telemetry.wait()
            record['elapsed_seconds'] = time.monotonic()-start
            with (output/'stages.jsonl').open('a') as f:
                f.write(json.dumps(record)+'\n')
    print(json.dumps(record),flush=True)
    print(logfile.read_text(errors='replace')[-3500:],flush=True)
    if record['status'] != 'ok':
        raise RuntimeError(f'{stage}: {record["status"]}; see {logfile}')

def metrics_to_csv(raw, destination):
    import numpy as np
    rows = np.loadtxt(raw,ndmin=2)
    if rows.shape[1] != 9 or rows.shape[0] < 2 or not np.isfinite(rows).all():
        raise ValueError('Invalid upstream metrics')
    with destination.open('w',newline='') as f:
        w = csv.writer(f)
        w.writerow(['view','PSNR','SSIM','LPIPS','AP50','AP75','AP80','AP85','AP90','AP95'])
        for i,row in enumerate(rows):
            w.writerow(['mean' if i == len(rows)-1 else i,*row])

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work',type=Path,required=True); p.add_argument('--output',type=Path,required=True)
    p.add_argument('--profile',choices=['smoke','pilot','amp_pilot','full','extended'],default='smoke')
    p.add_argument('--stages',nargs='+',choices=['train','evaluate','mesh'],default=['train','evaluate','mesh'])
    p.add_argument('--allow-cpu',action='store_true')
    p.add_argument('--amp',action='store_true',help='use autocast+GradScaler for MLP forwards during training')
    a = p.parse_args()
    import torch
    if not torch.cuda.is_available() and not a.allow_cpu:
        raise SystemExit('GPU unavailable. Activate GPU in Kaggle/Colab and rerun.')
    if a.allow_cpu and a.profile != 'smoke':
        raise SystemExit('CPU permitted only for engineering smoke tests')
    work,output = a.work.resolve(),a.output.resolve()
    upstream = work/'DM-NeRF'
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=upstream,text=True).strip() != SOURCE['commit']:
        raise RuntimeError('Unexpected upstream revision')
    apply(upstream)  # Also verifies that the prepared checkout has not changed.
    profile = json.loads((ROOT/'configs/dmnerf/profiles.json').read_text())[a.profile]
    output.mkdir(parents=True,exist_ok=True)
    name = 'smoke' if a.profile == 'smoke' else 'experiment'
    folder = output/'raw/study'/name; folder.mkdir(parents=True,exist_ok=True)
    identity = {'upstream_commit':SOURCE['commit'],'patch_sha256':sha256(upstream/'session.patch'),
                'dataset_manifest_sha256':sha256(work/'dataset_manifest.json'),'N_train':profile['N_train'],
                'train_skip':profile['train_skip'],'torch':torch.__version__,'python':platform.python_version(),
                'runtime_sha256':sha256(upstream/'runtime_control.py'),
                'environment_sha256':sha256(work/'environment.freeze.txt'),'amp':bool(a.amp)}
    manifest = json.loads((work/'dataset_manifest.json').read_text())
    if manifest['upstream_commit'] != SOURCE['commit'] or manifest['patch_sha256'] != identity['patch_sha256']:
        raise RuntimeError('Stale preparation; rerun prepare.py')
    identity_file = folder/'identity.json'
    if identity_file.exists() and json.loads(identity_file.read_text()) != identity:
        raise RuntimeError('Checkpoint/run identity mismatch. Use a separate output directory; never silently mix runs.')
    identity_file.write_text(json.dumps(identity,indent=2))
    for filename in ('dataset_manifest.json','environment.freeze.txt','environment.json'):
        shutil.copy2(work/filename,output/filename)
    shutil.copy2(upstream/'session.patch',output/'upstream.patch')
    repo_sha = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    source_hashes = {str(f.relative_to(ROOT)):sha256(f) for f in sorted((ROOT/'tools/dmnerf').glob('*.py'))}
    (output/f'{name}-run.json').write_text(json.dumps({'profile':a.profile,'settings':profile,'identity':identity,
       'repository_commit':repo_sha,'executor_files':source_hashes,'gpu':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
       'cuda':torch.version.cuda,'amp':bool(a.amp),'cpu_validation_only':a.allow_cpu,'experimental_conclusion':'pending review'},indent=2))
    env = dict(os.environ,CUDA_VISIBLE_DEVICES='0',MPLBACKEND='Agg',OMP_NUM_THREADS='2',
               DMNERF_STEPS=str(profile['steps']),DMNERF_SECONDS=str(profile['seconds']),
               DMNERF_GRID_DIM=str(profile['grid_dim']),DMNERF_TRAIN_SKIP=str(profile['train_skip']),
               DMNERF_AMP='1' if a.amp else '0')
    env.pop('DMNERF_RESUME',None)
    checkpoint = folder/'latest.tar'
    if checkpoint.exists():
        env['DMNERF_RESUME'] = str(checkpoint)
    config = output/f'{name}-official-config.txt'
    config.write_text((upstream/'configs/dmsr/train/study.txt').read_text())
    common = ['--config',str(config),'--basedir',str(output/'raw'),'--log_time',name,
              '--N_train',str(profile['N_train']),'--N_test',str(profile['N_test']),
              '--testskip',str(profile['testskip']),'--i_save',str(profile['save_every']),
              '--i_print','1' if name == 'smoke' else '100']
    try:
        for stage in a.stages:
            if stage == 'train':
                run_stage([sys.executable,'-u','train_dmsr.py',*common],upstream,env,output,stage,profile['seconds']+600)
                if not checkpoint.exists():
                    raise RuntimeError('No training checkpoint was produced')
            else:
                if not checkpoint.exists():
                    raise RuntimeError('No checkpoint; train first')
                state = json.loads((folder/'training_state.json').read_text())
                if a.profile in ('full','extended') and state['iteration']+1 < profile['steps']:
                    print('Budget reached: resume training in a new session before final evaluation.')
                    break
                run_stage([sys.executable,'-u','test_dmsr.py',*common,'--test_model','latest.tar',
                          '--render' if stage == 'evaluate' else '--mesh'],upstream,env,output,stage,900 if name == 'smoke' else 7200)
                if stage == 'evaluate':
                    raw = folder/f'render_test_{state["iteration"]:06d}/test_results.txt'
                    derived = output/'derived'/name; derived.mkdir(parents=True,exist_ok=True)
                    metrics_to_csv(raw,derived/'metrics.csv')
                else:
                    meshdir = folder/f'mesh_{state["iteration"]:06d}'
                    status = meshdir/'mesh_status.json'
                    if status.exists():
                        print('Mesh limitation:',status.read_text())
                        if name != 'smoke':
                            raise RuntimeError('No usable mesh; E0 remains incomplete')
                    elif not (meshdir/'mesh_instances.ply').exists():
                        raise RuntimeError('Missing instance mesh')
    finally:
        print('RESULTS:',shutil.make_archive(str(output.parent/(output.name+'-bundle')),'zip',output),flush=True)
if __name__ == '__main__':
    main()
