# 詳細設計

> **本セクションは基本設計(SCR/SYS/API/TBL/SEQ/PERM/ERR/MSG)を、実装者が迷わず実装できる粒度へ具体化した詳細設計書を管理する。**

処理条件・分岐条件・状態変化・入出力・例外処理・成否条件を明記し、後続のテスト設計が読み取れる状態を保つ。基本設計に無い仕様は推測で足さず、不明点は課題として分離する。運用ルールは [CLAUDE.md](../CLAUDE.md)、記載スタイルは [templates/](../templates/README.md) を正本とする。

## 技術前提

実装スタックは **TypeScript + Next.js(App Router) + Repository層**、プラットフォームは **Cloudflare**(Workers/Pages + D1(SQLite/FTS5) + Queues + Cron Triggers)。設計値の正本は [システム仕様書](../02_basic_design/07_system-spec.md)、状態の正本は [状態モデル](../02_basic_design/08_state-model.md)、用語の正本は [用語集](../01_requirements/00_glossary.md)。層横断トレーサビリティは [トレーサビリティ一覧](../02_basic_design/00_traceability/index.md) に一元管理し、本セクションの各設計書には `TR-NNN` を記載しない。

## 構成

| 系列 | 種別 | 配置 | 採番単位 |
|----|----|----|----|
| STS | 状態遷移図 | [`01_state_transitions/`](01_state_transitions/index.md) | STATEFULエンティティ1件=1図 |
| STR | 画面遷移図 | `02_screen_flows/`(未着手) | ロール/業務領域単位 |
| IO | 入出力設計書 | [`03_io_specs/`](03_io_specs/index.md) | 画面/API単位 |
| IPO | IPO処理機能記述書 | [`04_ipo/`](04_ipo/index.md) | 主要ビジネスロジック単位 |
| BAT | バッチ処理設計書 | [`05_batch/`](05_batch/index.md) | SYS(batch/async/monitor)単位 |
| EIF | 外部インターフェース設計図 | [`06_external_if/`](06_external_if/index.md) | 連携先サービス単位 |
| DBP | データベース物理設計書 | [`07_db_physical/`](07_db_physical/index.md) | テーブル/ドメイン単位 |
| DSQ | 詳細シーケンス図 | [`08_sequences/`](08_sequences/index.md) | 複雑/高リスクフロー単位 |
| ACT | アクティビティ図 | `09_activities/`(未着手) | 業務フロー単位 |
| CLS | クラス図 | [`10_class/`](10_class/index.md) | 機能/レイヤー単位 |
| MOD | モジュール構造図 | [`11_module/`](11_module/index.md) | モジュール単位 |

各系列は基本設計を入力に作成され、確定後に本一覧へ各サブフォルダ `index.md` へのリンクを追記する。

## パイロット成果物

「ウィジェット質問 → AI 回答可否判定 → 回答/未解決登録」の縦スライスで、9 系列の詳細設計を実装可能粒度で作成した(詳細設計の型を検証する先行整備)。

| ID | 種別 | 文書 |
|----|----|----|
| STS-001 | 状態遷移 | [未解決質問 状態遷移](01_state_transitions/STS-001.md#STS-001) |
| IO-001 | 入出力 | [ウィジェット質問送信 入出力](03_io_specs/IO-001.md#IO-001) |
| IPO-001 | IPO | [AI 回答可否判定](04_ipo/IPO-001.md#IPO-001) |
| BAT-001 | バッチ | [利用量リアルタイム集計](05_batch/BAT-001.md#BAT-001) |
| EIF-001 | 外部IF | [AI 推論 LLM 連携](06_external_if/EIF-001.md#EIF-001) |
| DBP-001 | DB物理 | [H_QUESTION_LOGS 物理設計](07_db_physical/DBP-001.md#DBP-001) |
| DSQ-001 | 詳細シーケンス | [ウィジェット質問→AI回答→未解決登録](08_sequences/DSQ-001.md#DSQ-001) |
| CLS-001 | クラス | [ウィジェット回答機能 クラス図](10_class/CLS-001.md#CLS-001) |
| MOD-001 | モジュール | [ウィジェット/AI回答 モジュール構造](11_module/MOD-001.md#MOD-001) |
