#!/usr/bin/env bash
# Compatibility CLI: the notebook calls the Python tools directly.
set -euo pipefail
MODE=${1:-setup}
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
WORK_ROOT=${WORK_ROOT:-/kaggle/temp/dissertacao-dmnerf/work}
OUTPUT_ROOT=${OUTPUT_ROOT:-/kaggle/working/dmnerf-results}
PYTHON="$WORK_ROOT/env/bin/python"
case "$MODE" in
  setup)
    python "$REPO_ROOT/tools/dmnerf/bootstrap.py" --work "$WORK_ROOT"
    "$PYTHON" "$REPO_ROOT/tools/dmnerf/prepare.py" --work "$WORK_ROOT";;
  smoke|pilot)
    "$PYTHON" "$REPO_ROOT/tools/dmnerf/run.py" --work "$WORK_ROOT" --output "$OUTPUT_ROOT" --profile "$MODE";;
  train)
    "$PYTHON" "$REPO_ROOT/tools/dmnerf/run.py" --work "$WORK_ROOT" --output "$OUTPUT_ROOT" --profile full --stages train;;
  test|mesh)
    STAGE=$MODE
    if [[ "$MODE" == test ]]; then STAGE=evaluate; fi
    "$PYTHON" "$REPO_ROOT/tools/dmnerf/run.py" --work "$WORK_ROOT" --output "$OUTPUT_ROOT" --profile full --stages "$STAGE";;
  collect)
    "$PYTHON" - "$OUTPUT_ROOT" <<'PY'
from pathlib import Path
import shutil,sys
p=Path(sys.argv[1]).resolve()
print(shutil.make_archive(str(p.parent/(p.name+'-bundle')),'zip',p))
PY
    ;;
  *) echo "Use setup, smoke, pilot, train, test, mesh or collect" >&2; exit 64;;
esac
