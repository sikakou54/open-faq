#!/usr/bin/env bash
# 設計再構成プロジェクトの GitHub Issue を一括起票し、解決済みを Close するスクリプト。
#
# 背景: 再構成作業中、GitHub MCP / gh CLI が当該セッションで利用不可だったため
#       Issue 操作を実行できなかった。本スクリプトは復旧後に 1 回実行することで、
#       エピック・フェーズ・検出課題を起票し、解決済み課題を Close する(冪等)。
#
# 前提: gh CLI が認証済み(`gh auth status`)であること。
# 使い方: bash 99_management/gh_issues.sh
#
# 冪等性: 同名タイトルの Issue が既に存在する場合は再作成しない。
set -euo pipefail
REPO="sikakou54/open-faq"
LABEL_BASE="design-restructure"

gh() { command gh "$@"; }

ensure_label() { # name color desc
  gh label create "$1" --repo "$REPO" --color "$2" --description "$3" 2>/dev/null \
    || gh label edit "$1" --repo "$REPO" --color "$2" --description "$3" 2>/dev/null || true
}

# 既存タイトル一覧(完全一致判定用)
existing_titles() { gh issue list --repo "$REPO" --state all --limit 400 --json title --jq '.[].title'; }
TITLES="$(existing_titles || true)"

find_num() { # title -> issue number (or empty)
  gh issue list --repo "$REPO" --state all --limit 400 --json number,title \
    --jq ".[] | select(.title==\"$1\") | .number" | head -1
}

mk() { # title labels body  -> creates if absent, echoes number
  local title="$1" labels="$2" body="$3" num
  if grep -Fxq "$title" <<<"$TITLES"; then
    num="$(find_num "$title")"
    echo "[skip-exists #$num] $title" >&2
  else
    num="$(gh issue create --repo "$REPO" --title "$title" --label "$labels" --body "$body" \
            | grep -oE '[0-9]+$' || true)"
    TITLES="$TITLES"$'\n'"$title"
    echo "[created #$num] $title" >&2
  fi
  echo "$num"
}

mk_closed() { # title labels body closecomment
  local num; num="$(mk "$1" "$2" "$3")"
  if [ -n "$num" ]; then
    gh issue close "$num" --repo "$REPO" --comment "$4" 2>/dev/null || true
    echo "[closed #$num] $1" >&2
  fi
}

echo "== ラベル整備 =="
ensure_label "$LABEL_BASE"      "5319e7" "要件定義書・基本設計書 再構成プロジェクト"
ensure_label "traceability"     "1d76db" "トレーサビリティ(要件↔UC↔SCR↔EVT↔API↔TBL)"
ensure_label "design-gap"       "d93f0b" "設計上の被覆/連結ギャップ"
ensure_label "needs-review"     "fbca04" "人的レビュー・判断が必要"
ensure_label "cleanup"          "0e8a16" "表記・体裁・重複の整理"
ensure_label "migration"        "c5def5" "記述の移管・棚卸し"

echo "== エピック =="
EPIC="$(mk "[設計再構成][エピック] 要件定義書・基本設計書 再構成" "$LABEL_BASE" \
"2 階層(01_requirements / 02_basic_design)で 要件定義 ＞ 業務ユースケース ＞ 画面設計 ＞ 画面イベント ＞ API設計 ＞ DB設計 ＞ シーケンス ＞ 権限/エラー/メッセージ の上流→下流トレースを確立する再構成。

## 完了状況
- 構造再編 P0〜P8: 完了(全ID個別/フラット採番、CLAUDE.md 改訂、両 99_restructure_result.md)。
- 被覆ギャップ解消(第1〜3段): UC→要件 128→0 / FR→UC 132→0 / RULE・孤立BR 結線。
- 構造ギャップ(API/TBL): 連結補完・分類で解消。
- リンク/アンカー: 0/0(1282 ページ)。

詳細レポート: 99_management/07_coverage_gap_report.md")"

echo "== フェーズ Issue(解決済み=Close) =="
mk_closed "[設計再構成][基盤] ディレクトリ改称 + portal_nav / CLAUDE 改修" "$LABEL_BASE" \
"02_basic-design→02_basic_design 改称、portal_nav の入れ子化、目標骨格作成。" \
"完了(c6ef921, 0a5e69f)。CLAUDE.md は P8 で新構成へ全面改訂。Refs エピック #$EPIC"

mk_closed "[設計再構成][要件] 要件を個別IDファイルへ分割・フラット再採番" "$LABEL_BASE,migration" \
"FR/BR/NFR を個別 ID ファイルへ分割、RULE 抽出、01_specifications/index 生成。" \
"完了(a412652)。BR-001..146 / FR-001..194 / NFR-001..079 / RULE-001..020。Refs #$EPIC"

mk_closed "[設計再構成][業務UC] 操作粒度の業務ユースケース確立" "$LABEL_BASE" \
"UC-001..247 を 15 項目テンプレで導出(画面起点/システム起点)。" \
"完了(ccf0ede)。Refs #$EPIC"

mk_closed "[設計再構成][画面] 画面フラット採番・画面イベントEVT個別化" "$LABEL_BASE" \
"SCR-001..030、EVT-001..229 個別化、EVT↔UC 1:1。" \
"完了(f47c2be)。Refs #$EPIC"

mk_closed "[設計再構成][API] エンドポイント別分割・フラット採番" "$LABEL_BASE" \
"API-001..059(1 エンドポイント 1 ファイル)、逆引き結線。" \
"完了(9b52982)。Refs #$EPIC"

mk_closed "[設計再構成][DB] テーブルのフラット採番・逆引き整備" "$LABEL_BASE" \
"TBL-001..031、項目セクション(PK/論理削除/監査/逆引き UC・API)。" \
"完了(87266fb)。Refs #$EPIC"

mk_closed "[設計再構成][権限/エラー/メッセージ/SEQ] 個別ID化" "$LABEL_BASE" \
"PERM-001..011 / ERR-001..035 / MSG-001..013 / SEQ-001..107。" \
"完了(5bd4045)。Refs #$EPIC"

mk_closed "[設計再構成][トレーサビリティ] 一気通貫マトリクス確立・ギャップ検出" "$LABEL_BASE,traceability" \
"要件→UC→SCR→EVT→API→TBL のマトリクス(247 行)とギャップ検出。" \
"完了(9fa0cf2)。検出ギャップは後続(第1〜3段・構造点検)で解消。Refs #$EPIC"

mk_closed "[設計再構成][統合] CLAUDE.md 改訂・両設計書に再構成結果サマリ" "$LABEL_BASE" \
"CLAUDE.md 全面改訂、99_restructure_result.md(両書)。" \
"完了(0a5e69f)。Refs #$EPIC"

echo "== 被覆ギャップ(解決済み=Close) =="
mk_closed "[設計再構成][traceability] 要件無し UC(128件)のトレース欠落" "$LABEL_BASE,design-gap,traceability" \
"画面イベント由来 UC-* の 対応要件ID が — のもの 128 件。" \
"解決(188f66a・第1段)。同一画面の兄弟 UC から候補要件を機械再連結し UC→要件 128→0(要レビュー)。Refs #$EPIC"

mk_closed "[設計再構成][traceability] FR→UC 被覆ギャップ(132件)" "$LABEL_BASE,design-gap,traceability" \
"194 FR 中 132 がどの UC からも逆引きされない。" \
"解決(6bfe7fc/755a841・第2段)。45 件を機械連結、30 件は横断受容、57 件は UC-248..304 を新設。FR→UC 残 0(要レビュー)。Refs #$EPIC"

mk_closed "[設計再構成][traceability] BR/RULE の UC 参照付与" "$LABEL_BASE,design-gap,traceability" \
"RULE 20・孤立 BR の UC 参照欠落。" \
"解決(73f624d・第3段)。RULE 17 を適用UC双方向、孤立 BR 5 を UC へ連結(BR-009 受容)。BR は原則 BR→FR→UC で間接トレース成立。Refs #$EPIC"

mk_closed "[設計再構成][design-gap] API/TBL 構造ギャップ(逆引き欠落)" "$LABEL_BASE,design-gap,traceability" \
"API→UC 2 / API→EVT 6 / TBL→UC 6 / TBL→API 10。" \
"解決(3a11d5f)。API-031/032→UC-304、ジャンクション3表は親表UC継承、横断3表・Control Plane系は受容分類。bare — を全系列ゼロ化。Refs #$EPIC"

echo "== 要レビュー / 後続(Open) =="
mk "[設計再構成][needs-review] 機械支援連結・新設UCの妥当性レビュー" "$LABEL_BASE,needs-review,traceability" \
"第1〜3段の機械連結値、および新設 UC-248..304 の 主アクター/基本フロー/事後条件は機械支援生成(各備考に「要レビュー」明記)。設計レビューで妥当性を確認し、必要なら既存 UC へ吸収・修正する。
## 完了条件
- 新設 UC の内容(フロー/アクター)をレビュー・確定。
- 機械連結した 対応要件ID / 対応業務UC の妥当性を確認。
Refs #$EPIC" >/dev/null

mk "[設計再構成][needs-review] NFR 採番の最終確定(79 vs 74)" "$LABEL_BASE,needs-review" \
"NFR は個別ファイル 79 件。P0 クロスウォーク想定(74)と差異(範囲行展開による)。整合確認と crosswalk 更新。
## 完了条件: NFR 採番を確定し crosswalk と一致。 Refs #$EPIC" >/dev/null

mk "[設計再構成][migration] 要件文の実装寄り記述の棚卸し" "$LABEL_BASE,migration" \
"要件文に内在する具体値・技法の基本設計移管要否を精査。
## 完了条件: 移管/存置を判断し反映。 Refs #$EPIC" >/dev/null

mk "[設計再構成][cleanup] EVT 命名正規化・処理セルの二重管理整理" "$LABEL_BASE,cleanup" \
"EVT 名は SCR §6 の流用で主語省略あり。EVT ## 処理 は SCR §6 の複製(正本=§6)で二重管理。命名統一と正本一元化方針を確定。
## 完了条件: 命名規約適用、処理の正本一元化方針を反映。 Refs #$EPIC" >/dev/null

mk "[設計再構成][needs-review] ERR 未採番の認可エラー・命名統一" "$LABEL_BASE,needs-review" \
"認可判定(PERM-002)参照の E-AUTH*/E-AUTHZ* は ERR 未採番。契約停止エラーは E-BIZ/E-BILL 混在。API ## エラー 表へ追記し ERR 採番・命名統一(E-BILL-* へ)。
## 完了条件: 該当コードを ERR 採番、命名統一。 Refs #$EPIC" >/dev/null

mk "[設計再構成][needs-review] PERM の UC 逆引き結線" "$LABEL_BASE,needs-review,traceability" \
"PERM-NNN の 対応業務UC が未結線(SCR/EVT/API は結線済)。UC↔権限の逆引きを付与。
## 完了条件: PERM↔UC を結線。 Refs #$EPIC" >/dev/null

mk "[設計再構成][cleanup] 体裁統一(API リード文体・MSG 節番号・TBL セクションアンカー・provenance 注記)" "$LABEL_BASE,cleanup" \
"API 要約の文体混在、MSG index の旧節番号、TBL ページのセクションアンカー不統一、UC 備考の旧ID provenance 注記。新構成へ統一・整理。
## 完了条件: 体裁を新構成基準へ統一。 Refs #$EPIC" >/dev/null

echo "== 完了。エピック #$EPIC 配下に起票/Close しました。 =="
