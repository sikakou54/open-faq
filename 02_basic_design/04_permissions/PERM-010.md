# <span id="PERM-010"></span>PERM-010: 規約再同意の認可割込み

> **このページは規約・プライバシーポリシー改定時に、ログイン後の認可フローへ再同意画面を割り込ませる発火条件と段階適用を定義します。**

*種別 権限定義 ・ ステータス ドラフト*

## <span id="perm"></span>1. ロール別操作可否

改定済みで未同意の文書があれば §認可判定の \#3 で SCR-020 へ割込み、割込み中は他画面の操作を許しません。発効 30 日前に予告し、同意期限は発効日 + 14 日です。

| 操作 | オーナー | メンバー(割当あり) | メンバー(割当なし) | 未認証 | ウィジェット利用者 |
|----|----|----|----|----|----|
| 規約再同意の同意 / 不同意 | 可 | 不可 | 不可 | — | — |
| 再同意未完了の契約での通常操作 | 不可(割込み) | 不可(契約側ゲートの影響) | — | — | — |

> [!IMPORTANT]
> **同意・割込みはオーナー専有** 規約再同意の同意 / 不同意操作はオーナー専有機能です(FR-015)。再同意未完了の契約に属するメンバーは、契約側の同意完了までゲートの影響を受けます。拒否時は `E-AUTHZ-TERMS`。

## <span id="trace"></span>2. 対応 UC / SCR / EVT / API

本権限が適用される画面・イベント・API・業務ユースケースの結線です。

| 観点 | 結線 |
|----|----|
| 対応業務UC | [UC-013](../../01_requirements/04_business_usecases/UC-013.md#UC-013) [UC-077](../../01_requirements/04_business_usecases/UC-077.md#UC-077) |
| 対応画面SCR | [SCR-020](../01_frontend/01_screens/SCR-020.md#SCR-020) |
| 対応EVT | EVT-135 EVT-169 |
| 対応API | [API-052](../02_backend/03_apis/API-052.md#API-052) [API-054](../02_backend/03_apis/API-054.md#API-054) [API-055](../02_backend/03_apis/API-055.md#API-055) |

## <span id="src"></span>3. 由来要件

| 由来要件 |
|----|
| [FR-010](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-010) [FR-015](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-015) |
