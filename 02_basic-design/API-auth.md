<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [API設計](02_api-design.md) ／ **認証 API**
<!-- /portal-top -->

# 認証 API

> **このページは、オーナー / メンバーの登録・ログイン・再認証・メール確認など認証系 API の契約を定義します。**
>
> **このページの API**
>
> - API-AUTH-001 新規登録
> - API-AUTH-002 ログイン
> - API-AUTH-003 ログアウト
> - API-AUTH-004 パスワード再設定要求
> - API-AUTH-005 再認証
> - API-AUTH-006 メール確認
> - API-AUTH-007 招待トークン検証・プレビュー
> - API-AUTH-008 メンバーアカウント有効化
> - API-AUTH-009 プロジェクト連絡先メール確認
> - API-AUTH-010 パスワード再設定確定
> - API-AUTH-011 連絡先確認メール再送

*版数 v1.7 ・ 更新 2026-06-20 ・ 承認済*

## <span id="API-AUTH-001"></span>API-AUTH-001 新規登録

<span id="511-post-authsignup"></span>

### 基本情報

| 項目           | 内容           |
|----------------|----------------|
| API ID         | API-AUTH-001   |
| API 名         | 新規登録       |
| エンドポイント | `/auth/signup` |
| HTTP メソッド  | POST           |
| 認証           | 不要           |
| 権限           | —(公開)        |

### 処理概要

オーナーアカウントを新規登録し、メール確認を要求する。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | Turnstile トークンを検証する |
| P-02 | 入力値(メール形式・パスワード強度・パスワード一致・規約 / プライバシー同意)を検証する |
| P-03 | `M_USER`(オーナー本体)と `M_CONTRACT` を作成する |
| P-04 | 利用規約・プライバシーポリシーへの同意を記録する |
| P-05 | メール確認トークンを発行し確認メールを送信する |
| P-06 | 受付結果を返す |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `M_USER`          | ◯   | —   | —   | —   |
| `M_CONTRACT`      | ◯   | ◯   | —   | —   |
| `T_TERMS_AGREE`   | ◯   | —   | —   | —   |
| `T_ACCESS_TOKENS` | ◯   | —   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{}
```

#### Request Body

```json
{
  "email": "admin@example.com",
  "password": "P@ssw0rd123!",
  "passwordConfirm": "P@ssw0rd123!",
  "agreedTerms": true,
  "agreedPrivacy": true,
  "turnstileToken": "..."
}
```

| 項目              | 型      | 説明                                       |
|-------------------|---------|--------------------------------------------|
| `email`           | string  | 登録するメールアドレス(必須)               |
| `password`        | string  | 初回パスワード(必須)                       |
| `passwordConfirm` | string  | パスワード確認用(必須・`password` と一致)  |
| `agreedTerms`     | boolean | 利用規約への同意(必須・`true`)             |
| `agreedPrivacy`   | boolean | プライバシーポリシーへの同意(必須・`true`) |
| `turnstileToken`  | string  | Turnstile 検証トークン(必須)               |

### レスポンス(202)

```json
{ "ok": true }
```

| 項目 | 型      | 説明                                                  |
|------|---------|-------------------------------------------------------|
| `ok` | boolean | 登録受付の成否(確認メール送信を受け付けた場合 `true`) |

### エラー

| HTTP ステータス | エラーコード                   | 内容               |
|-----------------|--------------------------------|--------------------|
| 400             | `VALIDATION_ERROR`(E-INPUT-\*) | 入力値の検証エラー |
| 400             | `TURNSTILE_FAILED`             | Turnstile 検証失敗 |

## <span id="API-AUTH-002"></span>API-AUTH-002 ログイン

<span id="512-post-authlogin"></span>

### 基本情報

| 項目           | 内容          |
|----------------|---------------|
| API ID         | API-AUTH-002  |
| API 名         | ログイン      |
| エンドポイント | `/auth/login` |
| HTTP メソッド  | POST          |
| 認証           | 不要          |
| 権限           | —(公開)       |

### 処理概要

メール / パスワードを認証しセッションを発行する。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 連続失敗時は Turnstile を要求し、提示があれば検証する |
| P-02 | メール / パスワードの資格情報を照合する(不一致は失敗試行として計上) |
| P-03 | アカウントロック状態・契約停止状態を判定する |
| P-04 | セッションを発行し、再規約同意要否と有効セッション一覧を返す |

### I/O

| テーブル      | C   | R   | U   | D   |
|---------------|-----|-----|-----|-----|
| `M_CONTRACT`  | —   | ◯   | ◯   | —   |
| `M_PRJ_USERS` | —   | ◯   | ◯   | —   |
| `T_SESSIONS`  | ◯   | —   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{}
```

#### Request Body

```json
{
  "email": "admin@example.com",
  "password": "...",
  "turnstileToken": "..."
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `email` | string | ログインするメールアドレス(必須) |
| `password` | string | パスワード(必須) |
| `turnstileToken` | string | Turnstile 検証トークン(連続失敗時に要求される場合に必須) |

### レスポンス(200)

```json
{
  "userId": "01HZ...",
  "actorType": "owner",
  "requireTermsAgreement": false,
  "activeSessions": [
    { "id": "...", "ipAddress": "203.0.113.x", "createdAt": "..." }
  ]
}
```

| 項目                    | 型                | 説明                           |
|-------------------------|-------------------|--------------------------------|
| `userId`                | string            | 認証された利用者の ID          |
| `actorType`             | enum              | 利用者の種別(`owner` = オーナー / `project_user` = メンバー) |
| `requireTermsAgreement` | boolean           | 再規約同意が必要かどうか       |
| `activeSessions`        | array\<object\>   | 現在有効なセッションの一覧     |
| `　└ id`                | string            | セッション ID                  |
| `　└ ipAddress`         | string            | セッション発行元の IP アドレス |
| `　└ createdAt`         | string (ISO 8601) | セッション作成日時             |

### エラー

| HTTP ステータス | エラーコード | 内容 |
|----|----|----|
| 401 | `INVALID_CREDENTIALS`(E-AUTH-CREDENTIAL) | 認証情報が不正 |
| 423 | `LOCKED_OUT`(E-AUTH-LOCKED) | アカウントロック中 |
| 400 | `TURNSTILE_REQUIRED` | Turnstile が必要 |
| 403 | `CONTRACT_SUSPENDED`(E-BILL-CONTRACT-SUSPENDED) | 契約停止中 |

## <span id="API-AUTH-003"></span>API-AUTH-003 ログアウト

### 基本情報

| 項目           | 内容           |
|----------------|----------------|
| API ID         | API-AUTH-003   |
| API 名         | ログアウト     |
| エンドポイント | `/auth/logout` |
| HTTP メソッド  | POST           |
| 認証           | Cookie + CSRF  |
| 権限           | 認証済み       |

### 処理概要

現在のセッションを失効する。

| 処理 ID | 処理内容                                     |
|---------|----------------------------------------------|
| P-01    | セッション Cookie と CSRF トークンを検証する |
| P-02    | 現在のセッションを失効する                   |
| P-03    | 完了結果を返す                               |

### I/O

| テーブル     | C   | R   | U   | D   |
|--------------|-----|-----|-----|-----|
| `T_SESSIONS` | —   | —   | ◯   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{}
```

#### Request Body

```json
{}
```

### レスポンス(200)

```json
{ "ok": true }
```

| 項目 | 型      | 説明                 |
|------|---------|----------------------|
| `ok` | boolean | セッション失効の成否 |

### エラー

想定エラーは本 API のエラー節を参照する(本 API 固有のエラーコードなし)。

## <span id="API-AUTH-004"></span>API-AUTH-004 パスワード再設定要求

<span id="514-post-authpassword-reset-request"></span>

### 基本情報

| 項目           | 内容                           |
|----------------|--------------------------------|
| API ID         | API-AUTH-004                   |
| API 名         | パスワード再設定要求           |
| エンドポイント | `/auth/password-reset-request` |
| HTTP メソッド  | POST                           |
| 認証           | 不要                           |
| 権限           | —(公開)                        |

### 処理概要

再設定メールの送信を要求する。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | Turnstile トークンを検証する |
| P-02 | 該当アカウントが存在する場合のみ再設定トークンを発行し再設定メールを送信する |
| P-03 | アカウントの存在有無を漏らさず一律の受付結果を返す |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `M_CONTRACT`      | —   | ◯   | —   | —   |
| `M_PRJ_USERS`     | —   | ◯   | —   | —   |
| `T_ACCESS_TOKENS` | ◯   | —   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{}
```

#### Request Body

```json
{ "email": "admin@example.com", "turnstileToken": "..." }
```

| 項目             | 型     | 説明                                     |
|------------------|--------|------------------------------------------|
| `email`          | string | 再設定メールの送信先メールアドレス(必須) |
| `turnstileToken` | string | Turnstile 検証トークン(必須)             |

### レスポンス(202)

```json
{ "ok": true }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `ok` | boolean | 再設定要求の受付成否(アカウントの存在有無に関わらず一律 `true`) |

> [!NOTE]
> **補足** 列挙攻撃対策として、アカウントの存在有無は応答に含めない。

## <span id="API-AUTH-005"></span>API-AUTH-005 再認証

<span id="515-post-authre-auth"></span>

### 基本情報

| 項目           | 内容            |
|----------------|-----------------|
| API ID         | API-AUTH-005    |
| API 名         | 再認証          |
| エンドポイント | `/auth/re-auth` |
| HTTP メソッド  | POST            |
| 認証           | 要(Cookie)      |
| 権限           | 認証済み        |

### 処理概要

機微操作の前にパスワードを再確認する。

| 処理 ID | 処理内容                                   |
|---------|--------------------------------------------|
| P-01    | セッションから認証済み利用者を特定する     |
| P-02    | パスワードを再照合する(不一致は 401)       |
| P-03    | 機微操作に使う再認証トークンを発行して返す |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `M_CONTRACT`      | —   | ◯   | —   | —   |
| `M_PRJ_USERS`     | —   | ◯   | —   | —   |
| `T_ACCESS_TOKENS` | ◯   | —   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{}
```

#### Request Body

```json
{ "password": "..." }
```

| 項目       | 型     | 説明                       |
|------------|--------|----------------------------|
| `password` | string | 再確認するパスワード(必須) |

### レスポンス(200)

```json
{ "ok": true, "token": "reauth_..." }
```

| 項目    | 型      | 説明                         |
|---------|---------|------------------------------|
| `ok`    | boolean | 再認証の成否                 |
| `token` | string  | 機微操作に使う再認証トークン |

### エラー

| HTTP ステータス | エラーコード       | 内容             |
|-----------------|--------------------|------------------|
| 401             | `INVALID_PASSWORD` | パスワードが不正 |

## <span id="API-AUTH-006"></span>API-AUTH-006 メール確認

<span id="516-post-authemail-verificationstoken"></span>

### 基本情報

| 項目           | 内容                                |
|----------------|-------------------------------------|
| API ID         | API-AUTH-006                        |
| API 名         | メール確認                          |
| エンドポイント | `/auth/email-verifications/{token}` |
| HTTP メソッド  | POST                                |
| 認証           | トークン認証                        |
| 権限           | —                                   |

トークン形式 = `email_verify` purpose の `T_ACCESS_TOKENS.token_hash` 検証。

### 処理概要

登録メールアドレスを確認する。

| 処理 ID | 処理内容                                       |
|---------|------------------------------------------------|
| P-01    | メール確認トークンの有効性(期限)を検証する     |
| P-02    | 対象アカウントのメールアドレスを確認済みにする |
| P-03    | 確認トークンを使用済みにする                   |
| P-04    | 確認結果を返す                                 |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `T_ACCESS_TOKENS` | —   | ◯   | ◯   | —   |
| `M_CONTRACT`      | —   | —   | ◯   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{ "token": "メール確認トークン" }
```

| 項目    | 型     | 説明                                     |
|---------|--------|------------------------------------------|
| `token` | string | メール確認トークン(必須・パス末尾で指定) |

#### Request Body

```json
{}
```

### レスポンス(200)

```json
{ "userId": "...", "verifiedAt": "..." }
```

| 項目         | 型                | 説明                               |
|--------------|-------------------|------------------------------------|
| `userId`     | string            | メール確認の対象アカウント ID      |
| `verifiedAt` | string (ISO 8601) | メールアドレスを確認済みとした日時 |

### エラー

| HTTP ステータス | エラーコード                          | 内容             |
|-----------------|---------------------------------------|------------------|
| 410             | `TOKEN_EXPIRED`(E-AUTH-TOKEN-EXPIRED) | トークン期限切れ |

## <span id="API-AUTH-007"></span>API-AUTH-007 招待トークン検証・プレビュー

<span id="517-post-authinvitationstokenpreview"></span>

### 基本情報

| 項目           | 内容                                  |
|----------------|---------------------------------------|
| API ID         | API-AUTH-007                          |
| API 名         | 招待トークン検証 + 招待情報プレビュー |
| エンドポイント | `/auth/invitations/{token}/preview`   |
| HTTP メソッド  | POST                                  |
| 認証           | 未認証可(トークン認証のみ)            |
| 権限           | —                                     |

トークン形式 = `activation` purpose の `T_ACCESS_TOKENS.token_hash` 検証。検証成功時は招待情報を返し、SCR-018 の招待情報パネル表示に使用する。Turnstile 不要(プレビューは情報取得のみで状態変更なし)。

### 処理概要

招待情報(プロジェクト名 / 招待元オーナー名 / 招待者メール)をプレビュー取得する。

| 処理 ID | 処理内容                                                         |
|---------|------------------------------------------------------------------|
| P-01    | 招待トークンの存在・有効性(期限・使用済み)を検証する             |
| P-02    | トークンから招待先プロジェクト・招待元情報を取得する |
| P-03    | 状態変更を行わず招待情報のプレビューを返す                       |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `T_ACCESS_TOKENS` | —   | ◯   | —   | —   |
| `M_PROJECTS`      | —   | ◯   | —   | —   |
| `M_PRJ_USERS`     | —   | ◯   | —   | —   |
| `M_PRJ_USERS`     | —   | ◯   | —   | —   |
| `M_CONTRACT`      | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{ "token": "招待トークン" }
```

| 項目    | 型     | 説明                             |
|---------|--------|----------------------------------|
| `token` | string | 招待トークン(必須・パス内で指定) |

#### Request Body

```json
{}
```

### レスポンス(200)

```json
{
  "userId": "01HZ...",
  "email": "newmember@...",
  "projectId": "proj_1",
  "projectName": "顧客サポート",
  "inviterOwnerName": "山田 一郎",
  "expiresAt": "2026-05-28T..."
}
```

| 項目               | 型                | 説明                                 |
|--------------------|-------------------|--------------------------------------|
| `userId`           | string            | 招待された利用者の ID                |
| `email`            | string            | 招待先メールアドレス                 |
| `projectId`        | string            | 招待先プロジェクトの ID              |
| `projectName`      | string            | 招待先プロジェクトの名称             |
| `inviterOwnerName` | string            | 招待元オーナーの氏名                 |
| `expiresAt`        | string (ISO 8601) | 招待トークンの有効期限               |

### エラー

| HTTP ステータス | エラーコード                          | 内容                 |
|-----------------|---------------------------------------|----------------------|
| 410             | `TOKEN_EXPIRED`(E-AUTH-TOKEN-EXPIRED) | トークン期限切れ     |
| 410             | `TOKEN_USED`(E-AUTH-TOKEN-USED)       | トークン使用済み     |
| 404             | `TOKEN_NOT_FOUND`                     | トークンが存在しない |

## <span id="API-AUTH-008"></span>API-AUTH-008 メンバーアカウント有効化

<span id="518-post-authinvitationstokenactivate"></span>

### 基本情報

| 項目           | 内容                                       |
|----------------|--------------------------------------------|
| API ID         | API-AUTH-008                               |
| API 名         | メンバーアカウント有効化                   |
| エンドポイント | `/auth/invitations/{token}/activate`       |
| HTTP メソッド  | POST                                       |
| 認証           | 未認証可(トークン認証のみ、Turnstile 必須) |
| 権限           | —                                          |

### 処理概要

招待されたメンバー本人が氏名・初回パスワード・規約同意を登録し有効化を完了する。本処理は 1 つのトランザクションで実行する。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 招待トークンの有効性(期限・使用済み)を検証する |
| P-02 | トークンから招待先プロジェクトを取得する |
| P-03 | 予約 `M_USER` 行に氏名・パスワードを設定し `status='active'` とする(アカウント有効化) |
| P-04 | 利用規約・プライバシーポリシーの最新版への同意を記録する(各文書種別に 1 件) |
| P-05 | 対象プロジェクトへの割当を有効化する |
| P-06 | 招待トークンを使用済みにする |
| P-07 | 監査ログ(アカウント有効化完了)を記録する |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `T_ACCESS_TOKENS` | —   | ◯   | ◯   | —   |
| `M_USER`          | —   | —   | ◯   | —   |
| `M_PRJ_USERS`     | —   | —   | ◯   | —   |
| `M_PRJ_USERS`     | —   | —   | ◯   | —   |
| `T_TERMS_AGREE`   | ◯   | —   | —   | —   |
| `H_AUDIT_LOGS`    | ◯   | —   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{ "token": "招待トークン" }
```

| 項目    | 型     | 説明                             |
|---------|--------|----------------------------------|
| `token` | string | 招待トークン(必須・パス内で指定) |

#### Request Body

```json
{
  "displayName": "山田 太郎",
  "password": "P@ssw0rd-strong",
  "passwordConfirm": "P@ssw0rd-strong",
  "termsAgreed": true,
  "privacyAgreed": true,
  "turnstileToken": "..."
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `displayName` | string | 本人の表示氏名(必須・1〜100 文字、前後空白トリム) |
| `password` | string | 初回パスワード(必須・12 文字以上、英大文字 / 小文字 / 数字 / 記号のうち 3 種類以上) |
| `passwordConfirm` | string | パスワード確認用(必須・`password` と一致) |
| `termsAgreed` | boolean | 利用規約への同意(必須・`true`) |
| `privacyAgreed` | boolean | プライバシーポリシーへの同意(必須・`true`) |
| `turnstileToken` | string | Turnstile 検証トークン(必須) |

バリデーション:

- `displayName`: 必須、1〜100 文字(前後空白トリム)
- `password`: 12 文字以上、英大文字 / 小文字 / 数字 / 記号のうち 3 種類以上(FR-006)
- `passwordConfirm`: `password` と一致
- `termsAgreed` / `privacyAgreed`: 両方 `true` 必須(FR-099 / FR-101)
- `turnstileToken`: 検証成功(FR-111)

### レスポンス(200)

```json
{ "userId": "01HZ...", "redirectUrl": "/auth/login" }
```

| 項目          | 型     | 説明                                   |
|---------------|--------|----------------------------------------|
| `userId`      | string | 有効化が完了した利用者の ID            |
| `redirectUrl` | string | 有効化完了後の遷移先 URL(ログイン画面) |

### エラー

| HTTP ステータス | エラーコード | 内容 |
|----|----|----|
| 410 | `TOKEN_EXPIRED`(E-AUTH-TOKEN-EXPIRED) | トークン期限切れ |
| 410 | `TOKEN_USED`(E-AUTH-TOKEN-USED) | トークン使用済み |
| 400 | `VALIDATION_ERROR` | 氏名長 / パスワード強度 / 規約同意未チェック |
| 400 | `TURNSTILE_FAILED` | Turnstile 検証失敗 |

## <span id="API-AUTH-009"></span>API-AUTH-009 プロジェクト連絡先メール確認

<span id="519-post-authcontact-verificationstoken"></span>

### 基本情報

| 項目           | 内容                                               |
|----------------|----------------------------------------------------|
| API ID         | API-AUTH-009                                       |
| API 名         | プロジェクト連絡先メール確認(プロジェクト管理派生) |
| エンドポイント | `/auth/contact-verifications/{token}`              |
| HTTP メソッド  | POST                                               |
| 認証           | 未認証可(トークン認証のみ、Turnstile 不要)         |
| 権限           | —                                                  |

Turnstile は不要(入力フォームを持たない単純な確認専用エンドポイントで、トークン HMAC-SHA256 検証 + IP / トークン単位のレート制限で十分)。

### 処理概要

プロジェクト連絡先メールを確認済みとし `M_PROJECTS.contact_verified_at` をセットする。本処理は 1 つのトランザクションで実行する。

| 処理 ID | 処理内容                                       |
|---------|------------------------------------------------|
| P-01    | 確認トークンの有効性(期限・使用済み)を検証する |
| P-02    | トークンから対象プロジェクトを取得する         |
| P-03    | プロジェクトの連絡先メールを確認済みにする     |
| P-04    | 確認トークンを使用済みにする                   |
| P-05    | 監査ログ(連絡先メール確認)を記録する           |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `T_ACCESS_TOKENS` | —   | ◯   | ◯   | —   |
| `M_PROJECTS`      | —   | ◯   | ◯   | —   |
| `H_AUDIT_LOGS`    | ◯   | —   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{ "token": "連絡先確認トークン" }
```

| 項目    | 型     | 説明                                   |
|---------|--------|----------------------------------------|
| `token` | string | 連絡先確認トークン(必須・パス内で指定) |

#### Request Body

```json
{}
```

### レスポンス(200)

```json
{ "projectId": "proj_1", "projectName": "サポートサイト", "verifiedAt": "2026-05-21T..." }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `projectId` | string | 連絡先メールを確認した対象プロジェクトの ID |
| `projectName` | string | 対象プロジェクトの名称 |
| `verifiedAt` | string (ISO 8601) | 連絡先メールを確認済みとした日時 |

### エラー

| HTTP ステータス | エラーコード                          | 内容                 |
|-----------------|---------------------------------------|----------------------|
| 410             | `TOKEN_EXPIRED`(E-AUTH-TOKEN-EXPIRED) | トークン期限切れ     |
| 410             | `TOKEN_USED`(E-AUTH-TOKEN-USED)       | トークン使用済み     |
| 404             | `TOKEN_NOT_FOUND`                     | トークンが存在しない |

## <span id="API-AUTH-010"></span>API-AUTH-010 パスワード再設定確定

### 基本情報

| 項目           | 内容                        |
|----------------|-----------------------------|
| API ID         | API-AUTH-010                |
| API 名         | パスワード再設定確定        |
| エンドポイント | `/auth/password-reset`      |
| HTTP メソッド  | POST                        |
| 認証           | 不要(トークン認証)          |
| 権限           | —(公開)                     |

### 処理概要

再設定トークンと新しいパスワードを受け取り、パスワードハッシュを更新して当該ユーザーの全セッションを失効する。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 再設定トークンの有効性(期限・使用済み)を検証する |
| P-02 | トークンから対象アカウント(オーナー / メンバー)を特定する |
| P-03 | 新パスワードの強度要件(FR-006: 12 文字以上・英大小文字 / 数字 / 記号 3 種類以上)を検証する |
| P-04 | 対象アカウントのパスワードハッシュを更新する |
| P-05 | 再設定トークンを使用済みにする |
| P-06 | 当該ユーザーの全セッションを失効する |
| P-07 | 確定結果を返す |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `T_ACCESS_TOKENS` | —   | ◯   | ◯   | —   |
| `M_CONTRACT`      | —   | ◯   | ◯   | —   |
| `M_PRJ_USERS`     | —   | ◯   | ◯   | —   |
| `T_SESSIONS`      | —   | —   | ◯   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{}
```

#### Request Body

```json
{
  "token": "reset_...",
  "password": "P@ssw0rd123!",
  "passwordConfirm": "P@ssw0rd123!"
}
```

| 項目              | 型     | 説明                                                                    |
|-------------------|--------|-------------------------------------------------------------------------|
| `token`           | string | 再設定トークン(必須・メールリンクから取得)                              |
| `password`        | string | 新しいパスワード(必須・12 文字以上、英大小文字 / 数字 / 記号 3 種類以上) |
| `passwordConfirm` | string | 新しいパスワード確認用(必須・`password` と一致)                        |

### レスポンス(200)

```json
{ "ok": true }
```

| 項目 | 型      | 説明                     |
|------|---------|--------------------------|
| `ok` | boolean | パスワード再設定確定の成否 |

### エラー

| HTTP ステータス | エラーコード                          | 内容                   |
|-----------------|---------------------------------------|------------------------|
| 410             | `TOKEN_EXPIRED`(E-AUTH-TOKEN-EXPIRED) | トークン期限切れ       |
| 410             | `TOKEN_USED`(E-AUTH-TOKEN-USED)       | トークン使用済み       |
| 404             | `TOKEN_NOT_FOUND`                     | トークンが存在しない   |
| 400             | `VALIDATION_ERROR`(E-INPUT-\*)        | パスワード強度不足等   |

## <span id="API-AUTH-011"></span>API-AUTH-011 連絡先確認メール再送

### 基本情報

| 項目           | 内容                                              |
|----------------|---------------------------------------------------|
| API ID         | API-AUTH-011                                      |
| API 名         | 連絡先確認メール再送                              |
| エンドポイント | `/auth/contact-verifications/resend`              |
| HTTP メソッド  | POST                                              |
| 認証           | 要(Cookie)                                        |
| 権限           | オーナー専有                                      |

### 処理概要

プロジェクトの連絡先メールアドレスへ確認メールを再送する。レート制限により一定時間内の再送回数を制限する。

| 処理 ID | 処理内容 |
|---------|----------|
| P-01 | セッションから認証済みオーナーを特定する |
| P-02 | 対象プロジェクトが当該オーナーの所有であることを検証する |
| P-03 | 連絡先メールが設定済みかつ未確認状態であることを確認する |
| P-04 | レート制限(直近 X 分以内の再送上限)を確認し、超過している場合は 429 を返す |
| P-05 | 新しい連絡先確認トークンを発行し確認メールを再送する |
| P-06 | 再送結果を返す |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `M_PROJECTS`      | —   | ◯   | —   | —   |
| `T_ACCESS_TOKENS` | ◯   | —   | ◯   | —   |
| `H_NOTIF_LOGS`    | ◯   | —   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{}
```

#### Request Body

```json
{ "projectId": "proj_01HMK4Z8Q..." }
```

| 項目        | 型     | 説明                               |
|-------------|--------|------------------------------------|
| `projectId` | string | 確認メールを再送する対象プロジェクト ID(必須) |

### レスポンス(202)

```json
{ "ok": true, "retryAfter": 300 }
```

| 項目          | 型      | 説明                                                     |
|---------------|---------|----------------------------------------------------------|
| `ok`          | boolean | 再送受付の成否                                           |
| `retryAfter`  | integer | 次回再送が可能になるまでの秒数(レート制限内の場合は `0`) |

### エラー

| HTTP ステータス | エラーコード                        | 内容                                             |
|-----------------|-------------------------------------|--------------------------------------------------|
| 429             | `RATE_LIMITED`(E-AUTH-RATE-LIMITED) | レート制限超過(再送間隔未到達)                   |
| 409             | `ALREADY_VERIFIED`                  | 連絡先メールが既に確認済み                       |
| 404             | `PROJECT_NOT_FOUND`                 | 対象プロジェクトが存在しない                     |
| 400             | `CONTACT_EMAIL_NOT_SET`             | 連絡先メールが未設定                             |

---

<!-- portal-bottom -->
[← API設計](02_api-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
