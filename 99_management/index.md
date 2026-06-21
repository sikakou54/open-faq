# 99_management(再構成プロジェクト 作業用・最終削除対象)

要件定義書・基本設計書 再構成プロジェクトの一時管理ディレクトリ。**最終成果物ではない。** 作業完了時に内容を正式設計書 / GitHub Issues へ移管し、本ディレクトリは削除する。

## 再開起点
全タスクは GitHub Issues に登録済み(エピック #3)。下表の Issue を上から順に消化する。

| フェーズ | Issue | 状態 |
|---|---|---|
| P0 骨格・クロスウォーク | (本作業・完了) | done |
| 基盤 ディレクトリ改称+portal_nav/CLAUDE | #4 | DONE(c6ef921・P8でCLAUDE全面改訂) |
| P1 要件定義 個別ID分割・再採番・RULE抽出 | #5 | DONE(0/0) |
| P2 業務ユースケース UC-001 導出 | #6 | DONE(0/0) |
| P3 画面設計 移設・SCR採番・EVT個別化 | #7 | DONE(0/0) |
| P4 API設計 エンドポイント別分割 | #8 | DONE(0/0) |
| P5 DB設計 移設・TBL採番 | #9 | DONE(0/0) |
| P6 権限/エラー/メッセージ+SEQ | #10 | DONE(0/0) |
| P7 トレーサビリティ・ギャップ検出 | #11 | DONE(0/0) |
| P8 統括統合・検証・99_management削除・全Close | #12 | 文書整備DONE(0/0・CLAUDE改訂・両99_restructure_result作成)。Issue Close と本DIR削除はオーナー確認待ち |

エピック: #3 / 検出課題・差し戻しは随時 `[設計再構成][区分]` で個別 Issue 化。

## 正本
- ID リナンバ: `01_crosswalk.md` / `crosswalk.json`(旧→新 534 件)
- 業務 UC リナンバ: `uc_crosswalk.json`(旧 UC-SCR-*-EV* / UC-SYSTEM-* → 新 UC-001..247・P2 成果)
- トレーサビリティ: `02_traceability_matrix.md`(P7 で生成)

## ファイル
- `01_crosswalk.md` / `crosswalk.json` … 旧→新 ID 対応
- `uc_crosswalk.json` … 旧業務 UC → 新 UC-NNN 対応(P2)
- `02_traceability_matrix.md` … 要件→UC→SCR→EVT→API→TBL(P7・UC 単位 247 行)
- `p7_linkgraph.json` … P7 リンクグラフ(UC/EVT/API/TBL 構造化リンク + 要件→UC 逆引き。機械可読)
- `p7_gaps.json` … P7 ギャップ一覧(分類別。機械可読)
- `06_remaining_issues.md` … 各フェーズ検出課題(GitHub MCP 復旧後に Issue 化)
- `07_coverage_gap_report.md` … 要件↔UC 被覆ギャップ精査レポート(P7 後続)。§7 第1段: UC→要件 128→0。§8 第2段: FR→UC 62→164・受容30・UC新設57(UC-248〜304)。**FR↔UC ギャップ解消(残0/0)**
- `p8_fr_uc_proposal.json` / `p8_new_uc_map.json` / `p8_uc_rules.json` … 第2段 FR→UC 候補・新設UCマップ / 第3段 UC→RULE マップ(機械可読)
- `05_agent_work_summary.md` … 各 Agent 作業サマリ(随時)
