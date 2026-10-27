"""Checkpoint/time controls; the upstream losses and optimizer step are unchanged."""
import json
import os
from pathlib import Path
import random
import time
import numpy as np
import torch
START = time.monotonic()
EFFECTIVE_UPDATES = 0
SKIPPED_UPDATES = 0

def seed():
    random.seed(0); np.random.seed(0); torch.manual_seed(3); torch.cuda.manual_seed_all(3)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

def load_resume(coarse, fine, optimizer, scaler=None):
    global EFFECTIVE_UPDATES, SKIPPED_UPDATES
    filename = os.environ.get('DMNERF_RESUME')
    if not filename:
        EFFECTIVE_UPDATES = 0; SKIPPED_UPDATES = 0
        return 0
    state = torch.load(filename, map_location='cpu')
    coarse.load_state_dict(state['network_coarse_state_dict'])
    fine.load_state_dict(state['network_fine_state_dict'])
    optimizer.load_state_dict(state['optimizer_state_dict'])
    if scaler is not None and scaler.is_enabled():
        if state.get('scaler_state_dict') is None:
            raise RuntimeError('AMP resume checkpoint has no GradScaler state; start a fresh AMP run')
        scaler.load_state_dict(state['scaler_state_dict'])
    rng = state['rng']
    random.setstate(rng['python']); np.random.set_state(rng['numpy'])
    torch.set_rng_state(rng['torch'].cpu())
    if torch.cuda.is_available():
        torch.cuda.set_rng_state_all([x.cpu() for x in rng['cuda']])
    EFFECTIVE_UPDATES = int(state.get('effective_updates', state['iteration'] + 1))
    SKIPPED_UPDATES = int(state.get('skipped_updates', 0))
    print('Resuming after iteration', state['iteration'], 'effective updates', EFFECTIVE_UPDATES, 'skipped', SKIPPED_UPDATES)
    return state['iteration'] + 1

def finish_step(i, coarse, fine, optimizer, args, loss, scaler=None, optimizer_step_applied=True):
    global EFFECTIVE_UPDATES, SKIPPED_UPDATES
    if not torch.isfinite(loss).all():
        raise RuntimeError('Non-finite loss; checkpoint not overwritten')
    if optimizer_step_applied:
        EFFECTIVE_UPDATES += 1
    else:
        SKIPPED_UPDATES += 1
    elapsed = time.monotonic() - START
    done = i + 1 >= int(os.environ['DMNERF_STEPS'])
    timed_out = elapsed >= float(os.environ['DMNERF_SECONDS'])
    folder = Path(args.basedir) / args.expname / args.log_time
    row = {'iteration':i,'effective_updates':EFFECTIVE_UPDATES,'skipped_updates':SKIPPED_UPDATES,
           'optimizer_step_applied':bool(optimizer_step_applied),'elapsed_seconds':elapsed,'loss':float(loss.detach().cpu()),
           'max_vram_bytes':torch.cuda.max_memory_allocated() if torch.cuda.is_available() else 0}
    with (folder / 'training.jsonl').open('a') as f:
        f.write(json.dumps(row) + '\n')
    if (i+1) % args.i_save == 0 or done or timed_out:
        state = {'iteration':i,'network_coarse_state_dict':coarse.state_dict(),
                 'network_fine_state_dict':fine.state_dict(),'optimizer_state_dict':optimizer.state_dict(),
                 'scaler_state_dict':scaler.state_dict() if scaler is not None else None,
                 'effective_updates':EFFECTIVE_UPDATES,'skipped_updates':SKIPPED_UPDATES,
                 'rng':{'python':random.getstate(),'numpy':np.random.get_state(),'torch':torch.get_rng_state(),
                        'cuda':torch.cuda.get_rng_state_all() if torch.cuda.is_available() else []}}
        temporary = folder / 'latest.tar.tmp'
        torch.save(state, temporary); temporary.replace(folder / 'latest.tar')
        (folder / 'training_state.json').write_text(json.dumps(dict(row, target_steps=int(os.environ['DMNERF_STEPS']),
                         complete=done, stopped_for_budget=timed_out and not done), indent=2))
        print('Checkpoint saved:', folder / 'latest.tar')
    return done or timed_out
