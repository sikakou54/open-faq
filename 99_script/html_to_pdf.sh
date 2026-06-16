#!/usr/bin/env bash
set -euo pipefail

# HTML -> PDF 生成スクリプト
#
# 優先順位:
#   1. Google Chrome (headless)        ← Mac 標準で入っていることが多い
#   2. Chromium / Microsoft Edge       ← 代替ブラウザ
#   3. WeasyPrint (Python)             ← フォールバック
#
# CSS の @page ルール、page-break-after、grid/flex に対応。
#
# 使い方:
#   bash 99_script/html_to_pdf.sh input.html output.pdf
#   bash 99_script/html_to_pdf.sh 01_メインシステム/画面遷移図_オーナー.html
#   bash 99_script/html_to_pdf.sh --out PDF出力/01_メインシステム 01_メインシステム/画面遷移図_オーナー.html
#   bash 99_script/html_to_pdf.sh --engine chrome 画面遷移図_オーナー.html
#
# 引数のパターン:
#   - 引数 2 個 (input.html output.pdf): プロンプト指定形式。指定パスに 1 ファイル出力。
#   - 引数 1 個 (input.html): カレントディレクトリに同名 .pdf を出力。
#   - --out OUT_DIR 指定: OUT_DIR に <basename>.pdf を出力(複数 HTML 可)。
#   - 引数 0 個: メイン(アカウント種別別 4 ファイル)+ 運営者(画面遷移図.html)を自動検出。

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="."
OUT_FILE=""
ENGINE="auto"

usage() {
  cat <<USAGE
Usage:
  $0 input.html output.pdf
  $0 [--out OUT_DIR] [--engine ENGINE] [html files...]

Options:
  --out OUT_DIR        PDFの出力先ディレクトリ(省略時: カレントディレクトリ)
  --engine ENGINE      使用エンジン: auto / chrome / weasyprint(省略時: auto)
  -h, --help           このヘルプを表示

Examples:
  $0 01_メインシステム/画面遷移図_オーナー.html PDF出力/01_メインシステム/画面遷移図_オーナー.pdf
  $0 --out PDF出力/01_メインシステム 01_メインシステム/画面遷移図_オーナー.html
  $0 --engine weasyprint 02_運営者システム/画面遷移図.html

依存(いずれか1つ):
  - Google Chrome / Chromium / Microsoft Edge のいずれか
  - WeasyPrint (Python): pip3 install weasyprint --break-system-packages
USAGE
}

HTML_FILES=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)
      [[ $# -lt 2 ]] && { echo "ERROR: --out の後に出力先ディレクトリを指定してください。" >&2; exit 1; }
      OUT_DIR="$2"
      shift 2
      ;;
    --engine)
      [[ $# -lt 2 ]] && { echo "ERROR: --engine の後にエンジン名(auto/chrome/weasyprint)を指定してください。" >&2; exit 1; }
      ENGINE="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      HTML_FILES+=("$1")
      shift
      ;;
  esac
done

# 「input.html output.pdf」形式の判定: 引数 2 個で 2 つ目が .pdf
if [[ ${#HTML_FILES[@]} -eq 2 && "${HTML_FILES[1]}" == *.pdf ]]; then
  OUT_FILE="${HTML_FILES[1]}"
  HTML_FILES=("${HTML_FILES[0]}")
fi

# 引数なしの場合、リポジトリ内の主要な HTML を自動検出
if [[ ${#HTML_FILES[@]} -eq 0 ]]; then
  REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
  for f in \
    "${REPO_ROOT}/01_メインシステム/画面遷移図_ウィジェット利用者.html" \
    "${REPO_ROOT}/01_メインシステム/画面遷移図_プロジェクトメンバー.html" \
    "${REPO_ROOT}/01_メインシステム/画面遷移図_プロジェクト管理者.html" \
    "${REPO_ROOT}/01_メインシステム/画面遷移図_オーナー.html" \
    "${REPO_ROOT}/02_運営者システム/画面遷移図.html"; do
    [[ -f "$f" ]] && HTML_FILES+=("$f")
  done
fi

if [[ ${#HTML_FILES[@]} -eq 0 ]]; then
  echo "ERROR: PDF化するHTMLファイルが見つかりません。" >&2
  echo "例: $0 input.html output.pdf" >&2
  exit 1
fi

# ---------- エンジン検出 ----------

CHROME_BIN=""
detect_chrome() {
  for p in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"; do
    if [[ -x "$p" ]]; then
      CHROME_BIN="$p"
      return 0
    fi
  done
  for cmd in google-chrome chrome chromium chromium-browser microsoft-edge; do
    if command -v "$cmd" >/dev/null 2>&1; then
      CHROME_BIN="$(command -v "$cmd")"
      return 0
    fi
  done
  return 1
}

has_weasyprint() {
  command -v python3 >/dev/null 2>&1 && python3 -c "import weasyprint" >/dev/null 2>&1
}

case "$ENGINE" in
  auto)
    if detect_chrome; then
      ENGINE="chrome"
    elif has_weasyprint; then
      ENGINE="weasyprint"
    else
      echo "ERROR: PDF変換エンジンが見つかりません。" >&2
      echo "  Mac: Google Chrome をインストールしてください。" >&2
      echo "  または: pip3 install weasyprint --break-system-packages" >&2
      exit 1
    fi
    ;;
  chrome)
    if ! detect_chrome; then
      echo "ERROR: Google Chrome / Chromium / Edge が見つかりません。" >&2
      exit 1
    fi
    ;;
  weasyprint)
    if ! has_weasyprint; then
      echo "ERROR: WeasyPrint が見つかりません。" >&2
      echo "  pip3 install weasyprint --break-system-packages" >&2
      exit 1
    fi
    ;;
  *)
    echo "ERROR: 未知のエンジン: $ENGINE (auto / chrome / weasyprint のいずれか)" >&2
    exit 1
    ;;
esac

# 出力先準備
if [[ -n "$OUT_FILE" ]]; then
  out_dir_only="$(dirname "$OUT_FILE")"
  mkdir -p "$out_dir_only"
  out_dir_abs="$(cd "$out_dir_only" && pwd)"
  OUT_FILE="${out_dir_abs}/$(basename "$OUT_FILE")"
else
  mkdir -p "$OUT_DIR"
  OUT_DIR="$(cd "$OUT_DIR" && pwd)"
fi

echo "Engine: $ENGINE"
[[ "$ENGINE" == "chrome" ]] && echo "  Browser: $CHROME_BIN"

# ---------- 変換ループ ----------

for html in "${HTML_FILES[@]}"; do
  if [[ ! -f "$html" ]]; then
    echo "ERROR: ファイルが見つかりません: $html" >&2
    exit 1
  fi

  if [[ -n "$OUT_FILE" ]]; then
    pdf="$OUT_FILE"
  else
    base="$(basename "$html")"
    base="${base%.html}"
    base="${base%.htm}"
    pdf="$OUT_DIR/${base}.pdf"
  fi

  abs_html="$(cd "$(dirname "$html")" && pwd)/$(basename "$html")"

  echo ""
  echo "Creating PDF: $pdf"
  echo "  source: $abs_html"

  case "$ENGINE" in
    chrome)
      TMP_USER_DATA="$(mktemp -d -t chrome-pdf-XXXXXX)"
      rm -f "$pdf"

      "$CHROME_BIN" \
        --headless \
        --disable-gpu \
        --no-pdf-header-footer \
        --hide-scrollbars \
        --disable-extensions \
        --disable-default-apps \
        --no-first-run \
        --mute-audio \
        --user-data-dir="$TMP_USER_DATA" \
        --print-to-pdf="$pdf" \
        "file://${abs_html}" \
        </dev/null >/dev/null 2>&1 &
      CHROME_PID=$!

      WAIT_SEC=0
      while [[ ! -s "$pdf" ]] && [[ $WAIT_SEC -lt 60 ]]; do
        if ! kill -0 $CHROME_PID 2>/dev/null; then
          break
        fi
        sleep 1
        WAIT_SEC=$((WAIT_SEC + 1))
      done

      [[ -s "$pdf" ]] && sleep 1

      kill $CHROME_PID >/dev/null 2>&1 || true
      sleep 0.3
      kill -9 $CHROME_PID >/dev/null 2>&1 || true
      pkill -9 -f "user-data-dir=$TMP_USER_DATA" >/dev/null 2>&1 || true

      wait $CHROME_PID 2>/dev/null || true

      rm -rf "$TMP_USER_DATA"
      ;;

    weasyprint)
      python3 -m weasyprint "$abs_html" "$pdf" 2>&1 | \
        grep -v -E "^(WARNING|INFO):" || true
      ;;
  esac

  if [[ -f "$pdf" ]]; then
    size=$(ls -l "$pdf" | awk '{print $5}')
    echo "  -> ${size} bytes"
  else
    echo "ERROR: PDF が生成されませんでした: $pdf" >&2
    exit 1
  fi
done

echo ""
if [[ -n "$OUT_FILE" ]]; then
  echo "Done. Output: $OUT_FILE"
else
  echo "Done. Output directory: $OUT_DIR"
fi
