#!/bin/bash
# Generic: bundle Markdown files and replace sources in a NotebookLM notebook.
#
# Usage:
#   bash sync.sh                        # reads REPO/.claude/nlm-sync.json
#   bash sync.sh --notebook NOTEBOOK_ID # override notebook (alias / UUID)
#   bash sync.sh --config FILE          # use a different config file
#   bash sync.sh --dry-run              # bundle only, skip upload
#
# Config file format (.claude/nlm-sync.json):
#   {
#     "notebook": "UUID-OR-ALIAS",
#     "bundles": {
#       "bundle_name": ["glob1", "glob2"],
#       ...
#     }
#   }
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"

REPO="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
SCRIPTS="$REPO/.claude/skills/full-layer-review/scripts"
BUILD="$REPO/_build/nlm_sync"
CONFIG="$REPO/.claude/nlm-sync.json"
NOTEBOOK=""
DRY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --notebook) NOTEBOOK="$2"; shift 2 ;;
    --config)   CONFIG="$2";   shift 2 ;;
    --dry-run)  DRY=1;         shift ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ ! -f "$CONFIG" ]]; then
  echo "[nlm-sync] config not found: $CONFIG" >&2; exit 1
fi

# Read notebook from config if not overridden
if [[ -z "$NOTEBOOK" ]]; then
  NOTEBOOK=$(python3 -c "import json,sys; print(json.load(open('$CONFIG'))['notebook'])")
fi

echo "[nlm-sync] notebook: $NOTEBOOK"

# Build --bundle flags from config
BUNDLE_ARGS=$(python3 -c "
import json, sys
cfg = json.load(open('$CONFIG'))
args = []
for name, globs in cfg.get('bundles', {}).items():
    args.append('--bundle')
    args.append(name + '=' + ','.join(globs))
print('\n'.join(args))
")

echo "[nlm-sync] bundling markdown files..."
while IFS= read -r line; do
  [[ -n "$line" ]] && BUNDLE_OPTS+=("$line")
done < <(echo "$BUNDLE_ARGS")

python3 "$SCRIPTS/nlm_bundle.py" \
  --root "$REPO" \
  --out  "$BUILD/bundles" \
  "${BUNDLE_OPTS[@]}"

if [[ "$DRY" -eq 1 ]]; then
  echo "[nlm-sync] dry-run done (bundles: $BUILD/bundles)."
  exit 0
fi

echo "[nlm-sync] replacing NotebookLM sources..."
python3 "$SCRIPTS/nlm_sync.py" \
  --notebook    "$NOTEBOOK" \
  --bundles-dir "$BUILD/bundles" \
  --ids-out     "$BUILD/source_ids.json" \
  --replace

echo "[nlm-sync] done."
