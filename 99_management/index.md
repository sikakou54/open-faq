# 99_management(再構成プロジェクト 作業用・最終削除対象)

要件定義書・基本設計書 再構成プロジェクトの一時管理ディレクトリ。**最終成果物ではない。** 作業完了時に内容を正式設計書 / GitHub Issues へ移管し、本ディレクトリは削除する。

## 再開起点
全タスクは GitHub Issues に登録済み(エピック #3)。下表の Issue を上から順に消化する。

| フェーズ | Issue | 状態 |
|---|---|---|
| P0 骨格・クロスウォーク | (本作業・完了) | done |
| 基盤 ディレクトリ改称+portal_nav/CLAUDE | #4 | open |
| P1 要件定義 個別ID分割・再採番・RULE抽出 | #5 | DONE(0/0) |
| P2 業務ユースケース UC-001 導出 | #6 | DONE(0/0) |
| P3 画面設計 移設・SCR採番・EVT個別化 | #7 | DONE(0/0) |
| P4 API設計 エンドポイント別分割 | #8 | DONE(0/0) |
| P5 DB設計 移設・TBL採番 | #9 | DONE(0/0) |
| P6 権限/エラー/メッセージ+SEQ | #10 | open |
| P7 トレーサビリティ・ギャップ検出 | #11 | open |
| P8 統括統合・検証・99_management削除・全Close | #12 | open |

エピック: #3 / 検出課題・差し戻しは随時 `[設計再構成][区分]` で個別 Issue 化。

## 正本
- ID リナンバ: `01_crosswalk.md` / `crosswalk.json`(旧→新 534 件)
- 業務 UC リナンバ: `uc_crosswalk.json`(旧 UC-SCR-*-EV* / UC-SYSTEM-* → 新 UC-001..247・P2 成果)
- トレーサビリティ: `02_traceability_matrix.md`(P7 で生成)

## ファイル
- `01_crosswalk.md` / `crosswalk.json` … 旧→新 ID 対応
- `uc_crosswalk.json` … 旧業務 UC → 新 UC-NNN 対応(P2)
- `02_traceability_matrix.md` … 要件→UC→SCR→EVT→API→TBL(P7)
- `05_agent_work_summary.md` … 各 Agent 作業サマリ(随時)
