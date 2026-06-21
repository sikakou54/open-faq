<!-- portal-top -->
[設計ポータル](../../README.md) ／ [要件定義](../index.md) ／ [要件仕様](index.md) ／ **RULE-004: 無操作タイムアウト**
<!-- /portal-top -->

# <span id="RULE-004"></span>RULE-004: 無操作タイムアウト

> **この業務ルールは「無操作タイムアウト」の定量しきい値・ポリシーを定義します。**

*種別 業務ルール ・ ステータス ドラフト*

## <span id="ルール"></span>ルール

無操作が 30 分続いた時にセッションを失効させる。

## <span id="由来"></span>由来

| 由来要件 |
|----|
| [FR-008](FR-008.md#FR-008) |

## <span id="適用"></span>適用UC

本ルールは由来要件(FR)を実現する次の業務ユースケースに適用される。

| 適用UC | 名称 |
|----|----|
| [UC-242](../02_business_usecases/UC-242.md#UC-242) | セッション失効・再認証 |
| [UC-244](../02_business_usecases/UC-244.md#UC-244) | 契約停止時セッション一斉無効化 |

---

<!-- portal-bottom -->
[← 要件仕様](index.md) ・ [要件定義](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
