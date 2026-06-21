<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [API設計](02_api-design.md) ／ **お知らせ受信箱 API**
<!-- /portal-top -->

# お知らせ受信箱 API

> **このページは、お知らせ受信箱の一覧・既読化・未読件数取得の API 契約を定義します。**
>
> **このページの API**
>
> - API-ANN-001 お知らせ一覧
> - API-ANN-002 お知らせ個別既読
> - API-ANN-003 お知らせ一括既読
> - API-ANN-004 お知らせ未読件数

*版数 v1.6 ・ 更新 2026-06-17 ・ 承認済*

## <span id="API-ANN-001"></span>API-ANN-001 お知らせ一覧

<span id="581-get-meannouncementscursor"></span>

### 基本情報

| 項目           | 内容                |
|----------------|---------------------|
| API ID         | API-ANN-001         |
| API 名         | お知らせ一覧        |
| エンドポイント | `/me/announcements` |
| HTTP メソッド  | GET                 |
| 認証           | Cookie              |
| 権限           | オーナー / メンバー          |

### 処理概要

お知らせ受信箱の一覧を返す。

| 処理 ID | 処理内容                                           |
|---------|----------------------------------------------------|
| P-01    | 認証・認可(オーナー / メンバー)を検証する          |
| P-02    | 当該ユーザー宛のお知らせを取得し既読状態を付与する |
| P-03    | カーソルページネーションで整形して返却する         |

### I/O

| テーブル      | C   | R   | U   | D   |
|---------------|-----|-----|-----|-----|
| `T_INBOX_MSG` | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{ "cursor": "共通仕様", "limit": "共通仕様" }
```

| 項目     | 型      | 説明                                       |
|----------|---------|--------------------------------------------|
| `cursor` | string  | ページネーション用カーソル。任意(共通仕様) |
| `limit`  | integer | 1 ページの取得件数。任意(共通仕様)         |

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
      "id": "ann_...",
      "title": "...",
      "category": "billing|announcement|system",
      "priority": "low|normal|high|critical",
      "bodyHtml": "<p>本文</p>",
      "readAt": "..." | null,
      "createdAt": "..."
    }
  ],
  "nextCursor": null
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `items` | array\<object\> | お知らせの配列 |
| `　└ id` | string | お知らせの ID |
| `　└ title` | string | お知らせのタイトル |
| `　└ category` | enum | カテゴリ。`billing` / `announcement` / `system` |
| `　└ priority` | enum | 重要度。`low` / `normal` / `high` / `critical` |
| `　└ bodyHtml` | string | お知らせ本文(HTML) |
| `　└ readAt` | string (ISO 8601) | 既読日時(未読時は `null`) |
| `　└ createdAt` | string (ISO 8601) | お知らせの配信日時 |
| `nextCursor` | string | 次ページ取得用カーソル(末尾は `null`) |

## <span id="API-ANN-002"></span>API-ANN-002 お知らせ個別既読

<span id="582-post-meannouncementsidread"></span>

### 基本情報

| 項目           | 内容                          |
|----------------|-------------------------------|
| API ID         | API-ANN-002                   |
| API 名         | お知らせ個別既読              |
| エンドポイント | `/me/announcements/{id}/read` |
| HTTP メソッド  | POST                          |
| 認証           | Cookie + CSRF                 |
| 権限           | オーナー / メンバー                    |

### 処理概要

お知らせ 1 件を既読にする。

| 処理 ID | 処理内容                                          |
|---------|---------------------------------------------------|
| P-01    | 認証・認可(オーナー / メンバー、CSRF)を検証する   |
| P-02    | 対象お知らせ 1 件を既読に更新する(既読済みは冪等) |
| P-03    | 既読時刻を返却する                                |

### I/O

| テーブル      | C   | R   | U   | D   |
|---------------|-----|-----|-----|-----|
| `T_INBOX_MSG` | —   | —   | ◯   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{ "id": "お知らせ ID" }
```

| 項目 | 型     | 説明                          |
|------|--------|-------------------------------|
| `id` | string | 既読にするお知らせの ID。必須 |

#### Request Body

```json
{}
```

### レスポンス(200)

```json
{ "id": "...", "readAt": "..." }
```

| 項目     | 型                | 説明                    |
|----------|-------------------|-------------------------|
| `id`     | string            | 既読にしたお知らせの ID |
| `readAt` | string (ISO 8601) | 既読日時                |

## <span id="API-ANN-003"></span>API-ANN-003 お知らせ一括既読

<span id="582a-post-meannouncementsread"></span>

### 基本情報

| 項目           | 内容                     |
|----------------|--------------------------|
| API ID         | API-ANN-003              |
| API 名         | お知らせ一括既読         |
| エンドポイント | `/me/announcements/read` |
| HTTP メソッド  | POST                     |
| 認証           | Cookie + CSRF            |
| 権限           | オーナー / メンバー               |

選択した複数のお知らせを一括で既読にする。1 リクエストの上限は **100 件**。超過時は 400 `VALIDATION_ERROR`。冪等(既読済みは再記録しない)。一括既読操作は操作者・対象件数・実行日時を監査記録する(FR-094 相当、正本: 09_セキュリティ設計.html)。

### 処理概要

選択した複数のお知らせを一括で既読にする(1 リクエスト上限 100 件)。

| 処理 ID | 処理内容                                                     |
|---------|--------------------------------------------------------------|
| P-01    | 認証・認可(オーナー / メンバー、CSRF)を検証する              |
| P-02    | 件数上限(100 件)を検証する                                   |
| P-03    | 指定または全件のお知らせを一括既読に更新する(既読済みは冪等) |
| P-04    | 操作者・対象件数・実行日時を監査記録する                     |
| P-05    | 既読件数を返却する                                           |

### I/O

| テーブル       | C   | R   | U   | D   |
|----------------|-----|-----|-----|-----|
| `T_INBOX_MSG`  | —   | —   | ◯   | —   |
| `H_AUDIT_LOGS` | ◯   | —   | —   | —   |

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
{ "ids": ["ann_...", "ann_..."] }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `ids` | array | 既読にするお知らせ ID の配列(1 リクエスト上限 100 件)。`all` 未指定時は必須 |
| `all` | boolean | 全件既読を指定する場合に `true`。任意(`ids` の代わりに指定) |

(全件既読を指定する場合は `{ "all": true }`)

### レスポンス(200)

```json
{ "readCount": 8, "readAt": "..." }
```

| 項目        | 型                | 説明               |
|-------------|-------------------|--------------------|
| `readCount` | integer           | 今回既読にした件数 |
| `readAt`    | string (ISO 8601) | 一括既読の実行日時 |

### エラー

| HTTP ステータス | エラーコード       | 内容       |
|-----------------|--------------------|------------|
| 400             | `VALIDATION_ERROR` | 100 件超過 |

## <span id="API-ANN-004"></span>API-ANN-004 お知らせ未読件数

<span id="583-get-meannouncementsunread-summary"></span>

### 基本情報

| 項目           | 内容                               |
|----------------|------------------------------------|
| API ID         | API-ANN-004                        |
| API 名         | お知らせ未読件数                   |
| エンドポイント | `/me/announcements/unread-summary` |
| HTTP メソッド  | GET                                |
| 認証           | Cookie                             |
| 権限           | オーナー / メンバー                         |

### 処理概要

未読件数と直近お知らせを返す。

| 処理 ID | 処理内容                               |
|---------|----------------------------------------|
| P-01    | 認証・認可(オーナー / メンバー)を検証する       |
| P-02    | 未読件数を集計し直近お知らせを取得する |
| P-03    | 整形して返却する                       |

### I/O

| テーブル      | C   | R   | U   | D   |
|---------------|-----|-----|-----|-----|
| `T_INBOX_MSG` | —   | ◯   | —   | —   |

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
{ "unreadsCount": 5, "recent": [...] }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `unreadsCount` | integer | 未読お知らせの件数 |
| `recent` | array\<object\> | 直近お知らせの配列(各要素は API-ANN-001 の `items` と同形式) |

---

<!-- portal-bottom -->
[← API設計](02_api-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
