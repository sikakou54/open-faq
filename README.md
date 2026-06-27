# FAQ AI ウィジェット SaaS / メインシステム 設計ポータル

本リポジトリは「FAQ AI ウィジェット SaaS / メインシステム」の **要件定義書**・**基本設計書** を **Markdown** で管理する。Markdown を正本とする。

- 図は ` ```mermaid ` で保持。相互参照は `<span id="…">` アンカーで結線する。
- 読み順: 要件定義 ＞ 業務ユースケース ＞ 画面設計 ＞ システム設計 ＞ API設計 ＞ DB設計 ＞ シーケンス ＞ 権限 / エラー / メッセージ。
- 全設計のトレーサビリティ(業務UC × 画面 × API × データベース ほか)は [トレーサビリティ一覧](02_basic_design/00_traceability/index.md) に一元化する。各ドキュメントはトレーサビリティID(`TR-NNN`)で本表を参照する。

## ドキュメント

各セクションの一覧・詳細は、それぞれの `index.md` を起点に辿る。

| セクション | 入口 | 内容 |
|----|----|----|
| 要件定義 | [01_requirements/index.md](01_requirements/index.md) | 業務要件 BR / 機能要件 FR / 非機能要件 NFR / 業務ルール RULE / 業務ユースケース UC |
| 基本設計 | [02_basic_design/index.md](02_basic_design/index.md) | 画面 SCR / システム SYS / API / テーブル TBL / シーケンス SEQ / 権限 PERM / エラー ERR / メッセージ MSG / 課金 |
| トレーサビリティ | [02_basic_design/00_traceability/index.md](02_basic_design/00_traceability/index.md) | 業務UC × 画面 × システム × API × データベース × 要件 × シーケンス の対応一覧(TR-ID で一元管理) |
| 横断正本 | [用語集](01_requirements/00_glossary.md) / [システム仕様書](02_basic_design/07_system-spec.md) / [状態モデル](02_basic_design/08_state-model.md) | 用語(GLO)・設計値(しきい値/単価/保持期間)・状態(一覧+遷移図)の単一正本 |
| 将来対応 | [03_future/index.md](03_future/index.md) | MVP 後バックログ FUT |

## 運用・テンプレート

- 保守・編集のルール(正本): [CLAUDE.md](CLAUDE.md)
- 各層の作成テンプレート(雛形): [templates/README.md](templates/README.md)
