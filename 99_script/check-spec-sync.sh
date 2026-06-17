#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# 仕様同期スモークチェック(HTML 正本版)
# SC-001 〜 SC-012 を実施する。設計書は HTML が正本(pandoc --wrap=none 由来の
# 1 ブロック 1 行構造)。完全な静的解析ではなく、ドリフト検出のレビュー補助。
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

for system in "01_メインシステム" "02_運営者システム"; do
  for layer in "01_要件定義" "02_基本設計" "03_詳細設計" "04_運用設計" "05_future"; do
    require_dir "${system}/${layer}"
    require_file "${system}/${layer}/index.html"
  done
done

# 画面遷移図(原 HTML)。メインは各 SCR_*.html の §3 画面レイアウトへ取り込み済みのため廃止。
# 運営者は統合 1 ファイルを維持する。
require_file "02_運営者システム/画面遷移図.html"

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
# メインは画面設計をフォルダ分割(01_画面設計/index.html + SCR_*.html)済み。運営者はモノリス維持。
main_bd_file() { case "$1" in "01_画面設計.html") echo "01_画面設計/index.html";; "02_API設計.html") echo "02_API設計/index.html";; *) echo "$1";; esac; }
for f in "${BASIC_DESIGN_FILES[@]}"; do
  require_file "01_メインシステム/02_基本設計/$(main_bd_file "$f")"
  require_file "02_運営者システム/02_基本設計/${f}"
done

OPS_DESIGN_FILES=(
  "01_監視設計.html" "02_バックアップ・リストア設計.html" "03_ログ設計.html"
  "04_障害対応設計.html" "05_リリース・デプロイ設計.html" "06_運用手順.html"
)
for system in "01_メインシステム" "02_運営者システム"; do
  for f in "${OPS_DESIGN_FILES[@]}"; do require_file "${system}/04_運用設計/${f}"; done
done

# ============================================================================
# SC-001: 各基本設計 11 ファイルに <h1> / <h2> 見出しが存在
# ============================================================================
for f in "${BASIC_DESIGN_FILES[@]}"; do
  for path in "01_メインシステム/02_基本設計/$(main_bd_file "$f")" "02_運営者システム/02_基本設計/${f}"; do
    require_pattern "<h1[ >]" "${path}"
    require_pattern "<h2[ >]" "${path}"
  done
done

# ============================================================================
# SC-002: 共有概念正本ファイルでの必須キーワード出現
# ============================================================================
require_pattern "オーナー境界|contract_owner_user_id" "01_メインシステム/02_基本設計/08_認証・認可設計.html"
require_pattern "users" "01_メインシステム/02_基本設計/03_テーブル設計.html"
require_pattern "contract_owners" "01_メインシステム/02_基本設計/03_テーブル設計.html"
require_pattern "project_users" "01_メインシステム/02_基本設計/03_テーブル設計.html"
require_pattern "contract_owner_user_id" "01_メインシステム/02_基本設計/03_テーブル設計.html"
require_pattern "ハッシュチェーン" "02_運営者システム/02_基本設計/09_セキュリティ設計.html"
require_pattern "4-eyes" "02_運営者システム/02_基本設計/08_認証・認可設計.html"
require_pattern "IP allowlist" "02_運営者システム/02_基本設計/08_認証・認可設計.html"
require_pattern "AES-256-GCM" "01_メインシステム/02_基本設計/09_セキュリティ設計.html"

# ============================================================================
# SC-003: index 相互リンクの存在(再掲禁止・リンクのみ)
# ============================================================================
require_pattern "../../02_運営者システム/02_基本設計" "01_メインシステム/02_基本設計/index.html"
require_pattern "../../01_メインシステム/02_基本設計" "02_運営者システム/02_基本設計/index.html"
require_pattern "共有/共有概念.html" "01_メインシステム/02_基本設計/index.html"
require_pattern "共有/共有概念.html" "02_運営者システム/02_基本設計/index.html"

# ============================================================================
# SC-004: SCR ID クロスチェック
# ============================================================================
MAIN_SCRS=("SCR-001" "SCR-002" "SCR-003" "SCR-004" "SCR-004-001" "SCR-005" "SCR-006" "SCR-006-002" "SCR-007" "SCR-008" "SCR-009" "SCR-009-001" "SCR-010" "SCR-011" "SCR-012" "SCR-013" "SCR-014" "SCR-015" "SCR-016" "SCR-017" "SCR-018" "SCR-019" "SCR-020" "SCR-021" "SCR-021-001" "SCR-022" "SCR-023")
for scr in "${MAIN_SCRS[@]}"; do
  require_pattern "${scr}" "01_メインシステム/02_基本設計/01_画面設計/index.html"
  require_pattern "${scr}" "01_メインシステム/02_基本設計/07_トレーサビリティマトリクス.html"
done
ADMIN_SCRS=("SCR-090" "SCR-091" "SCR-092" "SCR-093" "SCR-094" "SCR-095" "SCR-096" "SCR-097" "SCR-098" "SCR-AUTH" "SCR-AUTH-M1" "SCR-HOME" "SCR-APPROVALS" "SCR-APPROVALS-M1" "SCR-APPROVALS-M2")
for scr in "${ADMIN_SCRS[@]}"; do
  require_pattern "${scr}" "02_運営者システム/02_基本設計/01_画面設計.html"
  require_pattern "${scr}" "02_運営者システム/02_基本設計/07_トレーサビリティマトリクス.html"
done

# ============================================================================
# SC-005: メッセージ ID 体系
# ============================================================================
require_pattern "MSG-SCR-001-" "01_メインシステム/02_基本設計/06_メッセージ一覧.html"
require_pattern "MSG-SCR-AUTH-" "02_運営者システム/02_基本設計/06_メッセージ一覧.html"

# ============================================================================
# SC-006: エラー ID 体系
# ============================================================================
require_pattern "E-AUTH-" "01_メインシステム/02_基本設計/05_エラー設計.html"
require_pattern "E-AUTHZ-" "01_メインシステム/02_基本設計/05_エラー設計.html"
require_pattern "E-BIZ-" "01_メインシステム/02_基本設計/05_エラー設計.html"
require_pattern "E-OP-AUTH-" "02_運営者システム/02_基本設計/05_エラー設計.html"
require_pattern "E-OP-4EYES-" "02_運営者システム/02_基本設計/05_エラー設計.html"

# ============================================================================
# SC-007: contract_owners.contract_status 4 値(コード値 <code>…</code> = >値<)
# ============================================================================
for v in "active" "suspended" "deleted_pending" "deleted"; do
  require_pattern ">${v}<" "01_メインシステム/02_基本設計/10_課金・請求設計.html"
  require_pattern ">${v}<|'${v}'" "01_メインシステム/02_基本設計/03_テーブル設計.html"
done

# ============================================================================
# SC-008: 通知重要度 4 値 + critical 強制送信
# ============================================================================
for v in "low" "normal" "high" "critical"; do
  require_pattern ">${v}<" "01_メインシステム/02_基本設計/06_メッセージ一覧.html"
done
require_pattern "強制送信" "01_メインシステム/02_基本設計/06_メッセージ一覧.html"

# ============================================================================
# SC-009: 連携 IF #1〜#12(メイン送信側 + 運営者主管責任表)
# ============================================================================
for if_num in 1 2 4 5 6 7 8 9 10 12; do
  require_pattern "IF #${if_num}" "01_メインシステム/02_基本設計/02_API設計/index.html"
done
require_pattern "IF#|連携 IF 主管責任|連携 IF 共通仕様" "02_運営者システム/02_基本設計/02_API設計.html"
for if_num in 1 2 4 5 6 7 8 9 10 12; do
  require_pattern ">#${if_num}<" "02_運営者システム/02_基本設計/02_API設計.html"
done

# ============================================================================
# SC-010: 参照到達性 + 運用ルール(CLAUDE.md)の構成記述
# ============================================================================
require_pattern "01_メインシステム/02_基本設計" "共有/共有概念.html"
require_pattern "02_運営者システム/02_基本設計" "共有/共有概念.html"
for layer in "01_要件定義" "02_基本設計" "03_詳細設計" "04_運用設計" "05_future"; do
  require_pattern "$layer" "CLAUDE.md"
done

# ============================================================================
# SC-011: FR / DD / FUT グループファイル(.html)の連番・件数
# ============================================================================
MAIN_FR_COUNT=$(find "01_メインシステム/01_要件定義" -maxdepth 1 -name "FR*.html" | wc -l | tr -d ' ')
require_file_series "01_メインシステム/01_要件定義" "FR" 21 "メインシステム FR"
OP_FR_COUNT=$(find "02_運営者システム/01_要件定義" -maxdepth 1 -name "FR*.html" | wc -l | tr -d ' ')
require_file_series "02_運営者システム/01_要件定義" "FR" 24 "運営者システム FR"
MAIN_DD_COUNT=$(find "01_メインシステム/03_詳細設計" -maxdepth 1 -name "DD*.html" | wc -l | tr -d ' ')
require_file_series "01_メインシステム/03_詳細設計" "DD" 14 "メインシステム DD"
OP_DD_COUNT=$(find "02_運営者システム/03_詳細設計" -maxdepth 1 -name "DD*.html" | wc -l | tr -d ' ')
require_file_series "02_運営者システム/03_詳細設計" "DD" 12 "運営者システム DD"
MAIN_FUT_COUNT=$(find "01_メインシステム/05_future" -maxdepth 1 -name "FUT*.html" | wc -l | tr -d ' ')
require_unique_file_series "01_メインシステム/05_future" "FUT" 6 "メインシステム FUT"
OP_FUT_COUNT=$(find "02_運営者システム/05_future" -maxdepth 1 -name "FUT*.html" | wc -l | tr -d ' ')
require_unique_file_series "02_運営者システム/05_future" "FUT" 3 "運営者システム FUT"

# ============================================================================
# SC-012: 番号体系の連続性(HTML 見出し / テーブル解析)+ 廃番識別子の再混入防止
# ============================================================================
python3 - <<'PY'
import re, sys
def read(p):
    with open(p, encoding="utf-8") as f: return f.read()
def fail(m): print("ERROR: "+m, file=sys.stderr); sys.exit(1)

def heading_nums(path, level, prefix, suffix=r' '):
    """<hLEVEL ...>PREFIX(\d+)SUFFIX を順に抽出。"""
    t = read(path)
    pat = r'<h%d[^>]*>%s([0-9]+)%s' % (level, re.escape(prefix), suffix)
    return [int(x) for x in re.findall(pat, t)]

def check_seq(label, actual, expected):
    if actual != expected:
        fail("%s が不連続: actual=%s expected=%s" % (label, actual, expected))

M = "01_メインシステム/02_基本設計/"

# (a) テーブル一覧 2.1 の第 1 列 = 1..31
t = read(M + "03_テーブル設計.html")
seg = re.search(r'<h3[^>]*>2\.1.*?(?=<h3[^>]*>2\.2|\Z)', t, re.S).group(0)
tbl = re.search(r'<table>.*?</table>', seg, re.S).group(0)
nums = [int(x) for x in re.findall(r'<tr>\s*<td>(\d+)</td>', tbl)]
check_seq("メインテーブル一覧", nums, list(range(1, 32)))

# (b) テーブル詳細節 3.N = 1..31
check_seq("メインテーブル詳細節", heading_nums(M+"03_テーブル設計.html", 3, "3."), list(range(1, 32)))
# (d) 画面メッセージ節 4.N (SCR-|エンドユーザー) = 1..27
t = read(M + "06_メッセージ一覧.html")
msg = [int(x) for x in re.findall(r'<h3[^>]*>4\.([0-9]+) (?:SCR-|エンドユーザー)', t)]
check_seq("メイン画面メッセージ節", msg, list(range(1, 28)))
# (e) メールテンプレート節 4.N TPL- = 1..14
t = read(M + "11_メール設計.html")
mail = [int(x) for x in re.findall(r'<h3[^>]*>4\.([0-9]+) TPL-', t)]
check_seq("メインメールテンプレート節", mail, list(range(1, 15)))
# (f) API 一覧(分割後 index)に全カテゴリの API-<PFX>- リンクが存在
t = read(M + "02_API設計/index.html")
napi = len(re.findall(r'href="API-[A-Z]+-[0-9]+\.html"', t))
if napi < 60: fail("メイン API 一覧リンク数が不足: %d (期待 62 前後)" % napi)
PY

# (g) FR-070..077 が未解決質問登録の両システム文書に出現、FR-078/079 は再混入禁止
for fr in 070 071 072 073 074 075 076 077; do
  require_pattern ">FR-${fr}<" "01_メインシステム/01_要件定義/FR06_未解決質問登録.html"
  require_pattern ">FR-${fr}<" "02_運営者システム/01_要件定義/FR06_未解決質問登録.html"
done
reject_pattern "FR-078|FR-079" "01_メインシステム/01_要件定義/FR06_未解決質問登録.html"
reject_pattern "FR-078|FR-079" "02_運営者システム/01_要件定義/FR06_未解決質問登録.html"

# (h)-(k) 廃番識別子の再混入防止(.html 走査)
if grep -R -E --include='*.html' 'SCR-(028|029|030|031|032|035|036|037|038|039|040|041|042)' \
  "01_メインシステム/01_要件定義" "01_メインシステム/02_基本設計" \
  "01_メインシステム/03_詳細設計" "01_メインシステム/04_運用設計" >/dev/null; then
  fail "メインシステムの現行文書に旧 SCR ID が残っている"
fi
if grep -R -E --include='*.html' 'SCR-099' \
  "02_運営者システム/01_要件定義" "02_運営者システム/02_基本設計" \
  "02_運営者システム/03_詳細設計" "02_運営者システム/04_運用設計" >/dev/null; then
  fail "運営者システムの現行文書に旧 SCR-099 が残っている"
fi
if grep -R -E --include='*.html' 'inquiry_status_history|TPL-FAQ_REGISTERED|NOTIF-CHAT_REPLY_TO_USER|notification-settings|E-AUTHZ-ADMIN-DELETE-PROTECTED|MSG-COMMON-ADMIN-DELETE-PROTECTED|MSG-SCR-009-M1-TOOLTIP-ADMIN-DELETE' \
  "01_メインシステム/01_要件定義" "01_メインシステム/02_基本設計" \
  "01_メインシステム/03_詳細設計" "01_メインシステム/04_運用設計" >/dev/null; then
  fail "削除済み識別子がメインシステムの現行文書に再混入している"
fi
if grep -R -E --include='*.html' 'MSG-SCR-HOME-EMPTY-001|MSG-SCR-095-WARN-001' \
  "02_運営者システム/01_要件定義" "02_運営者システム/02_基本設計" \
  "02_運営者システム/03_詳細設計" "02_運営者システム/04_運用設計" >/dev/null; then
  fail "削除済み識別子が運営者システムの現行文書に再混入している"
fi

# ============================================================================
echo "spec sync smoke check passed (SC-001 〜 SC-012) [HTML 正本]"
echo "  - 要件定義 FR: メイン ${MAIN_FR_COUNT} / 運営者 ${OP_FR_COUNT}"
echo "  - 詳細設計 DD: メイン ${MAIN_DD_COUNT} / 運営者 ${OP_DD_COUNT}"
echo "  - 将来対応 FUT: メイン ${MAIN_FUT_COUNT} / 運営者 ${OP_FUT_COUNT}"
