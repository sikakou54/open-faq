<!-- portal-top -->
[設計ポータル](../../README.md) ／ [要件定義](../index.md) ／ [要件仕様](index.md) ／ **RULE-010: FAQ 件数上限**
<!-- /portal-top -->

# <span id="RULE-010"></span>RULE-010: FAQ 件数上限

> **この業務ルールは「FAQ 件数上限」の定量しきい値・ポリシーを定義します。**

*種別 業務ルール ・ ステータス ドラフト*

## <span id="ルール"></span>ルール

1 契約あたり FAQ 件数は警告 8,000 件 / 強制拒否 12,000 件(運用想定上限 10,000 件)。

## <span id="由来"></span>由来

| 由来要件 |
|----|
| [FR-054](FR-054.md#FR-054) |

## <span id="適用"></span>適用UC

本ルールは由来要件(FR)を実現する次の業務ユースケースに適用される。

| 適用UC | 名称 |
|----|----|
| [UC-059](../02_business_usecases/UC-059.md#UC-059) | 登録先 FAQ リンクを押下 |
| [UC-060](../02_business_usecases/UC-060.md#UC-060) | 候補 FAQ リンクを押下 |
| [UC-061](../02_business_usecases/UC-061.md#UC-061) | 「FAQ 登録へ」を押下 |

---

<!-- portal-bottom -->
[← 要件仕様](index.md) ・ [要件定義](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
