#!/usr/bin/env bash
set -euo pipefail

# HTML -> PDF 生成スクリプト v2
#
# 優先順位:
#   1. Google Chrome (headless)        ← Mac 標準で入っていることが多い
#   2. Chromium / Microsoft Edge       ← 代替ブラウザ
#   3. WeasyPrint (Python)             ← フォールバック
#
# CSS の @page ルール、page-break-after、grid/flex に対応。
#
# 使い方:
#   chmod 755 html_to_pdf.sh
#   ./html_to_pdf.sh wireframes.html
#   ./html_to_pdf.sh wireframes.html design.html
#
# 出力先を指定:
#   ./html_to_pdf.sh --out ./pdf_output wireframes.html
#
# エンジンを明示指定:
#   ./html_to_pdf.sh --engine chrome wireframes.html
#   ./html_to_pdf.sh --engine weasyprint wireframes.html

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="."
ENGINE="auto"

usage() {
  cat <<USAGE
Usage: $0 [--out OUT_DIR] [--engine ENGINE] [html files...]

Options:
  --out OUT_DIR        PDFの出力先ディレクトリを指定します。省略時: カレントディレクトリ
  --engine ENGINE      使用エンジンを指定します。auto / chrome / weasyprint
                       省略時: auto(chrome があれば chrome、無ければ weasyprint)
  -h, --help           このヘルプを表示します。

Examples:
  $0 wireframes.html                          # カレントディレクトリに wireframes.pdf を出力
  $0 --out ./dist wireframes.html design.html
  $0 --engine weasyprint wireframes.html

依存(いずれか1つ):
  - Google Chrome / Chromium / Microsoft Edge のいずれか
    (Mac の Chrome は通常 /Applications/Google Chrome.app に入っています)
  - WeasyPrint (Python ライブラリ)
    インストール例: pip3 install weasyprint --break-system-packages
USAGE
}

HTML_FILES=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --out の後に出力先ディレクトリを指定してください。" >&2
        exit 1
      fi
      OUT_DIR="$2"
      shift 2
      ;;
    --engine)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --engine の後にエンジン名(auto/chrome/weasyprint)を指定してください。" >&2
        exit 1
      fi
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

# 引数が指定されていない場合、スクリプトと同じディレクトリにある主要なHTMLを自動検出
if [[ ${#HTML_FILES[@]} -eq 0 ]]; then
  for f in \
    "$SCRIPT_DIR/wireframes.html" \
    "$SCRIPT_DIR/index.html"; do
    [[ -f "$f" ]] && HTML_FILES+=("$f")
  done
fi

if [[ ${#HTML_FILES[@]} -eq 0 ]]; then
  echo "ERROR: PDF化するHTMLファイルが見つかりません。" >&2
  echo "例: $0 wireframes.html" >&2
  exit 1
fi

# ---------- エンジン検出 ----------

CHROME_BIN=""
detect_chrome() {
  # Mac 標準のパス
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

  # PATH 上のコマンド
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

# 使用エンジンを決定
case "$ENGINE" in
  auto)
    if detect_chrome; then
      ENGINE="chrome"
    elif has_weasyprint; then
      ENGINE="weasyprint"
    else
      echo "ERROR: PDF変換エンジンが見つかりません。" >&2
      echo "  Mac の場合: Google Chrome をインストールしてください。" >&2
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
      echo "次のコマンドでインストールしてください:" >&2
      echo "  pip3 install weasyprint --break-system-packages" >&2
      exit 1
    fi
    ;;
  *)
    echo "ERROR: 未知のエンジン: $ENGINE (auto / chrome / weasyprint のいずれか)" >&2
    exit 1
    ;;
esac

mkdir -p "$OUT_DIR"
# OUT_DIR を絶対パスに正規化
OUT_DIR="$(cd "$OUT_DIR" && pwd)"

echo "Engine: $ENGINE"
[[ "$ENGINE" == "chrome" ]] && echo "  Browser: $CHROME_BIN"

# ---------- 変換ループ ----------

for html in "${HTML_FILES[@]}"; do
  if [[ ! -f "$html" ]]; then
    echo "ERROR: ファイルが見つかりません: $html" >&2
    exit 1
  fi

  base="$(basename "$html")"
  base="${base%.html}"
  base="${base%.htm}"
  pdf="$OUT_DIR/${base}.pdf"

  # 絶対パスに変換
  abs_html="$(cd "$(dirname "$html")" && pwd)/$(basename "$html")"

  echo ""
  echo "Creating PDF: $pdf"
  echo "  source: $abs_html"

  case "$ENGINE" in
    chrome)
      # Chrome 用の一時ユーザーデータディレクトリ(競合を防ぐ)
      TMP_USER_DATA="$(mktemp -d -t chrome-pdf-XXXXXX)"

      # 既存PDFを消しておく(生成検知のため)
      rm -f "$pdf"

      # Chrome を バックグラウンド で起動。
      # Mac の Chrome は --headless でも子プロセス(GPU/レンダラ)が残って
      # 親プロセスが return しないことがあるため、PDF が生成された時点で
      # 親 Chrome を明示的に kill する。
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

      # PDF が生成されるまで待つ(最大 60 秒)
      WAIT_SEC=0
      while [[ ! -s "$pdf" ]] && [[ $WAIT_SEC -lt 60 ]]; do
        if ! kill -0 $CHROME_PID 2>/dev/null; then
          # Chrome 自体が落ちている
          break
        fi
        sleep 1
        WAIT_SEC=$((WAIT_SEC + 1))
      done

      # PDF 書き出し直後にディスクへ flush するための小休止
      [[ -s "$pdf" ]] && sleep 1

      # Chrome を確実に終了させる(残留プロセス含む)
      kill $CHROME_PID >/dev/null 2>&1 || true
      sleep 0.3
      kill -9 $CHROME_PID >/dev/null 2>&1 || true
      # 同じユーザーデータを使っている子プロセスもまとめて終了
      pkill -9 -f "user-data-dir=$TMP_USER_DATA" >/dev/null 2>&1 || true

      wait $CHROME_PID 2>/dev/null || true

      # 一時ディレクトリ削除
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
echo "Done. Output directory: $OUT_DIR"