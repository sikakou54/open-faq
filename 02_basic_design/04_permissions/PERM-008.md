# <span id="PERM-008"></span>PERM-008: アカウント状態と利用可否

> **このページはアカウント状態（有効 / 招待中 / メール未確認 / ロック中 / 無効化）ごとのログイン可否と利用範囲を定義します。**

| ID | 業務ユースケースID | イベント(画面ID EVT-NN) | API ID |
|----|----|----|----|
| PERM-008 | [UC-002](../../01_requirements/04_business_usecases/UC-002.md#UC-002) ・ [UC-003](../../01_requirements/04_business_usecases/UC-003.md#UC-003) ・ [UC-006](../../01_requirements/04_business_usecases/UC-006.md#UC-006) ・ [UC-019](../../01_requirements/04_business_usecases/UC-019.md#UC-019) ・ [UC-021](../../01_requirements/04_business_usecases/UC-021.md#UC-021) | SCR-018 EVT-01 ・ SCR-023 EVT-04 | [API-006](../02_backend/03_apis/API-006.md#API-006) [API-008](../02_backend/03_apis/API-008.md#API-008) [API-023](../02_backend/03_apis/API-023.md#API-023) |
*種別 権限定義 ・ ステータス ドラフト*

## <span id="criteria"></span>1. 判定基準（ビジネスロジック）

アカウント状態は認可判定の \#2 で評価します。招待中・メール未確認は利用を限定し、最後の割当解除による無効化では全セッション・未使用招待を失効させます。

| アカウント状態 | オーナー | メンバー | 未認証 | ウィジェット利用者 |
|----|----|----|----|----|
| 有効 | 全操作 | 割当に応じた操作 | — | — |
| 招待中（有効化前） | — | — | 招待リンクからの有効化のみ | — |
| メール未確認 | メール確認のみ | メール確認のみ | — | — |
| ロック中 | 不可（ロックアウト中） | 不可（ロックアウト中） | 不可 | — |
| 無効化（最後の割当解除） | — | — | 不可 | — |

## <span id="invariant"></span>2. 不変条件（ビジネスルール）

- **最後の割当解除による自動無効化**: メンバーの最後の有効割当が解除されたとき、対象アカウントを自動で無効化し、全セッション・未使用招待を失効させます（[FR-031](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-031) / [FR-185](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-185)）。
- **データ消去の事前告知**: [システム仕様書 §4](../07_system-spec.md#4-データ保持期間削除猶予) の保持期間経過後にデータが消去される旨は割当解除の確認時に明示します。

## <span id="deny"></span>3. 権限不足時の挙動

- 招待中のアカウントが招待リンク以外からアクセスした場合 → ログイン不可として再ログイン誘導またはエラーを表示します。
- メール未確認のアカウントが管理機能にアクセスした場合 → メール確認を促す画面へ誘導します。
- 無効化されたアカウントがログインを試みた場合 → 認証エラーとして扱います。

## <span id="trace"></span>4. 関連設計

| 観点 | 結線 |
|----|----|
| 対応画面SCR | [SCR-018](../01_frontend/01_screens/SCR-018.md#SCR-018) [SCR-023](../01_frontend/01_screens/SCR-023.md#SCR-023) |
| 対応EVT | SCR-018 EVT-01 SCR-023 EVT-04 |
| 対応API | [API-006](../02_backend/03_apis/API-006.md#API-006) [API-008](../02_backend/03_apis/API-008.md#API-008) [API-023](../02_backend/03_apis/API-023.md#API-023) |
