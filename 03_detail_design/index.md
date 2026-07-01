# 詳細設計

> **本セクションは基本設計(SCR/SYS/API/TBL/SEQ/PERM/ERR/MSG)を、実装者が迷わず実装できる粒度へ具体化した詳細設計書を管理する。**

処理条件・分岐条件・状態変化・入出力・例外処理・成否条件を明記し、後続のテスト設計が読み取れる状態を保つ。基本設計に無い仕様は推測で足さず、不明点は課題として分離する。運用ルールは [CLAUDE.md](../CLAUDE.md)、記載スタイルは [templates/](../templates/README.md) を正本とする。

## 技術前提

実装スタックは **TypeScript + Next.js(App Router) + Repository層**、プラットフォームは **Cloudflare**(Workers/Pages + D1(SQLite/FTS5) + Queues + Cron Triggers)。設計値の正本は [システム仕様書](../02_basic_design/07_system-spec.md)、状態の正本は [状態モデル](../02_basic_design/08_state-model.md)、用語の正本は [用語集](../01_requirements/00_glossary.md)。層横断トレーサビリティは [トレーサビリティ一覧](../02_basic_design/00_traceability/index.md) に一元管理し、本セクションの各設計書には `TR-NNN` を記載しない。

## 構成

| 系列 | 種別 | 配置 | 採番単位 |
|----|----|----|----|
| STS | 状態遷移図 | `01_state_transitions/` | STATEFULエンティティ1件=1図 |
| STR | 画面遷移図 | `02_screen_flows/` | ロール/業務領域単位 |
| IO | 入出力設計書 | `03_io_specs/` | 画面/API単位 |
| IPO | IPO処理機能記述書 | `04_ipo/` | 主要ビジネスロジック単位 |
| BAT | バッチ処理設計書 | `05_batch/` | SYS(batch/async/monitor)単位 |
| EIF | 外部インターフェース設計図 | `06_external_if/` | 連携先サービス単位 |
| DBP | データベース物理設計書 | `07_db_physical/` | テーブル/ドメイン単位 |
| DSQ | 詳細シーケンス図 | `08_sequences/` | 複雑/高リスクフロー単位 |
| ACT | アクティビティ図 | `09_activities/` | 業務フロー単位 |
| CLS | クラス図 | `10_class/` | 機能/レイヤー単位 |
| MOD | モジュール構造図 | `11_module/` | モジュール単位 |

各系列は基本設計を入力に作成され、確定後に本一覧へ各サブフォルダ `index.md` へのリンクを追記する。
