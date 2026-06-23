# 将来対応(FUT)テンプレート

> **本テンプレートは将来対応(FUT)の記載骨格を定義します。**

運用ルールの正本は [../CLAUDE.md](../CLAUDE.md)。共通記載スタイルは [共通記載スタイル](00_common-style.md) を参照する。

- **配置先**: `03_future/`(`index.md` + `FUT-01.md`〜)。`FUT-06` は `FUT-06.md`(概要)+ `FUT-06-req.md`(要件)+ `FUT-06-detail.md`(詳細設計)の親子構成。
- **採番**: `FUT-01`〜(ハイフン + 2 桁連番。MVP 後バックログ・カテゴリ別。3 桁フラット連番の例外)。ID は H1 に `# <span id="FUT-0N"></span>FUT-0N: 名称` で保持し、親子は `FUT-06` / `FUT-06-req` / `FUT-06-detail` の各アンカーを持つ。

## 骨格

- MVP 後の候補・バックログ。FUT カテゴリ別。要件定義テンプレートに準じる。
- 要件定義テンプレート(共通骨格)は [共通記載スタイル](00_common-style.md) と要件仕様テンプレート([業務要件](01_business-requirement.md) / [機能要件](02_functional-requirement.md) / [非機能要件](03_non-functional-requirement.md))を参照する。

## 記載例(ファイル骨格)

```markdown
# <span id="FUT-01"></span>FUT-01: 名称

> **本項目は MVP 後の「…」候補を定義します。**

*種別 将来対応 ・ ステータス バックログ*

## 概要

…

## 内容

…(要件定義テンプレートに準じる)
```
