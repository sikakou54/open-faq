<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [権限設計](index.md) ／ **PERM-009: 契約状態によるアクセス制限**
<!-- /portal-top -->

# <span id="PERM-009"></span>PERM-009: 契約状態によるアクセス制限

> **このページは契約状態(停止中 / 退会申請中 / 退会済み)ごとに管理画面で許す操作とセッションの扱いを定義します。**

*種別 権限定義 ・ ステータス ドラフト ・ 再構成 P6b*

## <span id="perm"></span>1. ロール別操作可否

契約状態は §認可判定の \#4 で評価し、`suspended` / `deleted_pending` / `deleted` のときアクセスを制限します。支払方法ゲートはこの契約停止とは別経路です。

| 操作 | オーナー | メンバー(割当あり) | メンバー(割当なし) | 未認証 | ウィジェット利用者 |
|----|----|----|----|----|----|
| 停止中(suspended): 課金・退会 | 可 | 不可 | — | — | — |
| 停止中(suspended): その他操作 | 不可(403) | 不可(403) | — | — | — |
| 退会申請中(deleted_pending): 参照 | 可 | 不可 | — | — | — |
| 退会申請中(deleted_pending): 新規書込 | 不可 | 不可 | — | — | — |
| 退会済み(deleted): ログイン | 不可 | 不可 | — | 不可 | — |

> [!NOTE]
> **支払方法ゲートは契約停止ではない** 支払方法未登録 + 無料枠超過によるウィジェット受付停止は契約サスペンションではありません(`status` は `active` のまま)。本制限の対象外で管理画面は通常どおり利用できます。拒否時は `E-BIZ-CONTRACT-SUSPENDED` / `E-BIZ-CONTRACT-DELETED`。契約状態遷移は [課金・請求設計書](../05_billing-design.md) が正本。

## <span id="trace"></span>2. 対応 UC / SCR / EVT / API

本権限が適用される画面・イベント・API・業務ユースケースの結線です。

| 観点 | 結線 |
|----|----|
| 対応業務UC | — |
| 対応画面SCR | — |
| 対応EVT | — |
| 対応API | [API-002](../03_apis/API-002.md#API-002) [API-037](../03_apis/API-037.md#API-037) |

## <span id="src"></span>3. 由来要件

| 由来要件 |
|----|
| [FR-098](../../01_requirements/01_specifications/FR-098.md#FR-098) |

---

<!-- portal-bottom -->
[← 権限設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
