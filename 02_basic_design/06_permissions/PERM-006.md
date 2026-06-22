<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [権限設計](index.md) ／ **PERM-006: 重要操作の再認証**
<!-- /portal-top -->

# <span id="PERM-006"></span>PERM-006: 重要操作の再認証

> **このページは不可逆・高リスクな操作の直前に求める再認証(当該操作 1 回 + 15 分以内)と、対象 5 操作を定義します。**

*種別 権限定義 ・ ステータス ドラフト ・ 再構成 P6b*

## <span id="perm"></span>1. ロール別操作可否

ログイン済みでも、重要操作の直前に改めて本人確認(再認証)を求めます。再認証は「当該操作 1 回かつ 15 分以内」でのみ有効で、未充足のまま対象 API に到達した場合は `E-AUTH-REAUTH-REQUIRED` に落とします。

| 操作 | オーナー | メンバー(割当あり) | メンバー(割当なし) | 未認証 | ウィジェット利用者 |
|----|----|----|----|----|----|
| パスワード変更 | 再認証必須 | 再認証必須 | — | — | — |
| 退会 | 再認証必須 | — | — | — | — |
| 課金情報変更 | 再認証必須 | — | — | — | — |
| メンバーの登録・停止・削除 | 再認証必須 | 再認証必須 | — | — | — |
| 月次上限件数の変更 | 再認証必須 | 再認証必須 | — | — | — |

> [!IMPORTANT]
> **対象範囲は要件で固定** 再認証の対象は上記 5 種に固定します(FR-005 / BR-002)。再認証はセッションの寿命判定(無操作 30 分 / 絶対 12 時間)とは別軸で働きます。

## <span id="trace"></span>2. 対応 UC / SCR / EVT / API

本権限が適用される画面・イベント・API・業務ユースケースの結線です。

| 観点 | 結線 |
|----|----|
| 対応業務UC | [UC-009](../../01_requirements/04_business_usecases/UC-009.md#UC-009) [UC-010](../../01_requirements/04_business_usecases/UC-010.md#UC-010) [UC-035](../../01_requirements/04_business_usecases/UC-035.md#UC-035) [UC-072](../../01_requirements/04_business_usecases/UC-072.md#UC-072) |
| 対応画面SCR | [SCR-019](../01_screens/SCR-019.md#SCR-019) |
| 対応EVT | — |
| 対応API | [API-005](../03_apis/API-005.md#API-005) [API-012](../03_apis/API-012.md#API-012) [API-013](../03_apis/API-013.md#API-013) [API-045](../03_apis/API-045.md#API-045) [API-056](../03_apis/API-056.md#API-056) |

## <span id="src"></span>3. 由来要件

| 由来要件 |
|----|
| [FR-005](../../01_requirements/02_FunctionalRequirement/01_account-fr.md#FR-005) [BR-002](../../01_requirements/01_BusinessRequirement/01_account-br.md#BR-002) |

---

<!-- portal-bottom -->
[← 権限設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
