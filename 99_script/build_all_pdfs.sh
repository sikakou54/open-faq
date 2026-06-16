#!/usr/bin/env bash
set -euo pipefail

# build_all_pdfs.sh
#
# リポジトリ内の全 HTML 設計書(正本)を `PDF出力/` 配下に
# 同じツリー構造で一括 PDF 化する。
#
# 仕様:
# - 対象: 01_メインシステム/ / 02_運営者システム/ / 共有/ 配下の *.html(本文ページ)
# - 除外: 画面遷移図ラッパー(*.view.html)、assets/、99_script/、PDF出力/
# - 出力先: PDF出力/<元の相対パス>/<basename>.{pdf}
# - html_to_pdf.sh を内部で呼び出す(Chrome headless が portal.js を実行しシェルを描画)
# - 失敗があっても続行し、最後に集計を表示
#
# 使い方:
#   bash 99_script/build_all_pdfs.sh                # 全ファイル
#   bash 99_script/build_all_pdfs.sh --changed-only # git status で変更のあったファイルのみ
#   bash 99_script/build_all_pdfs.sh --dry-run      # 何が処理されるかだけ表示
#   bash 99_script/build_all_pdfs.sh --quiet        # 進捗ログを抑制(エラーのみ表示)
#
# 環境変数:
#   PDF_FONT_NAME / PDF_MONO_FONT_NAME / PDF_TABLE_HEADER_BG / PDF_TABLE_HEADER_FG
#     md_to_pdf.sh に渡される(詳細は同スクリプト参照)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUT_ROOT="${REPO_ROOT}/PDF出力"

CHANGED_ONLY=0
DRY_RUN=0
QUIET=0

usage() {
  sed -n '3,21p' "$0" | sed 's/^# *//'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --changed-only) CHANGED_ONLY=1; shift ;;
    --dry-run)      DRY_RUN=1; shift ;;
    --quiet)        QUIET=1; shift ;;
    -h|--help)      usage; exit 0 ;;
    *) echo "ERROR: 未知のオプション: $1" >&2; usage; exit 1 ;;
  esac
done

log() { [[ $QUIET -eq 0 ]] && echo "$@"; }

cd "$REPO_ROOT"

# 対象ファイル収集(bash 3.2 互換: 配列でなく一時ファイル経由)
TMP_LIST="$(mktemp)"
trap 'rm -f "$TMP_LIST"' EXIT

# 一時的に pipefail を外して 0 件マッチの grep が中断させないようにする
set +e
set +o pipefail

if [[ $CHANGED_ONLY -eq 1 ]]; then
  # tracked のステージ済/未ステージ変更 + 未追跡ファイル を統合して取得。
  # NUL 区切りで安全に扱う(マルチバイトファイル名対応)。
  {
    git diff --name-only -z HEAD
    git ls-files --others --exclude-standard -z
  } 2>/dev/null \
    | tr '\0' '\n' \
    | awk '/\.html$/' \
    | grep -vE '\.view\.html$' \
    | sort -u \
    | grep -vE '^99_script/' \
    | grep -vE '^PDF出力/' \
    | grep -vE '^assets/' \
    > "$TMP_LIST"
else
  # 全 .html を再帰検索。assets/・99_script/・PDF出力/・*.view.html を除外。
  find . \
       -type d \( -name 'PDF出力' -o -name '99_script' -o -name '.git' -o -name 'assets' \) -prune \
    -o -type f -name '*.html' -print \
    | sed 's|^\./||' \
    | grep -vE '\.view\.html$' \
    | sort \
    > "$TMP_LIST"
fi

set -e
set -o pipefail

TOTAL=$(wc -l < "$TMP_LIST" | tr -d ' ')
if [[ $TOTAL -eq 0 ]]; then
  echo "対象ファイルが見つかりません。"
  exit 0
fi

log "対象ファイル数: $TOTAL"
log "出力先ルート: $OUT_ROOT"
[[ $DRY_RUN -eq 1 ]] && log "(--dry-run: 実行はせず一覧のみ表示)"
log ""

OK=0
FAIL=0
SKIP=0
FAIL_LIST=""

while IFS= read -r src; do
  [[ -z "$src" ]] && continue
  if [[ ! -f "$src" ]]; then
    log "SKIP (not file): $src"
    SKIP=$((SKIP + 1))
    continue
  fi

  rel_dir="$(dirname "$src")"
  base="$(basename "$src")"
  ext="${base##*.}"
  stem="${base%.*}"
  out_dir="${OUT_ROOT}/${rel_dir}"
  out_pdf="${out_dir}/${stem}.pdf"

  if [[ $DRY_RUN -eq 1 ]]; then
    log "DRY: $src -> ${out_pdf#${REPO_ROOT}/}"
    continue
  fi

  mkdir -p "$out_dir"
  log "[$((OK + FAIL + 1))/$TOTAL] $src"

  TMP_LOG="$(mktemp)"
  case "$ext" in
    html)
      if bash "${SCRIPT_DIR}/html_to_pdf.sh" "$src" "$out_pdf" >"$TMP_LOG" 2>&1; then
        OK=$((OK + 1))
      else
        FAIL=$((FAIL + 1))
        FAIL_LIST="${FAIL_LIST}${src}\n"
        echo "  FAILED: $src" >&2
        tail -15 "$TMP_LOG" | sed 's/^/    /' >&2
      fi
      ;;
    *)
      SKIP=$((SKIP + 1))
      ;;
  esac
  rm -f "$TMP_LOG"
done < "$TMP_LIST"

log ""
log "===================================="
log "完了: OK=$OK / FAIL=$FAIL / SKIP=$SKIP / TOTAL=$TOTAL"
if [[ $FAIL -gt 0 ]]; then
  echo "失敗ファイル:" >&2
  printf "%b" "$FAIL_LIST" >&2
  exit 1
fi
