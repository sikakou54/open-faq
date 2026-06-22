<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [権限設計](index.md) ／ **PERM-011: critical 通知の宛先解決**
<!-- /portal-top -->

# <span id="PERM-011"></span>PERM-011: critical 通知の宛先解決

> **このページはcritical 通知を「誰に送るか」を決める宛先解決(オーナー + 当該プロジェクトの有効メンバーの 2 マスタ合算・重複排除)を定義します。**

*種別 権限定義 ・ ステータス ドラフト ・ 再構成 P6b*

## <span id="perm"></span>1. ロール別操作可否

宛先はオーナー(`M_CONTRACT` 由来)と当該プロジェクトの有効メンバー(`M_PRJ_USERS valid=1`)の 2 マスタを合算し、認証主体(`M_USER` の `user_id`)で重複排除します。配信契機・文面は [メッセージ設計](../08_messages/index.md) が正本です。

| 操作 | オーナー | メンバー(割当あり) | メンバー(割当なし) | 未認証 | ウィジェット利用者 |
|----|----|----|----|----|----|
| 契約横断 critical 通知の受信 | 受信(網羅) | 受信(当該PJ) | — | — | — |
| プロジェクト限定通知(上限アラート等)の受信 | 受信(対象PJ) | 受信(対象PJのvalid=1) | — | — | — |

> [!NOTE]
> **宛先解決ロジックの正本** 「誰が宛先か」を決める解決ロジックは本ページが正本です。配信契機・件名・本文テンプレートは [メッセージ設計](../08_messages/index.md) が正本です。

## <span id="trace"></span>2. 対応 UC / SCR / EVT / API

本権限が適用される画面・イベント・API・業務ユースケースの結線です。

| 観点 | 結線 |
|----|----|
| 対応業務UC | [UC-251](../../01_requirements/04_business_usecases/UC-251.md#UC-251) |
| 対応画面SCR | — |
| 対応EVT | — |
| 対応API | [API-021](../03_apis/API-021.md#API-021) [API-024](../03_apis/API-024.md#API-024) |

## <span id="src"></span>3. 由来要件

| 由来要件 |
|----|
| [FR-034](../../01_requirements/02_FunctionalRequirement/01_account-fr.md#FR-034) [FR-185](../../01_requirements/02_FunctionalRequirement/01_account-fr.md#FR-185) |

---

<!-- portal-bottom -->
[← 権限設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
