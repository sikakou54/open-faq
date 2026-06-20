<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [API設計](02_api-design.md) ／ **メール配信 IF**
<!-- /portal-top -->

# メール配信 IF

> **このページは、メール送信 / Webhook 検証を抽象化する内部 IF(`EmailProvider`)の契約を定義します。**
>
> **このページの API**
>
> - API-MAIL-001 メール配信 IF(`EmailProvider`)

*版数 v1.6 ・ 更新 2026-06-17 ・ 承認済*

## <span id="API-MAIL-001"></span>API-MAIL-001 メール配信 IF(`EmailProvider`)

送信(`send`)と Webhook 検証(`verifyWebhook`)を持つ内部抽象インターフェースです。MVP は `ResendEmailProvider` として実装します。

```
export interface EmailProvider {
  send(input: {
    to: string; from: string; reply_to?: string; subject: string;
    html: string; text?: string; headers?: Record<string, string>;
    idempotency_key: string;
  }): Promise<{ message_id: string }>;

  verifyWebhook(headers: Headers, body: string): Promise<{
    valid: boolean;
    event_type: 'sent'|'delivered'|'bounced'|'complained'|'failed'|'opened'|'clicked';
    message_id: string;
    timestamp: string;
  }>;
}
```

MVP は Resend 実装(`ResendEmailProvider`)。

**`send` の戻り値**

| 項目         | 型     | 説明                          |
|--------------|--------|-------------------------------|
| `message_id` | string | 送信したメールのメッセージ ID |

**`verifyWebhook` の戻り値**

| 項目 | 型 | 説明 |
|----|----|----|
| `valid` | boolean | Webhook 署名検証の成否 |
| `event_type` | enum | 配信イベント種別(`sent` / `delivered` / `bounced` / `complained` / `failed` / `opened` / `clicked`) |
| `message_id` | string | 対象メールのメッセージ ID |
| `timestamp` | string | イベント発生時刻 |

### 処理概要

送信(`send`)と Webhook 検証(`verifyWebhook`)を持つ内部抽象インターフェースです。MVP は `ResendEmailProvider` として実装します。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | `send` で宛先・件名・本文をプロバイダへ渡しメールを送信する(冪等キーで重複送信を排除) |
| P-02 | 送信結果のメッセージ ID を返す |
| P-03 | `verifyWebhook` で受信した Webhook の署名を検証する |
| P-04 | 配信イベント種別・メッセージ ID・発生時刻を返す |

---

---

<!-- portal-bottom -->
[← API設計](02_api-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
