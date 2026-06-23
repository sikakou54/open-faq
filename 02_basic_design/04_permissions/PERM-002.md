# <span id="PERM-002"></span>PERM-002: 認可判定の順序

> **このページは1 リクエストを許可するまでに通す認可判定の段(セッション → 契約状態 → オーナー判定 → 境界 → 専有 → 再認証 → 利用上限)と、各段の拒否時エラーを定義します。**

*種別 権限定義 ・ ステータス ドラフト*

## <span id="perm"></span>1. ロール別操作可否

判定段は上から評価します。各段は拒否時に対応するエラー分類へ落とし、エラー定義の正本は [エラー設計](../05_errors/index.md) です。

| \# | 判定段 | 内容 | 拒否時のエラー |
|----|----|----|----|
| 1 | セッション検証 | 無操作 30 分 / 絶対 12 時間を満たす有効セッションか | [ERR-036](../05_errors/ERR-036.md#ERR-036)(`E-AUTH-SESSION-EXPIRED`) |
| 2 | アカウント有効性 | アカウントが利用可能状態か(無効化済みなら再ログインへ誘導) | — |
| 3 | 規約再同意ゲート | 改定済みで未同意の文書があれば SCR-020 割込みへ | [SCR-020](../01_frontend/01_screens/SCR-020.md#SCR-020) へ誘導(`E-AUTHZ-TERMS`・エラーではなくゲート) |
| 4 | 契約状態ゲート | `suspended` / `deleted_pending` / `deleted` 時はアクセス制限を適用 | [ERR-006](../05_errors/ERR-006.md#ERR-006) 等 |
| 5 | オーナー判定(isOwner bypass) | `M_CONTRACT.user_id` 一致で自契約配下を無条件許可 | — |
| 6 | オーナー境界判定 | 非オーナーは契約境界キー一致を要求。不一致は 404 偽装 | [ERR-019](../05_errors/ERR-019.md#ERR-019)(`E-AUTHZ-OWNER-BOUNDARY`) |
| 7 | プロジェクト境界判定 | 対象プロジェクトへの割当があること。割当なしは 404 偽装 | [ERR-021](../05_errors/ERR-021.md#ERR-021) / [ERR-032](../05_errors/ERR-032.md#ERR-032) |
| 8 | オーナー専有機能判定 | 専有機能を非オーナーが要求した場合は 403 | [ERR-017](../05_errors/ERR-017.md#ERR-017) |
| 9 | オーナー保護・自己操作禁止 | 不可制約に該当すれば拒否 | [ERR-023](../05_errors/ERR-023.md#ERR-023) / [ERR-024](../05_errors/ERR-024.md#ERR-024) |
| 10 | 再認証判定 | 重要操作で再認証が「当該操作 1 回 + 15 分以内」を満たすか | [ERR-015](../05_errors/ERR-015.md#ERR-015)(`E-AUTH-REAUTH-REQUIRED`) |
| 11 | 利用上限判定 | 認可通過後に上限を確認(レート = 契約単位、上限・無料枠 = プロジェクト単位) | [課金・請求設計書](../05_billing-design.md) |

## <span id="trace"></span>2. 対応 UC / SCR / EVT / API

本権限が適用される画面・イベント・API・業務ユースケースの結線です。

| 観点 | 結線 |
|----|----|
| 対応業務UC | [UC-008](../../01_requirements/04_business_usecases/UC-008.md#UC-008) |
| 対応画面SCR | — |
| 対応EVT | — |
| 対応API | — |

## <span id="src"></span>3. 由来要件

| 由来要件 |
|----|
| [FR-188](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-188) [FR-189](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-189) [FR-191](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-191) |
