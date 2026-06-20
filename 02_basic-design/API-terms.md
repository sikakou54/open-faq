<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [API設計](02_api-design.md) ／ **規約・退会 API**
<!-- /portal-top -->

# 規約・退会 API

> **このページは、利用規約 / プライバシーポリシーの取得・同意とオーナー退会申請の API 契約を定義します。**
>
> **このページの API**
>
> - API-TRM-001 利用規約 最新版取得
> - API-TRM-002 プライバシーポリシー 最新版取得
> - API-TRM-003 利用規約 同意
> - API-TRM-004 プライバシーポリシー 同意
> - API-TRM-005 退会申請

*版数 v1.6 ・ 更新 2026-06-17 ・ 承認済*

## <span id="API-TRM-001"></span>API-TRM-001 利用規約 最新版取得

<span id="591-get-termscurrent"></span>

### 基本情報

| 項目           | 内容                |
|----------------|---------------------|
| API ID         | API-TRM-001         |
| API 名         | 利用規約 最新版取得 |
| エンドポイント | `/terms/current`    |
| HTTP メソッド  | GET                 |
| 認証           | 不要                |
| 権限           | —(公開)             |

### 処理概要

利用規約の最新版を返す。

| 処理 ID | 処理内容                                   |
|---------|--------------------------------------------|
| P-01    | 最新版の利用規約を取得する                 |
| P-02    | 本文・施行日・主な変更点を整形して返却する |

### I/O

| テーブル                                     | C   | R   | U   | D   |
|----------------------------------------------|-----|-----|-----|-----|
| `M_TERMS_VER`(`doc_type='terms_of_service'`) | —   | ◯   | —   | —   |

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
{ "docType": "terms_of_service", "version": "...", "effectiveDate": "...", "bodyHtml": "...", "diffSummary": "..." }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `docType` | string | 文書種別(利用規約は `terms_of_service` 固定) |
| `version` | string | 返却した利用規約のバージョン |
| `effectiveDate` | string (ISO 8601) | 当該バージョンの施行日 |
| `bodyHtml` | string | 利用規約の本文 HTML |
| `diffSummary` | string | 主な変更点(`M_TERMS_VER.diff_summary`。NULL の場合は省略) |

(最新版のみ。`diffSummary` は `M_TERMS_VER.diff_summary`。SCR-015 の「主な変更点」表示に用いる。NULL の場合は省略)

## <span id="API-TRM-002"></span>API-TRM-002 プライバシーポリシー 最新版取得

<span id="591a-get-privacycurrent"></span>

### 基本情報

| 項目           | 内容                            |
|----------------|---------------------------------|
| API ID         | API-TRM-002                     |
| API 名         | プライバシーポリシー 最新版取得 |
| エンドポイント | `/privacy/current`              |
| HTTP メソッド  | GET                             |
| 認証           | 不要                            |
| 権限           | —(公開)                         |

### 処理概要

プライバシーポリシーの最新版を返す。

| 処理 ID | 処理内容                                   |
|---------|--------------------------------------------|
| P-01    | 最新版のプライバシーポリシーを取得する     |
| P-02    | 本文・施行日・主な変更点を整形して返却する |

### I/O

| テーブル                                   | C   | R   | U   | D   |
|--------------------------------------------|-----|-----|-----|-----|
| `M_TERMS_VER`(`doc_type='privacy_policy'`) | —   | ◯   | —   | —   |

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
{ "docType": "privacy_policy", "version": "...", "effectiveDate": "...", "bodyHtml": "...", "diffSummary": "..." }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `docType` | string | 文書種別(プライバシーポリシーは `privacy_policy` 固定) |
| `version` | string | 返却したプライバシーポリシーのバージョン |
| `effectiveDate` | string (ISO 8601) | 当該バージョンの施行日 |
| `bodyHtml` | string | プライバシーポリシーの本文 HTML |
| `diffSummary` | string | 主な変更点(`M_TERMS_VER.diff_summary`。NULL の場合は省略) |

(最新版のみ。`diffSummary` は `M_TERMS_VER.diff_summary`。SCR-015 の「主な変更点」表示に用いる。NULL の場合は省略)

## <span id="API-TRM-003"></span>API-TRM-003 利用規約 同意

<span id="592-post-termsagree"></span>

### 基本情報

| 項目           | 内容           |
|----------------|----------------|
| API ID         | API-TRM-003    |
| API 名         | 利用規約 同意  |
| エンドポイント | `/terms/agree` |
| HTTP メソッド  | POST           |
| 認証           | Cookie + CSRF  |
| 権限           | admin          |

### 処理概要

利用規約への同意を記録する(冪等)。

| 処理 ID | 処理内容                                                       |
|---------|----------------------------------------------------------------|
| P-01    | 認証・認可(admin、CSRF)を検証する                              |
| P-02    | 指定バージョンへの利用規約同意を記録する(既存同意があれば冪等) |
| P-03    | 同意記録結果を返却する                                         |

### I/O

| テーブル                                       | C   | R   | U   | D   |
|------------------------------------------------|-----|-----|-----|-----|
| `T_TERMS_AGREE`(`doc_type='terms_of_service'`) | ◯   | ◯   | —   | —   |

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
{ "version": "..." }
```

| 項目      | 型     | 説明                               |
|-----------|--------|------------------------------------|
| `version` | string | 同意対象の利用規約バージョン(必須) |

`T_TERMS_AGREE` に `(user_id, doc_type='terms_of_service', terms_version)` で 1 行記録(冪等: 既存同意があれば 200)。

### レスポンス(200)

同意記録結果。

## <span id="API-TRM-004"></span>API-TRM-004 プライバシーポリシー 同意

<span id="592a-post-privacyagree"></span>

### 基本情報

| 項目           | 内容                      |
|----------------|---------------------------|
| API ID         | API-TRM-004               |
| API 名         | プライバシーポリシー 同意 |
| エンドポイント | `/privacy/agree`          |
| HTTP メソッド  | POST                      |
| 認証           | Cookie + CSRF             |
| 権限           | admin                     |

### 処理概要

プライバシーポリシーへの同意を記録する(冪等)。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 認証・認可(admin、CSRF)を検証する |
| P-02 | 指定バージョンへのプライバシーポリシー同意を記録する(既存同意があれば冪等) |
| P-03 | 同意記録結果を返却する |

### I/O

| テーブル                                     | C   | R   | U   | D   |
|----------------------------------------------|-----|-----|-----|-----|
| `T_TERMS_AGREE`(`doc_type='privacy_policy'`) | ◯   | ◯   | —   | —   |

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
{ "version": "..." }
```

| 項目      | 型     | 説明                                           |
|-----------|--------|------------------------------------------------|
| `version` | string | 同意対象のプライバシーポリシーバージョン(必須) |

`T_TERMS_AGREE` に `(user_id, doc_type='privacy_policy', terms_version)` で 1 行記録(冪等: 既存同意があれば 200)。SCR-015 / SCR-018 では利用規約・プライバシーポリシー双方の同意が必須条件であり、改定再同意では改定された文書の agree のみを呼び出す。

### レスポンス(200)

同意記録結果。

## <span id="API-TRM-005"></span>API-TRM-005 退会申請

<span id="593-post-withdrawal-requests"></span>

### 基本情報

| 項目           | 内容                     |
|----------------|--------------------------|
| API ID         | API-TRM-005              |
| API 名         | 退会申請                 |
| エンドポイント | `/withdrawal-requests`   |
| HTTP メソッド  | POST                     |
| 認証           | オーナー専有、再認証必須 |
| 権限           | オーナー専有             |

### 処理概要

オーナーの退会を申請する。

| 処理 ID | 処理内容                                       |
|---------|------------------------------------------------|
| P-01    | 認証・認可(オーナー専有、再認証必須)を検証する |
| P-02    | 退会申請を登録し受付状態とする                 |
| P-03    | 受付結果を返却する                             |

### I/O

| テーブル         | C   | R   | U   | D   |
|------------------|-----|-----|-----|-----|
| `T_WITHDRAW_REQ` | ◯   | —   | —   | —   |
| `M_CONTRACT`     | —   | ◯   | ◯   | —   |

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
{ "reason": "退会申請内容(理由等)" }
```

| 項目     | 型     | 説明                     |
|----------|--------|--------------------------|
| `reason` | string | 退会理由・申請内容(任意) |

### レスポンス(2xx)

退会申請の受付結果。

### エラー

| HTTP ステータス | エラーコード        | 内容               |
|-----------------|---------------------|--------------------|
| 403             | `PERMISSION_DENIED` | メンバーは申請不可 |

---

---

---

<!-- portal-bottom -->
[← API設計](02_api-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
