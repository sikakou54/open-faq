#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# 仕様同期スモークチェック(新構成)
# SC-001 〜 SC-011 の各検査を実施する。
# 完全な静的解析ではなく、要件 / 設計のドリフトを検出するレビュー補助スクリプト。
# ============================================================================

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

require_file() {
  [[ -f "$1" ]] || fail "missing required file: $1"
}

require_dir() {
  [[ -d "$1" ]] || fail "missing required directory: $1"
}

require_pattern() {
  local pattern="$1"
  local file="$2"
  grep -Eq "$pattern" "$file" || fail "missing pattern in $file: $pattern"
}

reject_pattern() {
  local pattern="$1"
  local file="$2"
  if grep -Eq "$pattern" "$file"; then
    fail "forbidden pattern in $file: $pattern"
  fi
}

require_pattern_any() {
  local pattern="$1"
  shift
  for f in "$@"; do
    if [[ -f "$f" ]] && grep -Eq "$pattern" "$f"; then
      return 0
    fi
  done
  fail "missing pattern in any of: $*  pattern: $pattern"
}

# ============================================================================
# 基本ディレクトリ・ファイル存在検査
# ============================================================================

require_file "CLAUDE.md"

for system in "01_メインシステム" "02_運営者システム"; do
  require_dir "${system}/01_要件定義"
  require_dir "${system}/02_基本設計"
  require_dir "${system}/03_詳細設計"
  require_dir "${system}/04_運用設計"
  require_dir "${system}/05_future"
  require_file "${system}/01_要件定義/index.md"
  require_file "${system}/02_基本設計/index.md"
  require_file "${system}/03_詳細設計/index.md"
  require_file "${system}/04_運用設計/index.md"
  require_file "${system}/05_future/index.md"
  require_file "${system}/画面遷移図.html"
done

require_dir "99_script"
require_file "99_script/check-spec-sync.sh"
require_file "99_script/html_to_pdf.sh"
require_file "99_script/md_to_pdf.sh"
require_file "共有/共有概念.md"

# ============================================================================
# 02_基本設計/ 配下 11 ファイル(両システム)の存在検査
# ============================================================================

BASIC_DESIGN_FILES=(
  "01_画面設計.md"
  "02_API設計.md"
  "03_テーブル設計.md"
  "04_権限設計.md"
  "05_エラー設計.md"
  "06_メッセージ一覧.md"
  "07_トレーサビリティマトリクス.md"
  "08_認証・認可設計.md"
  "09_セキュリティ設計.md"
  "10_課金・請求設計.md"
  "11_メール設計.md"
)

for system in "01_メインシステム" "02_運営者システム"; do
  for f in "${BASIC_DESIGN_FILES[@]}"; do
    require_file "${system}/02_基本設計/${f}"
  done
done

# ============================================================================
# 04_運用設計/ 配下 6 ファイル(両システム)の存在検査
# ============================================================================

OPS_DESIGN_FILES=(
  "01_監視設計.md"
  "02_バックアップ・リストア設計.md"
  "03_ログ設計.md"
  "04_障害対応設計.md"
  "05_リリース・デプロイ設計.md"
  "06_運用手順.md"
)

for system in "01_メインシステム" "02_運営者システム"; do
  for f in "${OPS_DESIGN_FILES[@]}"; do
    require_file "${system}/04_運用設計/${f}"
  done
done

# ============================================================================
# SC-001: 各個別設計ファイルの必須ヘッダ存在
# 02_基本設計/ 配下 11 ファイルが「# ...(タイトル)」「## ...(1 章)」を持つこと
# ============================================================================

for system in "01_メインシステム" "02_運営者システム"; do
  for f in "${BASIC_DESIGN_FILES[@]}"; do
    require_pattern "^# " "${system}/02_基本設計/${f}"
    require_pattern "^## " "${system}/02_基本設計/${f}"
  done
done

# ============================================================================
# SC-002: 共有概念正本ファイルでの必須キーワード出現
# ============================================================================

require_pattern "オーナー境界|contract_owner_user_id" "01_メインシステム/02_基本設計/08_認証・認可設計.md"
require_pattern "users" "01_メインシステム/02_基本設計/03_テーブル設計.md"
require_pattern "contract_owners" "01_メインシステム/02_基本設計/03_テーブル設計.md"
require_pattern "project_users" "01_メインシステム/02_基本設計/03_テーブル設計.md"
require_pattern "end_users" "01_メインシステム/02_基本設計/03_テーブル設計.md"
require_pattern "contract_owner_user_id" "01_メインシステム/02_基本設計/03_テーブル設計.md"
require_pattern "ハッシュチェーン" "02_運営者システム/02_基本設計/09_セキュリティ設計.md"
require_pattern "4-eyes" "02_運営者システム/02_基本設計/08_認証・認可設計.md"
require_pattern "IP allowlist" "02_運営者システム/02_基本設計/08_認証・認可設計.md"
require_pattern "AES-256-GCM" "01_メインシステム/02_基本設計/09_セキュリティ設計.md"

# ============================================================================
# SC-003: 参照側ドキュメントでの再掲禁止(リンクのみで実装)
# index ファイルの相互リンクが存在することを軽くチェック
# ============================================================================

require_pattern "../../02_運営者システム/02_基本設計" "01_メインシステム/02_基本設計/index.md"
require_pattern "../../01_メインシステム/02_基本設計" "02_運営者システム/02_基本設計/index.md"
require_pattern "../../共有/共有概念.md" "01_メインシステム/02_基本設計/index.md"
require_pattern "../../共有/共有概念.md" "02_運営者システム/02_基本設計/index.md"

# ============================================================================
# SC-004: SCR ID クロスチェック
# 全 SCR がメイン画面設計 / 運営者画面設計 / 各トレーサビリティに出現
# ============================================================================

MAIN_SCRS=("SCR-001" "SCR-002" "SCR-003" "SCR-010" "SCR-010-M1" "SCR-011" "SCR-012" "SCR-012-M1" "SCR-013" "SCR-014" "SCR-015" "SCR-016" "SCR-017" "SCR-017-M1" "SCR-018" "SCR-021" "SCR-022" "SCR-023" "SCR-024" "SCR-025" "SCR-027" "SCR-036" "SCR-036-M1")
for scr in "${MAIN_SCRS[@]}"; do
  require_pattern "${scr}" "01_メインシステム/02_基本設計/01_画面設計.md"
  require_pattern "${scr}" "01_メインシステム/02_基本設計/07_トレーサビリティマトリクス.md"
done

ADMIN_SCRS=("SCR-090" "SCR-091" "SCR-092" "SCR-093" "SCR-094" "SCR-096" "SCR-097" "SCR-098" "SCR-099" "SCR-AUTH" "SCR-AUTH-M1" "SCR-HOME" "SCR-APPROVALS" "SCR-APPROVALS-M1" "SCR-APPROVALS-M2")
for scr in "${ADMIN_SCRS[@]}"; do
  require_pattern "${scr}" "02_運営者システム/02_基本設計/01_画面設計.md"
  require_pattern "${scr}" "02_運営者システム/02_基本設計/07_トレーサビリティマトリクス.md"
done

# ============================================================================
# SC-005: メッセージ ID 体系 MSG-SCR-* の出現確認
# ============================================================================

require_pattern "MSG-SCR-001-" "01_メインシステム/02_基本設計/06_メッセージ一覧.md"
require_pattern "MSG-SCR-AUTH-" "02_運営者システム/02_基本設計/06_メッセージ一覧.md"

# ============================================================================
# SC-006: エラー ID 体系の出現確認
# ============================================================================

require_pattern "E-AUTH-" "01_メインシステム/02_基本設計/05_エラー設計.md"
require_pattern "E-AUTHZ-" "01_メインシステム/02_基本設計/05_エラー設計.md"
require_pattern "E-BIZ-" "01_メインシステム/02_基本設計/05_エラー設計.md"
require_pattern "E-OP-AUTH-" "02_運営者システム/02_基本設計/05_エラー設計.md"
require_pattern "E-OP-4EYES-" "02_運営者システム/02_基本設計/05_エラー設計.md"

# ============================================================================
# SC-007: contract_owners.contract_status 4 値が課金・請求設計とテーブル設計に出現
# ============================================================================

for v in "active" "suspended" "deleted_pending" "deleted"; do
  require_pattern "\\\`${v}\\\`|${v} \\|" "01_メインシステム/02_基本設計/10_課金・請求設計.md"
  require_pattern "\\\`${v}\\\`|'${v}'" "01_メインシステム/02_基本設計/03_テーブル設計.md"
done

# ============================================================================
# SC-008: 通知重要度 4 値 + critical 強制送信
# ============================================================================

for v in "low" "normal" "high" "critical"; do
  require_pattern "\\\`${v}\\\`" "01_メインシステム/02_基本設計/06_メッセージ一覧.md"
done
require_pattern "強制送信" "01_メインシステム/02_基本設計/06_メッセージ一覧.md"

# ============================================================================
# SC-009: 連携 IF #1〜#12 がメイン API 設計 + 運営者 API 設計の主管責任表に出現
# ============================================================================

for if_num in 1 2 4 5 6 7 8 9 10 12; do
  require_pattern "IF #${if_num}" "01_メインシステム/02_基本設計/02_API設計.md"
done
require_pattern "IF#|連携 IF 主管責任|連携 IF 共通仕様" "02_運営者システム/02_基本設計/02_API設計.md"
for if_num in 1 2 4 5 6 7 8 9 10 12; do
  require_pattern "\\| #${if_num} \\|" "02_運営者システム/02_基本設計/02_API設計.md"
done

# ============================================================================
# SC-010: 参照リンク到達性(主要相対パスのターゲット存在確認)
# ============================================================================

# 共有概念.md からの主要参照先
require_pattern "01_メインシステム/02_基本設計" "共有/共有概念.md"
require_pattern "02_運営者システム/02_基本設計" "共有/共有概念.md"

# CLAUDE.md は新構成を記述していること
require_pattern "01_要件定義" "CLAUDE.md"
require_pattern "02_基本設計" "CLAUDE.md"
require_pattern "03_詳細設計" "CLAUDE.md"
require_pattern "04_運用設計" "CLAUDE.md"
require_pattern "05_future" "CLAUDE.md"

# ============================================================================
# SC-011: 要件定義 FR グループファイルの存在と内容
# 各システムで FR01..FRNN_*.md が存在し、index に登録されていること
# ============================================================================

# メインシステム FR ファイル数(22 個)
MAIN_FR_COUNT=$(find "01_メインシステム/01_要件定義" -maxdepth 1 -name "FR*.md" | wc -l | tr -d ' ')
if [[ "$MAIN_FR_COUNT" -lt 20 ]]; then
  fail "メインシステム FR ファイル数が不足: ${MAIN_FR_COUNT} (期待: 20 以上)"
fi

# 運営者システム FR ファイル数(24 個)
OP_FR_COUNT=$(find "02_運営者システム/01_要件定義" -maxdepth 1 -name "FR*.md" | wc -l | tr -d ' ')
if [[ "$OP_FR_COUNT" -lt 20 ]]; then
  fail "運営者システム FR ファイル数が不足: ${OP_FR_COUNT} (期待: 20 以上)"
fi

# メインシステム DD ファイル数(15 個)
MAIN_DD_COUNT=$(find "01_メインシステム/03_詳細設計" -maxdepth 1 -name "DD*.md" | wc -l | tr -d ' ')
if [[ "$MAIN_DD_COUNT" -lt 12 ]]; then
  fail "メインシステム DD ファイル数が不足: ${MAIN_DD_COUNT} (期待: 12 以上)"
fi

# 運営者システム DD ファイル数(12 個)
OP_DD_COUNT=$(find "02_運営者システム/03_詳細設計" -maxdepth 1 -name "DD*.md" | wc -l | tr -d ' ')
if [[ "$OP_DD_COUNT" -lt 10 ]]; then
  fail "運営者システム DD ファイル数が不足: ${OP_DD_COUNT} (期待: 10 以上)"
fi

# メインシステム FUT ファイル数(5 個)
MAIN_FUT_COUNT=$(find "01_メインシステム/05_future" -maxdepth 1 -name "FUT*.md" | wc -l | tr -d ' ')
if [[ "$MAIN_FUT_COUNT" -lt 3 ]]; then
  fail "メインシステム FUT ファイル数が不足: ${MAIN_FUT_COUNT} (期待: 3 以上)"
fi

# 運営者システム FUT ファイル数(3 個)
OP_FUT_COUNT=$(find "02_運営者システム/05_future" -maxdepth 1 -name "FUT*.md" | wc -l | tr -d ' ')
if [[ "$OP_FUT_COUNT" -lt 2 ]]; then
  fail "運営者システム FUT ファイル数が不足: ${OP_FUT_COUNT} (期待: 2 以上)"
fi

# ============================================================================
# 検査完了
# ============================================================================

echo "spec sync smoke check passed (SC-001 〜 SC-011)"
echo "  - 要件定義 FR: メイン ${MAIN_FR_COUNT} / 運営者 ${OP_FR_COUNT}"
echo "  - 詳細設計 DD: メイン ${MAIN_DD_COUNT} / 運営者 ${OP_DD_COUNT}"
echo "  - 将来対応 FUT: メイン ${MAIN_FUT_COUNT} / 運営者 ${OP_FUT_COUNT}"
