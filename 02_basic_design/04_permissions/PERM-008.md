<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [権限設計](index.md) ／ **PERM-008: アカウント状態と利用可否**
<!-- /portal-top -->

# <span id="PERM-008"></span>PERM-008: アカウント状態と利用可否

> **このページはアカウント状態(有効 / 招待中 / メール未確認 / ロック中 / 無効化)ごとのログイン可否と利用範囲を定義します。**

*種別 権限定義 ・ ステータス ドラフト*

## <span id="perm"></span>1. ロール別操作可否

アカウント状態は §認可判定の \#2 で評価します。招待中・メール未確認は利用を限定し、最後の割当解除による無効化では全セッション・未使用招待を失効させます。

| 操作 | オーナー | メンバー(割当あり) | メンバー(割当なし) | 未認証 | ウィジェット利用者 |
|----|----|----|----|----|----|
| 有効 | 全操作 | 割当に応じた操作 | — | — | — |
| 招待中(有効化前) | — | — | — | 招待リンクからの有効化のみ | — |
| メール未確認 | メール確認のみ | メール確認のみ | — | — | — |
| ロック中 | 不可(15分) | 不可(15分) | — | 不可 | — |
| 無効化(最後の割当解除) | — | — | 不可 | 不可 | — |

> [!IMPORTANT]
> **最後の割当解除による自動無効化** メンバーの最後の有効割当が解除されたとき、対象アカウントを自動で無効化し、全セッション・未使用招待を失効させます(FR-031 / FR-189)。一定期間(90 日)経過後にデータが消去される旨は割当解除の確認時に明示します。

## <span id="trace"></span>2. 対応 UC / SCR / EVT / API

本権限が適用される画面・イベント・API・業務ユースケースの結線です。

| 観点 | 結線 |
|----|----|
| 対応業務UC | [UC-002](../../01_requirements/04_business_usecases/UC-002.md#UC-002) [UC-019](../../01_requirements/04_business_usecases/UC-019.md#UC-019) [UC-021](../../01_requirements/04_business_usecases/UC-021.md#UC-021) [UC-003](../../01_requirements/04_business_usecases/UC-003.md#UC-003) [UC-006](../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| 対応画面SCR | [SCR-018](../01_frontend/01_screens/SCR-018.md#SCR-018) [SCR-023](../01_frontend/01_screens/SCR-023.md#SCR-023) |
| 対応EVT | [EVT-151](../01_frontend/02_screen_events/EVT-151.md#EVT-151) [EVT-190](../01_frontend/02_screen_events/EVT-190.md#EVT-190) |
| 対応API | [API-006](../02_backend/03_apis/API-006.md#API-006) [API-008](../02_backend/03_apis/API-008.md#API-008) [API-023](../02_backend/03_apis/API-023.md#API-023) |

## <span id="src"></span>3. 由来要件

| 由来要件 |
|----|
| [FR-003](../../01_requirements/02_FunctionalRequirement/01_account-fr.md#FR-003) [FR-021](../../01_requirements/02_FunctionalRequirement/01_account-fr.md#FR-021) [FR-031](../../01_requirements/02_FunctionalRequirement/01_account-fr.md#FR-031) [FR-189](../../01_requirements/02_FunctionalRequirement/01_account-fr.md#FR-189) |

---

<!-- portal-bottom -->
[← 権限設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
