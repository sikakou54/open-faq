<!-- portal-top -->
[設計ポータル](../../README.md) ／ [要件定義](../index.md) ／ [要件仕様](index.md) ／ **RULE-002: 再認証の有効範囲**
<!-- /portal-top -->

# <span id="RULE-002"></span>RULE-002: 再認証の有効範囲

> **この業務ルールは「再認証の有効範囲」の定量しきい値・ポリシーを定義します。**

*種別 業務ルール ・ ステータス ドラフト*

## <span id="ルール"></span>ルール

重要操作の再認証は、当該操作 1 回かつ 15 分以内を有効範囲とする。

## <span id="由来"></span>由来

| 由来要件 |
|----|
| [FR-005](FR-005.md#FR-005) |

## <span id="適用"></span>適用UC

本ルールは由来要件(FR)を実現する次の業務ユースケースに適用される。

| 適用UC | 名称 |
|----|----|
| [UC-176](../02_business_usecases/UC-176.md#UC-176) | メールアドレスを入力 |
| [UC-177](../02_business_usecases/UC-177.md#UC-177) | 「保存する」を押下(プロフィール) |
| [UC-178](../02_business_usecases/UC-178.md#UC-178) | 「パスワードを変更する」を押下 |
| [UC-206](../02_business_usecases/UC-206.md#UC-206) | 「保存」を押下 |
| [UC-242](../02_business_usecases/UC-242.md#UC-242) | セッション失効・再認証 |

---

<!-- portal-bottom -->
[← 要件仕様](index.md) ・ [要件定義](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
