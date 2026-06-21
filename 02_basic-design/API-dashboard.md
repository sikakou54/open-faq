<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [API設計](02_api-design.md) ／ **ダッシュボード API**
<!-- /portal-top -->

# ダッシュボード API

> **このページは、ダッシュボードサマリ(利用量・要対応・通知失敗の集約)の API 契約を定義します。**
>
> **このページの API**
>
> - API-DASH-001 ダッシュボードサマリ

*版数 v1.6 ・ 更新 2026-06-17 ・ 承認済*

## <span id="API-DASH-001"></span>API-DASH-001 ダッシュボードサマリ

<span id="58a1-get-dashboardsummary"></span>

### 基本情報

| 項目 | 内容 |
|----|----|
| API ID | API-DASH-001 |
| API 名 | ダッシュボードサマリ |
| エンドポイント | `/dashboard/summary` |
| HTTP メソッド | GET |
| 認証 | Cookie |
| 権限 | オーナー / 当該プロジェクトのメンバー(`notification` ブロックの配信失敗・バウンス件数はオーナー専有) |

質問数・未解決数(FR-077)、要対応状況の対応中 / 対応済み内訳(FR-078)、未解決傾向(FR-079)、期間絞り込み(FR-080)、通知失敗・バウンス件数(FR-081)をまとめて返す。`projectId` 未指定時はオーナーのみ契約全体を集約する(メンバーは `projectId` 必須)。期間は `period`(`current_month` / `last_30d`)または `from` / `to` で指定する。

### 処理概要

質問数・未解決・要対応状況・通知失敗 / バウンスをまとめて返す。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 認証・認可(対象プロジェクトへのアクセス権、メンバーは `projectId` 必須)を検証する |
| P-02 | 期間・プロジェクトの質問数・未解決数・要対応状況を集計する |
| P-03 | オーナー向けに通知失敗・バウンス件数を集計する(メンバー指定時は `null`) |
| P-04 | 整形して返却する |

### I/O

| テーブル          | C   | R   | U   | D   |
|-------------------|-----|-----|-----|-----|
| `T_USAGE_METER`   | —   | ◯   | —   | —   |
| `H_QUESTION_LOGS` | —   | ◯   | —   | —   |
| `T_INQUIRIES`     | —   | ◯   | —   | —   |
| `H_NOTIF_LOGS`    | —   | ◯   | —   | —   |

### リクエストパラメータ

#### Query Parameters

```json
{ "period": "current_month", "projectId": "{id}(メンバーは必須)", "from": "任意(period の代わりに範囲指定)", "to": "任意(period の代わりに範囲指定)" }
```

| 項目 | 型 | 説明 |
|----|----|----|
| `period` | enum | 集計期間。任意。`current_month` / `last_30d`。`from` / `to` を指定する場合は不要 |
| `projectId` | string | 対象プロジェクトの ID。オーナーは任意(未指定で契約全体を集約)、メンバーは必須 |
| `from` | string (ISO 8601) | 集計期間の起点。任意(`period` の代わりに範囲指定する場合に使用) |
| `to` | string (ISO 8601) | 集計期間の終点。任意(`period` の代わりに範囲指定する場合に使用) |

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
  "questions": { "total": 2450, "unresolved": 120 },
  "inquiryStatus": { "open": 35, "closed": 85 },
  "topQuestions": [ { "question": "返品方法は?", "count": 42 } ],
  "notification": { "failedCount": 3, "bouncedCount": 1 }
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `period` | object | 集計対象期間 |
| `　└ from` | string (ISO 8601) | 期間の起点 |
| `　└ to` | string (ISO 8601) | 期間の終点 |
| `questions` | object | 質問数の集計 |
| `　└ total` | integer | 期間内の総質問数 |
| `　└ unresolved` | integer | 未解決の質問数 |
| `inquiryStatus` | object | 未解決質問の状況別件数 |
| `　└ open` | integer | 対応中(`open`)の件数 |
| `　└ closed` | integer | 対応済み(`closed`)の件数 |
| `topQuestions` | array\<object\> | 頻出質問の配列 |
| `　└ question` | string | 質問内容 |
| `　└ count` | integer | 当該質問の出現回数 |
| `notification` | object | 通知の配信失敗・バウンス集計(メンバーが `projectId` 指定時は `null`) |
| `　└ failedCount` | integer | 配信失敗件数 |
| `　└ bouncedCount` | integer | バウンス件数 |

`notification.failedCount` / `bouncedCount` は `H_NOTIF_LOGS` の配信失敗・バウンス集計(列定義は [03_テーブル設計/index.md](03_database-design.md))。メンバーが `projectId` 指定で呼んだ場合、本ブロックは `null` を返す。

### エラー

| HTTP ステータス | エラーコード            | 内容                          |
|-----------------|-------------------------|-------------------------------|
| 400             | `VALIDATION_ERROR`      | メンバーが `projectId` 未指定 |
| 403             | `PROJECT_ACCESS_DENIED` | 当該プロジェクトへの権限なし  |

---

<!-- portal-bottom -->
[← API設計](02_api-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
