<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [API設計](index.md) ／ **外部 Webhook**
<!-- /portal-top -->

# 外部 Webhook

> **このページは、メール配信プロバイダ(Resend)からの配信状態 Webhook 受信の契約を定義します。**
>
> **このページの API**
>
> - API-WHK-001 外部 Webhook(Resend)

*版数 v1.6 ・ 更新 2026-06-17 ・ 承認済*

## <span id="API-WHK-001"></span>API-WHK-001 外部 Webhook(Resend)

<span id="5131-post-webhooksresend"></span>

### 基本情報

| 項目           | 内容                         |
|----------------|------------------------------|
| API ID         | API-WHK-001                  |
| API 名         | 外部 Webhook(Resend)         |
| エンドポイント | `/webhooks/resend`           |
| HTTP メソッド  | POST                         |
| 認証           | Resend 署名検証(HMAC-SHA256) |
| 権限           | —(署名検証のみ)              |

### 処理概要

メール配信状態 Webhook を受信し配信状態 / 抑制リストを更新する。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | Resend 署名(HMAC-SHA256)を検証する(失敗時は 401) |
| P-02 | イベント種別を判定する |
| P-03 | `H_NOTIF_LOGS.delivery_state` を遷移する |
| P-04 | `bounced` / `complained` の場合は `M_EMAIL_SUPPRESS` に追加する(全契約横断) |
| P-05 | 受領応答を返す |

### I/O

| テーブル           | C   | R   | U   | D   |
|--------------------|-----|-----|-----|-----|
| `H_NOTIF_LOGS`     | —   | —   | ◯   | —   |
| `M_EMAIL_SUPPRESS` | ◯   | —   | —   | —   |
| `H_AUDIT_LOGS`     | ◯   | —   | —   | —   |

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

(Resend 仕様準拠):

```json
{
  "type": "email.delivered|email.bounced|email.complained|email.delivery_delayed",
  "data": {
    "message_id": "...",
    "to": "...",
    "subject": "...",
    "timestamp": "..."
  }
}
```

| 項目 | 型 | 説明 |
|----|----|----|
| `type` | enum | 配信イベント種別(`email.delivered` / `email.bounced` / `email.complained` / `email.delivery_delayed`) |
| `data` | object | イベント詳細データ |
| 　└ `message_id` | string | 対象メールのメッセージ ID |
| 　└ `to` | string | 宛先メールアドレス |
| 　└ `subject` | string | メール件名 |
| 　└ `timestamp` | string (ISO 8601) | イベント発生時刻 |

### エラー

| HTTP ステータス | エラーコード        | 内容                           |
|-----------------|---------------------|--------------------------------|
| 401             | `SIGNATURE_INVALID` | 署名検証失敗                   |
| 200             | (冪等)              | 既存処理結果を返却(冪等性違反) |

---

<!-- portal-bottom -->
[← API設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
