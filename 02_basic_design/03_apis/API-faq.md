<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [API設計](index.md) ／ **FAQ 管理 API**
<!-- /portal-top -->

# FAQ 管理 API

> **このページは、FAQ の一覧・CRUD・一括状態変更・CSV 入出力・全文検索・質問ログ検索の API 契約を定義します。**
>
> **このページの API**
>
> - API-FAQ-001 FAQ 一覧
> - API-FAQ-002 FAQ 作成・更新・削除
> - API-FAQ-003 FAQ 一括状態変更
> - API-FAQ-004 FAQ CSV インポート
> - API-FAQ-005 FAQ インポートテンプレート
> - API-FAQ-006 FAQ CSV エクスポート
> - API-FAQ-007 FAQ 全文検索
> - API-FAQ-008 質問ログ検索
> - API-FAQ-009 FAQ 個別取得

*版数 v1.6 ・ 更新 2026-06-17 ・ 承認済*

## <span id="API-FAQ-001"></span>API-FAQ-001 FAQ 一覧

<span id="541-get-faqsstatusdraftprojectidkeywordcursor"></span>

### 基本情報

| 項目 | 内容 |
|----|----|
| API ID | API-FAQ-001 |
| API 名 | FAQ 一覧 |
| エンドポイント | `/faqs` |
| HTTP メソッド | GET |
| 認証 | Cookie |
| 権限 | オーナー / 当該プロジェクトのメンバー |

### 処理概要

状態 / プロジェクト / キーワードで FAQ を一覧取得する。

| 処理 ID | 処理内容                                                      |
|---------|---------------------------------------------------------------|
| P-01    | 認証・認可(オーナー / 当該プロジェクトの利用者)を検証する     |
| P-02    | 状態・プロジェクト・キーワードのフィルタ条件で FAQ を取得する |
| P-03    | ページング(カーソル)で整形して返す                            |

### I/O

| テーブル | C   | R   | U   | D   |
|----------|-----|-----|-----|-----|
| `M_FAQS` | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{
  "status": "draft(任意)",
  "projectId": "(必須)",
  "keyword": "(任意)",
  "cursor": "(共通仕様)",
  "limit": "(共通仕様)"
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `status` | enum | 状態での絞り込み(任意・`draft` / `published` / `hidden`) |
| `projectId` | string | 対象プロジェクトの ID(必須) |
| `keyword` | string | キーワードでの絞り込み(任意) |
| `cursor` | string | 次ページ取得用カーソル(任意・共通ページング仕様) |
| `limit` | integer | 1 ページの取得件数(任意・共通ページング仕様) |

#### Path Parameters

```json
{}
```

#### Request Body

```json
{}
```

### レスポンス(200)

FAQ の配列 + `nextCursor`(構造は API-025 のレスポンスに準ずる)。

| 項目 | 型 | 説明 |
|----|----|----|
| `items` | array\<object\> | フィルタ条件に一致した FAQ の一覧(各要素の構造は API-FAQ-007 全文検索のレスポンスに準ずる) |
| `nextCursor` | string | 次ページ取得用カーソル(末尾は `null`) |

### エラー

403 `PROJECT_ACCESS_DENIED` ほか(本 API のエラー節を参照)。

## <span id="API-FAQ-002"></span>API-FAQ-002 FAQ 作成・更新・削除

<span id="542-post-M_FAQS--patch-faqsid--delete-faqsid"></span>

### 基本情報

| 項目           | 内容                            |
|----------------|---------------------------------|
| API ID         | API-FAQ-002                     |
| API 名         | FAQ 作成・更新・削除            |
| エンドポイント | `/faqs`, `/faqs/{id}`           |
| HTTP メソッド  | POST / PATCH / DELETE           |
| 認証           | Cookie + CSRF                   |
| 権限           | オーナー / 当該プロジェクトのメンバー |

楽観ロック: `version` 必須。`CONFLICT` 時 409。

FAQ の状態(`draft` / `published` / `hidden`)は `status` フィールドで指定し、`PATCH /faqs/{id}` の保存操作で相互に自由遷移できる(専用の公開 API・状態遷移ガードは持たない)。SCR-006 の「保存」ボタンは「状態」ラジオで選択した値をそのまま本 API に渡す。`status='published'` への変更は当該プロジェクトのメンバー(オーナーを含む)が編集画面で内容を確認したうえで明示選択する操作であり、これが FR-030「FAQ の公開前に当該プロジェクトのメンバーが内容を確認できること」を満たす。`published` 設定時は `publishedAt` をサーバ側で記録する。

### 処理概要

FAQ の CRUD と状態(`draft` / `published` / `hidden`)の相互遷移。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 認証・認可(オーナー / 該当プロジェクトの編集権限)を検証する |
| P-02 | 入力値(質問 500 字 / 回答 5,000 字ほか)を検証する |
| P-03 | 更新 / 削除時は `version` による楽観ロックを判定する(不一致は 409) |
| P-04 | FAQ を作成 / 更新 / 論理削除し、指定状態へ遷移する |
| P-05 | `published` へ変更した場合は `publishedAt` を記録する |
| P-06 | 作成 / 更新後の FAQ を返す |

### I/O

| テーブル    | C   | R   | U   | D   |
|-------------|-----|-----|-----|-----|
| `M_FAQS`    | ◯   | ◯   | ◯   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{ "id": "FAQ ID(PATCH / DELETE 時)" }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `id` | string | 対象 FAQ の ID(PATCH / DELETE 時は必須・パス内で指定。POST 時は不要) |

#### Request Body

```json
{
  "question": "...",
  "answer": "...",
  "category": "...",
  "status": "draft | published | hidden",
  "version": 1
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `question` | string | 質問文(必須・最大 500 字) |
| `answer` | string | 回答文(必須・最大 5,000 字) |
| `category` | string | カテゴリ(任意) |
| `status` | enum | FAQ 状態(必須・`draft` / `published` / `hidden`) |
| `version` | integer | 楽観ロック用バージョン番号(更新 / 削除時は必須・不一致は 409) |

Request Body は FAQ 内容(POST は新規)。

### レスポンス(200 / 201)

作成 / 更新後の FAQ(`publishedAt` を含む)。

| 項目 | 型 | 説明 |
|----|----|----|
| `id` | string | 作成 / 更新した FAQ の ID |
| `question` | string | 質問文 |
| `answer` | string | 回答文 |
| `category` | string | カテゴリ |
| `status` | enum | FAQ 状態(`draft` / `published` / `hidden`) |
| `version` | integer | 楽観ロック用バージョン番号 |
| `publishedAt` | string (ISO 8601) | 公開日時(`published` 化時に記録、未公開は `null`) |

### エラー

| HTTP ステータス | エラーコード       | 内容                                    |
|-----------------|--------------------|-----------------------------------------|
| 409             | `CONFLICT`         | 楽観ロック競合(`version` 不一致)        |
| 400             | `VALIDATION_ERROR` | 質問 500 字 / 回答 5,000 字超過ほか(§3) |

## <span id="API-FAQ-003"></span>API-FAQ-003 FAQ 一括状態変更

<span id="542a-post-faqsbulk-status"></span>

### 基本情報

| 項目           | 内容                            |
|----------------|---------------------------------|
| API ID         | API-FAQ-003                     |
| API 名         | FAQ 一括状態変更                |
| エンドポイント | `/faqs/bulk-status`             |
| HTTP メソッド  | POST                            |
| 認証           | Cookie + CSRF                   |
| 権限           | オーナー / 当該プロジェクトのメンバー |

選択した複数 FAQ の状態を一括で `draft` / `published` / `hidden` に変更する。1 リクエストの上限は **50 件**(SCR-006 の BulkActionBar 上限、[画面設計.md](../01_screens/index.md))。超過時は 400 `VALIDATION_ERROR`。処理は行単位で評価し、対象外(他契約 / 論理削除済み)の ID は当該行のみ失敗として集計する(オーナー境界違反は §2.2 に従い結果から除外し成功扱いにしない)。`published` へ変更した行は `publishedAt` をサーバ側で記録する。

### 処理概要

選択した複数 FAQ の状態を一括で変更する(1 リクエスト上限 50 件)。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 認証・認可(オーナー / 該当プロジェクトの編集権限)を検証する |
| P-02 | 件数上限(50 件)と状態値を検証する(超過時は 400) |
| P-03 | 各 ID を行単位で評価し、対象外(他契約 / 論理削除済み)は当該行のみ失敗として集計する |
| P-04 | 対象 FAQ の状態を一括変更し、`published` 化した行は `publishedAt` を記録する |
| P-05 | 成功件数と失敗明細を返す |

### I/O

| テーブル | C   | R   | U   | D   |
|----------|-----|-----|-----|-----|
| `M_FAQS` | —   | ◯   | ◯   | —   |

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
{ "ids": ["faq_...", "faq_..."], "status": "published" }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `ids` | array | 状態を変更する FAQ の ID リスト(必須・1 リクエスト上限 50 件) |
| `status` | enum | 変更後の状態(必須・`draft` / `published` / `hidden`) |

### レスポンス(200)

```json
{ "succeeded": 48, "failed": [ { "id": "faq_...", "code": "NOT_FOUND" } ] }
```

| 項目        | 型              | 説明                                   |
|-------------|-----------------|----------------------------------------|
| `succeeded` | integer         | 状態変更に成功した件数                 |
| `failed`    | array\<object\> | 失敗した行の明細                       |
| `　└ id`    | string          | 失敗した FAQ の ID                     |
| `　└ code`  | string          | 失敗理由のエラーコード(例 `NOT_FOUND`) |

### エラー

| HTTP ステータス | エラーコード            | 内容                         |
|-----------------|-------------------------|------------------------------|
| 400             | `VALIDATION_ERROR`      | 50 件超過 / 不正な `status`  |
| 403             | `PROJECT_ACCESS_DENIED` | 当該プロジェクトへの権限なし |

## <span id="API-FAQ-004"></span>API-FAQ-004 FAQ CSV インポート

<span id="543-post-faqsimport"></span>

### 基本情報

| 項目           | 内容                            |
|----------------|---------------------------------|
| API ID         | API-FAQ-004                     |
| API 名         | FAQ CSV インポート              |
| エンドポイント | `/faqs/import`                  |
| HTTP メソッド  | POST                            |
| 認証           | Cookie + CSRF                   |
| 権限           | オーナー / 当該プロジェクトのメンバー |

### 処理概要

CSV による FAQ の一括取込(新規 / 上書き)。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 認証・認可(オーナー / 該当プロジェクトの編集権限)を検証する |
| P-02 | 受理形式(CSV・UTF-8・ヘッダ行・上限 1000 件)を検証する(不正は 415 / 400) |
| P-03 | 取込ジョブを受け付け、非同期処理として開始する |
| P-04 | 各行の `FAQ ID` で 新規 / 上書き / 当該契約に存在しない ID(行失敗)を判定し取り込む |
| P-05 | ジョブ ID と受付状態を返す |

### I/O

| テーブル    | C   | R   | U   | D   |
|-------------|-----|-----|-----|-----|
| `M_FAQS`    | ◯   | ◯   | ◯   | —   |

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

```
multipart/form-data { file: <CSV> }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `file` | string | 取込対象の CSV ファイル(必須・`multipart/form-data`、UTF-8、ヘッダ行必須、1 ファイル最大 1000 件) |

受理形式は **CSV のみ**(UTF-8、BOM 許容、ヘッダ行必須、1 ファイル最大 1000 件)。**JSON 形式は受理しない**(不正形式は 415 / 400、E-INPUT-CSV-INVALID)。CSV 列構成は `FAQ ID, 質問, 回答, カテゴリ`。各行の `FAQ ID` で **空欄 = 新規(`status=draft`)/ 既存 ID 一致 = 上書き(状態維持)/ 当該契約に存在しない ID = 当該行を失敗**(行単位エラー、E-INPUT-CSV-FAQID-NOTFOUND)と判定する。`status` 列は受理しない。

### レスポンス(202)

```json
{ "jobId": "job_...", "status": "processing" }
```

| 項目     | 型     | 説明                           |
|----------|--------|--------------------------------|
| `jobId`  | string | 受け付けた取込ジョブの ID      |
| `status` | enum   | ジョブの受付状態(`processing`) |

### エラー

| HTTP ステータス | エラーコード               | 内容                        |
|-----------------|----------------------------|-----------------------------|
| 415 / 400       | E-INPUT-CSV-INVALID        | CSV 以外 / 不正形式         |
| (行単位)        | E-INPUT-CSV-FAQID-NOTFOUND | 当該契約に存在しない FAQ ID |

## <span id="API-FAQ-005"></span>API-FAQ-005 FAQ インポートテンプレート

<span id="544-get-faqsimporttemplate"></span>

### 基本情報

| 項目           | 内容                                            |
|----------------|-------------------------------------------------|
| API ID         | API-FAQ-005                                     |
| API 名         | FAQ インポートテンプレート                      |
| エンドポイント | `/faqs/import/template`                         |
| HTTP メソッド  | GET                                             |
| 認証           | Cookie                                          |
| 権限           | オーナー / 当該プロジェクトのメンバー(API-022 と同一) |

### 処理概要

ヘッダ行のみの CSV テンプレートを返す。

| 処理 ID | 処理内容                                                    |
|---------|-------------------------------------------------------------|
| P-01    | 認証・認可(オーナー / 該当プロジェクトの編集権限)を検証する |
| P-02    | ヘッダ行のみの CSV テンプレートを生成する                   |
| P-03    | ダウンロード用ヘッダを付与して `text/csv` で返す            |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| (DB アクセスなし) | —   | —   | —   | —   |

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

ヘッダ行のみの CSV テンプレート(`FAQ ID,質問,回答,カテゴリ`)を `text/csv; charset=utf-8`(UTF-8 BOM 付与可)で返す。`Content-Disposition: attachment; filename="faq_import_template.csv"`。

| 項目 | 型 | 説明 |
|----|----|----|
| (本体) | string | ヘッダ行のみの CSV ファイル(列 `FAQ ID` / `質問` / `回答` / `カテゴリ`)。JSON 本体は返さない |

## <span id="API-FAQ-006"></span>API-FAQ-006 FAQ CSV エクスポート

<span id="545-get-faqsexport"></span>

### 基本情報

| 項目           | 内容                            |
|----------------|---------------------------------|
| API ID         | API-FAQ-006                     |
| API 名         | FAQ CSV エクスポート            |
| エンドポイント | `/faqs/export`                  |
| HTTP メソッド  | GET                             |
| 認証           | Cookie                          |
| 権限           | オーナー / 当該プロジェクトのメンバー |

### 処理概要

一覧フィルタ適用結果を CSV で出力する。

| 処理 ID | 処理内容                                                    |
|---------|-------------------------------------------------------------|
| P-01    | 認証・認可(オーナー / 該当プロジェクトの編集権限)を検証する |
| P-02    | 一覧と同じフィルタ条件で対象 FAQ を取得する                 |
| P-03    | CSV(UTF-8)に整形しダウンロードとして返す                    |

### I/O

| テーブル | C   | R   | U   | D   |
|----------|-----|-----|-----|-----|
| `M_FAQS` | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{
  "status": "(任意・一覧フィルタに準ずる)",
  "projectId": "(一覧フィルタに準ずる)",
  "keyword": "(任意・一覧フィルタに準ずる)"
}
```

| 項目        | 型     | 説明                                               |
|-------------|--------|----------------------------------------------------|
| `status`    | enum   | 状態での絞り込み(任意・一覧フィルタに準ずる)       |
| `projectId` | string | 対象プロジェクトの ID(一覧フィルタに準ずる)        |
| `keyword`   | string | キーワードでの絞り込み(任意・一覧フィルタに準ずる) |

#### Path Parameters

```json
{}
```

#### Request Body

```json
{}
```

Query Parameters は一覧フィルタに準ずる。

### レスポンス(200)

一覧フィルタ適用結果を **CSV(UTF-8、`text/csv`)** で返す(JSON 形式は提供しない)。

| 項目 | 型 | 説明 |
|----|----|----|
| (本体) | string | 一覧フィルタ適用結果の CSV ファイル(UTF-8、`text/csv`)。JSON 本体は返さない |

## <span id="API-FAQ-007"></span>API-FAQ-007 FAQ 全文検索

<span id="546-get-faqssearchfaq-"></span>

### 基本情報

| 項目           | 内容                            |
|----------------|---------------------------------|
| API ID         | API-FAQ-007                     |
| API 名         | FAQ 全文検索                    |
| エンドポイント | `/projects/{id}/faqs/search`    |
| HTTP メソッド  | GET                             |
| 認証           | Cookie                          |
| 権限           | オーナー / 当該プロジェクトのメンバー |

検索対象は現在開いているプロジェクトに属する FAQ に限る(§2.2 オーナー境界 + プロジェクト境界)。並び替え・ページングは共通仕様(§2.1)に従う。

### 処理概要

当該プロジェクトの FAQ をキーワードで全文検索する。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 認証・認可(オーナー / 当該プロジェクトの利用者)を検証する |
| P-02 | 検索範囲を当該プロジェクトの FAQ に限定する(オーナー境界 + プロジェクト境界) |
| P-03 | キーワードで全文検索し、指定の並び順(関連度 / 更新日時)で並べる |
| P-04 | ページング(カーソル)で整形して返す |

### I/O

| テーブル     | C   | R   | U   | D   |
|--------------|-----|-----|-----|-----|
| `M_FAQS`     | —   | ◯   | —   | —   |
| `TP_FAQ_FTS` | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{
  "keyword": "(必須)",
  "status": "(任意・draft / published / hidden)",
  "sort": "relevance(既定) / updated_at",
  "cursor": "(共通仕様)",
  "limit": "(50〜200)"
}
```

| 項目      | 型      | 説明                                                     |
|-----------|---------|----------------------------------------------------------|
| `keyword` | string  | 検索キーワード(必須)                                     |
| `status`  | enum    | 状態での絞り込み(任意・`draft` / `published` / `hidden`) |
| `sort`    | enum    | 並び順(任意・`relevance`(既定) / `updated_at`)           |
| `cursor`  | string  | 次ページ取得用カーソル(任意・共通ページング仕様)         |
| `limit`   | integer | 1 ページの取得件数(任意・50〜200)                        |

#### Path Parameters

```json
{ "id": "プロジェクト ID" }
```

| 項目 | 型     | 説明                                          |
|------|--------|-----------------------------------------------|
| `id` | string | 検索対象プロジェクトの ID(必須・パス内で指定) |

#### Request Body

```json
{}
```

全文検索方式・対象列は [データベース設計.md](../04_database/index.md)(FTS インデックス)を正本とする。

### レスポンス(200)

```json
{ "items": [ { "id": "faq_...", "question": "...", "answer": "...", "status": "published", "category": "...", "score": 0.82, "updatedAt": "..." } ], "nextCursor": null }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `items` | array\<object\> | 検索に一致した FAQ の一覧 |
| `　└ id` | string | FAQ ID |
| `　└ question` | string | 質問文 |
| `　└ answer` | string | 回答文 |
| `　└ status` | enum | FAQ 状態(`draft` / `published` / `hidden`) |
| `　└ category` | string | カテゴリ |
| `　└ score` | number | 検索の関連度スコア |
| `　└ updatedAt` | string (ISO 8601) | 更新日時 |
| `nextCursor` | string | 次ページ取得用カーソル(末尾は `null`) |

## <span id="API-FAQ-008"></span>API-FAQ-008 質問ログ検索

<span id="547-get-question-logssearch"></span>

### 基本情報

| 項目           | 内容                                  |
|----------------|---------------------------------------|
| API ID         | API-FAQ-008                           |
| API 名         | 質問ログ検索                          |
| エンドポイント | `/projects/{id}/question-logs/search` |
| HTTP メソッド  | GET                                   |
| 認証           | Cookie                                |
| 権限           | オーナー / 当該プロジェクトのメンバー       |

検索対象は現在開いているプロジェクトに属する質問ログに限る。

### 処理概要

当該プロジェクトの質問ログをキーワード・期間で検索する。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 認証・認可(オーナー / 当該プロジェクトの利用者)を検証する |
| P-02 | 検索範囲を当該プロジェクトの質問ログに限定する |
| P-03 | キーワード・期間・回答有無のフィルタで検索し、作成日時降順で並べる |
| P-04 | ページング(カーソル)で整形して返す |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `H_QUESTION_LOGS` | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{
  "keyword": "(任意)",
  "from": "(任意・ISO 8601、期間)",
  "to": "(任意・ISO 8601、期間)",
  "answerType": "(任意・answered / unanswered)",
  "sort": "created_at 降順(既定)",
  "cursor": "(共通仕様)",
  "limit": "(50〜200)"
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `keyword` | string | 検索キーワード(任意) |
| `from` | string (ISO 8601) | 検索期間の開始日時(任意) |
| `to` | string (ISO 8601) | 検索期間の終了日時(任意) |
| `answerType` | enum | 回答有無での絞り込み(任意・`answered` / `unanswered`) |
| `sort` | enum | 並び順(任意・`created_at` 降順が既定) |
| `cursor` | string | 次ページ取得用カーソル(任意・共通ページング仕様) |
| `limit` | integer | 1 ページの取得件数(任意・50〜200) |

#### Path Parameters

```json
{ "id": "プロジェクト ID" }
```

| 項目 | 型     | 説明                                          |
|------|--------|-----------------------------------------------|
| `id` | string | 検索対象プロジェクトの ID(必須・パス内で指定) |

#### Request Body

```json
{}
```

対象列・全文検索方式は [データベース設計.md](../04_database/index.md) を正本とする。

### レスポンス(200)

```json
{ "items": [ { "id": "qlog_...", "question": "...", "answerType": "unanswered", "confidence": 0.42, "inquiryId": "inq_..." | null, "createdAt": "..." } ], "nextCursor": null }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `items` | array\<object\> | 検索に一致した質問ログの一覧 |
| `　└ id` | string | 質問ログ ID |
| `　└ question` | string | 質問文 |
| `　└ answerType` | enum | 回答有無(`answered` / `unanswered`) |
| `　└ confidence` | number | 回答の確信度スコア |
| `　└ inquiryId` | string | 関連する未解決質問の ID(無い場合は `null`) |
| `　└ createdAt` | string (ISO 8601) | 質問の作成日時 |
| `nextCursor` | string | 次ページ取得用カーソル(末尾は `null`) |

## <span id="API-FAQ-009"></span>API-FAQ-009 FAQ 個別取得

### 基本情報

| 項目           | 内容                                    |
|----------------|-----------------------------------------|
| API ID         | API-FAQ-009                             |
| API 名         | FAQ 個別取得                            |
| エンドポイント | `/faqs/{id}`                            |
| HTTP メソッド  | GET                                     |
| 認証           | Cookie                                  |
| 権限           | オーナー / 当該プロジェクトのメンバー   |

### 処理概要

指定した FAQ ID の詳細情報を 1 件取得する。

| 処理 ID | 処理内容                                                    |
|---------|-------------------------------------------------------------|
| P-01    | 認証・認可(オーナー / 該当プロジェクトの編集権限)を検証する |
| P-02    | 指定 FAQ が当該契約・プロジェクトに属するか検証する         |
| P-03    | FAQ の詳細情報を返す                                        |

### I/O

| テーブル | C   | R   | U   | D   |
|----------|-----|-----|-----|-----|
| `M_FAQS` | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{}
```

#### Path Parameters

```json
{ "id": "FAQ ID(必須)" }
```

| 項目 | 型     | 説明                              |
|------|--------|-----------------------------------|
| `id` | string | 取得対象 FAQ の ID(必須・パス内) |

#### Request Body

```json
{}
```

### レスポンス(200)

```json
{ "id": "faq_...", "question": "...", "answer": "...", "category": "...", "status": "draft", "version": 1, "publishedAt": null }
```

| 項目          | 型                | 説明                                                         |
|---------------|-------------------|--------------------------------------------------------------|
| `id`          | string            | FAQ ID                                                       |
| `question`    | string            | 質問文                                                       |
| `answer`      | string            | 回答文                                                       |
| `category`    | string            | カテゴリ                                                     |
| `status`      | enum              | FAQ 状態(`draft` / `published` / `hidden`)                   |
| `version`     | integer           | 楽観ロック用バージョン番号                                   |
| `publishedAt` | string (ISO 8601) | 公開日時(`published` 化時に記録、未公開は `null`)            |

### エラー

| HTTP ステータス | エラーコード            | 内容                                     |
|-----------------|-------------------------|------------------------------------------|
| 403             | `PROJECT_ACCESS_DENIED` | 当該プロジェクトへの権限なし             |
| 404             | `NOT_FOUND`             | 指定した FAQ が存在しない / 論理削除済み |

---

<!-- portal-bottom -->
[← API設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
