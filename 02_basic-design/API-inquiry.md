<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [API設計](02_api-design.md) ／ **未解決質問 API**
<!-- /portal-top -->

# 未解決質問 API

> **このページは、未解決質問の一覧取得と詳細取得 / 状況切替の API 契約を定義します。**
>
> **このページの API**
>
> - API-INQ-001 未解決質問一覧
> - API-INQ-002 未解決質問詳細・状況切替

*版数 v1.6 ・ 更新 2026-06-17 ・ 承認済*

## <span id="API-INQ-001"></span>API-INQ-001 未解決質問一覧

<span id="561-get-inquiriesstatusopenprojectidcursor"></span>

### 基本情報

| 項目           | 内容                            |
|----------------|---------------------------------|
| API ID         | API-INQ-001                     |
| API 名         | 未解決質問一覧                  |
| エンドポイント | `/inquiries`                    |
| HTTP メソッド  | GET                             |
| 認証           | Cookie                          |
| 権限           | オーナー / 該当 PJ の `member`+ |

### 処理概要

未解決質問を状況・プロジェクトで一覧取得する。

| 処理 ID | 処理内容                                             |
|---------|------------------------------------------------------|
| P-01    | 認証・認可(対象プロジェクトへのアクセス権)を検証する |
| P-02    | 状況・プロジェクトの条件で未解決質問を取得する       |
| P-03    | カーソルページネーションで整形して返却する           |

### I/O

| テーブル      | C   | R   | U   | D   |
|---------------|-----|-----|-----|-----|
| `T_INQUIRIES` | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{
  "status": "(任意・open / closed のいずれか、未指定で両方)",
  "projectId": "(任意)",
  "cursor": "(共通仕様)",
  "limit": "(共通仕様)"
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `status` | enum | 状況での絞り込み。任意。`open` / `closed` のいずれか(未指定で両方) |
| `projectId` | string | プロジェクトでの絞り込み。任意 |
| `cursor` | string | ページネーション用カーソル。任意(共通仕様) |
| `limit` | integer | 1 ページの取得件数。任意(共通仕様) |

#### Path Parameters

```json
{}
```

#### Request Body

```json
{}
```

### レスポンス(200)

未解決質問の配列 + `nextCursor`。

| 項目 | 型 | 説明 |
|----|----|----|
| `items` | array\<object\> | 未解決質問の配列 |
| `　└ id` | string | 未解決質問の ID |
| `　└ inquiryCode` | string | 未解決質問の管理用識別子 |
| `　└ question` | string | ウィジェット利用者が送信した質問内容 |
| `　└ status` | enum | 状況。`open` / `closed` |
| `　└ projectId` | string | 当該未解決質問が属するプロジェクトの ID |
| `　└ createdAt` | string (ISO 8601) | 未解決質問の登録日時 |
| `nextCursor` | string | 次ページ取得用カーソル(末尾は `null`) |

## <span id="API-INQ-002"></span>API-INQ-002 未解決質問詳細・状況切替

<span id="562-get-inquiriesid--patch-inquiriesid"></span>

### 基本情報

| 項目           | 内容                            |
|----------------|---------------------------------|
| API ID         | API-INQ-002                     |
| API 名         | 未解決質問詳細・状況切替        |
| エンドポイント | `/inquiries/{id}`               |
| HTTP メソッド  | GET / PATCH                     |
| 認証           | Cookie + CSRF(PATCH)            |
| 権限           | オーナー / 該当 PJ の `member`+ |

PATCH は状況の手動切替のみを更新可能とし、担当者概念は持たない。

### 処理概要

詳細取得と状況の手動切替(担当者概念は持たない)。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 認証・認可(PATCH は CSRF も)を検証する |
| P-02 | 対象未解決質問を特定する |
| P-03 | GET は詳細を取得する |
| P-04 | PATCH は状況(`open` ↔ `closed`)を更新する(担当者概念・履歴永続化なし) |
| P-05 | 結果を返却する |

### I/O

| テーブル      | C   | R   | U   | D   |
|---------------|-----|-----|-----|-----|
| `T_INQUIRIES` | —   | ◯   | ◯   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{ "id": "未解決質問 ID" }
```

| 項目 | 型     | 説明                        |
|------|--------|-----------------------------|
| `id` | string | 対象の未解決質問の ID。必須 |

#### Request Body

```json
{
  "status": "open" | "closed"
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `status` | enum | 切り替える状況。`open` / `closed`。PATCH 時のみ。任意(指定したものだけ更新) |

Request Body は PATCH 時のもの。各フィールドはオプション(指定したものだけ更新)。状況は `open` ↔ `closed` の双方向遷移を許容(再オープン制限なし)。FAQ 下書き保存・FAQ 公開は本フィールドを変更しない(連動ロジックなし)。状態変更履歴の永続化は行わない。

### レスポンス(200)

GET は未解決質問の詳細、PATCH は更新後の状況。

| 項目 | 型 | 説明 |
|----|----|----|
| `id` | string | 未解決質問の ID |
| `inquiryCode` | string | 未解決質問の管理用識別子 |
| `question` | string | ウィジェット利用者が送信した質問内容 |
| `status` | enum | 状況。`open` / `closed`(PATCH 時は更新後の値) |
| `projectId` | string | 当該未解決質問が属するプロジェクトの ID |
| `createdAt` | string (ISO 8601) | 未解決質問の登録日時 |
| `updatedAt` | string (ISO 8601) | 状況の最終更新日時 |

---

---

<!-- portal-bottom -->
[← API設計](02_api-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
