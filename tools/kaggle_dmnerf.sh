#!/usr/bin/env bash
set -euo pipefail

MODE=${1:-setup}
WORK_ROOT=${WORK_ROOT:-/kaggle/working/dissertacao_dmnerf}
DMNERF_DIR="$WORK_ROOT/DM-NeRF"
ENV_PREFIX="$WORK_ROOT/env"
DATA_ZIP="$WORK_ROOT/dmsr.zip"
DATA_EXTRACT="$WORK_ROOT/dmsr_extract"
OUT_DIR="$WORK_ROOT/outputs"
DMSR_URL=${DMSR_URL:-https://www.dropbox.com/s/1k75m38vahizbp9/dmsr.zip?dl=1}
mkdir -p "$WORK_ROOT" "$OUT_DIR"

runenv() { "$ENV_PREFIX/bin/python" "$@"; }
pipenv() { "$ENV_PREFIX/bin/python" -m pip "$@"; }

install_env() {
  command -v nvidia-smi >/dev/null && nvidia-smi || true
  if [ ! -x "$ENV_PREFIX/bin/python" ]; then
    echo '[setup] installing Python 3.7 environment...'
    MINIFORGE="$WORK_ROOT/miniforge.sh"
    curl -L --retry 3 -o "$MINIFORGE" https://github.com/conda-forge/miniforge/releases/download/23.3.1-1/Miniforge3-23.3.1-1-Linux-x86_64.sh
    bash "$MINIFORGE" -b -p "$WORK_ROOT/miniforge"
    "$WORK_ROOT/miniforge/bin/conda" create -y -p "$ENV_PREFIX" python=3.7 pip=23.3.2
  fi
  pipenv install --upgrade 'pip<24'
  pipenv install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
  pipenv install ConfigArgParse==1.5.3 h5py==3.4.0 imageio==2.9.0 lpips==0.1.4 matplotlib==3.4.3 numpy==1.21.6 opencv-python-headless==4.5.3.56 Pillow==9.2.0 scipy==1.7.1 scikit-image==0.18.3 trimesh==3.13.5
  if ! pipenv install open3d==0.13.0; then
    echo '[setup] open3d 0.13.0 unavailable; trying 0.15.2 and recording the divergence.'
    pipenv install open3d==0.15.2
  fi
}

clone_code() {
  if [ ! -d "$DMNERF_DIR/.git" ]; then
    git clone https://github.com/vLAR-group/DM-NeRF.git "$DMNERF_DIR"
  fi
  (cd "$DMNERF_DIR" && git rev-parse HEAD > "$OUT_DIR/dmnerf_commit.txt")
}

download_data() {
  if [ ! -f "$DATA_ZIP" ]; then
    echo '[setup] downloading official DM-SR...'
    curl -L --retry 5 --retry-delay 3 -o "$DATA_ZIP" "$DMSR_URL"
  fi
  if [ ! -d "$DATA_EXTRACT" ]; then
    mkdir -p "$DATA_EXTRACT"
    unzip -q "$DATA_ZIP" -d "$DATA_EXTRACT"
  fi
  STUDY_DIR=$(find "$DATA_EXTRACT" -type d -name study | head -n1 || true)
  if [ -z "$STUDY_DIR" ]; then
    echo 'ERROR: study directory not found after extracting DM-SR.' >&2
    find "$DATA_EXTRACT" -maxdepth 3 -type d | sort | head -200 >&2
    exit 2
  fi
  DMSR_ROOT=$(dirname "$STUDY_DIR")
  rm -rf "$DMNERF_DIR/data/dmsr"
  ln -s "$DMSR_ROOT" "$DMNERF_DIR/data/dmsr"
  echo "$DMSR_ROOT" > "$OUT_DIR/dmsr_root.txt"
}

make_resumable_train() {
  local target="$DMNERF_DIR/train_dmsr_resumable.py"
  cp "$DMNERF_DIR/train_dmsr.py" "$target"
  "$ENV_PREFIX/bin/python" - "$target" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
s=s.replace('N_iters = 500000 + 1', """N_iters = int(os.environ.get('DMNERF_MAX_ITERS', '500001'))
    start_iter = 0
    resume_path = os.environ.get('DMNERF_RESUME')
    if resume_path and os.path.isfile(resume_path):
        print('Resuming from', resume_path)
        ckpt = torch.load(resume_path, map_location=args.device)
        model_coarse.load_state_dict(ckpt['network_coarse_state_dict'])
        model_fine.load_state_dict(ckpt['network_fine_state_dict'])
        optimizer.load_state_dict(ckpt['optimizer_state_dict'])
        start_iter = int(ckpt['iteration']) + 1""")
s=s.replace('for i in range(0, N_iters):', 'for i in range(start_iter, N_iters):')
p.write_text(s)
PY
}

latest_run_dir() {
  find "$DMNERF_DIR/logs/dmsr/study" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort | tail -n1
}
latest_ckpt() {
  local d="$1"
  find "$d" -maxdepth 1 -type f -name '*.tar' | sort | tail -n1
}
make_eval_configs() {
  local run_dir="$1" ckpt="$2" stamp ckpt_name
  stamp=$(basename "$run_dir"); ckpt_name=$(basename "$ckpt")
  cp "$DMNERF_DIR/configs/dmsr/test/study.txt" "$WORK_ROOT/study_current.txt"
  cp "$DMNERF_DIR/configs/dmsr/test/meshing.txt" "$WORK_ROOT/meshing_current.txt"
  sed -i -E "s/^log_time = .*/log_time = $stamp/; s/^test_model = .*/test_model = $ckpt_name/" "$WORK_ROOT/study_current.txt" "$WORK_ROOT/meshing_current.txt"
}

case "$MODE" in
  setup)
    install_env; clone_code; download_data; make_resumable_train
    "$ENV_PREFIX/bin/python" - <<'PY' | tee "$OUT_DIR/environment.txt"
import sys, torch, numpy
print('python',sys.version)
print('torch',torch.__version__)
print('cuda_available',torch.cuda.is_available())
print('cuda_runtime',torch.version.cuda)
print('gpu',torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE')
print('numpy',numpy.__version__)
PY
    ;;
  smoke)
    [ -x "$ENV_PREFIX/bin/python" ] || { echo 'run setup first'; exit 3; }
    make_resumable_train
    cd "$DMNERF_DIR"
    DMNERF_MAX_ITERS=3 "$ENV_PREFIX/bin/python" -u train_dmsr_resumable.py --config configs/dmsr/train/study.txt --N_train 128 --N_test 256 --N_samples 16 --N_importance 32 --i_save 1 --i_test 1000000 | tee "$OUT_DIR/smoke_train.log"
    ;;
  train)
    cd "$DMNERF_DIR"; make_resumable_train
    RUN_DIR=$(latest_run_dir || true); RESUME=''
    if [ -n "$RUN_DIR" ]; then RESUME=$(latest_ckpt "$RUN_DIR" || true); fi
    if [ -n "$RESUME" ]; then
      echo "[train] resuming $RESUME"
      DMNERF_RESUME="$RESUME" "$ENV_PREFIX/bin/python" -u train_dmsr_resumable.py --config configs/dmsr/train/study.txt | tee "$OUT_DIR/train.log"
    else
      "$ENV_PREFIX/bin/python" -u train_dmsr_resumable.py --config configs/dmsr/train/study.txt | tee "$OUT_DIR/train.log"
    fi
    ;;
  test)
    cd "$DMNERF_DIR"; RUN_DIR=$(latest_run_dir); CKPT=$(latest_ckpt "$RUN_DIR"); make_eval_configs "$RUN_DIR" "$CKPT"
    "$ENV_PREFIX/bin/python" -u test_dmsr.py --config "$WORK_ROOT/study_current.txt" | tee "$OUT_DIR/test.log"
    ;;
  mesh)
    cd "$DMNERF_DIR"; RUN_DIR=$(latest_run_dir); CKPT=$(latest_ckpt "$RUN_DIR"); make_eval_configs "$RUN_DIR" "$CKPT"
    "$ENV_PREFIX/bin/python" -u test_dmsr.py --config "$WORK_ROOT/meshing_current.txt" | tee "$OUT_DIR/mesh.log"
    ;;
  collect)
    cd "$WORK_ROOT"
    RUN_DIR=$(latest_run_dir || true)
    [ -n "$RUN_DIR" ] && cp -a "$RUN_DIR" "$OUT_DIR/study_run" || true
    cp -f "$DMNERF_DIR/data/dmsr/study/study.ply" "$OUT_DIR/study_ground_truth.ply" 2>/dev/null || true
    tar -czf "$WORK_ROOT/dmnerf_study_outputs.tar.gz" -C "$OUT_DIR" .
    echo "$WORK_ROOT/dmnerf_study_outputs.tar.gz"
    ;;
  *) echo "invalid mode: $MODE"; exit 64;;
esac
