# API 設計書(運営者)

## 1. 文書概要

### 1.1 目的

運営者システムのすべての API(管理 API / 4-eyes 承認 API / 連携 IF #1〜#12(運営者主管)/ Stripe Webhook 一次受信)について、エンドポイント / 認証・認可 / 4-eyes 種別 / リクエスト / レスポンス / ステータスコード / エラー仕様を一元化する。

### 1.2 対象範囲

- 対象: 運営者向け管理 API(認証 / MFA / 4-eyes / 削除データ / AI パラメータ / 契約上書き / お知らせ / 監査 / Webhook / PII 報告)、運営者 → メインの連携 IF 送信(#1 / #2 / #4 / #5 / #6 / #7 / #10 / #12)、メイン → 運営者の受信(#8 / #9)、Stripe Webhook 一次受信
- 対象外: 利用者向け管理 API([01_メインシステム/個別設計書群/03_API設計書.md](../../01_メインシステム/個別設計書群/03_API設計書.md))

### 1.3 版数

| 項目 | 値 |
|---|---|
| 版数 | 1.0 |
| 更新日 | 2026-05-17 |

### 1.4 関連ドキュメント

| ドキュメント名 | 役割 | 参照先 |
|---|---|---|
| 索引 | 11 ドキュメント体系の俯瞰 | [00_索引.md](00_索引.md) |
| 画面設計書 | API を呼び出す画面 | [02_画面設計書.md](02_画面設計書.md) |
| テーブル定義書 | API が操作するテーブル | [04_テーブル定義書.md](04_テーブル定義書.md) |
| 認証・認可設計書 | 6 段認可判定 / 4-eyes 承認 | [09_認証認可設計書.md](09_認証認可設計書.md) |
| エラー設計書 | ステータスコード / エラー詳細 | [06_エラー設計書.md](06_エラー設計書.md) |
| メッセージ一覧 | エラー文言 | [07_メッセージ一覧.md](07_メッセージ一覧.md) |
| 権限設計書 | 4-eyes 対象 10 操作 | [05_権限設計書.md](05_権限設計書.md) |
| 課金・請求設計書 | Stripe Webhook 一次受信 / DLQ リプレイ | [11_課金請求設計書.md](11_課金請求設計書.md) |
| メイン側 API 設計書 | 連携 IF 受信側 | [../../01_メインシステム/個別設計書群/03_API設計書.md](../../01_メインシステム/個別設計書群/03_API設計書.md) |

## 2. API 一覧

### 2.1 機能ブロック別 API(§6.4)

| 機能ブロック | 主要 API | 認証 | Idempotency | 4-eyes |
|---|---|---|---|---|
| 運営者認証 | `POST /admin/v1/auth/login`, `/auth/mfa/verify`, `/auth/reauth` | Cookie + CSRF | - | - |
| 4-eyes 申請承認 | `POST /admin/v1/approvals`, `/approvals/{id}/approve|reject|withdraw` | Cookie + Re-Auth | `approval_id` | フロー中核 |
| 削除データ参照 | `GET /admin/v1/deleted-resources` | Cookie | - | - |
| 削除データ復元 | `POST /admin/v1/restorations` | Cookie + Re-Auth | `restoration_id` | 承認ログ |
| AI パラメータ | `PUT /admin/v1/ai-parameters/{scope}/{id}` | Cookie + Re-Auth | `parameter_revision` | **ハードゲート** |
| レート/予算上書き | `PUT /admin/v1/overrides/rate-limit/{id}`, `/budget/{id}` | Cookie + Re-Auth | `override_id` | 承認ログ |
| お知らせ配信 | `POST /admin/v1/announcements`, `/{id}/schedule|cancel` | Cookie + Re-Auth | `announcement_id` | 承認ログ(即時配信のみ)|
| 監査ログ | `GET /admin/v1/audit-logs`, `POST /audit-logs/exports` | Cookie | `export_id` | - |
| Webhook リプレイ | `POST /admin/v1/webhooks/replay` | Cookie + Re-Auth | `replay_id` | 承認ログ |
| PII 報告 | `POST /admin/v1/pii-rules/revisions` | Cookie + Re-Auth | `rule_revision` | 承認ログ |
| Stripe Webhook 受信 | `POST /webhooks/stripe` | Stripe 署名 | `event_id` | - |

## 3. 共通仕様

### 3.1 認証ヘッダ / セッション

| 項目 | 値 |
|---|---|
| Base URL | `https://admin.open-faq.example.com/admin/api/v1` |
| Content-Type | Request: `application/json` / Response: `application/json` / Error: `application/problem+json`(RFC 7807) |
| 日時形式 | ISO 8601 UTC |
| ID 形式 | ULID(26 文字)、Stripe ID 例外(`evt_*`, `sub_*`, `inv_*`, `cn_*`)|
| ページング | カーソル方式(`cursor`, `limit` 50〜200)|
| Idempotency | `Idempotency-Key` ヘッダ(ULID 推奨、24h 保管)|
| トレース | `X-Trace-Id: <ULID>` レスポンスヘッダ |
| パスワードハッシュ | Argon2id `m=128MB, t=4, p=4, salt=16B` |
| パスワード要件 | 12 文字以上、大文字+小文字+数字+記号各 1 文字以上 |
| セッション TTL | 8 時間絶対 / 30 分無操作 |
| 再認証有効期間 | **5 分以内、1 回限り** |
| ロックアウト | 5 連続失敗で `(IP × user_id)` 単位 15 分 |
| MFA | TOTP + 回復コード(Argon2id ハッシュ保管)|
| Cookie 属性 | `Secure; HttpOnly; SameSite=Strict; Domain=admin.open-faq.example.com; Path=/` |
| CSRF | 状態変更系で `X-CSRF-Token` ヘッダ必須 |
| レート制限 | 600 req/min/運営者(超過時 429)|

エラーレスポンス(RFC 7807):
```json
{
  "type": "https://docs.open-faq.example.com/errors/FORBIDDEN_HARD_GATE",
  "title": "Hard gate requires approval",
  "status": 403,
  "code": "FORBIDDEN_HARD_GATE",
  "detail": "action=ai_parameter.update requires X-Approval-Id header",
  "trace_id": "01J9V0...",
  "instance": "/admin/api/v1/ai-parameters/owner/01J9..."
}
```

### 3.2 ticket_id 入力規約

| ヘッダ | 用途 | 形式 |
|---|---|---|
| `X-Op-Ticket-Id` | 対応チケット ID(クリティカル操作必須)| 任意文字列、最大 64 文字。例: `JIRA-12345` / `INC-001` / `#1234` |

### 3.3 再認証(5 分以内)

ヘッダ: `X-Reauth-Id: <reauth_id>`(再認証から 5 分以内、1 回限り)

未保持時は 403 + 「再認証が必要です」(MSG-OP-REAUTH-REQUIRED、E-OP-REAUTH-REQUIRED)

### 3.4 4-eyes 承認チェック

ヘッダ: `X-Approval-Id: <approval_id>`(4-eyes ハードゲート操作時必須)

詳細フローは [09_認証認可設計書.md §7](09_認証認可設計書.md) を正本とする。

### 3.5 Stripe Webhook 一次受信仕様

詳細は §5.7 を参照。Stripe 署名検証 + 冪等性 + ペイロード差分検出。

### 3.6 連携 IF 共通仕様(mTLS + JWT)

メイン側 [03_API設計書.md §3.4 / §3.5](../../01_メインシステム/個別設計書群/03_API設計書.md) と整合。

## 4. レート制限・キャパシティ(運営者側 §11.7、全 17 項目)

| 機能 | リミット | 関連 |
|---|---|---|
| 監査ログ検索期間 | 最大 1 年 | FR-232 |
| 監査ログ検索ヒット | 最大 100 万件 | FR-232 |
| 監査ログエクスポート | 最大 10 万行(自動分割)| FR-232 |
| ページング | カーソル方式 100 件/ページ | FR-232 |
| DLQ 保持(Queues)| 4 日 | NFR-809 |
| DLQ R2 退避 | 30 日 | NFR-809 |
| Webhook リプレイ範囲 | 直近 30 日 | FR-302 |
| 4-eyes 承認待 TTL | **72 時間** | §6.3.1 |
| お知らせ予約上限 | 最大 30 日先 | FR-149 |
| お知らせ取消窓 | 配信開始 5 分前 | FR-149 |
| 運営者セッション | 8 時間絶対 / 30 分無操作 | D-18 |
| 再認証セッション | 5 分以内(1 回限り)| FR-005 |
| DLQ 自動 BO 間隔 | 1m → 4m → 16m | FR-302 |
| DLQ 自動 BO 最大回数 | 3 回(超過で永久失敗)| FR-302 |
| DLQ → 手動リプレイ移行 | 1 時間 | FR-302 |
| お知らせ失敗 BO | 1m → 4m → 16m(3 回)| FR-149 |
| 4-eyes 承認後未実行 TTL | 72 時間 | §6.3.1 |

## 5. API 詳細

### 5.1 運営者認証 API

#### 5.1.1 `POST /admin/v1/auth/login`

| 機能ID | F-OP-001 |
| 認証要否 | 不要(**IP 許可リスト適用**)|
| 関連画面 | SCR-AUTH |

リクエスト:
```json
{
  "email": "ops@example.com",
  "password": "..."
}
```

レスポンス(200): `{ "sessionId": "01J...", "csrfToken": "...", "mfaRequired": true, "mfaSetupRequired": false }` + Cookie 設定

エラー: 401 `INVALID_CREDENTIALS`(E-OP-AUTH-CREDENTIAL)、423 `LOCKED`(5 連続失敗、E-OP-AUTH-LOCKED)、400 `VALIDATION_ERROR`、401(IP allowlist 拒否、E-OP-IP-DENIED)

監査: `operator.login.attempt`(1y)

#### 5.1.2 `POST /admin/v1/auth/mfa/verify`

| 関連画面 | SCR-AUTH |
| 4-eyes 種別 | - |

リクエスト: `{ "code": "123456" }` または `{ "recoveryCode": "ABCDEF-..." }`

レスポンス(200): `{ "mfaVerifiedAt": "...", "expiresAt": "..." }`
エラー: 401 `MFA_INVALID_CODE`(E-OP-MFA-FAILED)、423 `LOCKED`(5 連続失敗)

監査: `operator.mfa.verify`(5y)

#### 5.1.3 `POST /admin/v1/auth/mfa/setup` / `GET /admin/v1/auth/mfa/setup?token=...`

| 認証 | 招待トークン(`mfa-setup:<operator_id>` KV、72h)|
| 関連画面 | SCR-AUTH-M1 |

GET レスポンス(QR + 秘密鍵 + 回復コード 10 個発行):
```json
{
  "qrCodeDataUrl": "data:image/png;base64,...",
  "secret": "BASE32...",
  "recoveryCodes": ["...", "..."]
}
```

POST リクエスト: `{ "setupToken": "...", "totpCode": "...", "recoveryCodesStored": true }`
レスポンス(200): `{ "mfaSetupCompletedAt": "..." }`
エラー: 401 `TOKEN_EXPIRED`(E-OP-MFA-SETUP-EXPIRED)、401 `TOTP_INVALID`、401 `TOKEN_ALREADY_USED`

監査: `operator.mfa.setup`(5y)

#### 5.1.4 `POST /admin/v1/me/reauth`(再認証)

| 機能ID | F-OP-004 |
| 認証 | セッション + MFA 完了 |

リクエスト: `{ "password": "...", "mfaToken": "..." }`
レスポンス(200): `{ "reauthenticatedAt": "...", "expiresAt": "<now+5min>", "reauthId": "01J..." }`
エラー: 401 `INVALID_CREDENTIALS`、423 `LOCKED`(15 分)

監査: `operator.reauth`(5y)

### 5.2 4-eyes 承認 API(本書の中核)

#### 5.2.1 `POST /admin/v1/approvals`(申請)

| 機能ID | F-OP-005 |
| 認証要否 | 要(service_operator)|
| 4-eyes 種別 | 申請フロー発火点 |
| 関連画面 | SCR-APPROVALS-M1 |
| 関連テーブル | `operator_approvals` |

リクエスト:
```json
{
  "actionCode": "ai_parameter.update",
  "targetType": "...",
  "targetId": "...",
  "payloadJson": { /* 操作ペイロード */ },
  "payloadHash": "<sha256hex>",
  "reason": "申請理由",
  "ticketId": "TKT-1234"
}
```

レスポンス(201): `{ "approvalId": "01J...", "expiresAt": "<now+72h>", "payloadHash": "<hex>" }`
エラー: 409 `APPROVAL_PENDING`(同一操作 5 分以内二重)、409 `PAYLOAD_HASH_MISMATCH`、400 `VALIDATION_ERROR`

監査: `operator_approval.request`(5y)

#### 5.2.2 `POST /admin/v1/approvals/{id}/approve`(承認)

| 機能ID | F-OP-006 |
| 認証 | 要(service_operator、**申請者以外**)|
| 4-eyes 種別 | 承認ハードゲート |
| 関連画面 | SCR-APPROVALS-M2 |

リクエスト: `{ "comment": "..." }` + `X-Approval-Id`(承認者トークン)
レスポンス(200): `{ "state": "approved", "approvedAt": "..." }`
エラー: 403 `FORBIDDEN_SELF_APPROVE`(E-OP-4EYES-SELF)、410 `APPROVAL_EXPIRED`(E-OP-4EYES-EXPIRED)、409 `APPROVAL_PAYLOAD_MISMATCH`(E-OP-4EYES-PAYLOAD-CHANGED)

監査: `operator_approval.approve`(5y)

#### 5.2.3 `POST /admin/v1/approvals/{id}/reject`(却下)

| 認可条件 | 申請者以外、**再認証必須** |
| 関連画面 | SCR-APPROVALS-M2 |

リクエスト: `{ "comment": "<必須>" }`
レスポンス(200): `{ "state": "rejected", "rejectedAt": "..." }`
エラー: 403 `FORBIDDEN_SELF_APPROVE`

監査: `operator_approval.reject`(5y)

#### 5.2.4 `POST /admin/v1/approvals/{id}/withdraw`(取下げ)

| 認可条件 | **申請者本人のみ** |

リクエスト: `{ "comment": "..." }`
レスポンス(200): `{ "state": "withdrawn", "withdrawnAt": "..." }`
エラー: 403 `FORBIDDEN`(申請者以外)、409 `CONFLICT`(`requested` 以外)

監査: `operator_approval.withdraw`(5y)

### 5.3 削除データ参照・復元 API

#### 5.3.1 `GET /admin/v1/deleted-resources`

| 機能ID | F-OP-009 |
| 関連画面 | SCR-090 |

クエリ: `ownerSearch`, `resourceTypes[]`, `deletionTypes[]`, `from`, `to`, `cursor`, `limit`

レスポンス(200):
```json
{
  "items": [
    {
      "resourceType": "owner",
      "resourceId": "...",
      "contractOwnerUserId": "...",
      "deletionType": "deleted_pending",
      "deletedAt": "...",
      "scheduledPhysicalDeleteAt": "...",
      "preview": { /* 直前主要属性プレビュー、本文非表示 */ }
    }
  ],
  "nextCursor": "..."
}
```

監査: (読取のみ)

#### 5.3.2 `POST /admin/v1/restorations`(削除データ復元)

| 機能ID | F-OP-010 |
| 4-eyes 種別 | **承認ログ**(action: `owner.restore_data`) |
| 関連画面 | SCR-091 |
| 関連テーブル | `deleted_resources`, `deletions`, `restorations`, `audit_logs` |
| 連携IF | #4(本書→メイン復元実行)、#12(管理者ユーザー通知)|

リクエスト:
```json
{
  "resourceType": "owner",
  "resourceId": "...",
  "reason": "顧客問合せ#ABC-123 対応"
}
```
ヘッダ: `X-Op-Ticket-Id`、`X-Approval-Id`

レスポンス(200):
```json
{
  "restorationId": "01J...",
  "restoredAt": "...",
  "rollback": {
    "stripeSubscriptionResumed": "sub_xxx",
    "dlqRequeued": 3,
    "inboxRequeued": 5
  }
}
```

エラー: 423 `RESTORE_LOCK_FAILED`(E-OP-RESTORE-LOCKED)、500 `RESTORE_SIDE_EFFECT_FAILED`

監査: `owner.restore` または `<resource>.restore`(5y)

### 5.4 AI パラメータ・契約上書き API

#### 5.4.1 `PUT /admin/v1/ai-parameters/{scope}/{scopeId}`

| 機能ID | F-OP-011 |
| 4-eyes 種別 | **ハードゲート**(action: `ai_parameter.update`)|
| 関連画面 | SCR-092 |
| 連携IF | #6(メイン同期)|
| scope | `global` / `owner` / `project` |
| scopeId | global は `"global"` 固定、それ以外は ID |

リクエスト:
```json
{
  "confidenceThreshold": 0.62,
  "relevanceThreshold": 0.55,
  "modelId": "@cf/meta/llama-3.1-8b-instruct",
  "rolloutPercentage": 10,
  "reason": "test increase..."
}
```
ヘッダ: `X-Op-Ticket-Id`、`X-Approval-Id`

レスポンス(200): `{ "scope": "owner", "scopeId": "01J...", "version": "...", "appliedAt": "...", "kvKey": "ai-params:owner:01J..." }`
エラー: 403 `FORBIDDEN_HARD_GATE`(E-OP-4EYES-HARDGATE)、400 `VALIDATION_ERROR`

監査: `ai_parameter.update`(5y)

#### 5.4.2 `PUT /admin/v1/overrides/rate-limit/{contract_owner_user_id}`

| 機能ID | F-OP-012 |
| 4-eyes 種別 | 承認ログ(action: `rate_limit.override`)|
| 連携IF | #5(メイン同期)|

リクエスト:
```json
{
  "widgetAskPerMin": 200,
  "chatEndUserPerMin": 10,
  "chatStaffPerMin": 30,
  "reason": "急増対応#TKT-1234"
}
```

レスポンス(200): `{ "overrideId": "...", "kvKey": "rate-limit:01J..." }`

監査: `rate_limit.override`(5y)

#### 5.4.3 `PUT /admin/v1/overrides/budget/{contract_owner_user_id}`

| 4-eyes 種別 | 承認ログ(action: `budget.override`)|

リクエスト: `{ "monthlyBudgetJpy": 100000, "reason": "..." }`

### 5.5 お知らせ API

#### 5.5.1 `POST /admin/v1/announcements`(作成)

| 機能ID | F-OP-013 |
| 関連画面 | SCR-094 |

リクエスト:
```json
{
  "kind": "announcement",
  "severity": "normal",
  "scope": { "type": "all" },
  "subject": "メンテナンス予告",
  "bodyHtml": "<p>...</p>",
  "optOut": "optional",
  "scheduledAt": "2026-05-15T10:00:00Z"
}
```

レスポンス(201): `{ "announcementId": "...", "state": "draft", "sanitizedBodyHtml": "..." }`
エラー: 422 `XSS_PATTERN_DETECTED`(タグ/属性フィルタ)

監査: `announcement.create`(5y)

#### 5.5.2 `POST /admin/v1/announcements/{id}/schedule`(配信予約)

| 認証 | 要(**再認証 + チケット ID**)|

バリデーション: `now ≤ scheduledAt ≤ now + 30d`
監査: `announcement.schedule`(5y)

#### 5.5.3 `POST /admin/v1/announcements/{id}/send`(即時配信)

| 4-eyes 種別 | **承認ログ + 確認**(緊急用、HardgateBadge)|

連携 IF #7 経由でメインへ配信指示。

### 5.6 監査・PII 報告 API

#### 5.6.1 `GET /admin/v1/audit-logs`

| 機能ID | F-OP-017 |
| 関連画面 | SCR-096 |

クエリ: `action`, `actorId`, `targetId`, `contractOwnerUserId`, `from`, `to`, `ipMasked`, `ticketId`, `cursor`, `limit`
バリデーション: `to - from ≤ 365 日`

レスポンス(200):
```json
{
  "items": [
    {
      "id": "01J...",
      "occurredAt": "...",
      "actorId": "...",
      "action": "owner.restore",
      "targetId": "...",
      "ticketId": "TKT-1234",
      "beforeValue": { /* 差分 */ },
      "afterValue": { /* 差分 */ },
      "prevHash": "...",
      "recordHash": "..."
    }
  ],
  "nextCursor": "..."
}
```

監査: (読取のみ)

#### 5.6.2 `POST /admin/v1/audit-logs/exports`

| 機能ID | F-OP-018 |
| 認証 | 再認証 |

リクエスト: `{ "filter": { "action": "owner.*", "from": "2026-04-01", "to": "2026-05-01" }, "format": "csv" }`

レスポンス(202): `{ "exportId": "01J...", "status": "processing", "estimatedRows": 12345, "files": [] }`

完了後: `GET /admin/v1/audit-logs/exports/{exportId}` で `files: [{ url, sigUrl, rows }]`
エラー: 422 `EXPORT_TOO_LARGE`(>100 万行)

監査: `audit.export`(5y)

#### 5.6.3 `POST /admin/v1/pii-rules/revisions`

| 機能ID | F-OP-016 |
| 4-eyes 種別 | 承認ログ(action: `pii_rule.update`)|
| 関連画面 | SCR-098 |

リクエスト:
```json
{
  "regexRules": [
    { "id": "phone_jp", "pattern": "0[789]0-\\d{4}-\\d{4}", "enabled": true }
  ],
  "classifierParams": { "threshold": 0.85 },
  "rolloutPercentage": 10,
  "reason": "誤検出報告#PFP-001 対応"
}
```

レスポンス(201): `{ "revisionId": "...", "kvKey": "pii-rules:regex" }`

監査: `pii_rule.update`(5y)

### 5.7 Webhook 関連 API

#### 5.7.1 `POST /admin/v1/webhooks/replay`(DLQ リプレイ)

| 機能ID | F-OP-015 |
| 4-eyes 種別 | 承認ログ(action: `webhook.replay`)|
| 関連画面 | SCR-097 |

リクエスト: `{ "eventId": "evt_xxx", "ticketId": "TKT-1234" }` + `X-Op-Ticket-Id`
バリデーション: `state='dlq_manual_replay'`、自動 BO 完了済み、受信から 30 日以内

レスポンス(200): `{ "state": "processing", "replayId": "..." }`
エラー: 409 `WEBHOOK_REPLAY_AUTO_BO_IN_PROGRESS`、410 `WEBHOOK_REPLAY_WINDOW_EXPIRED`(30 日超、E-OP-WEBHOOK-REPLAY-EXPIRED)

監査: `webhook.replay`(5y)

#### 5.7.2 `POST /webhooks/stripe`(Stripe Webhook 一次受信)

| 認証 | Stripe 署名(HMAC-SHA256)|
| 4-eyes 種別 | なし(自動処理)|

ヘッダ:
- `Stripe-Signature: t=<unix_ts>,v1=<hmac_sha256>,v1=<hmac_sha256_alternative>`
- `Content-Type: application/json`

ボディ(Stripe 仕様):
```json
{
  "id": "evt_xxxxx",
  "object": "event",
  "api_version": "2024-06-20",
  "created": 1718160000,
  "data": { /* ... */ },
  "livemode": true,
  "pending_webhooks": 1,
  "request": { "id": "req_xxxxx", "idempotency_key": "..." },
  "type": "invoice.paid"
}
```

##### 署名検証アルゴリズム

```
verifyStripeSignature(payload, header, secret, tolerance=300s):
  parts = parseHeader(header)
  timestamp = parts.t
  if |now - timestamp| > tolerance: return false  // Replay 攻撃防止
  signedPayload = timestamp + "." + payload
  expectedSig = HMAC-SHA256(secret, signedPayload)
  for sig in parts.v1[]:
    if constantTimeEqual(sig, expectedSig): return true
  return false
```

**失敗時**: HTTP 401 即返却 + 運営者 inbox(`system`/`high`)+ `audit.webhook.signature_invalid`(5y)

##### 冪等性・差分検出

| 項目 | 仕様 |
|---|---|
| 冪等性キー | Stripe `event_id`(`evt_*`)を `webhook_events.event_id` PK |
| 正規化 JSON | キーソート + 空白除去 → SHA-256 ハッシュ |
| 同 event_id + ハッシュ一致 | 200 OK「duplicate, skipped, hash_match」+ ログ |
| 同 event_id + ハッシュ不一致 | 200 OK + `webhook_payload_diffs` INSERT + SCR-099 記録 + 運営者 high alert + **自動上書き禁止** |

##### 内部転送対象イベント(メイン側へ mTLS + JWT 同期)

| event_type | 処理 |
|---|---|
| `invoice.paid` | 支払成功確定 → サスペンション解除 |
| `invoice.payment_failed` | 支払失敗 → 猶予突入 |
| `invoice.finalized` | 請求書確定 |
| `customer.subscription.updated` | プラン変更反映 |
| `customer.subscription.deleted` | 解約 → `suspended` 遷移 |
| `charge.refunded` | 返金 → 請求書更新 |

##### DLQ・リプレイ設計

| 項目 | 仕様 |
|---|---|
| Cloudflare Queues 保持 | 4 日 |
| R2 退避パス | `dlq-stripe-events/<event_id>.json` |
| R2 保持期間 | 30 日(`dlq_archived` で以降リプレイ不可)|
| 自動 BO | 1m → 4m → 16m(3 回、超過で永久失敗)|
| 手動リプレイ | SCR-097 から運営者の明示操作のみ |
| タイムアウト | 30 秒 |

#### 5.7.3 Stripe Webhook 除外フィールド(差分検出時、付録 H 全件)

ルートレベル: `created`, `request.id`, `request.idempotency_key`, `idempotency_key_resent`, `livemode`, `api_version`, `pending_webhooks`

data.object レベル: `data.object.created`, `data.object.updated_at`, `data.object.test_clock`, `data.object.metadata.test_*`, `data.object.metadata._stripe_internal_*`, `data.previous_attributes`

配列要素内(再帰): `*.created`, `*.updated_at`

### 5.8 連携 IF(送信 / 受信)

#### 5.8.1 連携 IF 主管責任(運営者側)

| IF# | 連携先 | 方向 | 認証 | 冪等性キー | DLQ | TO | 関連 FR |
|---|---|---|---|---|---|---|---|
| #1 | メイン | 本書 → | mTLS + JWT(`aud=main`)| `(operation_id, owner_id, target_status)` | 100/30m | 5s | FR-124 |
| #2 | メイン | 本書 → | mTLS + JWT | `(operation_id, owner_id)` | 100/30m | 3s | FR-224 |
| #4 | メイン | 本書 → | mTLS + JWT | `(restore_operation_id)` | 50/24h | 10s | FR-200〜209 |
| #5 | メイン | 本書 → | mTLS + JWT | `(owner_id, override_id)` | 50/30m | 3s | FR-121 |
| #6 | メイン | 本書 → | mTLS + JWT | `(owner_id, scope, version)` | 50/30m | 3s | FR-055 |
| #7 | メイン | 本書 → | mTLS + JWT | `(announcement_id, owner_id)` | 1000/h | 30s | FR-149 |
| #8 | メイン | メ → 本書 | mTLS + JWT(`aud=admin`)| `(metric_window_id)` | n/a | 10s | NFR-804 |
| #9 | メイン | メ → 本書 | mTLS + JWT(`aud=admin`)| `(detection_id)` | 200/30m | 5s | FR-195 |
| #10 | Stripe → 本書 → メイン | 本書 → | Stripe 署名 + mTLS + JWT | Stripe `event_id` | 1000/24h + R2 30d | 10s | FR-302 |
| #12 | メイン | 本書 → | mTLS + JWT | `(operation_id, owner_id)` | 200/30m | 5s | FR-211 |

#### 5.8.2 IF #1 契約停止イベント送信

POST 先: メイン側 `/internal/admin-integration/v1/owner/suspend`
詳細は [メイン側 §5.13.1](../../01_メインシステム/個別設計書群/03_API設計書.md) を参照。

#### 5.8.3 IF #8 監視メトリクス取得(受信)

エンドポイント: `GET /internal/main-integration/v1/metrics?window=5m`
認証: mTLS + JWT(`aud=admin`)

詳細は [メイン側 §5.13.7](../../01_メインシステム/個別設計書群/03_API設計書.md) を参照。

#### 5.8.4 IF #9 不正利用検知通知(受信)

エンドポイント: `POST /internal/main-integration/v1/fraud/detected`

#### 5.8.5 IF #10 Stripe Webhook → メイン転送

§5.7.2 参照。Stripe 一次受信後にメイン側へ転送。

#### 5.8.6 IF #12 運営者操作通知送信

POST 先: メイン側 `/internal/admin-integration/v1/admin-operation/notify`
詳細は [メイン側 §5.13.10](../../01_メインシステム/個別設計書群/03_API設計書.md) を参照。

## 6. 4-eyes × API 対応表

| 4-eyes action code | 種別 | API | 関連画面 |
|---|---|---|---|
| `owner.physical_delete` | **ハードゲート** | `DELETE /admin/v1/owners/:id/physical`(MVP 範囲) | SCR-091 派生 |
| `ai_parameter.update` | **ハードゲート** | `PUT /admin/v1/ai-parameters/{scope}/{id}` | SCR-092 |
| `key.master_rotate` | **ハードゲート** | (運用 CLI、API なし) | - |
| `owner.suspend` / `owner.restore` | 承認ログ | `POST /admin/v1/owners/:id/suspend`, `/restore`(IF #1 経由) | SCR-091 派生 |
| `rate_limit.override` | 承認ログ | `PUT /admin/v1/overrides/rate-limit/{owner_id}` | SCR-093 |
| `budget.override` | 承認ログ | `PUT /admin/v1/overrides/budget/{owner_id}` | SCR-093 |
| `owner.force_stop` | 承認ログ | `POST /admin/v1/owners/:id/force-stop` | SCR-093 派生 |
| `owner.restore_data` | 承認ログ | `POST /admin/v1/restorations` | SCR-091 |
| `webhook.replay` | 承認ログ | `POST /admin/v1/webhooks/replay` | SCR-097 |
| `owner.legal_review.record` | 承認ログ | `POST /admin/v1/legal-review` | SCR-098 派生 |

## 7. 未決事項

| No | 内容 | 確認先 | 期限 | ステータス |
|---|---|---|---|---|

## 8. 変更履歴

| 日付 | 版数 | 変更内容 | 変更者 |
|---|---|---|---|
| 2026-05-17 | 1.0 | 初版作成 | claude |
