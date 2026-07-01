# エラー設計

> **このページは、API レスポンスで返すエラーコードの一覧と、画面イベント / API からエラーへの対応表です。** 各エラーは HTTP ステータス・分類・メッセージ・業務ユースケースID・API ID を `ERR-NNN.md` で個別定義します。エラーの正本は各 ERR ファイル、認証・認可の判定段との対応は [権限設計](../04_permissions/index.md) を参照します。

*ステータス ドラフト*

## <span id="reading"></span>読み順

API設計 ＞ 本エラー設計 ＞ メッセージ設計。各 API の `## エラー` 表から本 ERR を参照する。

## <span id="list"></span>1. エラーコード一覧(36)

分類・HTTP ステータス・主エラーコードの索引です。各 ERR の定義は個別ファイルが正本です。

| ERR ID | 分類 | HTTP | エラーコード | 分類コード | メッセージ |
|----|----|----|----|----|----|
| <span id="ERR-001"></span>[ERR-001](ERR-001.md#ERR-001) | 入力検証 | 400 | `VALIDATION_ERROR` | — | 入力値の検証エラー |
| <span id="ERR-002"></span>[ERR-002](ERR-002.md#ERR-002) | 認証 | 401 | `INVALID_CREDENTIALS` | `E-AUTH-CREDENTIAL` | 認証情報が不正 |
| <span id="ERR-003"></span>[ERR-003](ERR-003.md#ERR-003) | 認証 | 423 | `LOCKED_OUT` | `E-AUTH-LOCKED` | アカウントロック中 |
| <span id="ERR-004"></span>[ERR-004](ERR-004.md#ERR-004) | 業務(課金) | 403 | `BILLING_ACCOUNT_SUSPENDED` | `E-BILL-ACCOUNT-SUSPENDED` | 課金アカウントがサスペンション中(支払い不能) |
| <span id="ERR-005"></span>[ERR-005](ERR-005.md#ERR-005) | 認証 | 401 | `INVALID_PASSWORD` | — | パスワードが不正 |
| <span id="ERR-006"></span>[ERR-006](ERR-006.md#ERR-006) | 認証 | 410 | `TOKEN_EXPIRED` | `E-AUTH-TOKEN-EXPIRED` | トークン期限切れ |
| <span id="ERR-007"></span>[ERR-007](ERR-007.md#ERR-007) | 認証 | 410 | `TOKEN_USED` | `E-AUTH-TOKEN-USED` | トークン使用済み |
| <span id="ERR-008"></span>[ERR-008](ERR-008.md#ERR-008) | 認証 | 404 | `TOKEN_NOT_FOUND` | — | トークンが存在しない |
| <span id="ERR-009"></span>[ERR-009](ERR-009.md#ERR-009) | 認証 | 429 | `RATE_LIMITED` | `E-AUTH-RATE-LIMITED` | レート制限超過(再送間隔未到達) |
| <span id="ERR-010"></span>[ERR-010](ERR-010.md#ERR-010) | 入力検証 | 409 | `ALREADY_VERIFIED` | — | 連絡先メールが既に確認済み |
| <span id="ERR-011"></span>[ERR-011](ERR-011.md#ERR-011) | 業務 | 404 | `PROJECT_NOT_FOUND` | — | 対象プロジェクトが存在しない |
| <span id="ERR-012"></span>[ERR-012](ERR-012.md#ERR-012) | 入力検証 | 400 | `CONTACT_EMAIL_NOT_SET` | — | 連絡先メールが未設定 |
| <span id="ERR-013"></span>[ERR-013](ERR-013.md#ERR-013) | 認証 | 401 | `REAUTH_REQUIRED` | `E-AUTH-REAUTH-REQUIRED` | 再認証トークンが無効または未提示 |
| <span id="ERR-014"></span>[ERR-014](ERR-014.md#ERR-014) | 入力検証 | 409 | `EMAIL_ALREADY_USED` | — | 入力メールアドレスが既に使用中 |
| <span id="ERR-015"></span>[ERR-015](ERR-015.md#ERR-015) | 認可 | 403 | `OWNER_ONLY` | `E-AUTHZ-OWNER-ONLY` | オーナー以外は不可 |
| <span id="ERR-016"></span>[ERR-016](ERR-016.md#ERR-016) | 入力検証 | 409 | `DUPLICATE_NAME` | — | プロジェクト名重複 |
| <span id="ERR-017"></span>[ERR-017](ERR-017.md#ERR-017) | 認可 | 404 | `NOT_FOUND` | `E-AUTHZ-OWNER-BOUNDARY` | オーナー境界違反偽装 |
| <span id="ERR-018"></span>[ERR-018](ERR-018.md#ERR-018) | 入力検証 | 409 | `ALREADY_EXISTS_IN_PROJECT` | — | 既に該当プロジェクトに割当あり |
| <span id="ERR-019"></span>[ERR-019](ERR-019.md#ERR-019) | 認可 | 403 | `PROJECT_ACCESS_DENIED` | `E-AUTHZ-PROJECT-DENIED` | 当該プロジェクトへの権限なし |
| <span id="ERR-020"></span>[ERR-020](ERR-020.md#ERR-020) | 入力検証 | 409 | `EMAIL_ALREADY_EXISTS` | — | メールアドレスの重複 |
| <span id="ERR-021"></span>[ERR-021](ERR-021.md#ERR-021) | 認可 | 403 | `OWNER_PROTECTED` | `E-AUTHZ-OWNER-PROTECTED` | オーナーは解除不可 |
| <span id="ERR-022"></span>[ERR-022](ERR-022.md#ERR-022) | 認可 | 403 | `SELF_MUTATION_FORBIDDEN` | `E-AUTHZ-SELF-MUTATION` | 自分自身は解除不可 |
| <span id="ERR-023"></span>[ERR-023](ERR-023.md#ERR-023) | 入力検証 | 409 | `CONFLICT` | — | リソースの状態が競合している(楽観ロックの `version` 不一致、または既に確定済みの状態への重複操作 等) |
| <span id="ERR-024"></span>[ERR-024](ERR-024.md#ERR-024) | 入力検証 | 415 / 400 | `CSV_INVALID` | `E-INPUT-CSV-INVALID` | CSV 以外 / 不正形式 |
| <span id="ERR-025"></span>[ERR-025](ERR-025.md#ERR-025) | 入力検証 | (行単位) | `CSV_FAQ_ID_NOT_FOUND` | `E-INPUT-CSV-FAQID-NOTFOUND` | 当該プロジェクトに存在しない FAQ ID |
| <span id="ERR-026"></span>[ERR-026](ERR-026.md#ERR-026) | 認証 | 401 | `WIDGET_KEY_INVALID` | — | 公開キーが不正 |
| <span id="ERR-027"></span>[ERR-027](ERR-027.md#ERR-027) | 認可 | 403 | `DOMAIN_NOT_ALLOWED` | — | 許可ドメイン外 |
| <span id="ERR-028"></span>[ERR-028](ERR-028.md#ERR-028) | 業務(課金) | 402 | `PAYMENT_METHOD_DECLINED` | `E-BILL-PAYMENT-FAILED` | カードが拒否された |
| <span id="ERR-029"></span>[ERR-029](ERR-029.md#ERR-029) | 業務 | 422 | `UNSUPPORTED_FIELD` | — | `freeQuota` / `alertEnabled` / `alertFrequency` を指定 |
| <span id="ERR-030"></span>[ERR-030](ERR-030.md#ERR-030) | 認可 | 403 | `PERMISSION_DENIED` | `E-AUTHZ-FORBIDDEN` | 境界通過後の操作権限不足(メンバーが専有操作を要求、本人以外の招待受諾 等)。割当なし・部外者は本エラーではなく 404 偽装 |
| <span id="ERR-031"></span>[ERR-031](ERR-031.md#ERR-031) | 認証 | 401 | `SIGNATURE_INVALID` | — | 署名検証失敗 |
| <span id="ERR-032"></span>[ERR-032](ERR-032.md#ERR-032) | 業務 | 200 | `IDEMPOTENT_REPLAY` | — | 既存処理結果を返却(冪等性違反) |
| <span id="ERR-033"></span>[ERR-033](ERR-033.md#ERR-033) | 認証 | 401 | `SESSION_EXPIRED` | `E-AUTH-SESSION-EXPIRED` | セッション期限切れ(再ログインへ) |
| <span id="ERR-034"></span>[ERR-034](ERR-034.md#ERR-034) | 業務(課金) | 403 | `ACCOUNT_WITHDRAWN` | `E-BILL-ACCOUNT-WITHDRAWN` | 退会済み(請求情報の閲覧のみ可) |
| <span id="ERR-035"></span>[ERR-035](ERR-035.md#ERR-035) | 業務 | 404 | `INVITE_TARGET_NOT_REGISTERED` | `E-INVITE-TARGET-NOT-REGISTERED` | 招待先メールが未登録(先にアカウント登録が必要) |
| <span id="ERR-036"></span>[ERR-036](ERR-036.md#ERR-036) | システム | 503 | `AI_UNAVAILABLE` | `E-AI-UNAVAILABLE` | AI 推論タイムアウトまたはプロバイダエラー |

## <span id="trace"></span>2. EVT / API ↔ エラー 対応表

各 API(と対応 EVT)が返しうるエラーの結線一覧です。EVT を持たない内部 / IF 系 API は EVT 欄を `—` とします。

| API ID | API名 | 対応EVT | 返しうるエラー |
|----|----|----|----|
| [API-001](../02_backend/03_apis/API-001.md#API-001) | 新規登録 | SCR-002 EVT-05 SCR-018 EVT-02 | [ERR-001](ERR-001.md#ERR-001) [ERR-009](ERR-009.md#ERR-009) [ERR-014](ERR-014.md#ERR-014) |
| [API-002](../02_backend/03_apis/API-002.md#API-002) | ログイン | SCR-001 EVT-02 | [ERR-001](ERR-001.md#ERR-001) [ERR-002](ERR-002.md#ERR-002) [ERR-003](ERR-003.md#ERR-003) [ERR-004](ERR-004.md#ERR-004) [ERR-034](ERR-034.md#ERR-034) |
| [API-005](../02_backend/03_apis/API-005.md#API-005) | 再認証 | SCR-034 EVT-02 SCR-019 EVT-03 SCR-028 EVT-02 SCR-028 EVT-06 | [ERR-005](ERR-005.md#ERR-005) |
| [API-006](../02_backend/03_apis/API-006.md#API-006) | メール確認 | SCR-018 EVT-01 | [ERR-001](ERR-001.md#ERR-001) [ERR-006](ERR-006.md#ERR-006) [ERR-007](ERR-007.md#ERR-007) [ERR-008](ERR-008.md#ERR-008) |
| [API-007](../02_backend/03_apis/API-007.md#API-007) | 招待トークン検証・プレビュー | SCR-023 EVT-01 | [ERR-006](ERR-006.md#ERR-006) [ERR-007](ERR-007.md#ERR-007) [ERR-008](ERR-008.md#ERR-008) |
| [API-008](../02_backend/03_apis/API-008.md#API-008) | 招待受諾(割当有効化) | SCR-023 EVT-04 | [ERR-006](ERR-006.md#ERR-006) [ERR-007](ERR-007.md#ERR-007) [ERR-030](ERR-030.md#ERR-030) |
| [API-009](../02_backend/03_apis/API-009.md#API-009) | プロジェクト連絡先メール確認 | SCR-024 EVT-01 | [ERR-006](ERR-006.md#ERR-006) [ERR-007](ERR-007.md#ERR-007) [ERR-008](ERR-008.md#ERR-008) |
| [API-010](../02_backend/03_apis/API-010.md#API-010) | パスワード再設定確定 | SCR-003 EVT-06 | [ERR-001](ERR-001.md#ERR-001) [ERR-006](ERR-006.md#ERR-006) [ERR-007](ERR-007.md#ERR-007) [ERR-008](ERR-008.md#ERR-008) |
| [API-011](../02_backend/03_apis/API-011.md#API-011) | 連絡先確認メール再送 | SCR-005 EVT-06 | [ERR-009](ERR-009.md#ERR-009) [ERR-010](ERR-010.md#ERR-010) [ERR-011](ERR-011.md#ERR-011) [ERR-012](ERR-012.md#ERR-012) |
| [API-012](../02_backend/03_apis/API-012.md#API-012) | 自己プロフィール更新 | SCR-022 EVT-03 | [ERR-001](ERR-001.md#ERR-001) |
| [API-013](../02_backend/03_apis/API-013.md#API-013) | 自己パスワード変更 | SCR-022 EVT-04 | [ERR-001](ERR-001.md#ERR-001) [ERR-013](ERR-013.md#ERR-013) |
| [API-014](../02_backend/03_apis/API-014.md#API-014) | アカウント設定取得 | SCR-022 EVT-01 | — |
| [API-015](../02_backend/03_apis/API-015.md#API-015) | セキュリティ設定更新 | SCR-022 EVT-03 | [ERR-001](ERR-001.md#ERR-001) [ERR-013](ERR-013.md#ERR-013) [ERR-014](ERR-014.md#ERR-014) |
| [API-017](../02_backend/03_apis/API-017.md#API-017) | プロジェクト新規作成 | SCR-005 EVT-04 | [ERR-001](ERR-001.md#ERR-001) [ERR-016](ERR-016.md#ERR-016) |
| [API-018](../02_backend/03_apis/API-018.md#API-018) | プロジェクト更新・削除 | SCR-005 EVT-02 SCR-005 EVT-05 SCR-005 EVT-08 SCR-011 EVT-10 | [ERR-001](ERR-001.md#ERR-001) [ERR-013](ERR-013.md#ERR-013) [ERR-015](ERR-015.md#ERR-015) [ERR-017](ERR-017.md#ERR-017) |
| [API-019](../02_backend/03_apis/API-019.md#API-019) | ウィジェット鍵ローテーション | SCR-011 EVT-09 | [ERR-013](ERR-013.md#ERR-013) |
| [API-021](../02_backend/03_apis/API-021.md#API-021) | メンバー招待 | SCR-014 EVT-03 | [ERR-013](ERR-013.md#ERR-013) [ERR-001](ERR-001.md#ERR-001) [ERR-018](ERR-018.md#ERR-018) [ERR-019](ERR-019.md#ERR-019) [ERR-035](ERR-035.md#ERR-035) |
| [API-022](../02_backend/03_apis/API-022.md#API-022) | メンバー情報更新 | SCR-014 EVT-05 | [ERR-013](ERR-013.md#ERR-013) [ERR-001](ERR-001.md#ERR-001) [ERR-017](ERR-017.md#ERR-017) [ERR-019](ERR-019.md#ERR-019) [ERR-020](ERR-020.md#ERR-020) |
| [API-023](../02_backend/03_apis/API-023.md#API-023) | プロジェクト割当解除 | SCR-014 EVT-07 | [ERR-013](ERR-013.md#ERR-013) [ERR-017](ERR-017.md#ERR-017) [ERR-019](ERR-019.md#ERR-019) [ERR-021](ERR-021.md#ERR-021) [ERR-022](ERR-022.md#ERR-022) |
| [API-024](../02_backend/03_apis/API-024.md#API-024) | 招待メール再送 | SCR-014 EVT-04 | [ERR-013](ERR-013.md#ERR-013) [ERR-017](ERR-017.md#ERR-017) [ERR-019](ERR-019.md#ERR-019) [ERR-021](ERR-021.md#ERR-021) [ERR-022](ERR-022.md#ERR-022) |
| [API-070](../02_backend/03_apis/API-070.md#API-070) | ログイン失敗ロック解除 | SCR-014 EVT-10 | [ERR-017](ERR-017.md#ERR-017) [ERR-019](ERR-019.md#ERR-019) |
| [API-026](../02_backend/03_apis/API-026.md#API-026) | FAQ 作成・更新・削除 | SCR-008 EVT-10 SCR-009 EVT-03 SCR-009 EVT-04 SCR-009 EVT-06 | [ERR-001](ERR-001.md#ERR-001) [ERR-023](ERR-023.md#ERR-023) |
| [API-027](../02_backend/03_apis/API-027.md#API-027) | FAQ 一括状態変更 | SCR-008 EVT-08 SCR-008 EVT-09 | [ERR-001](ERR-001.md#ERR-001) [ERR-019](ERR-019.md#ERR-019) |
| [API-028](../02_backend/03_apis/API-028.md#API-028) | FAQ CSV インポート | SCR-010 EVT-04 | [ERR-024](ERR-024.md#ERR-024) [ERR-025](ERR-025.md#ERR-025) |
| [API-033](../02_backend/03_apis/API-033.md#API-033) | FAQ 個別取得 | SCR-009 EVT-01 | [ERR-017](ERR-017.md#ERR-017) [ERR-019](ERR-019.md#ERR-019) |
| [API-037](../02_backend/03_apis/API-037.md#API-037) | ウィジェット起動 | SCR-030 EVT-02 SCR-030 EVT-07 | [ERR-004](ERR-004.md#ERR-004) [ERR-026](ERR-026.md#ERR-026) [ERR-027](ERR-027.md#ERR-027) |
| [API-038](../02_backend/03_apis/API-038.md#API-038) | ウィジェット質問送信 | SCR-030 EVT-04 SCR-030 EVT-05 SCR-030 EVT-06 SCR-030 EVT-07 | [ERR-009](ERR-009.md#ERR-009) [ERR-027](ERR-027.md#ERR-027) [ERR-036](ERR-036.md#ERR-036) |
| [API-040](../02_backend/03_apis/API-040.md#API-040) | ダッシュボードサマリ | SCR-012 EVT-01 SCR-012 EVT-02 | [ERR-001](ERR-001.md#ERR-001) [ERR-019](ERR-019.md#ERR-019) |
| [API-045](../02_backend/03_apis/API-045.md#API-045) | 支払方法 取得・登録・更新 | SCR-028 EVT-02 SCR-028 EVT-06 | [ERR-013](ERR-013.md#ERR-013) [ERR-001](ERR-001.md#ERR-001) [ERR-028](ERR-028.md#ERR-028) |
| [API-047](../02_backend/03_apis/API-047.md#API-047) | プロジェクト上限・アラート更新 | SCR-027 EVT-05 | [ERR-013](ERR-013.md#ERR-013) [ERR-029](ERR-029.md#ERR-029) [ERR-030](ERR-030.md#ERR-030) |
| [API-050](../02_backend/03_apis/API-050.md#API-050) | お知らせ一括既読 | SCR-016 EVT-07 SCR-016 EVT-08 SCR-016 EVT-09 | [ERR-001](ERR-001.md#ERR-001) |
| [API-056](../02_backend/03_apis/API-056.md#API-056) | アカウント退会(即時) | SCR-019 EVT-03 | [ERR-013](ERR-013.md#ERR-013) [ERR-001](ERR-001.md#ERR-001) [ERR-023](ERR-023.md#ERR-023) |
| [API-059](../02_backend/03_apis/API-059.md#API-059) | 外部 Webhook(Resend) | — | [ERR-031](ERR-031.md#ERR-031) [ERR-032](ERR-032.md#ERR-032) |

## <span id="authz-map"></span>3. 認可ミドルウェア段コード ↔ ERR 対応

[権限設計 PERM-002](../04_permissions/PERM-002.md#PERM-002) の認可判定段で用いる taxonomy コードと、API レスポンスへ乗る ERR の対応です。横断的に全認証保護 API へ適用されるため、§2 の API 別表には個別計上しません。

| 認可段コード | 対応 ERR | HTTP | 備考 |
|----|----|----|----|
| `E-AUTH-SESSION-EXPIRED` | [ERR-033](ERR-033.md#ERR-033) | 401 | セッション期限切れ。全認証保護 API 共通 |
| `E-AUTH-REAUTH-REQUIRED` | [ERR-013](ERR-013.md#ERR-013) | 401 | 重要操作の再認証要求 |
| `E-AUTHZ-OWNER-BOUNDARY` | [ERR-017](ERR-017.md#ERR-017) | 404 | オーナー境界違反の 404 偽装 |
| `E-AUTHZ-PROJECT-DENIED` | [ERR-019](ERR-019.md#ERR-019) | 403 | 関係者(割当あり)だが当該操作の権限不足。割当なし・部外者は 404 偽装(段7・ERR-017)で本エラーは用いない |
| `E-AUTHZ-TERMS` | — | — | エラーではなくゲート。[SCR-020](../01_frontend/01_screens/SCR-020.md#SCR-020) 再同意へ誘導 |
