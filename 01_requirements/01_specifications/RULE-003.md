<!-- portal-top -->
[設計ポータル](../../README.md) ／ [要件定義](../index.md) ／ [要件仕様](index.md) ／ **RULE-003: パスワードポリシー**
<!-- /portal-top -->

# <span id="RULE-003"></span>RULE-003: パスワードポリシー

> **この業務ルールは「パスワードポリシー」の定量しきい値・ポリシーを定義します。**

*種別 業務ルール ・ ステータス ドラフト*

## <span id="ルール"></span>ルール

パスワードは最低 12 文字、英大文字・小文字・数字・記号のうち 3 種類以上。パスワードリセットリンクの有効期限は 1 時間。

## <span id="由来"></span>由来

| 由来要件 |
|----|
| [FR-006](FR-006.md#FR-006) |

## <span id="適用"></span>適用UC

本ルールは由来要件(FR)を実現する次の業務ユースケースに適用される。

| 適用UC | 名称 |
|----|----|
| [UC-009](../02_business_usecases/UC-009.md#UC-009) | パスワードを入力 |
| [UC-010](../02_business_usecases/UC-010.md#UC-010) | パスワード(確認)を入力 |
| [UC-024](../02_business_usecases/UC-024.md#UC-024) | 新パスワードを入力 |
| [UC-025](../02_business_usecases/UC-025.md#UC-025) | 「新しいパスワードを設定する」を押下 |
| [UC-178](../02_business_usecases/UC-178.md#UC-178) | 「パスワードを変更する」を押下 |
| [UC-183](../02_business_usecases/UC-183.md#UC-183) | 初回パスワードを入力 |
| [UC-184](../02_business_usecases/UC-184.md#UC-184) | パスワード(確認)を入力 |

---

<!-- portal-bottom -->
[← 要件仕様](index.md) ・ [要件定義](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
