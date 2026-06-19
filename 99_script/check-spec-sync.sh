#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# 仕様同期スモークチェック(HTML 正本版 / メインシステム単独)
# SC-001 〜 SC-012 を実施する。設計書は HTML が正本(pandoc --wrap=none 由来の
# 1 ブロック 1 行構造)。完全な静的解析ではなく、ドリフト検出のレビュー補助。
# 運営者システムは別途再設計予定のため、本チェックはメインシステムのみを対象とする。
# ============================================================================

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() { echo "ERROR: $*" >&2; exit 1; }
require_file() { [[ -f "$1" ]] || fail "missing required file: $1"; }
require_dir() { [[ -d "$1" ]] || fail "missing required directory: $1"; }
require_pattern() { grep -Eq "$1" "$2" || fail "missing pattern in $2: $1"; }
reject_pattern() { if grep -Eq "$1" "$2"; then fail "forbidden pattern in $2: $1"; fi; }

require_file_series() {
  local dir="$1" prefix="$2" max="$3" label="$4" n padded count
  for ((n = 1; n <= max; n++)); do
    printf -v padded "%02d" "$n"
    count=$(find "$dir" -maxdepth 1 -name "${prefix}${padded}_*.html" | wc -l | tr -d ' ')
    [[ "$count" -eq 1 ]] || fail "${label} ${prefix}${padded} が一意に存在しない: ${count} 件"
  done
  count=$(find "$dir" -maxdepth 1 -name "${prefix}[0-9][0-9]_*.html" | wc -l | tr -d ' ')
  [[ "$count" -eq "$max" ]] || fail "${label} のファイル数が不正: ${count} (期待: ${max})"
}

require_unique_file_series() {
  local dir="$1" prefix="$2" max="$3" label="$4" actual expected n padded
  actual=$(find "$dir" -maxdepth 1 -name "${prefix}[0-9][0-9]_*.html" -print \
    | sed -E "s#^.*/${prefix}([0-9]{2})_.*#\\1#" | sort -u)
  expected=""
  for ((n = 1; n <= max; n++)); do printf -v padded "%02d" "$n"; expected+="${expected:+$'\n'}${padded}"; done
  [[ "$actual" == "$expected" ]] || fail "${label} の番号が不連続: actual=[$actual] expected=[$expected]"
}

# ============================================================================
# 基本ディレクトリ・ファイル存在検査
# ============================================================================

require_file "CLAUDE.md"                         # 運用ルール正本(Claude Code 自動読込)
require_file "index.html"                       # ポータル入口
require_file "assets/css/style.css"
require_file "assets/js/portal.js"
require_file "assets/js/nav-data.js"
require_file "assets/js/search-index.js"

for layer in "01_要件定義" "02_基本設計" "03_詳細設計" "04_運用設計" "05_future"; do
  require_dir "01_メインシステム/${layer}"
  require_file "01_メインシステム/${layer}/index.html"
done

require_dir "99_script"
require_file "99_script/check-spec-sync.sh"
require_file "99_script/build-search-index.py"
require_file "99_script/html_to_pdf.sh"
require_file "共有/共有概念.html"

BASIC_DESIGN_FILES=(
  "01_画面設計.html" "02_API設計.html" "03_テーブル設計.html" "04_権限設計.html"
  "05_エラー設計.html" "06_メッセージ一覧.html" "07_トレーサビリティマトリクス.html"
  "08_認証・認可設計.html" "09_セキュリティ設計.html" "10_課金・請求設計.html" "11_メール設計.html"
)
# メインは画面設計・API 設計・テーブル設計をフォルダ分割(index.html + 個別ファイル)済み。
main_bd_file() { case "$1" in "01_画面設計.html") echo "01_画面設計/index.html";; "02_API設計.html") echo "02_API設計/index.html";; "03_テーブル設計.html") echo "03_テーブル設計/index.html";; *) echo "$1";; esac; }
for f in "${BASIC_DESIGN_FILES[@]}"; do
  require_file "01_メインシステム/02_基本設計/$(main_bd_file "$f")"
done

OPS_DESIGN_FILES=(
  "01_監視設計.html" "02_バックアップ・リストア設計.html" "03_ログ設計.html"
  "04_障害対応設計.html" "05_リリース・デプロイ設計.html" "06_運用手順.html"
)
for f in "${OPS_DESIGN_FILES[@]}"; do require_file "01_メインシステム/04_運用設計/${f}"; done

# ============================================================================
# SC-001: 各基本設計 11 ファイルに <h1> / <h2> 見出しが存在
# ============================================================================
for f in "${BASIC_DESIGN_FILES[@]}"; do
  path="01_メインシステム/02_基本設計/$(main_bd_file "$f")"
  require_pattern "<h1[ >]" "${path}"
  require_pattern "<h2[ >]" "${path}"
done

# ============================================================================
# SC-002: 主要概念正本ファイルでの必須キーワード出現
# ============================================================================
require_pattern "オーナー境界|contract_owner_user_id" "01_メインシステム/02_基本設計/08_認証・認可設計.html"
require_pattern "M_OWNERS" "01_メインシステム/02_基本設計/03_テーブル設計/index.html"
require_pattern "M_PRJ_USERS" "01_メインシステム/02_基本設計/03_テーブル設計/index.html"
require_pattern "M_PRJ_USER_ASGN" "01_メインシステム/02_基本設計/03_テーブル設計/index.html"
require_pattern "contract_owner_user_id" "01_メインシステム/02_基本設計/03_テーブル設計/テーブル構造設計.html"
require_pattern "AES-256-GCM" "01_メインシステム/02_基本設計/09_セキュリティ設計.html"

# ============================================================================
# SC-003: index から共有概念へのリンク(再掲禁止・リンクのみ)
# ============================================================================
require_pattern "共有/共有概念.html" "01_メインシステム/02_基本設計/index.html"

# ============================================================================
# SC-004: SCR ID クロスチェック(画面設計 index ↔ トレーサビリティ)
# ============================================================================
MAIN_SCRS=("SCR-001" "SCR-002" "SCR-003" "SCR-004" "SCR-004-001" "SCR-005" "SCR-006" "SCR-006-002" "SCR-007" "SCR-008" "SCR-009" "SCR-009-001" "SCR-010" "SCR-011" "SCR-012" "SCR-013" "SCR-014" "SCR-015" "SCR-016" "SCR-017" "SCR-018" "SCR-019" "SCR-020" "SCR-021" "SCR-021-001" "SCR-022" "SCR-023")
for scr in "${MAIN_SCRS[@]}"; do
  require_pattern "${scr}" "01_メインシステム/02_基本設計/01_画面設計/index.html"
  require_pattern "${scr}" "01_メインシステム/02_基本設計/07_トレーサビリティマトリクス.html"
done

# ============================================================================
# SC-005: メッセージ ID 体系
# ============================================================================
require_pattern "MSG-SCR-001-" "01_メインシステム/02_基本設計/06_メッセージ一覧.html"

# ============================================================================
# SC-006: エラー ID 体系
# ============================================================================
require_pattern "E-AUTH-" "01_メインシステム/02_基本設計/05_エラー設計.html"
require_pattern "E-AUTHZ-" "01_メインシステム/02_基本設計/05_エラー設計.html"
require_pattern "E-BIZ-" "01_メインシステム/02_基本設計/05_エラー設計.html"

# ============================================================================
# SC-007: contract_owners.contract_status 4 値(コード値 <code>…</code> = >値<)
# ============================================================================
for v in "active" "suspended" "deleted_pending" "deleted"; do
  require_pattern ">${v}<" "01_メインシステム/02_基本設計/10_課金・請求設計.html"
  require_pattern ">${v}<|'${v}'" "01_メインシステム/02_基本設計/03_テーブル設計/TBL-M-001_m_owners.html"
done

# ============================================================================
# SC-008: 通知重要度 4 値 + critical 強制送信
# ============================================================================
for v in "low" "normal" "high" "critical"; do
  require_pattern ">${v}<" "01_メインシステム/02_基本設計/06_メッセージ一覧.html"
done
require_pattern "強制送信" "01_メインシステム/02_基本設計/06_メッセージ一覧.html"

# ============================================================================
# SC-010: 参照到達性 + 運用ルール(CLAUDE.md)の構成記述
# ============================================================================
require_pattern "01_メインシステム/02_基本設計" "共有/共有概念.html"
for layer in "01_要件定義" "02_基本設計" "03_詳細設計" "04_運用設計" "05_future"; do
  require_pattern "$layer" "CLAUDE.md"
done

# ============================================================================
# SC-011: FR / DD / FUT グループファイル(.html)の連番・件数
# ============================================================================
MAIN_FR_COUNT=$(find "01_メインシステム/01_要件定義" -maxdepth 1 -name "FR*.html" | wc -l | tr -d ' ')
require_file_series "01_メインシステム/01_要件定義" "FR" 21 "メインシステム FR"
MAIN_DD_COUNT=$(find "01_メインシステム/03_詳細設計" -maxdepth 1 -name "DD*.html" | wc -l | tr -d ' ')
require_file_series "01_メインシステム/03_詳細設計" "DD" 14 "メインシステム DD"
MAIN_FUT_COUNT=$(find "01_メインシステム/05_future" -maxdepth 1 -name "FUT*.html" | wc -l | tr -d ' ')
require_unique_file_series "01_メインシステム/05_future" "FUT" 6 "メインシステム FUT"

# ============================================================================
# SC-012: 番号体系の連続性(HTML 見出し / テーブル解析)+ 廃番識別子の再混入防止
# ============================================================================
python3 - <<'PY'
import re, sys
def read(p):
    with open(p, encoding="utf-8") as f: return f.read()
def fail(m): print("ERROR: "+m, file=sys.stderr); sys.exit(1)

def check_seq(label, actual, expected):
    if actual != expected:
        fail("%s が不連続: actual=%s expected=%s" % (label, actual, expected))

M = "01_メインシステム/02_基本設計/"

# (a) テーブル一覧(§1)の第 1 列 = 1..31
t = read(M + "03_テーブル設計/index.html")
seg = re.search(r'<h2[^>]*>1\.\s*テーブル一覧.*?(?=<h3[^>]*>1\.1)',t, re.S).group(0)
tbl = re.search(r'<table>.*?</table>', seg, re.S).group(0)
nums = [int(x) for x in re.findall(r'<tr>\s*<td>(\d+)</td>', tbl)]
check_seq("メインテーブル一覧", nums, list(range(1, 32)))

# (b) テーブル詳細は個別ファイル化。index §1 テーブル一覧に 31 件の個別リンクが存在
t31 = read(M + "03_テーブル設計/index.html")
seg31 = re.search(r'<h2[^>]*>1\.\s*テーブル一覧.*?(?=<h3[^>]*>1\.1)',t31, re.S).group(0)
links31 = len(re.findall(r'href="[A-Za-z0-9_-]+\.html"', re.search(r'<table>.*?</table>', seg31, re.S).group(0)))
if links31 != 31: fail("メインテーブル一覧の個別リンク数が不足: %d" % links31)
# (d) 画面メッセージ節 4.N (SCR-|エンドユーザー) = 1..27
t = read(M + "06_メッセージ一覧.html")
msg = [int(x) for x in re.findall(r'<h3[^>]*>4\.([0-9]+) (?:SCR-|エンドユーザー)', t)]
check_seq("メイン画面メッセージ節", msg, list(range(1, 28)))
# (e) メールテンプレート節 4.N TPL- = 1..14
t = read(M + "11_メール設計.html")
mail = [int(x) for x in re.findall(r'<h3[^>]*>4\.([0-9]+) TPL-', t)]
check_seq("メインメールテンプレート節", mail, list(range(1, 15)))
# (f) API 一覧(分割後 index)に全カテゴリの API-<PFX>- リンクが存在
#     リンクはカテゴリ別ファイルへのアンカー形式(例 href="認証.html#API-AUTH-001")
t = read(M + "02_API設計/index.html")
napi = len(re.findall(r'href="[^"]+\.html#API-[A-Z]+-[0-9]+"', t))
if napi < 45: fail("メイン API 一覧リンク数が不足: %d (期待 51 前後)" % napi)
PY

# (g) FR-070..077 が未解決質問登録文書に出現、FR-078/079 は再混入禁止
for fr in 070 071 072 073 074 075 076 077; do
  require_pattern ">FR-${fr}<" "01_メインシステム/01_要件定義/FR06_未解決質問登録.html"
done
reject_pattern "FR-078|FR-079" "01_メインシステム/01_要件定義/FR06_未解決質問登録.html"

# (h)-(k) 廃番識別子の再混入防止(.html 走査)
if grep -R -E --include='*.html' 'SCR-(028|029|030|031|032|035|036|037|038|039|040|041|042)' \
  "01_メインシステム/01_要件定義" "01_メインシステム/02_基本設計" \
  "01_メインシステム/03_詳細設計" "01_メインシステム/04_運用設計" >/dev/null; then
  fail "メインシステムの現行文書に旧 SCR ID が残っている"
fi
if grep -R -E --include='*.html' 'inquiry_status_history|TPL-FAQ_REGISTERED|NOTIF-CHAT_REPLY_TO_USER|notification-settings|E-AUTHZ-ADMIN-DELETE-PROTECTED|MSG-COMMON-ADMIN-DELETE-PROTECTED|MSG-SCR-009-M1-TOOLTIP-ADMIN-DELETE' \
  "01_メインシステム/01_要件定義" "01_メインシステム/02_基本設計" \
  "01_メインシステム/03_詳細設計" "01_メインシステム/04_運用設計" >/dev/null; then
  fail "削除済み識別子がメインシステムの現行文書に再混入している"
fi

# ============================================================================
echo "spec sync smoke check passed (SC-001 〜 SC-012) [HTML 正本 / メイン単独]"
echo "  - 要件定義 FR: メイン ${MAIN_FR_COUNT}"
echo "  - 詳細設計 DD: メイン ${MAIN_DD_COUNT}"
echo "  - 将来対応 FUT: メイン ${MAIN_FUT_COUNT}"
