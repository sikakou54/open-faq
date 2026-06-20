<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [API設計](02_api-design.md) ／ **利用量・課金 API**
<!-- /portal-top -->

# 利用量・課金 API

> **このページは、利用量サマリ・請求サマリ・請求書一覧・支払方法・プロジェクト上限の API 契約を定義します。**
>
> **このページの API**
>
> - API-BIL-001 利用量サマリ(プロジェクト)
> - API-BIL-002 利用量サマリ(契約)
> - API-BIL-003 請求サマリ
> - API-BIL-004 請求書一覧
> - API-BIL-005 支払方法 取得・登録・更新
> - API-BIL-006 プロジェクト上限・アラート取得
> - API-BIL-007 プロジェクト上限・アラート更新

*版数 v1.6 ・ 更新 2026-06-17 ・ 承認済*

## <span id="API-BIL-001"></span>API-BIL-001 利用量サマリ(プロジェクト)

<span id="571-get-usageperiodcurrent"></span>

### 基本情報

| 項目           | 内容                                                  |
|----------------|-------------------------------------------------------|
| API ID         | API-BIL-001                                           |
| API 名         | 利用量サマリ(プロジェクト)                            |
| エンドポイント | `/usage`                                              |
| HTTP メソッド  | GET                                                   |
| 認証           | Cookie                                                |
| 権限           | オーナー / 該当プロジェクトの `admin` または `member` |

契約全体の利用状況は API-033 `GET /owner/projects/usage` を使用する。

### 処理概要

プロジェクト単位の利用量を返す。

| 処理 ID | 処理内容                                             |
|---------|------------------------------------------------------|
| P-01    | 認証・認可(対象プロジェクトへのアクセス権)を検証する |
| P-02    | 対象期間・プロジェクトの質問数・FAQ 件数を集計する   |
| P-03    | 上限・無料枠・利用率を算出し整形して返却する         |

### I/O

| テーブル        | C   | R   | U   | D   |
|-----------------|-----|-----|-----|-----|
| `T_USAGE_METER` | —   | ◯   | —   | —   |
| `M_FAQS`        | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{ "period": "current_month", "viewMode": "project", "projectId": "{id}" }
```

| 項目        | 型     | 説明                                              |
|-------------|--------|---------------------------------------------------|
| `period`    | enum   | 集計期間。任意。`current_month` 等                |
| `viewMode`  | enum   | 集計の表示単位。任意。`project`(プロジェクト単位) |
| `projectId` | string | 対象プロジェクトの ID。必須                       |

#### Path Parameters

```json
{}
```

#### Request Body

```json
{}
```

### レスポンス(200)

`viewMode=project` の例:

```json
{
  "period": "2026-05-01T00:00:00Z",
  "projectId": "prj_...",
  "questions": { "used": 750, "limit": 1000, "freeQuota": 1000, "percentage": 75, "resetAt": "2026-06-01T..." },
  "faqs": { "used": 85, "freeQuota": 100 }
}
```

| 項目             | 型                | 説明                       |
|------------------|-------------------|----------------------------|
| `period`         | string (ISO 8601) | 集計対象期間の起点         |
| `projectId`      | string            | 対象プロジェクトの ID      |
| `questions`      | object            | 質問数の利用状況           |
| `　└ used`       | integer           | 当月の質問数(利用済み件数) |
| `　└ limit`      | integer           | 月次上限件数               |
| `　└ freeQuota`  | integer           | 質問数の無料利用枠         |
| `　└ percentage` | integer           | 上限に対する利用率(%)      |
| `　└ resetAt`    | string (ISO 8601) | 利用量がリセットされる日時 |
| `M_FAQS`         | object            | FAQ 件数の利用状況         |
| `　└ used`       | integer           | 公開 FAQ 件数              |
| `　└ freeQuota`  | integer           | FAQ 件数の無料利用枠       |

## <span id="API-BIL-002"></span>API-BIL-002 利用量サマリ(契約)

<span id="572-get-ownerprojectsusageperiodcurrent_month"></span>

### 基本情報

| 項目           | 内容                    |
|----------------|-------------------------|
| API ID         | API-BIL-002             |
| API 名         | 利用量サマリ(契約)      |
| エンドポイント | `/owner/projects/usage` |
| HTTP メソッド  | GET                     |
| 認証           | Cookie                  |
| 権限           | オーナー専有            |

契約全体サマリーとプロジェクト別の質問数、質問数上限に対する利用率、公開 FAQ 件数、最終更新日時を返す。

### 処理概要

契約全体サマリーとプロジェクト別利用量を返す。

| 処理 ID | 処理内容                                                  |
|---------|-----------------------------------------------------------|
| P-01    | 認証・認可(オーナー専有)を検証する                        |
| P-02    | 契約配下の全プロジェクトの質問数・公開 FAQ 件数を集計する |
| P-03    | 契約全体サマリーとプロジェクト別内訳を整形して返却する    |

### I/O

| テーブル        | C   | R   | U   | D   |
|-----------------|-----|-----|-----|-----|
| `T_USAGE_METER` | —   | ◯   | —   | —   |
| `M_FAQS`        | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{ "period": "current_month" }
```

| 項目     | 型   | 説明                               |
|----------|------|------------------------------------|
| `period` | enum | 集計期間。任意。`current_month` 等 |

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
{
  "period": { "from": "2026-06-01T00:00:00Z", "to": "2026-06-30T23:59:59Z" },
  "summary": { "projectCount": 3, "questionCount": 2450, "publishedFaqCount": 184 },
  "projects": [
    {
      "projectId": "prj_...",
      "projectName": "サポートサイト",
      "questions": { "used": 750, "limitEnabled": true, "limit": 1000, "percentage": 75 },
      "publishedFaqCount": 85
    }
  ],
  "updatedAt": "2026-06-14T05:00:00Z"
}
```

| 項目                    | 型                | 説明                         |
|-------------------------|-------------------|------------------------------|
| `period`                | object            | 集計対象期間                 |
| `　└ from`              | string (ISO 8601) | 期間の起点                   |
| `　└ to`                | string (ISO 8601) | 期間の終点                   |
| `summary`               | object            | 契約全体のサマリー           |
| `　└ projectCount`      | integer           | 契約配下のプロジェクト数     |
| `　└ questionCount`     | integer           | 契約全体の質問数             |
| `　└ publishedFaqCount` | integer           | 契約全体の公開 FAQ 件数      |
| `M_PROJECTS`            | array\<object\>   | プロジェクト別の利用量内訳   |
| `　└ projectId`         | string            | プロジェクトの ID            |
| `　└ projectName`       | string            | プロジェクト名               |
| `　└ questions`         | object            | プロジェクトの質問数利用状況 |
| `　　└ used`            | integer           | 当月の質問数                 |
| `　　└ limitEnabled`    | boolean           | 月次上限が有効か             |
| `　　└ limit`           | integer           | 月次上限件数                 |
| `　　└ percentage`      | integer           | 上限に対する利用率(%)        |
| `　└ publishedFaqCount` | integer           | プロジェクトの公開 FAQ 件数  |
| `updatedAt`             | string (ISO 8601) | 集計値の最終更新日時         |

## <span id="API-BIL-003"></span>API-BIL-003 請求サマリ

<span id="573-get-billingsummaryperiodcurrent"></span>

### 基本情報

| 項目           | 内容               |
|----------------|--------------------|
| API ID         | API-BIL-003        |
| API 名         | 請求サマリ         |
| エンドポイント | `/billing/summary` |
| HTTP メソッド  | GET                |
| 認証           | Cookie             |
| 権限           | オーナー専有       |

### 処理概要

当月請求見込み合計・次回請求日・請求状態・プロジェクト別内訳・支払方法登録状態を返す。

| 処理 ID | 処理内容                                         |
|---------|--------------------------------------------------|
| P-01    | 認証・認可(オーナー専有)を検証する               |
| P-02    | 当月の請求見込み・プロジェクト別内訳を算出する   |
| P-03    | 次回請求日・請求状態・支払方法登録状態を解決する |
| P-04    | 整形して返却する                                 |

### I/O

| テーブル        | C   | R   | U   | D   |
|-----------------|-----|-----|-----|-----|
| `T_BILL_SUBS`   | —   | ◯   | —   | —   |
| `T_USAGE_METER` | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{ "period": "current_month" }
```

| 項目     | 型   | 説明                               |
|----------|------|------------------------------------|
| `period` | enum | 集計期間。任意。`current_month` 等 |

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
{
  "estimatedTotal": 12500,
  "currency": "JPY",
  "nextBillingDate": "2026-07-01",
  "billingStatus": "normal|payment_method_required|payment_failed",
  "paymentMethod": { "registered": true, "brand": "visa", "last4": "4242" },
  "projects": [
    {
      "projectId": "prj_...",
      "projectName": "サポートサイト",
      "questionCharge": 3500,
      "faqCharge": 1000,
      "subtotal": 4500
    }
  ]
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `estimatedTotal` | integer | 当月請求見込み合計 |
| `currency` | string | 通貨コード |
| `nextBillingDate` | string (ISO 8601) | 次回請求日 |
| `billingStatus` | enum | 請求状態。`normal` / `payment_method_required` / `payment_failed` |
| `paymentMethod` | object | 支払方法の登録状態 |
| `　└ registered` | boolean | 支払方法が登録済みか |
| `　└ brand` | string | カードブランド |
| `　└ last4` | string | カード番号下 4 桁 |
| `M_PROJECTS` | array\<object\> | プロジェクト別の請求内訳 |
| `　└ projectId` | string | プロジェクトの ID |
| `　└ projectName` | string | プロジェクト名 |
| `　└ questionCharge` | integer | 質問数に対する課金額 |
| `　└ faqCharge` | integer | FAQ 件数に対する課金額 |
| `　└ subtotal` | integer | プロジェクトの小計 |

## <span id="API-BIL-004"></span>API-BIL-004 請求書一覧

<span id="574-get-billinginvoiceslimit6"></span>

### 基本情報

| 項目           | 内容                |
|----------------|---------------------|
| API ID         | API-BIL-004         |
| API 名         | 請求書一覧          |
| エンドポイント | `/billing/invoices` |
| HTTP メソッド  | GET                 |
| 認証           | Cookie              |
| 権限           | オーナー専有        |

### 処理概要

過去請求書を一覧取得する。

| 処理 ID | 処理内容                                      |
|---------|-----------------------------------------------|
| P-01    | 認証・認可(オーナー専有)を検証する            |
| P-02    | 過去請求書を新しい順に取得する                |
| P-03    | PDF 署名 URL(有効期限 5 分)を付与して返却する |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `T_BILL_INVOICES` | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{ "limit": "6(等)" }
```

| 項目    | 型      | 説明                                |
|---------|---------|-------------------------------------|
| `limit` | integer | 取得する請求書の件数。任意(例: `6`) |

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
{
  "items": [
    {
      "id": "inv_...",
      "date": "2026-05-01T...",
      "amount": 5000,
      "currency": "JPY",
      "status": "paid|failed|draft",
      "pdfUrl": "https://..."
    }
  ]
}
```

| 項目           | 型                | 説明                                      |
|----------------|-------------------|-------------------------------------------|
| `items`        | array\<object\>   | 請求書の配列(新しい順)                    |
| `　└ id`       | string            | 請求書の ID                               |
| `　└ date`     | string (ISO 8601) | 請求日                                    |
| `　└ amount`   | integer           | 請求金額                                  |
| `　└ currency` | string            | 通貨コード                                |
| `　└ status`   | enum              | 請求書の状態。`paid` / `failed` / `draft` |
| `　└ pdfUrl`   | string            | 請求書 PDF の署名 URL(有効期限 5 分)      |

`pdfUrl` は R2 署名 URL(有効期限 5 分)。

## <span id="API-BIL-005"></span>API-BIL-005 支払方法 取得・登録・更新

<span id="574a-get--put-billingpayment-method"></span>

### 基本情報

| 項目           | 内容                            |
|----------------|---------------------------------|
| API ID         | API-BIL-005                     |
| API 名         | 支払方法 取得・登録・更新       |
| エンドポイント | `/billing/payment-method`       |
| HTTP メソッド  | GET / PUT                       |
| 認証           | Cookie + CSRF(PUT は再認証必須) |
| 権限           | **オーナー専有**                |

支払方法はクレジットカードのみ(FR-136)。カード番号等の生データはサーバで保持せず、課金プロバイダのトークンを受領して紐付ける(PCI スコープ最小化、正本: 09_セキュリティ設計.html)。サスペンション中もオーナーは本 API を実行できる(FR-138)。

### 処理概要

支払方法の取得と登録 / 更新(クレジットカードのみ)。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 認証・認可(オーナー専有、PUT は再認証必須)を検証する |
| P-02 | GET は登録済み支払方法(ブランド・下 4 桁等)を取得する |
| P-03 | PUT は課金プロバイダのトークンを検証し支払方法を登録 / 更新する(生データは保持しない) |
| P-04 | 結果を返却する |

### I/O

| テーブル      | C   | R   | U   | D   |
|---------------|-----|-----|-----|-----|
| `T_BILL_SUBS` | —   | ◯   | ◯   | —   |

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
{ "paymentToken": "tok_..." }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `paymentToken` | string | 課金プロバイダが発行した支払方法トークン。PUT 時のみ必須(GET ではボディなし) |

(GET: なし。PUT のみ。`paymentToken` は課金プロバイダ発行トークン)

### レスポンス(200)

GET: `{ "registered": true, "brand": "visa", "last4": "4242", "expMonth": 12, "expYear": 2028 }`(未登録時は `{ "registered": false }`)。PUT: `{ "registered": true, "brand": "visa", "last4": "4242" }`。

**GET レスポンス**

| 項目 | 型 | 説明 |
|----|----|----|
| `registered` | boolean | 支払方法が登録済みか(未登録時は本項目のみ `false` を返す) |
| `brand` | string | カードブランド |
| `last4` | string | カード番号下 4 桁 |
| `expMonth` | integer | カード有効期限(月) |
| `expYear` | integer | カード有効期限(年) |

**PUT レスポンス**

| 項目         | 型      | 説明                             |
|--------------|---------|----------------------------------|
| `registered` | boolean | 支払方法が登録済みか             |
| `brand`      | string  | 登録 / 更新したカードブランド    |
| `last4`      | string  | 登録 / 更新したカード番号下 4 桁 |

### エラー

| HTTP ステータス | エラーコード | 内容 |
|----|----|----|
| 400 | `VALIDATION_ERROR` | 入力値の検証エラー |
| 402 | `PAYMENT_METHOD_DECLINED`(E-BILL-PAYMENT-FAILED) | カードが拒否された |
| 403 | `E-AUTHZ-OWNER-ONLY` | オーナー以外は不可 |

## <span id="API-BIL-006"></span>API-BIL-006 プロジェクト上限・アラート取得

<span id="575-get-projectsidquota-limits"></span>

### 基本情報

| 項目 | 内容 |
|----|----|
| API ID | API-BIL-006 |
| API 名 | プロジェクト上限・アラート取得 |
| エンドポイント | `/projects/{id}/quota-limits` |
| HTTP メソッド | GET |
| 認証 | Cookie |
| 権限 | オーナー / 該当プロジェクトの `admin` または `member`(閲覧) |

SCR-021 の表示には `used` / `limitEnabled` / `limit` / `percentage` / `yenEquivalent` だけを使用し、アラート設定・設定元は表示しない。SCR-021-001 は `limitEnabled` / `limit` / `alertThresholds` を使用する。FAQ 件数は扱わないためレスポンスに含めない。質問数の無料利用枠は課金判定用の内部データとして保持するが、本 API のレスポンスには含めない。

### 処理概要

当該プロジェクトの質問数について利用状況・月次上限件数・アラート設定を返す。

| 処理 ID | 処理内容                                                  |
|---------|-----------------------------------------------------------|
| P-01    | 認証・認可(対象プロジェクトへのアクセス権)を検証する      |
| P-02    | 質問数の利用状況・月次上限・アラート設定を取得する        |
| P-03    | 上限消化時の参考課金額(`yenEquivalent`)を算出して返却する |

### I/O

| テーブル             | C   | R   | U   | D   |
|----------------------|-----|-----|-----|-----|
| `M_PRJ_QUOTA_LIMITS` | —   | ◯   | —   | —   |
| `T_USAGE_METER`      | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{ "id": "プロジェクト ID" }
```

| 項目 | 型     | 説明                        |
|------|--------|-----------------------------|
| `id` | string | 対象プロジェクトの ID。必須 |

#### Request Body

```json
{}
```

### レスポンス(200)

```json
{
  "projectId": "prj_...",
  "period": "2026-05-01T00:00:00Z",
  "questions": { "used": 750, "limitEnabled": true, "limit": 5000, "percentage": 15, "alertThresholds": [80, 100], "yenEquivalent": 2000, "source": "owner" }
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `projectId` | string | 対象プロジェクトの ID |
| `period` | string (ISO 8601) | 集計対象期間の起点 |
| `questions` | object | 質問数の利用状況・上限・アラート設定 |
| `　└ used` | integer | 当月の質問数 |
| `　└ limitEnabled` | boolean | 月次上限が有効か(OFF 時は `false`) |
| `　└ limit` | integer | 月次上限件数(OFF 時は `null`) |
| `　└ percentage` | integer | 上限に対する利用率(%、OFF 時は `null`) |
| `　└ alertThresholds` | array | アラート発火の閾値(%)の配列 |
| `　└ yenEquivalent` | integer | 上限消化時の参考課金額(OFF 時は `null`) |
| `　└ source` | enum | 上限設定元。`owner` |

`yenEquivalent` は上限件数をすべて利用した場合の最大課金額の参考値で、`billableCount = max(0, limit - 適用中の質問数無料利用枠)`、`yenEquivalent = billableCount × 質問単価` により算出する。画面では「5,000件 - 1,000件(無料枠) = 4,000件 (¥2,000 / 月)」の形式で表示する。上限 OFF 時は `limitEnabled=false`、`limit=null`、`percentage=null`、`yenEquivalent=null` を返す。SCR-021 は「今月の利用上限」を「OFF」と表示し、「利用量」には割合・件数比・ProgressBar・状態バッジを描画しない。

## <span id="API-BIL-007"></span>API-BIL-007 プロジェクト上限・アラート更新

<span id="576-patch-projectsidquota-limitsquestions"></span>

### 基本情報

| 項目 | 内容 |
|----|----|
| API ID | API-BIL-007 |
| API 名 | プロジェクト上限・アラート更新 |
| エンドポイント | `/projects/{id}/quota-limits/questions` |
| HTTP メソッド | PATCH |
| 認証 | 再認証必須 |
| 権限 | オーナー / 該当プロジェクトの `admin`(member は `E-AUTHZ-FORBIDDEN`) |

`M_PRJ_QUOTA_LIMITS.resource_kind='q_monthly_limit'` かつ `source='owner'` の 1 行だけを upsert する。質問数の `free_quota` と FAQ 件数の行は更新しない。

### 処理概要

質問数の月次上限 ON/OFF・件数・アラート閾値を更新する。

| 処理 ID | 処理内容                                                        |
|---------|-----------------------------------------------------------------|
| P-01    | 認証・認可(オーナー / 該当 PJ の `admin`、再認証必須)を検証する |
| P-02    | 入力(上限 ON/OFF・件数・アラート閾値)を検証し正規化する         |
| P-03    | 質問数月次上限(`source='owner'`)を作成 / 更新する               |
| P-04    | 参考課金額を再算出し更新後の値を返却する                        |

### I/O

| テーブル             | C   | R   | U   | D   |
|----------------------|-----|-----|-----|-----|
| `M_PRJ_QUOTA_LIMITS` | —   | —   | ◯   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{ "id": "プロジェクト ID" }
```

| 項目 | 型     | 説明                        |
|------|--------|-----------------------------|
| `id` | string | 対象プロジェクトの ID。必須 |

#### Request Body

```json
{ "limitEnabled": true, "limit": 5000, "alertThresholds": [25, 50, 80, 90, 100] }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `limitEnabled` | boolean | 月次上限の有効 / 無効。必須 |
| `limit` | integer | 月次上限件数。`limitEnabled=true` の場合は必須(範囲内・1 件刻み)、`false` の場合は `null` |
| `alertThresholds` | array | アラート発火の閾値(%)の配列。`25` / `50` / `80` / `90` / `100` の重複しない値。空配列で通知なし |

例(ON)。例(OFF): `{ "limitEnabled": false, "limit": null, "alertThresholds": [] }`。

バリデーション: `limitEnabled=true` の場合、`limit` は必須かつ 1 件刻みで最小件数・最大件数の範囲内。`alertThresholds` は `25` / `50` / `80` / `90` / `100` の重複しない配列とし、サーバ側で昇順へ正規化する。空配列はアラート通知なし。`limitEnabled=false` の場合は `limit=null`、`alertThresholds=[]` とする。`freeQuota` / `alertEnabled` / `alertFrequency` を指定した場合は未サポート項目として 422。

### レスポンス(200)

```json
{ "projectId": "prj_...", "limitEnabled": true, "limit": 5000, "alertThresholds": [25, 50, 80, 90, 100], "yenEquivalent": 2000, "source": "owner", "updatedAt": "..." }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `projectId` | string | 対象プロジェクトの ID |
| `limitEnabled` | boolean | 更新後の月次上限の有効 / 無効 |
| `limit` | integer | 更新後の月次上限件数(OFF 時は `null`) |
| `alertThresholds` | array | 更新後のアラート閾値(%、昇順)の配列 |
| `yenEquivalent` | integer | 上限消化時の参考課金額(OFF 時は `null`) |
| `source` | enum | 上限設定元。`owner` |
| `updatedAt` | string (ISO 8601) | 更新日時 |

### エラー

| HTTP ステータス | エラーコード | 内容 |
|----|----|----|
| 422 | (未サポート項目) | `freeQuota` / `alertEnabled` / `alertFrequency` を指定 |
| 403 | `E-AUTHZ-FORBIDDEN` | member による変更 / 当該プロジェクトに割当のないユーザー |

---

---

<!-- portal-bottom -->
[← API設計](02_api-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
