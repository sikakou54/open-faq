#!/bin/bash
# Generic: bundle Markdown files and upload image files to a NotebookLM notebook.
#
# Usage:
#   bash sync.sh                        # reads REPO/.claude/nlm-sync.json
#   bash sync.sh --notebook NOTEBOOK_ID # override notebook (alias / UUID)
#   bash sync.sh --config FILE          # use a different config file
#   bash sync.sh --dry-run              # bundle/collect only, skip upload
#
# Config file format (.claude/nlm-sync.json):
#   {
#     "notebook": "UUID-OR-ALIAS",
#     "bundles": {
#       "bundle_name": ["glob1", "glob2"]
#     },
#     "images": ["glob1", "glob2"]       # optional: PNG/JPG files uploaded individually
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

# ── Markdown bundles ──────────────────────────────────────────────────────────

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
BUNDLE_OPTS=()
while IFS= read -r line; do
  [[ -n "$line" ]] && BUNDLE_OPTS+=("$line")
done < <(echo "$BUNDLE_ARGS")

python3 "$SCRIPTS/nlm_bundle.py" \
  --root "$REPO" \
  --out  "$BUILD/bundles" \
  "${BUNDLE_OPTS[@]}"

# ── Image files ───────────────────────────────────────────────────────────────

IMAGE_GLOBS=$(python3 -c "
import json
cfg = json.load(open('$CONFIG'))
globs = cfg.get('images', [])
print(','.join(globs))
")

# ── Upload ────────────────────────────────────────────────────────────────────

if [[ "$DRY" -eq 1 ]]; then
  echo "[nlm-sync] dry-run done (bundles: $BUILD/bundles)."
  if [[ -n "$IMAGE_GLOBS" ]]; then
    echo "[nlm-sync] image globs (not uploaded): $IMAGE_GLOBS"
  fi
  exit 0
fi

echo "[nlm-sync] replacing NotebookLM sources (markdown)..."
python3 "$SCRIPTS/nlm_sync.py" \
  --notebook    "$NOTEBOOK" \
  --bundles-dir "$BUILD/bundles" \
  --ids-out     "$BUILD/source_ids.json" \
  --replace

if [[ -n "$IMAGE_GLOBS" ]]; then
  echo "[nlm-sync] syncing image sources..."
  python3 "$SCRIPTS/nlm_sync_images.py" \
    --notebook "$NOTEBOOK" \
    --root     "$REPO" \
    --globs    "$IMAGE_GLOBS" \
    --ids-out  "$BUILD/image_source_ids.json" \
    --replace
fi

echo "[nlm-sync] done."
