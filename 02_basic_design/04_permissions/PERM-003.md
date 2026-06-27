# <span id="PERM-003"></span>PERM-003: オーナー専有機能

> **このページは、対象プロジェクトのオーナー（作成者）だけに付与するオーナー専有機能（当該プロジェクトの課金・請求確認・プロジェクト CRUD）と、その判定段を定義します。支払方法・退会・規約再同意はアカウント（本人）単位の操作で、オーナー専有ではありません。**

| ID | 業務ユースケースID | イベント(画面ID EVT-NN) | API ID |
|----|----|----|----|
| PERM-003 | [UC-013](../../01_requirements/04_business_usecases/UC-013.md#UC-013) ・ [UC-015](../../01_requirements/04_business_usecases/UC-015.md#UC-015) ・ [UC-016](../../01_requirements/04_business_usecases/UC-016.md#UC-016) ・ [UC-017](../../01_requirements/04_business_usecases/UC-017.md#UC-017) ・ [UC-022](../../01_requirements/04_business_usecases/UC-022.md#UC-022) ・ [UC-022](../../01_requirements/04_business_usecases/UC-022.md#UC-022) ・ [UC-035](../../01_requirements/04_business_usecases/UC-035.md#UC-035) ・ [UC-036](../../01_requirements/04_business_usecases/UC-036.md#UC-036) ・ [UC-037](../../01_requirements/04_business_usecases/UC-037.md#UC-037) | — | [API-014](../02_backend/03_apis/API-014.md#API-014) [API-015](../02_backend/03_apis/API-015.md#API-015) [API-017](../02_backend/03_apis/API-017.md#API-017) [API-018](../02_backend/03_apis/API-018.md#API-018) [API-045](../02_backend/03_apis/API-045.md#API-045) [API-056](../02_backend/03_apis/API-056.md#API-056) |
*種別 権限定義 ・ ステータス ドラフト*

## <span id="criteria"></span>1. 判定基準（ビジネスロジック）

当該プロジェクトの課金・請求確認、プロジェクトの作成・編集・削除は、**対象プロジェクトの作成者**であることを判定条件とします。当該プロジェクトのメンバーには付与しません。非オーナーが要求した場合は認可判定の \#8 で 403 に落とします。

支払方法の登録・更新・退会・規約再同意は**アカウント（本人）単位の操作**で、特定プロジェクトのオーナーであることを問わず、認証済み本人であれば実行できます。

| 操作 | 対象PJのオーナー（作成者） | 対象PJのメンバー | 未認証 | ウィジェット利用者 |
|----|----|----|----|----|
| 当該プロジェクトの課金・請求の確認 | 可 | 不可 | 不可 | 不可 |
| プロジェクトの作成・編集・削除 | 可 | 不可 | 不可 | 不可 |
| 支払方法の登録・更新（アカウント単位・本人） | 可（本人） | 可（本人） | 不可 | 不可 |
| 退会（アカウント単位・本人） | 可（本人） | 可（本人） | 不可 | 不可 |
| 規約再同意の同意 / 不同意（アカウント単位・本人） | 可（本人） | 可（本人） | 不可 | 不可 |
| プロジェクト単位の上限・無料枠の変更 | 可 | 可（当該PJ） | 不可 | 不可 |

## <span id="invariant"></span>2. 不変条件（ビジネスルール）

- **オーナー専有とアカウント単位操作の区別**: 「当該プロジェクトの課金・請求の確認」「プロジェクトの作成・編集・削除」はオーナー専有です。「支払方法の登録・更新」「退会」「規約再同意」はアカウント本人単位で、プロジェクトの立場を問いません。
- **上限・無料枠の変更はメンバーも可**: プロジェクト単位の利用上限・無料枠は、オーナーまたは当該プロジェクトのメンバーが変更できます（[BR-017](../../01_requirements/01_business_requirement/01_account-br.md#BR-017)）。

## <span id="deny"></span>3. 権限不足時の挙動

- 非オーナーがオーナー専有機能を要求した場合 → **403**（権限不足）を表示します。
- 未認証ユーザーが実行を試みた場合 → 認証エラーへ誘導します。

## <span id="trace"></span>4. 関連設計

| 観点 | 結線 |
|----|----|
| 対応画面SCR | [SCR-005](../01_frontend/01_screens/SCR-005.md#SCR-005) [SCR-019](../01_frontend/01_screens/SCR-019.md#SCR-019) [SCR-028](../01_frontend/01_screens/SCR-028.md#SCR-028) |
| 対応EVT | — |
| 対応API | [API-014](../02_backend/03_apis/API-014.md#API-014) [API-015](../02_backend/03_apis/API-015.md#API-015) [API-017](../02_backend/03_apis/API-017.md#API-017) [API-018](../02_backend/03_apis/API-018.md#API-018) [API-045](../02_backend/03_apis/API-045.md#API-045) [API-056](../02_backend/03_apis/API-056.md#API-056) |
