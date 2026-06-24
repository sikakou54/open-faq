# <span id="PERM-003"></span>PERM-003: オーナー専有機能

> **このページは非オーナーに付与してはならないオーナー専有機能(課金・契約設定・プロジェクト CRUD・退会・規約再同意)と、その判定段を定義します。**

*種別 権限定義 ・ ステータス ドラフト*

## <span id="perm"></span>1. ロール別操作可否

課金情報・支払方法・請求履歴・退会・規約再同意・契約設定、プロジェクトの作成・編集・削除はオーナー専有です。メンバーには付与しません。非オーナーが要求した場合は §認可判定の \#8 で 403(`E-AUTHZ-OWNER-ONLY`)に落とします。

| 操作 | オーナー | メンバー(割当あり) | メンバー(割当なし) | 未認証 | ウィジェット利用者 |
|----|----|----|----|----|----|
| 契約設定の取得・更新 | 可 | 不可 | 不可 | 不可 | 不可 |
| 支払方法の登録・更新 | 可 | 不可 | 不可 | 不可 | 不可 |
| プロジェクトの作成・編集・削除 | 可 | 不可 | 不可 | 不可 | 不可 |
| 退会申請 | 可 | 不可 | 不可 | 不可 | 不可 |
| 規約再同意の同意 / 不同意 | 可 | 不可 | 不可 | 不可 | 不可 |
| プロジェクト単位の上限・無料枠の変更 | 可 | 可(当該PJ) | 不可 | 不可 | 不可 |

> [!NOTE]
> **上限・無料枠はメンバーも変更可** プロジェクト単位の利用上限・無料枠は、オーナーまたは当該プロジェクトのメンバーが変更できます(BR-017)。

## <span id="trace"></span>2. 対応 SCR / EVT / API

本権限が適用される画面・イベント・API の結線です。

| 観点 | 結線 |
|----|----|
| トレーサビリティID | [TR-013](../00_traceability/index.md#TR-013) ・ [TR-015](../00_traceability/index.md#TR-015) ・ [TR-016](../00_traceability/index.md#TR-016) ・ [TR-017](../00_traceability/index.md#TR-017) ・ [TR-022](../00_traceability/index.md#TR-022) ・ [TR-023](../00_traceability/index.md#TR-023) ・ [TR-036](../00_traceability/index.md#TR-036) ・ [TR-037](../00_traceability/index.md#TR-037) ・ [TR-038](../00_traceability/index.md#TR-038) |
| 対応画面SCR | [SCR-005](../01_frontend/01_screens/SCR-005.md#SCR-005) [SCR-019](../01_frontend/01_screens/SCR-019.md#SCR-019) [SCR-028](../01_frontend/01_screens/SCR-028.md#SCR-028) |
| 対応EVT | — |
| 対応API | [API-014](../02_backend/03_apis/API-014.md#API-014) [API-015](../02_backend/03_apis/API-015.md#API-015) [API-017](../02_backend/03_apis/API-017.md#API-017) [API-018](../02_backend/03_apis/API-018.md#API-018) [API-045](../02_backend/03_apis/API-045.md#API-045) [API-056](../02_backend/03_apis/API-056.md#API-056) |
