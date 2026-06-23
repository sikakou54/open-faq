# エラー設計

> **このページは、API レスポンスで返すエラーコードの一覧と、API からエラーへの対応表です。** 各エラーは HTTP ステータス・分類・メッセージ・対応 API を `ERR-NNN.md` で個別定義します。エラーの正本は各 ERR ファイル、認証・認可の判定段との対応は [権限設計](../04_permissions/index.md) を参照します。

*ステータス ドラフト*

## <span id="reading"></span>読み順

API設計 ＞ 本エラー設計 ＞ メッセージ設計。各 API の `## エラー` 表から本 ERR を参照する。

## <span id="list"></span>1. エラーコード一覧(36)

分類・HTTP ステータス・主エラーコードの索引です。各 ERR の定義は個別ファイルが正本です。

| ERR ID | 分類 | HTTP | エラーコード | 分類コード | メッセージ |
|----|----|----|----|----|----|
| <span id="ERR-001"></span>[ERR-001](ERR-001.md#ERR-001) | 入力検証 | 400 | `VALIDATION_ERROR` | — | 入力値の検証エラー |
| <span id="ERR-002"></span>[ERR-002](ERR-002.md#ERR-002) | 入力検証 | 400 | `TURNSTILE_FAILED` | — | Turnstile 検証失敗 |
| <span id="ERR-003"></span>[ERR-003](ERR-003.md#ERR-003) | 認証 | 401 | `INVALID_CREDENTIALS` | `E-AUTH-CREDENTIAL` | 認証情報が不正 |
| <span id="ERR-004"></span>[ERR-004](ERR-004.md#ERR-004) | 認証 | 423 | `LOCKED_OUT` | `E-AUTH-LOCKED` | アカウントロック中 |
| <span id="ERR-005"></span>[ERR-005](ERR-005.md#ERR-005) | 入力検証 | 400 | `TURNSTILE_REQUIRED` | — | Turnstile が必要 |
| <span id="ERR-006"></span>[ERR-006](ERR-006.md#ERR-006) | 業務(課金) | 403 | `CONTRACT_SUSPENDED` | `E-BILL-CONTRACT-SUSPENDED` | 契約停止中 |
| <span id="ERR-007"></span>[ERR-007](ERR-007.md#ERR-007) | 認証 | 401 | `INVALID_PASSWORD` | — | パスワードが不正 |
| <span id="ERR-008"></span>[ERR-008](ERR-008.md#ERR-008) | 認証 | 410 | `TOKEN_EXPIRED` | `E-AUTH-TOKEN-EXPIRED` | トークン期限切れ |
| <span id="ERR-009"></span>[ERR-009](ERR-009.md#ERR-009) | 認証 | 410 | `TOKEN_USED` | `E-AUTH-TOKEN-USED` | トークン使用済み |
| <span id="ERR-010"></span>[ERR-010](ERR-010.md#ERR-010) | 認証 | 404 | `TOKEN_NOT_FOUND` | — | トークンが存在しない |
| <span id="ERR-011"></span>[ERR-011](ERR-011.md#ERR-011) | 認証 | 429 | `RATE_LIMITED` | `E-AUTH-RATE-LIMITED` | レート制限超過(再送間隔未到達) |
| <span id="ERR-012"></span>[ERR-012](ERR-012.md#ERR-012) | 入力検証 | 409 | `ALREADY_VERIFIED` | — | 連絡先メールが既に確認済み |
| <span id="ERR-013"></span>[ERR-013](ERR-013.md#ERR-013) | 業務 | 404 | `PROJECT_NOT_FOUND` | — | 対象プロジェクトが存在しない |
| <span id="ERR-014"></span>[ERR-014](ERR-014.md#ERR-014) | 入力検証 | 400 | `CONTACT_EMAIL_NOT_SET` | — | 連絡先メールが未設定 |
| <span id="ERR-015"></span>[ERR-015](ERR-015.md#ERR-015) | 認証 | 401 | `REAUTH_REQUIRED` | `E-AUTH-REAUTH-REQUIRED` | 再認証トークンが無効または未提示 |
| <span id="ERR-016"></span>[ERR-016](ERR-016.md#ERR-016) | 入力検証 | 409 | `EMAIL_ALREADY_USED` | — | 入力メールアドレスが既に使用中 |
| <span id="ERR-017"></span>[ERR-017](ERR-017.md#ERR-017) | 認可 | 403 | `E-AUTHZ-OWNER-ONLY` | `E-AUTHZ-OWNER-ONLY` | オーナー以外は不可 |
| <span id="ERR-018"></span>[ERR-018](ERR-018.md#ERR-018) | 入力検証 | 409 | `DUPLICATE_NAME` | — | プロジェクト名重複 |
| <span id="ERR-019"></span>[ERR-019](ERR-019.md#ERR-019) | 認可 | 404 | `NOT_FOUND` | `E-AUTHZ-OWNER-BOUNDARY` | オーナー境界違反偽装 |
| <span id="ERR-020"></span>[ERR-020](ERR-020.md#ERR-020) | 入力検証 | 409 | `ALREADY_EXISTS_IN_PROJECT` | — | 既に該当プロジェクトに割当あり |
| <span id="ERR-021"></span>[ERR-021](ERR-021.md#ERR-021) | 認可 | 403 | `PROJECT_ACCESS_DENIED` | `E-AUTHZ-PROJECT-DENIED` | 当該プロジェクトへの権限なし |
| <span id="ERR-022"></span>[ERR-022](ERR-022.md#ERR-022) | 入力検証 | 409 | `EMAIL_ALREADY_EXISTS` | — | メールアドレスの重複 |
| <span id="ERR-023"></span>[ERR-023](ERR-023.md#ERR-023) | 認可 | 403 | `E-AUTHZ-OWNER-PROTECTED` | `E-AUTHZ-OWNER-PROTECTED` | オーナーは解除不可 |
| <span id="ERR-024"></span>[ERR-024](ERR-024.md#ERR-024) | 認可 | 403 | `E-AUTHZ-SELF-MUTATION` | `E-AUTHZ-SELF-MUTATION` | 自分自身は解除不可 |
| <span id="ERR-025"></span>[ERR-025](ERR-025.md#ERR-025) | 入力検証 | 409 | `CONFLICT` | — | 楽観ロック競合(`version` 不一致) |
| <span id="ERR-026"></span>[ERR-026](ERR-026.md#ERR-026) | 入力検証 | 415 / 400 | `E-INPUT-CSV-INVALID` | `E-INPUT-CSV-INVALID` | CSV 以外 / 不正形式 |
| <span id="ERR-027"></span>[ERR-027](ERR-027.md#ERR-027) | 入力検証 | (行単位) | `E-INPUT-CSV-FAQID-NOTFOUND` | `E-INPUT-CSV-FAQID-NOTFOUND` | 当該契約に存在しない FAQ ID |
| <span id="ERR-028"></span>[ERR-028](ERR-028.md#ERR-028) | 認証 | 401 | `WIDGET_KEY_INVALID` | — | 公開キーが不正 |
| <span id="ERR-029"></span>[ERR-029](ERR-029.md#ERR-029) | 認可 | 403 | `DOMAIN_NOT_ALLOWED` | — | 許可ドメイン外 |
| <span id="ERR-030"></span>[ERR-030](ERR-030.md#ERR-030) | 業務(課金) | 402 | `PAYMENT_METHOD_DECLINED` | `E-BILL-PAYMENT-FAILED` | カードが拒否された |
| <span id="ERR-031"></span>[ERR-031](ERR-031.md#ERR-031) | 業務 | 422 | (未サポート項目) | — | `freeQuota` / `alertEnabled` / `alertFrequency` を指定 |
| <span id="ERR-032"></span>[ERR-032](ERR-032.md#ERR-032) | 認可 | 403 | `E-AUTHZ-FORBIDDEN` | `E-AUTHZ-FORBIDDEN` | 当該プロジェクトに割当のないユーザー |
| <span id="ERR-033"></span>[ERR-033](ERR-033.md#ERR-033) | 認可 | 403 | `PERMISSION_DENIED` | — | メンバーは申請不可 |
| <span id="ERR-034"></span>[ERR-034](ERR-034.md#ERR-034) | 認証 | 401 | `SIGNATURE_INVALID` | — | 署名検証失敗 |
| <span id="ERR-035"></span>[ERR-035](ERR-035.md#ERR-035) | 業務 | 200 | (冪等) | — | 既存処理結果を返却(冪等性違反) |
| <span id="ERR-036"></span>[ERR-036](ERR-036.md#ERR-036) | 認証 | 401 | `SESSION_EXPIRED` | `E-AUTH-SESSION-EXPIRED` | セッション期限切れ(再ログインへ) |

## <span id="trace"></span>2. API ↔ エラー 対応表

各 API が返しうるエラーの結線一覧です。

| API ID | API名 | 返しうるエラー |
|----|----|----|
| [API-001](../02_backend/03_apis/API-001.md#API-001) | 新規登録 | [ERR-001](ERR-001.md#ERR-001) [ERR-002](ERR-002.md#ERR-002) |
| [API-002](../02_backend/03_apis/API-002.md#API-002) | ログイン | [ERR-003](ERR-003.md#ERR-003) [ERR-004](ERR-004.md#ERR-004) [ERR-005](ERR-005.md#ERR-005) [ERR-006](ERR-006.md#ERR-006) |
| [API-005](../02_backend/03_apis/API-005.md#API-005) | 再認証 | [ERR-007](ERR-007.md#ERR-007) |
| [API-006](../02_backend/03_apis/API-006.md#API-006) | メール確認 | [ERR-008](ERR-008.md#ERR-008) |
| [API-007](../02_backend/03_apis/API-007.md#API-007) | 招待トークン検証・プレビュー | [ERR-008](ERR-008.md#ERR-008) [ERR-009](ERR-009.md#ERR-009) [ERR-010](ERR-010.md#ERR-010) |
| [API-008](../02_backend/03_apis/API-008.md#API-008) | メンバーアカウント有効化 | [ERR-001](ERR-001.md#ERR-001) [ERR-002](ERR-002.md#ERR-002) [ERR-008](ERR-008.md#ERR-008) [ERR-009](ERR-009.md#ERR-009) |
| [API-009](../02_backend/03_apis/API-009.md#API-009) | プロジェクト連絡先メール確認 | [ERR-008](ERR-008.md#ERR-008) [ERR-009](ERR-009.md#ERR-009) [ERR-010](ERR-010.md#ERR-010) |
| [API-010](../02_backend/03_apis/API-010.md#API-010) | パスワード再設定確定 | [ERR-001](ERR-001.md#ERR-001) [ERR-008](ERR-008.md#ERR-008) [ERR-009](ERR-009.md#ERR-009) [ERR-010](ERR-010.md#ERR-010) |
| [API-011](../02_backend/03_apis/API-011.md#API-011) | 連絡先確認メール再送 | [ERR-011](ERR-011.md#ERR-011) [ERR-012](ERR-012.md#ERR-012) [ERR-013](ERR-013.md#ERR-013) [ERR-014](ERR-014.md#ERR-014) |
| [API-012](../02_backend/03_apis/API-012.md#API-012) | 自己プロフィール更新 | [ERR-001](ERR-001.md#ERR-001) [ERR-015](ERR-015.md#ERR-015) [ERR-016](ERR-016.md#ERR-016) |
| [API-013](../02_backend/03_apis/API-013.md#API-013) | 自己パスワード変更 | [ERR-001](ERR-001.md#ERR-001) [ERR-015](ERR-015.md#ERR-015) |
| [API-014](../02_backend/03_apis/API-014.md#API-014) | 契約設定取得 | [ERR-017](ERR-017.md#ERR-017) |
| [API-015](../02_backend/03_apis/API-015.md#API-015) | 契約設定更新 | [ERR-001](ERR-001.md#ERR-001) [ERR-017](ERR-017.md#ERR-017) |
| [API-017](../02_backend/03_apis/API-017.md#API-017) | プロジェクト新規作成 | [ERR-001](ERR-001.md#ERR-001) [ERR-017](ERR-017.md#ERR-017) [ERR-018](ERR-018.md#ERR-018) |
| [API-018](../02_backend/03_apis/API-018.md#API-018) | プロジェクト更新・削除 | [ERR-017](ERR-017.md#ERR-017) [ERR-019](ERR-019.md#ERR-019) |
| [API-021](../02_backend/03_apis/API-021.md#API-021) | メンバー招待 | [ERR-001](ERR-001.md#ERR-001) [ERR-020](ERR-020.md#ERR-020) [ERR-021](ERR-021.md#ERR-021) |
| [API-022](../02_backend/03_apis/API-022.md#API-022) | メンバー情報更新 | [ERR-001](ERR-001.md#ERR-001) [ERR-019](ERR-019.md#ERR-019) [ERR-021](ERR-021.md#ERR-021) [ERR-022](ERR-022.md#ERR-022) |
| [API-023](../02_backend/03_apis/API-023.md#API-023) | プロジェクト割当解除 | [ERR-019](ERR-019.md#ERR-019) [ERR-021](ERR-021.md#ERR-021) [ERR-023](ERR-023.md#ERR-023) [ERR-024](ERR-024.md#ERR-024) |
| [API-024](../02_backend/03_apis/API-024.md#API-024) | 招待メール再送 | [ERR-019](ERR-019.md#ERR-019) [ERR-023](ERR-023.md#ERR-023) [ERR-024](ERR-024.md#ERR-024) |
| [API-026](../02_backend/03_apis/API-026.md#API-026) | FAQ 作成・更新・削除 | [ERR-001](ERR-001.md#ERR-001) [ERR-025](ERR-025.md#ERR-025) |
| [API-027](../02_backend/03_apis/API-027.md#API-027) | FAQ 一括状態変更 | [ERR-001](ERR-001.md#ERR-001) [ERR-021](ERR-021.md#ERR-021) |
| [API-028](../02_backend/03_apis/API-028.md#API-028) | FAQ CSV インポート | [ERR-026](ERR-026.md#ERR-026) [ERR-027](ERR-027.md#ERR-027) |
| [API-033](../02_backend/03_apis/API-033.md#API-033) | FAQ 個別取得 | [ERR-019](ERR-019.md#ERR-019) [ERR-021](ERR-021.md#ERR-021) |
| [API-037](../02_backend/03_apis/API-037.md#API-037) | ウィジェット起動 | [ERR-006](ERR-006.md#ERR-006) [ERR-028](ERR-028.md#ERR-028) [ERR-029](ERR-029.md#ERR-029) |
| [API-038](../02_backend/03_apis/API-038.md#API-038) | ウィジェット質問送信 | [ERR-011](ERR-011.md#ERR-011) [ERR-029](ERR-029.md#ERR-029) |
| [API-040](../02_backend/03_apis/API-040.md#API-040) | ダッシュボードサマリ | [ERR-001](ERR-001.md#ERR-001) [ERR-021](ERR-021.md#ERR-021) |
| [API-045](../02_backend/03_apis/API-045.md#API-045) | 支払方法 取得・登録・更新 | [ERR-001](ERR-001.md#ERR-001) [ERR-017](ERR-017.md#ERR-017) [ERR-030](ERR-030.md#ERR-030) |
| [API-047](../02_backend/03_apis/API-047.md#API-047) | プロジェクト上限・アラート更新 | [ERR-031](ERR-031.md#ERR-031) [ERR-032](ERR-032.md#ERR-032) |
| [API-050](../02_backend/03_apis/API-050.md#API-050) | お知らせ一括既読 | [ERR-001](ERR-001.md#ERR-001) |
| [API-056](../02_backend/03_apis/API-056.md#API-056) | 退会申請 | [ERR-033](ERR-033.md#ERR-033) |
| [API-059](../02_backend/03_apis/API-059.md#API-059) | 外部 Webhook(Resend) | [ERR-034](ERR-034.md#ERR-034) [ERR-035](ERR-035.md#ERR-035) |

## <span id="authz-map"></span>3. 認可ミドルウェア段コード ↔ ERR 対応

[権限設計 PERM-002](../04_permissions/PERM-002.md#PERM-002) の認可判定段で用いる taxonomy コードと、API レスポンスへ乗る ERR の対応です。横断的に全認証保護 API へ適用されるため、§2 の API 別表には個別計上しません。

| 認可段コード | 対応 ERR | HTTP | 備考 |
|----|----|----|----|
| `E-AUTH-SESSION-EXPIRED` | [ERR-036](ERR-036.md#ERR-036) | 401 | セッション期限切れ。全認証保護 API 共通 |
| `E-AUTH-REAUTH-REQUIRED` | [ERR-015](ERR-015.md#ERR-015) | 401 | 重要操作の再認証要求 |
| `E-AUTHZ-OWNER-BOUNDARY` | [ERR-019](ERR-019.md#ERR-019) | 404 | オーナー境界違反の 404 偽装 |
| `E-AUTHZ-PROJECT-DENIED` | [ERR-021](ERR-021.md#ERR-021) | 403 | プロジェクト割当なし |
| `E-AUTHZ-TERMS` | — | — | エラーではなくゲート。[SCR-020](../01_frontend/01_screens/SCR-020.md#SCR-020) 再同意へ誘導 |
