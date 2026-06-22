<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [権限設計](index.md) ／ **PERM-007: セッションとログイン失敗ロックアウト**
<!-- /portal-top -->

# <span id="PERM-007"></span>PERM-007: セッションとログイン失敗ロックアウト

> **このページはセッションの寿命(無操作 30 分・絶対 12 時間)・複数デバイス同時ログイン・失効優先順位と、5 回連続失敗による 15 分ロックアウトを定義します。**

*種別 権限定義 ・ ステータス ドラフト ・ 再構成 P6b*

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
| 対応業務UC | [UC-004](../../01_requirements/02_business_usecases/UC-004.md#UC-004) [UC-242](../../01_requirements/02_business_usecases/UC-242.md#UC-242) [UC-243](../../01_requirements/02_business_usecases/UC-243.md#UC-243) [UC-244](../../01_requirements/02_business_usecases/UC-244.md#UC-244) |
| 対応画面SCR | [SCR-001](../01_screens/SCR-001.md#SCR-001) |
| 対応EVT | [EVT-004](../02_screen_events/EVT-004.md#EVT-004) |
| 対応API | [API-002](../03_apis/API-002.md#API-002) [API-003](../03_apis/API-003.md#API-003) |

## <span id="src"></span>3. 由来要件

| 由来要件 |
|----|
| [FR-007](../../01_requirements/01_specifications/01_account-fr.md#FR-007) [FR-008](../../01_requirements/01_specifications/01_account-fr.md#FR-008) [FR-011](../../01_requirements/01_specifications/01_account-fr.md#FR-011) [FR-182](../../01_requirements/01_specifications/01_account-fr.md#FR-182) [FR-188](../../01_requirements/01_specifications/01_account-fr.md#FR-188) [BR-004](../../01_requirements/01_specifications/01_account-br.md#BR-004) [BR-005](../../01_requirements/01_specifications/01_account-br.md#BR-005) [BR-006](../../01_requirements/01_specifications/01_account-br.md#BR-006) |

---

<!-- portal-bottom -->
[← 権限設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
