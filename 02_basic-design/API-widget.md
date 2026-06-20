<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [API設計](02_api-design.md) ／ **ウィジェット API**
<!-- /portal-top -->

# ウィジェット API

> **このページは、ウィジェットの起動・質問送信・未解決質問登録の公開 API 契約を定義します。**
>
> **このページの API**
>
> - API-WGT-001 ウィジェット起動
> - API-WGT-002 ウィジェット質問送信
> - API-WGT-003 ウィジェット未解決質問登録

*版数 v1.6 ・ 更新 2026-06-17 ・ 承認済*

## <span id="API-WGT-001"></span>API-WGT-001 ウィジェット起動

<span id="551-post-widgetv1bootstrap"></span>

### 基本情報

| 項目           | 内容                   |
|----------------|------------------------|
| API ID         | API-WGT-001            |
| API 名         | ウィジェット起動       |
| エンドポイント | `/widget/v1/bootstrap` |
| HTTP メソッド  | POST                   |
| 認証           | 不要(ドメイン検証)     |
| 権限           | end_user(公開キー)     |

### 処理概要

公開キーとドメインを検証しウィジェットセッションを発行する。

| 処理 ID | 処理内容                                               |
|---------|--------------------------------------------------------|
| P-01    | 公開キーを検証し、対象プロジェクトを特定する           |
| P-02    | リクエスト元オリジンが許可ドメインに含まれるか検証する |
| P-03    | 契約状態(停止中か)を確認する                           |
| P-04    | ウィジェットセッショントークンを発行する               |
| P-05    | プロジェクト表示設定を整形して返却する                 |

### I/O

| テーブル            | C   | R   | U   | D   |
|---------------------|-----|-----|-----|-----|
| `M_PROJECTS`        | —   | ◯   | —   | —   |
| `M_ALLOWED_DOMAINS` | —   | ◯   | —   | —   |
| `M_CONTRACT`        | —   | ◯   | —   | —   |
| `T_SESSIONS`        | ◯   | —   | —   | —   |

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
  "publicKey": "pk_live_abc123...",
  "origin": "https://example.com"
}
```

| 項目        | 型     | 説明                                               |
|-------------|--------|----------------------------------------------------|
| `publicKey` | string | プロジェクトの公開キー。必須                       |
| `origin`    | string | リクエスト元オリジン(許可ドメイン検証に使用)。必須 |

### レスポンス(200)

```json
{
  "sessionToken": "wst_...",
  "expiresIn": 3600,
  "projectConfig": {
    "headerColor": "#06c",
    "placement": "bottom-right",
    "headerTitle": "お問い合わせ",
    "contactEmail": "contact@..."
  }
}
```

| 項目               | 型      | 説明                                     |
|--------------------|---------|------------------------------------------|
| `sessionToken`     | string  | 発行されたウィジェットセッショントークン |
| `expiresIn`        | integer | セッショントークンの有効期限(秒)         |
| `projectConfig`    | object  | ウィジェット表示用のプロジェクト設定     |
| `　└ headerColor`  | string  | ヘッダーの表示色                         |
| `　└ placement`    | string  | ウィジェットの表示位置                   |
| `　└ headerTitle`  | string  | ヘッダーに表示するタイトル               |
| `　└ contactEmail` | string  | 問い合わせ先メールアドレス               |

### エラー

| HTTP ステータス | エラーコード         | 内容           |
|-----------------|----------------------|----------------|
| 401             | `WIDGET_KEY_INVALID` | 公開キーが不正 |
| 403             | `DOMAIN_NOT_ALLOWED` | 許可ドメイン外 |
| 403             | `CONTRACT_SUSPENDED` | 契約停止中     |

## <span id="API-WGT-002"></span>API-WGT-002 ウィジェット質問送信

<span id="552-post-widgetv1ask"></span>

### 基本情報

| 項目           | 内容                 |
|----------------|----------------------|
| API ID         | API-WGT-002          |
| API 名         | 質問送信             |
| エンドポイント | `/widget/v1/ask`     |
| HTTP メソッド  | POST                 |
| 認証           | Bearer session_token |
| 権限           | end_user(セッション) |

### 処理概要

AI 回答を生成し質問ログを記録する。未回答時は未解決質問を同時生成する。

| 処理 ID | 処理内容                                             |
|---------|------------------------------------------------------|
| P-01    | セッショントークンとオリジンを検証する               |
| P-02    | 契約単位のレート制限とプロジェクト月次上限を判定する |
| P-03    | AI 推論 IF で候補 FAQ から回答を生成する             |
| P-04    | 質問ログを記録する                                   |
| P-05    | 未回答時は未解決質問を同一トランザクションで生成する |
| P-06    | 回答または未回答理由・連絡先を返却する               |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `H_QUESTION_LOGS` | ◯   | —   | —   | —   |
| `M_FAQS`          | —   | ◯   | —   | —   |
| `T_USAGE_METER`   | ◯   | —   | ◯   | —   |
| `T_INQUIRIES`     | ◯   | —   | —   | —   |

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
{ "question": "返品の手続きは?", "projectId": "proj_..." }
```

| 項目        | 型     | 説明                                       |
|-------------|--------|--------------------------------------------|
| `question`  | string | ウィジェット利用者が送信した質問内容。必須 |
| `projectId` | string | 対象プロジェクトの ID。必須                |

### レスポンス(200)

answered:

```json
{
  "type": "answered",
  "answer": "返品は商品到着後 7 日以内に...",
  "confidence": 0.78,
  "referencedFaqs": [
    { "id": "faq_...", "question": "返品ポリシー", "answer": "..." }
  ],
  "questionLogId": "qlog_..."
}
```

| 項目             | 型              | 説明                            |
|------------------|-----------------|---------------------------------|
| `type`           | enum            | 回答種別。`answered`(回答あり)  |
| `answer`         | string          | AI が生成した回答本文           |
| `confidence`     | number          | 回答の確信度(0〜1)              |
| `referencedFaqs` | array\<object\> | 回答の根拠とした参照 FAQ の配列 |
| `　└ id`         | string          | 参照 FAQ の ID                  |
| `　└ question`   | string          | 参照 FAQ の質問                 |
| `　└ answer`     | string          | 参照 FAQ の回答                 |
| `questionLogId`  | string          | 記録された質問ログの ID         |

### レスポンス(200)

unanswered:

```json
{
  "type": "unanswered",
  "reason": "low_confidence" | "no_faq_match" | "pii_detected",
  "questionLogId": "qlog_...",
  "inquiryId": "inq_...",
  "inquiryCode": "INQ-20260513-XYZ123",
  "contactEmail": "support@example.com"
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `type` | enum | 回答種別。`unanswered`(回答不可) |
| `reason` | enum | 未回答理由。`low_confidence`(確信度不足)/ `no_faq_match`(該当 FAQ なし)/ `pii_detected`(個人情報検出) |
| `questionLogId` | string | 記録された質問ログの ID |
| `inquiryId` | string | 同時生成された未解決質問の ID |
| `inquiryCode` | string | 未解決質問の管理用識別子(ウィジェットには描画しない) |
| `contactEmail` | string | プロジェクトの問い合わせ先メールアドレス(未設定時は `null`) |

`unanswered` では質問ログと未解決質問を同一トランザクションで作成する。`inquiryCode` は管理用識別子としてレスポンス互換性のため返却するが、ウィジェットには描画しない。ウィジェットは回答できなかった旨と確認済みプロジェクト連絡先メールを表示し、FAQ 質問入力は継続可能とする。連絡先未設定時は `contactEmail=null` を返す。冪等性は `questionLogId` を基準に担保する。

### エラー

| HTTP ステータス | エラーコード         | 内容               |
|-----------------|----------------------|--------------------|
| 429             | `RATE_LIMITED`       | レート制限超過(§3) |
| 403             | `DOMAIN_NOT_ALLOWED` | 許可ドメイン外     |

## <span id="API-WGT-003"></span>API-WGT-003 ウィジェット未解決質問登録

<span id="553-post-widgetv1inquiries"></span>

### 基本情報

| 項目           | 内容                   |
|----------------|------------------------|
| API ID         | API-WGT-003            |
| API 名         | 未解決質問登録         |
| エンドポイント | `/widget/v1/inquiries` |
| HTTP メソッド  | POST                   |
| 認証           | Bearer session_token   |
| 権限           | end_user(セッション)   |

### 処理概要

未解決質問を登録する(チャット部屋は作成しない)。

| 処理 ID | 処理内容                                                       |
|---------|----------------------------------------------------------------|
| P-01    | セッショントークンを検証する                                   |
| P-02    | 冪等キーで重複登録を排除する                                   |
| P-03    | 対象質問ログから未解決質問を登録する(チャット部屋は作成しない) |
| P-04    | 登録結果(未解決質問 ID・状況)を返却する                        |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `T_INQUIRIES`     | ◯   | —   | —   | —   |
| `H_QUESTION_LOGS` | —   | ◯   | —   | —   |

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
  "questionId": "qlog_...",
  "idempotencyKey": "<UUIDv4>"
}
```

| 項目             | 型     | 説明                                     |
|------------------|--------|------------------------------------------|
| `questionId`     | string | 未解決質問の元となる質問ログの ID。必須  |
| `idempotencyKey` | string | 重複登録を排除する冪等キー(UUIDv4)。必須 |

### レスポンス(201)

```json
{ "inquiryId": "inq_...", "inquiryCode": "INQ-20260513-XYZ123", "status": "open" }
```

| 項目          | 型     | 説明                                |
|---------------|--------|-------------------------------------|
| `inquiryId`   | string | 登録された未解決質問の ID           |
| `inquiryCode` | string | 未解決質問の管理用識別子            |
| `status`      | enum   | 未解決質問の状況。`open` / `closed` |

> [!NOTE]
> **補足** 未解決質問登録ではチャット部屋を作成しない。

---

---

---

<!-- portal-bottom -->
[← API設計](02_api-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
