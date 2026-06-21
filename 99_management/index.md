# 99_management(再構成プロジェクト 作業用・最終削除対象)

要件定義書・基本設計書 再構成プロジェクトの一時管理ディレクトリ。**最終成果物ではない。** 作業完了時に内容を正式設計書 / GitHub Issues へ移管し、本ディレクトリは削除する。

## 進捗(レジューム用)
- [x] P0 骨格・クロスウォーク確定(`01_crosswalk.md` / `crosswalk.json`、旧→新 ID 534 件)
- [ ] P1 要件定義 個別 ID 分割・フラット再採番・RULE 抽出
- [ ] P2 業務ユースケース UC-001 導出(要件定義書内)
- [ ] P3 画面設計 移設・SCR 採番・EVT 個別化
- [ ] P4 API 設計 エンドポイント別分割・API 採番
- [ ] P5 DB 設計 移設・TBL 採番・監査項目
- [ ] P6 権限/エラー/メッセージ + シーケンス 抽出生成
- [ ] P7 トレーサビリティマトリクス・ギャップ検出
- [ ] P8 統括統合 portal_nav/CLAUDE/検証/99_management 削除/全 Issue Close

## 正本
- 計画: リポジトリ外プラン(承認済)。本ディレクトリ `01_crosswalk.md` が ID リナンバの正本。
- 全タスクは GitHub Issues(ラベル `design-restructure`)に登録済み。各 Issue がフェーズ・課題の単位。

## ファイル
- `01_crosswalk.md` / `crosswalk.json` … 旧→新 ID 対応
- `02_traceability_matrix.md` … 要件→UC→SCR→EVT→API→TBL(P7 で生成)
- `05_agent_work_summary.md` … 各 Agent 作業サマリ(随時)
