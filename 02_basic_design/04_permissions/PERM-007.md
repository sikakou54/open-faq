# <span id="PERM-007"></span>PERM-007: セッションとログイン失敗ロックアウト

> **このページはセッションの寿命(無操作 30 分・絶対 12 時間)・複数デバイス同時ログイン・失効優先順位と、5 回連続失敗による 15 分ロックアウトを定義します。**

*種別 権限定義 ・ ステータス ドラフト*

## <span id="perm"></span>1. ロール別操作可否

セッションは無操作 30 分・絶対 12 時間で失効させ、強制ログアウトを最優先に評価します。ログインが 5 回連続失敗したら当該アカウントを 15 分ロックし、ロック中の到達は `E-AUTH-LOCKED` に落とします。

| 操作 | オーナー | メンバー(割当あり) | メンバー(割当なし) | 未認証 | ウィジェット利用者 |
|----|----|----|----|----|----|
| 複数デバイス同時ログイン | 可 | 可 | — | — | — |
| 自身のアクティブセッション一覧・終了 | 不可(MVP対象外) | 不可(MVP対象外) | — | — | — |
| ロック中のログイン | 不可(15分) | 不可(15分) | — | 不可 | — |
| ロック解除 | 可 | 可(当該PJ) | — | 時間経過のみ | — |

> [!NOTE]
> **失効の優先順位** 強制ログアウト > 絶対タイムアウト(12h) > 無操作タイムアウト(30分) > 通常セッション の順で評価します。割当変更は既存セッションを即時失効させず、次回認可チェック時(キャッシュ TTL 60 秒以内)に反映します(FR-188)。

## <span id="trace"></span>2. 対応 UC / SCR / EVT / API

本権限が適用される画面・イベント・API・業務ユースケースの結線です。

| 観点 | 結線 |
|----|----|
| 対応業務UC | [UC-001](../../01_requirements/04_business_usecases/UC-001.md#UC-001) [UC-072](../../01_requirements/04_business_usecases/UC-072.md#UC-072) [UC-073](../../01_requirements/04_business_usecases/UC-073.md#UC-073) [UC-074](../../01_requirements/04_business_usecases/UC-074.md#UC-074) |
| 対応画面SCR | [SCR-001](../01_frontend/01_screens/SCR-001.md#SCR-001) |
| 対応EVT | EVT-004 |
| 対応API | [API-002](../02_backend/03_apis/API-002.md#API-002) [API-003](../02_backend/03_apis/API-003.md#API-003) |

## <span id="src"></span>3. 由来要件

| 由来要件 |
|----|
| [FR-007](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-007) [FR-008](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-008) [FR-011](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-011) [FR-182](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-182) [FR-188](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-188) [BR-004](../../01_requirements/01_business_requirement/01_account-br.md#BR-004) [BR-005](../../01_requirements/01_business_requirement/01_account-br.md#BR-005) [BR-006](../../01_requirements/01_business_requirement/01_account-br.md#BR-006) |
