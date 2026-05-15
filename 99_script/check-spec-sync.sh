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
require_file "01_main/01_requirements.md"
require_file "01_main/02_basic_design.md"
require_file "02_admin/01_requirements.md"
require_file "02_admin/02_basic_design.md"
require_file "04_future/future_requirements.md"

# Current document versions referenced from the basic design reference sections.
require_pattern "顧客管理システム 要件定義書 v2\\.6" "01_main/02_basic_design.md"
require_pattern "顧客管理システム 基本設計書 v3\\.3" "01_main/02_basic_design.md"
require_pattern "要件定義書 v2\\.6" "02_admin/02_basic_design.md"
require_pattern "メインシステム要件定義 v2\\.6" "02_admin/02_basic_design.md"
require_pattern "メインシステム基本設計 v3\\.3" "02_admin/02_basic_design.md"

# Shared state and notification definitions remain in the basic design docs as the source of truth.
require_pattern "active.*/.*suspended.*/.*deleted_pending.*/.*deleted" "01_main/02_basic_design.md"
require_pattern "active.*/.*suspended.*/.*deleted_pending.*/.*deleted" "02_admin/02_basic_design.md"
reject_pattern "tenants\\.status='pending_legal_review'" "02_admin/02_basic_design.md"
require_pattern "tenant_registration_reviews\\.status='pending_legal_review'" "02_admin/02_basic_design.md"

# Notification importance: English enum tokens must live in basic design; requirement docs must use business terms only.
require_pattern "low.*/.*normal.*/.*high.*/.*critical" "01_main/02_basic_design.md"
require_pattern "low.*/.*normal.*/.*high.*/.*critical" "02_admin/02_basic_design.md"
reject_pattern "low.*/.*normal.*/.*high.*/.*critical" "01_main/01_requirements.md"
reject_pattern "low.*/.*normal.*/.*high.*/.*critical" "02_admin/01_requirements.md"
require_pattern "低.*通常.*重要.*最重要|低」「通常」「重要」「最重要" "01_main/01_requirements.md"
require_pattern "低.*通常.*重要.*最重要|低」「通常」「重要」「最重要" "02_admin/01_requirements.md"

# Requirement docs must not embed DB identifiers used as design tokens.
reject_pattern "\\\`tenants\\.status\\\`" "01_main/01_requirements.md"
reject_pattern "\\\`tenants\\.status\\\`" "02_admin/01_requirements.md"
reject_pattern "\\\`case_status\\\`" "01_main/01_requirements.md"
reject_pattern "\\\`case_status\\\`" "02_admin/01_requirements.md"

# External interface specs: requirements keep WHAT and basic design owns HOW.
require_pattern "外部インターフェース要件" "01_main/01_requirements.md"
require_pattern "連携要件\\(WHAT\\).*基本設計書 §8" "01_main/01_requirements.md"
require_pattern "連携要件\\(WHAT\\).*基本設計書 §8" "02_admin/01_requirements.md"
require_pattern "対応 FR\\(メインシステム\\).*対応 FR\\(顧客管理システム\\)" "01_main/02_basic_design.md"
require_pattern "通信仕様正本はメイン基本設計 §8\\.7\\.2 / §8\\.7\\.3" "02_admin/02_basic_design.md"
reject_pattern "通信方式・認証方式を定義する|正本マトリクス|§11\\.3\\.[1-2]|§11\\.5\\.[1-5]" "01_main/01_requirements.md"
reject_pattern "通信方式・認証方式を定義する|正本マトリクス|§11\\.3\\.[1-2]|§11\\.5\\.[1-5]" "02_admin/01_requirements.md"

# FR-079 / AC-024: retention must not auto-close inquiry case_status.
reject_pattern "730 日.*closed|強制.*closed|case\\.close\\.by_system_failsafe" "01_main/02_basic_design.md"
require_pattern "case_status.*変更しない|自動遷移させず" "01_main/02_basic_design.md"

# Acceptance-condition trace.
require_pattern "AC-047" "01_main/02_basic_design.md"
require_pattern "AC-047" "02_admin/02_basic_design.md"

# Future baseline must follow current MVP FR-089 value.
require_pattern "FR-089.*自動クローズ段階 1 は 7 日" "04_future/future_requirements.md"

echo "spec sync smoke check passed"
