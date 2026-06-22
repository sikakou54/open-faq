<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [権限設計](index.md) ／ **PERM-001: ユーザー種別とオーナー判定**
<!-- /portal-top -->

# <span id="PERM-001"></span>PERM-001: ユーザー種別とオーナー判定

> **このページは認可の起点となるユーザー種別(オーナー / メンバー / ウィジェット利用者)の判定方法と権限の表し方を定義します。**

*種別 権限定義 ・ ステータス ドラフト ・ 再構成 P6b*

## <span id="perm"></span>1. ロール別操作可否

認証主体は全ユーザー共通の `M_USER` で、セッション / トークンは `user_id` で `M_USER` を指します。種別は導出で判定し、オーナーは `M_CONTRACT.user_id` 一致(`isOwner`)、メンバーは `M_PRJ_USERS` の有効割当(`valid=1`)で導出します。

| 操作 | オーナー | メンバー(割当あり) | メンバー(割当なし) | 未認証 | ウィジェット利用者 |
|----|----|----|----|----|----|
| 自契約配下の全プロジェクト操作 | 可(isOwner bypass) | — | — | 不可 | 不可 |
| 割当プロジェクト内の全操作 | 可 | 可 | 不可 | 不可 | 不可 |
| オーナー専有機能 | 可 | 不可 | 不可 | 不可 | 不可 |
| ウィジェットへの質問送信 | — | — | — | — | 可(公開キー) |

> [!IMPORTANT]
> **オーナー判定 = isOwner bypass を先頭に** 認可権威は `M_CONTRACT.user_id` がセッションの `user_id` と一致すること(`isOwner=true`)による bypass を最優先とし、`M_PRJ_USERS` の owner 行は一覧表示・通知宛先の網羅用で専有判定には用いません。メンバー権限は `M_PRJ_USERS` の有効割当(`valid=1`)でのみ付与されます。オーナーは役割変更・降格・譲渡なし。プロジェクト内の役割差は持ちません。

## <span id="trace"></span>2. 対応 UC / SCR / EVT / API

本権限が適用される画面・イベント・API・業務ユースケースの結線です。

| 観点 | 結線 |
|----|----|
| 対応業務UC | [UC-236](../../01_requirements/02_business_usecases/UC-236.md#UC-236) |
| 対応画面SCR | [SCR-013](../01_screens/SCR-013.md#SCR-013) |
| 対応EVT | — |
| 対応API | [API-002](../03_apis/API-002.md#API-002) |

## <span id="src"></span>3. 由来要件

| 由来要件 |
|----|
| [FR-013](../../01_requirements/01_specifications/01_account-fr.md#FR-013) [FR-014](../../01_requirements/01_specifications/01_account-fr.md#FR-014) [FR-016](../../01_requirements/01_specifications/01_account-fr.md#FR-016) [FR-035](../../01_requirements/01_specifications/01_account-fr.md#FR-035) [FR-186](../../01_requirements/01_specifications/01_account-fr.md#FR-186) |

---

<!-- portal-bottom -->
[← 権限設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
