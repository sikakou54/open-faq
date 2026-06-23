# FAQ AI ウィジェット SaaS / メインシステム 設計ポータル

本リポジトリは「FAQ AI ウィジェット SaaS / メインシステム」の **要件定義書**・**基本設計書** を **Markdown** で管理する。Markdown を正本とする。

- 図は ` ```mermaid ` で保持。相互参照は `<span id="…">` アンカーで結線する。
- 読み順: 要件定義 ＞ 業務ユースケース ＞ 画面設計 ＞ システム設計 ＞ API設計 ＞ DB設計 ＞ シーケンス ＞ 権限 / エラー / メッセージ。

## ドキュメント

各セクションの一覧・詳細は、それぞれの `index.md` を起点に辿る。

| セクション | 入口 | 内容 |
|----|----|----|
| 要件定義 | [01_requirements/index.md](01_requirements/index.md) | 業務要件 BR / 機能要件 FR / 非機能要件 NFR / 業務ルール RULE / 業務ユースケース UC |
| 基本設計 | [02_basic_design/index.md](02_basic_design/index.md) | 画面 SCR / システム SYS / API / テーブル TBL / シーケンス SEQ / 権限 PERM / エラー ERR / メッセージ MSG / 課金 |
| 将来対応 | [03_future/index.md](03_future/index.md) | MVP 後バックログ FUT |

## 運用・テンプレート

- 保守・編集のルール(正本): [CLAUDE.md](CLAUDE.md)
- 各層の作成テンプレート(雛形): [templates/README.md](templates/README.md)
