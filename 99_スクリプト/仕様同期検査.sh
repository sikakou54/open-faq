#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

require_file() {
  [[ -f "$1" ]] || fail "missing required file: $1"
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

require_file "CLAUDE.md"
require_file "01_メインシステム/01_要件定義書.md"
require_file "01_メインシステム/02_基本設計書.md"
require_file "02_運営者システム/01_要件定義書.md"
require_file "02_運営者システム/02_基本設計書.md"
require_file "04_将来拡張/01_将来要件定義書.md"

# Shared state and notification definitions remain in the basic design docs as the source of truth.
require_pattern "active.*/.*suspended.*/.*deleted_pending.*/.*deleted" "01_メインシステム/02_基本設計書.md"
require_pattern "active.*/.*suspended.*/.*deleted_pending.*/.*deleted" "02_運営者システム/02_基本設計書.md"
require_pattern "owner_registration_reviews\\.status='pending_legal_review'" "02_運営者システム/02_基本設計書.md"

# Notification importance: English enum tokens must live in basic design; requirement docs must use business terms only.
require_pattern "low.*/.*normal.*/.*high.*/.*critical" "01_メインシステム/02_基本設計書.md"
require_pattern "low.*/.*normal.*/.*high.*/.*critical" "02_運営者システム/02_基本設計書.md"
reject_pattern "low.*/.*normal.*/.*high.*/.*critical" "01_メインシステム/01_要件定義書.md"
reject_pattern "low.*/.*normal.*/.*high.*/.*critical" "02_運営者システム/01_要件定義書.md"
require_pattern "低.*通常.*重要.*最重要|低」「通常」「重要」「最重要" "01_メインシステム/01_要件定義書.md"
require_pattern "低.*通常.*重要.*最重要|低」「通常」「重要」「最重要" "02_運営者システム/01_要件定義書.md"

# Requirement docs must not embed DB identifiers used as design tokens.
reject_pattern "\\\`case_status\\\`" "01_メインシステム/01_要件定義書.md"
reject_pattern "\\\`case_status\\\`" "02_運営者システム/01_要件定義書.md"

# External interface specs: requirements keep WHAT and basic design owns HOW.
require_pattern "外部インターフェース要件" "01_メインシステム/01_要件定義書.md"
require_pattern "連携要件\\(WHAT\\).*基本設計書 §8" "01_メインシステム/01_要件定義書.md"
require_pattern "連携要件\\(WHAT\\).*基本設計書 §8" "02_運営者システム/01_要件定義書.md"
require_pattern "対応 FR\\(メインシステム\\).*対応 FR\\(顧客管理システム\\)" "01_メインシステム/02_基本設計書.md"
require_pattern "通信仕様正本はメイン基本設計 §8\\.7\\.2 / §8\\.7\\.3" "02_運営者システム/02_基本設計書.md"
reject_pattern "通信方式・認証方式を定義する|正本マトリクス|§11\\.3\\.[1-2]|§11\\.5\\.[1-5]" "01_メインシステム/01_要件定義書.md"
reject_pattern "通信方式・認証方式を定義する|正本マトリクス|§11\\.3\\.[1-2]|§11\\.5\\.[1-5]" "02_運営者システム/01_要件定義書.md"

# FR-079 / AC-024: retention must not auto-close inquiry case_status.
reject_pattern "730 日.*closed|強制.*closed|case\\.close\\.by_system_failsafe" "01_メインシステム/02_基本設計書.md"
require_pattern "case_status.*変更しない|自動遷移させず" "01_メインシステム/02_基本設計書.md"

# Acceptance-condition trace.
require_pattern "AC-047" "01_メインシステム/02_基本設計書.md"
require_pattern "AC-047" "02_運営者システム/02_基本設計書.md"

# Future baseline must follow current MVP FR-089 value.
require_pattern "FR-089.*自動クローズ段階 1 は 7 日" "04_将来拡張/01_将来要件定義書.md"

# ============================================================================
# 11 ドキュメント体系の個別設計書群 checks (SC-001 ~ SC-010)
# ============================================================================

DISTRIBUTED_FILES=(
  "01_メインシステム/個別設計書群/00_索引.md"
  "01_メインシステム/個別設計書群/02_画面設計書.md"
  "01_メインシステム/個別設計書群/03_API設計書.md"
  "01_メインシステム/個別設計書群/04_テーブル定義書.md"
  "01_メインシステム/個別設計書群/05_権限設計書.md"
  "01_メインシステム/個別設計書群/06_エラー設計書.md"
  "01_メインシステム/個別設計書群/07_メッセージ一覧.md"
  "01_メインシステム/個別設計書群/08_トレーサビリティマトリクス.md"
  "01_メインシステム/個別設計書群/09_認証認可設計書.md"
  "01_メインシステム/個別設計書群/10_セキュリティ設計書.md"
  "01_メインシステム/個別設計書群/11_課金請求設計書.md"
  "02_運営者システム/個別設計書群/00_索引.md"
  "02_運営者システム/個別設計書群/02_画面設計書.md"
  "02_運営者システム/個別設計書群/03_API設計書.md"
  "02_運営者システム/個別設計書群/04_テーブル定義書.md"
  "02_運営者システム/個別設計書群/05_権限設計書.md"
  "02_運営者システム/個別設計書群/06_エラー設計書.md"
  "02_運営者システム/個別設計書群/07_メッセージ一覧.md"
  "02_運営者システム/個別設計書群/08_トレーサビリティマトリクス.md"
  "02_運営者システム/個別設計書群/09_認証認可設計書.md"
  "02_運営者システム/個別設計書群/10_セキュリティ設計書.md"
  "02_運営者システム/個別設計書群/11_課金請求設計書.md"
  "共有/共有概念.md"
)

# SC-001: Required header in each 個別設計書群ファイル (# 文書名 + ## 1. 文書概要 + 関連ドキュメント or equivalent)
# 索引(00_索引.md) と 共有概念.md は構造が異なるため除外、それ以外をチェック
for f in "${DISTRIBUTED_FILES[@]}"; do
  [[ -f "$f" ]] || fail "missing required file: $f"
  case "$f" in
    */00_索引.md|*/共有概念.md)
      # index / shared concepts は通常の文書概要を持たないためスキップ
      ;;
    *)
      require_pattern "^# " "$f"
      require_pattern "^## 1\\." "$f"
      require_pattern "関連ドキュメント|Related" "$f"
      ;;
  esac
done

# SC-007: accounts.contract_status 4 values must each appear in main billing (canonical)
for v in "active" "suspended" "deleted_pending" "deleted"; do
  require_pattern "\\\`${v}\\\`|${v} \\|" "01_メインシステム/個別設計書群/11_課金請求設計書.md"
  require_pattern "\\\`${v}\\\`|'${v}'" "01_メインシステム/個別設計書群/04_テーブル定義書.md"
done

# SC-008: Notification importance 4 values + critical メール強制送信
for v in "low" "normal" "high" "critical"; do
  require_pattern "\\\`${v}\\\`" "01_メインシステム/個別設計書群/07_メッセージ一覧.md"
done
require_pattern "強制送信" "01_メインシステム/個別設計書群/07_メッセージ一覧.md"

# SC-009: Connectors IF #1〜#12 catalog must appear in both main and admin API designs
# (main: 個別 §5.13.x で全 IF を扱う / admin: §5.8.1 主管責任表で全 IF を表化)
for if_num in 1 2 4 5 6 7 8 9 10 12; do
  require_pattern "IF #${if_num}" "01_メインシステム/個別設計書群/03_API設計書.md"
done
# 運営者側は主管責任表で行ごとに記載されるため、表ヘッダ「IF#」「#1」等の存在を確認
require_pattern "IF#" "02_運営者システム/個別設計書群/03_API設計書.md"
require_pattern "連携 IF 主管責任|連携 IF 共通仕様" "02_運営者システム/個別設計書群/03_API設計書.md"
for if_num in 1 2 4 5 6 7 8 9 10 12; do
  # admin では行頭 | #N | のように記載
  require_pattern "\\| #${if_num} \\|" "02_運営者システム/個別設計書群/03_API設計書.md"
done

# SC-002: Shared concept keywords must appear in canonical files
require_pattern "オーナー境界|owner_account_id" "01_メインシステム/個別設計書群/09_認証認可設計書.md"
require_pattern "ハッシュチェーン" "02_運営者システム/個別設計書群/10_セキュリティ設計書.md"
require_pattern "4-eyes" "02_運営者システム/個別設計書群/09_認証認可設計書.md"
require_pattern "IP allowlist" "02_運営者システム/個別設計書群/09_認証認可設計書.md"
require_pattern "AES-256-GCM" "01_メインシステム/個別設計書群/10_セキュリティ設計書.md"

# SC-006: Error ID pattern E-* in main / E-OP-* in admin
require_pattern "E-AUTH-" "01_メインシステム/個別設計書群/06_エラー設計書.md"
require_pattern "E-AUTHZ-" "01_メインシステム/個別設計書群/06_エラー設計書.md"
require_pattern "E-BIZ-" "01_メインシステム/個別設計書群/06_エラー設計書.md"
require_pattern "E-OP-AUTH-" "02_運営者システム/個別設計書群/06_エラー設計書.md"
require_pattern "E-OP-4EYES-" "02_運営者システム/個別設計書群/06_エラー設計書.md"

# SC-005: Message ID pattern MSG-* in both
require_pattern "MSG-SCR-001-" "01_メインシステム/個別設計書群/07_メッセージ一覧.md"
require_pattern "MSG-SCR-AUTH-" "02_運営者システム/個別設計書群/07_メッセージ一覧.md"

# SC-004: SCR ID coverage - all 20 main SCRs in screen design / all 15 admin SCRs in screen design
MAIN_SCRS=("SCR-001" "SCR-002" "SCR-003" "SCR-010" "SCR-010-M1" "SCR-011" "SCR-012" "SCR-013" "SCR-014" "SCR-015" "SCR-016" "SCR-017" "SCR-017-M1" "SCR-018" "SCR-021" "SCR-022" "SCR-023" "SCR-024" "SCR-025" "SCR-027")
for scr in "${MAIN_SCRS[@]}"; do
  require_pattern "${scr}" "01_メインシステム/個別設計書群/02_画面設計書.md"
done
ADMIN_SCRS=("SCR-090" "SCR-091" "SCR-092" "SCR-093" "SCR-094" "SCR-096" "SCR-097" "SCR-098" "SCR-099" "SCR-AUTH" "SCR-AUTH-M1" "SCR-HOME" "SCR-APPROVALS" "SCR-APPROVALS-M1" "SCR-APPROVALS-M2")
for scr in "${ADMIN_SCRS[@]}"; do
  require_pattern "${scr}" "02_運営者システム/個別設計書群/02_画面設計書.md"
done

# SC-003: Reference-only enforcement for cross-document concepts
# (rough check: ensure cross-references with [...](...) syntax exist; deep mutual-reference rules are documented but not enforced here)
require_pattern "../../01_メインシステム/個別設計書群" "02_運営者システム/個別設計書群/00_索引.md"
require_pattern "../../02_運営者システム/個別設計書群" "01_メインシステム/個別設計書群/00_索引.md"
require_pattern "../../共有/共有概念.md" "01_メインシステム/個別設計書群/00_索引.md"
require_pattern "../../共有/共有概念.md" "02_運営者システム/個別設計書群/00_索引.md"

# SC-010: Document baseline — CLAUDE.md must describe the 11-document layout.
require_pattern "11 ドキュメント体系" "CLAUDE.md"

echo "spec sync smoke check passed (incl. SC-001~SC-010)"
