# 詳細設計

> **本セクションは基本設計(SCR/SYS/API/TBL/SEQ/PERM/ERR/MSG)を、実装者が迷わず実装できる粒度へ具体化した詳細設計書を管理する。**

処理条件・分岐条件・状態変化・入出力・例外処理・成否条件を明記し、後続のテスト設計が読み取れる状態を保つ。基本設計に無い仕様は推測で足さず、不明点は課題として分離する。運用ルールは [CLAUDE.md](../CLAUDE.md)、記載スタイルは [templates/](../templates/README.md) を正本とする。

## 技術前提

実装スタックは **TypeScript + Next.js(App Router) + Repository層**、プラットフォームは **Cloudflare**(Workers/Pages + D1(SQLite/FTS5) + Queues + Cron Triggers)。設計値の正本は [システム仕様書](../02_basic_design/07_system-spec.md)、状態の正本は [状態モデル](../02_basic_design/08_state-model.md)、用語の正本は [用語集](../01_requirements/00_glossary.md)。層横断トレーサビリティは [トレーサビリティ一覧](../02_basic_design/00_traceability/index.md) に一元管理し、本セクションの各設計書には `TR-NNN` を記載しない(各ヘッダーは業務ユースケース `UC-NNN` と設計上必要な関連ID のみを持つ)。

## 構成

| 系列 | 種別 | 一覧 | 件数 | 採番単位 |
|----|----|----|----|----|
| STS | 状態遷移図 | [`01_state_transitions/`](01_state_transitions/index.md) | 10 | STATEFULエンティティ1件=1図 |
| STR | 画面遷移図 | [`02_screen_flows/`](02_screen_flows/index.md) | 8 | ロール/業務領域単位 |
| IO | 入出力設計書 | [`03_io_specs/`](03_io_specs/index.md) | 35 | 画面/API単位 |
| IPO | IPO処理機能記述書 | [`04_ipo/`](04_ipo/index.md) | 16 | 主要ビジネスロジック単位 |
| BAT | バッチ処理設計書 | [`05_batch/`](05_batch/index.md) | 13 | SYS(batch/async/monitor)単位 |
| EIF | 外部インターフェース設計図 | [`06_external_if/`](06_external_if/index.md) | 3 | 連携先サービス単位 |
| DBP | データベース物理設計書 | [`07_db_physical/`](07_db_physical/index.md) | 13 | テーブル/ドメイン単位 |
| DSQ | 詳細シーケンス図 | [`08_sequences/`](08_sequences/index.md) | 6 | 複雑/高リスクフロー単位 |
| ACT | アクティビティ図 | [`09_activities/`](09_activities/index.md) | 5 | E2E業務フロー単位 |
| CLS | クラス図 | [`10_class/`](10_class/index.md) | 12 | 機能/レイヤー単位 |
| MOD | モジュール構造図 | [`11_module/`](11_module/index.md) | 11 | モジュール単位 |

## 整備方針

「ウィジェット質問 → AI 回答可否判定 → 回答/未解決登録」の縦スライスで 9 系列のパイロット(STS-001 / IO-001 / IPO-001 / BAT-001 / EIF-001 / DBP-001 / DSQ-001 / CLS-001 / MOD-001)を先行整備して詳細設計の型を確立し、全系列へ展開した。各設計書は基本設計を入力に作成し、IPO(判定ロジック)と BAT(実行機構)、CLS(クラス構造)と MOD(モジュール分割)のように対をなす系列は相互リンクで責務を分離する。不明点・基本設計の不足は本文に混ぜず課題として分離する。
