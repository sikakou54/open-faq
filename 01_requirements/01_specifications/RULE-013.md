<!-- portal-top -->
[設計ポータル](../../README.md) ／ [要件定義](../index.md) ／ [要件仕様](index.md) ／ **RULE-013: 質問数上限の停止・追加通知**
<!-- /portal-top -->

# <span id="RULE-013"></span>RULE-013: 質問数上限の停止・追加通知

> **この業務ルールは「質問数上限の停止・追加通知」の定量しきい値・ポリシーを定義します。**

*種別 業務ルール ・ ステータス ドラフト*

## <span id="ルール"></span>ルール

質問数が設定上限の 100% 到達でウィジェット新規質問受付を停止し、125% で追加アラート通知を行う。

## <span id="由来"></span>由来

| 由来要件 |
|----|
| [FR-089](FR-089.md#FR-089), [FR-094](FR-094.md#FR-094) |

## <span id="適用"></span>適用UC

本ルールは由来要件(FR)を実現する次の業務ユースケースに適用される。

| 適用UC | 名称 |
|----|----|
| [UC-199](../02_business_usecases/UC-199.md#UC-199) | 初期表示 |
| [UC-204](../02_business_usecases/UC-204.md#UC-204) | 「今月の利用上限」を入力 |
| [UC-206](../02_business_usecases/UC-206.md#UC-206) | 「保存」を押下 |
| [UC-208](../02_business_usecases/UC-208.md#UC-208) | 初期表示 |
| [UC-237](../02_business_usecases/UC-237.md#UC-237) | 質問数上限アラート通知 |
| [UC-240](../02_business_usecases/UC-240.md#UC-240) | 上限到達ウィジェット受付停止 |

---

<!-- portal-bottom -->
[← 要件仕様](index.md) ・ [要件定義](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
