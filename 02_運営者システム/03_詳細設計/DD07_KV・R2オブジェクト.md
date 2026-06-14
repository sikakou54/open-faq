# DD07: KV・R2 オブジェクト(運営者システム)

## 0. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | DD07: KV・R2 オブジェクト(運営者システム) |
| 詳細設計ID | DD07 |
| 対象システム | FAQ AI ウィジェット SaaS / 運営者システム |
| 関連機能ID | TH-7, D-13, D-14, D-15, D-17, D-19 |
| 作成日 | 2026-05-17 |
| 版数 | v1.0 |
| ステータス | 承認済 |

## 1. 対象範囲

| 種別 | ID | 名称 |
|---|---|---|
| 機能 | TH-7 | KV キー・R2 オブジェクト一覧の確定 |
| KV namespace | `admin_cache` | 運営者プレーン専用 KV |
| R2 bucket | `admin_archive` | 運営者プレーン専用 R2 |
| API | 全機能横断 | KV 参照型機能フラグ / レート上書き / AI パラメータ等 |

## 2. 収録ロジック・対応章

| 元章 | 元タイトル | 概要 |
|---|---|---|
| §9 全文 | KV キー・R2 オブジェクト一覧(★TH-7) | 全 KV キーの命名・値スキーマ・TTL・サンプル・参照 Worker |
| 付録 J | KV キー早見表 | 1 ページ集約 + 監視 KPI 動的閾値 + サーキットブレーカ |

## 3. 詳細設計本文

### 3.1 KV キー命名規則

| 項目 | 規約 |
|---|---|
| 一般形式 | `<feature>:<scope>:<id>`(英小文字 + ハイフン + コロン区切り) |
| 機能ごとに TTL を設定 | 認証系 60s〜15min、フラグ系 60s、ルール系 60s、レート/上限件数 30s、トークン系 個別 |
| 文字制限 | 英数 + `-` + `_` + `:`、最大 512 バイト |
| 値形式 | JSON 文字列、bool、数値、または ID 文字列 |
| Namespace | `admin_cache`(本書側専用 KV namespace) |

### 3.2 KV キー全表

#### 3.2.1 認証・セッション

| キー形式 | 値スキーマ | TTL | 更新タイミング | 参照 Worker | サンプル |
|---|---|---|---|---|---|
| `operator-session:<session_id>` | `{ operatorId, mfaVerifiedAt, reauthenticatedAt, csrfToken, expiresAt }` | 60 秒(キャッシュ) | ログイン時、ログアウト時失効 | AdminConsoleWorker | `{"operatorId":"01J...","mfaVerifiedAt":"...","csrfToken":"abc"}` |
| `operator-ip-allowlist:<operator_id>` | `["203.0.113.0/24","2001:db8::/48"]`(CIDR 配列) | 60 秒 | IP リスト変更時に Invalidate | エッジ(AdminConsoleWorker) | `["203.0.113.0/24"]` |
| `mfa-setup:<operator_id>` | `{ token, secret, expiresAt }` | 72 時間 | MFA セットアップ開始時 | AdminConsoleWorker | - |
| `password-reset:<token_hash>` | `{ operatorId, expiresAt }` | 60 分 | リセット要求時 | AdminConsoleWorker | - |
| `re-auth:<session_id>` | `{ operatorId, reauthenticatedAt, consumed }` | 15 分(1 回限り、`consumed=true` で即時失効) | 再認証成功時 | AdminConsoleWorker | `{"operatorId":"01J...","consumed":false}` |
| `login-lockout:<ip_hash>:<operator_id>` | `{ failedCount, lockedUntil }` | 15 分 | ログイン失敗時 | AdminConsoleWorker | `{"failedCount":5,"lockedUntil":"..."}` |

#### 3.2.2 機能フラグ

| キー形式 | 値 | TTL | 用途 |
|---|---|---|---|
| `feature:hard-gate:<action_code>` | `true` / `false` | 60 秒(キャッシュ) | MVP ハードゲート 3 操作を制御 |
| `feature:ai-model:rollout:<version>` | `{ percentage: 0\|10\|50\|100 }` | 60 秒 | AI モデルロールアウト |
| `feature:pii-rule-rollout:<revision_id>` | `{ percentage: 0\|10\|50\|100 }` | 60 秒 | PII ルールロールアウト |
| `feature:announcement-batch-size` | 数値 | 60 秒 | 1 cron tick あたりのお知らせ最大処理件数(既定 100) |

#### 3.2.3 ルール・パラメータ

| キー形式 | 値スキーマ | TTL | 主管 | 更新元 |
|---|---|---|---|---|
| `pii-rules:regex` | `[{ id, pattern, enabled }, ...]` | 60 秒(D-13) | 本書 | SCR-097 `POST /pii-rules/revisions` |
| `pii-rules:classifier` | `{ threshold, weights, modelId }` | 60 秒(D-13) | 本書 | 同上 |
| `ai-params:global` | `{ confidenceThreshold, relevanceThreshold, modelId }` | 60 秒(D-15) | 本書 | SCR-092 |
| `ai-params:owner:<contract_owner_user_id>` | 同上 | 60 秒 | 本書 | SCR-092 |
| `ai-params:project:<project_id>` | 同上 | 60 秒 | 本書 | SCR-092 |
| `ai-models:available` | `["@cf/meta/llama-3.1-8b-instruct", ...]` | 60 秒 | 本書 | 運営者手動 |
| `ai-cost:unit-prices` | `{ "<model_id>": { "input_per_1k_tokens": <yen>, "output_per_1k_tokens": <yen> } }` | 60 秒 | 本書 | 運営者手動(NFR-804 (m) FR-304) |

#### 3.2.4 レート(契約単位) / 月次上限件数・無料枠(プロジェクト単位)上書き

| キー形式 | 値スキーマ | TTL | 用途 |
|---|---|---|---|
| `rate-limit:<contract_owner_user_id>` | `{ widgetAskPerMin, chatEndUserPerMin, chatStaffPerMin }` | 30 秒(D-14) | メイン側参照(レート、契約単位)|
| `usage-limit:<contract_owner_user_id>:<project_id>` | `{ questionMonthlyLimit, questionFreeQuota, faqFreeQuota, chatRoomFreeQuota, paymentGateStopped }` | 30 秒 | メイン側参照(質問数上限・課金対象別無料枠、**プロジェクト単位**)|
| `usage-limit:default:<kind>` | 件数 | 永続(運営者更新時のみ Invalidate)| プロジェクト別デフォルト上限件数 |
| `usage-limit:free-default:<kind>` | 件数 | 永続 | プロジェクト別デフォルト無料枠 |
| `usage-limit:min` | `{ question }` | 永続 | 質問数上限のバリデーション下限 |
| `usage-limit:max` | `{ question }` | 永続 | 質問数上限のバリデーション上限 |

#### 3.2.5 Webhook・トークン

| キー形式 | 値スキーマ | TTL | 用途 |
|---|---|---|---|
| `webhook:idempotency:<event_id>` | `{ payloadHash, state, processedAt }` | 30 日 | event_id 冪等(D1 `webhook_events` のキャッシュ) |
| `audit-export:<job_id>` | `{ status, files, signature }` | 24 時間 | エクスポート進捗 |

#### 3.2.6 通知集約

| キー形式 | 値スキーマ | TTL | 用途 |
|---|---|---|---|
| `notify-batch:<contract_owner_user_id>:<operation_kind>` | `{ entries: [...], firstAt }` | 10 分(D-19) | FR-211 集約窓 |

### 3.3 R2 オブジェクトパス

Namespace: `admin_archive`(本書側専用 R2 バケット)

| パス | 用途 | 保持 | アクセス |
|---|---|---|---|
| `dlq-stripe-events/<event_id>.json` | DLQ 退避 Webhook ペイロード | 30 日(life-cycle rule) | BillingWebhookWorker / SCR-096 |
| `audit-export/<job_id>-<seq>.csv` | 監査ログエクスポート(CSV) | 24 時間 | AdminConsoleWorker |
| `audit-export/<job_id>-<seq>.jsonl` | 同(JSONL) | 24 時間 | 同上 |
| `audit-export/<job_id>-<seq>.sig` | HMAC 署名ファイル(D-17) | 24 時間 | 同上 |
| `webhook-payload-snapshots/<event_id>-<received_at>.json` | ペイロード差分検出時のスナップショット | 30 日 | BillingWebhookWorker |
| `audit-archive/<retention_class>/<year>/<month>.tar.gz` | 監査ログ年次アーカイブ | 法令対応期間内 | R2AuditArchiveWorker |
| `backup/d1-snapshots/<env>/<date>.sqlite` | D1 日次バックアップ(NFR-803 三層) | 日次 30 日 / 週次 12 週 / 月次 12 ヶ月 | Backup Worker(別 Worker) |

### 3.4 KV キー早見表(付録 J 同等)

| キー形式 | 値 | TTL | 用途 |
|---|---|---|---|
| `operator-session:<sid>` | JSON | 60s | セッションキャッシュ |
| `operator-ip-allowlist:<operator_id>` | JSON 配列 | 60s | エッジ IP 判定 |
| `mfa-setup:<operator_id>` | JSON | 72h | 初回 MFA |
| `password-reset:<token_hash>` | JSON | 60m | リセット |
| `re-auth:<sid>` | JSON | 15m | 1 回限り |
| `login-lockout:<ip_hash>:<operator_id>` | JSON | 15m | ロックアウト |
| `feature:hard-gate:<action_code>` | bool | 60s | 4-eyes 切替 |
| `feature:pii-layer2:enabled` | bool | 60s | PII NER |
| `feature:ai-model:rollout:<version>` | JSON | 60s | モデル段階展開 |
| `feature:pii-rule-rollout:<revision>` | JSON | 60s | PII ルール段階 |
| `feature:announcement-batch-size` | int | 60s | お知らせバッチ |
| `pii-rules:regex` | JSON 配列 | 60s | PII 第 1 層 |
| `ai-params:global` | JSON | 60s | AI 既定値 |
| `ai-params:owner:<contract_owner_user_id>` | JSON | 60s | 契約上書き |
| `ai-params:project:<project_id>` | JSON | 60s | プロジェクト上書き |
| `ai-models:available` | JSON 配列 | 60s | モデル一覧 |
| `ai-cost:unit-prices` | JSON | 60s | 単価表(FR-304) |
| `rate-limit:<contract_owner_user_id>` | JSON | 30s | レート上書き(契約単位)|
| `usage-limit:<contract_owner_user_id>:<project_id>` | JSON | 30s | 月次上限件数・無料枠上書き(プロジェクト単位)|
| `usage-limit:default:<kind>` / `free-default:<kind>` | 件数 | 永続 | プロジェクト別デフォルト上限 / 無料枠 |
| `usage-limit:min` / `max` | JSON | 永続 | 質問数上限のバリデーション |
| `webhook:idempotency:<event_id>` | JSON | 30d | 冪等キャッシュ |
| `audit-export:<job_id>` | JSON | 24h | エクスポート進捗 |
| `notify-batch:<contract_owner_user_id>:<kind>` | JSON | 10m | FR-211 集約 |
| `monitoring:thresholds:<kpi_id>` | JSON | 永続 | KPI 動的閾値(下表で初期値定義) |
| `cb:internal-api:<endpoint>` | JSON | 60s (open 時) | サーキットブレーカ状態 |
| `sre:planned-outage:<id>` | JSON | 永続 | 計画停止期間(SLA 除外用) |

### 3.5 監視 KPI 動的閾値の初期値(`monitoring:thresholds:<kpi_id>`)

`SLAComputeWorker` が KPI 集計時に参照する。MVP の初期値を以下に固定し、運営が `wrangler kv key put` で CLI 更新する。

| kpi_id | 初期値 | 単位 | 意味 | チューニングガイド |
|---|---|---|---|---|
| `NFR-103-ai-p95` | 2500 | ms | AI 推論 p95 目標 | MVP で 2500ms を維持。p95 が 80% を超える日が月内 3 回以上 → 緩和判定(運営合議) |
| `NFR-105-admin-p95` | 800 | ms | 管理画面一覧 p95 | 4 週連続達成で AC-046 判定 |
| `NFR-106-unread-p95` | 200 | ms | 未読件数バッジ p95 | 同上 |
| `audit-search-p95` | 1000 | ms | 監査ログ検索 p95 | 100 万件超過時に運営者へ通知 |
| `audit-export-duration-p95` | 60 | s | エクスポート完了時間 p95 | 行平均サイズ実測値で運営者へ通知 |
| `chain-verify-duration` | 3600 | s | ハッシュチェーン日次検証時間 | 1000 万行超過時に分割検証へ |
| `dlq-stale-1h-count` | 0 | count | 1h 超過 DLQ 件数 | 0 維持、1 件で high alert |
| `four-eyes-pending-72h` | 0 | count | 72h 経過承認待ち件数 | 0 維持、1 件で high alert |
| `webhook-payload-diff-detected-24h` | 0 | count | 24h 内 detected 件数 | 0 維持、1 件で normal alert |
| `pii-fp-pending-3bd` | 0 | count | 3 営業日経過 PII 誤検出報告 | 0 維持、1 件で normal alert |
| `owner-mau-total` | — | count | 全契約横断 MAU | 観測のみ、閾値なし |
| `ai-cost-per-owner-monthly` | 50000 | yen | 契約月次 AI 原価(運営判断用) | 5 万円超過契約は月次レビュー対象 |

**変更履歴監査**: 閾値変更時は `monitoring.threshold.update` action コード(`retention_class='5y'`)で `audit_logs` に記録。`before` / `after` 値を `audit_logs.diff` に格納。

### 3.6 サーキットブレーカ KV(`cb:internal-api:<endpoint>`)

値の形式:

```json
{
  "state": "closed" | "open" | "half_open",
  "openedAt": 1715600000000,
  "failureCount": 3
}
```

TTL は `open` 状態時 60s、`closed` 復帰時は明示 DELETE。

### 3.7 計画停止 KV(`sre:planned-outage:<id>`)

SLA 集計時に除外する計画停止期間を管理:

```json
{
  "outageId": "01J...",
  "scope": ["api","webhook"],
  "startsAt": "2026-06-01T19:00:00Z",
  "endsAt": "2026-06-01T20:00:00Z",
  "reason": "Cloudflare maintenance"
}
```

`SLAComputeWorker` が集計時に重複期間を除外する。

### 3.8 KV 運用ガイドライン

| 項目 | ガイドライン |
|---|---|
| TTL 既定 | キャッシュ 60 秒、レート/上限件数 30 秒、トークン 個別、フラグ 60 秒 |
| Invalidate | 値変更後に必ず `DELETE`(TTL 待ちでは設計上の遅延が許容できる場合のみ放置) |
| 値サイズ | 1 KB 以下を推奨、超過時は R2 退避を検討 |
| KV API レート | `admin_cache` namespace 全体で 1000 RPS 上限を想定。超過時は L1 cache(Worker メモリ)併用 |
| 監査 | KV 値の運営者操作変更は対応する `<resource>.<verb>` action_code を必ず記録(`feature.hard_gate.toggle` 等) |

### 3.9 R2 運用ガイドライン

| 項目 | ガイドライン |
|---|---|
| Lifecycle Rule | `dlq-stripe-events/*` は 30 日後自動削除、`webhook-payload-snapshots/*` も 30 日 |
| 監査エクスポート | 24 時間後自動削除(必要なら運営者が手元 PC へダウンロード) |
| アーカイブ | `audit-archive/*` は法令保持期間まで保持、Lifecycle なし |
| バックアップ | `backup/d1-snapshots/<env>/*` は日次 30 / 週次 12 / 月次 12 |
| アクセス制御 | 公開 URL は Pre-signed URL のみ、TTL 24h、HMAC 署名(HKDF info=`r2-presigned`) |

## 4. 関連設計

| 種別 | 参照先 |
|---|---|
| 要件 | [../01_要件定義/index.md](../01_要件定義/index.md) |
| 基本設計 | [../02_基本設計/index.md](../02_基本設計/index.md) |
| セキュリティ設計(正本) | [../02_基本設計/09_セキュリティ設計.md](../02_基本設計/09_セキュリティ設計.md) |
| 関連 DD | [DD01_運営者認証・6段認可.md](DD01_運営者認証・6段認可.md) / [DD03_監査ハッシュチェーン.md](DD03_監査ハッシュチェーン.md) / [DD04_Stripe_Webhook一次受信.md](DD04_Stripe_Webhook一次受信.md) / [DD06_お知らせ承認・配信.md](DD06_お知らせ承認・配信.md) / [DD10_PII偽陽性報告.md](DD10_PII偽陽性報告.md) |
| 運用設計 | [../04_運用設計/index.md](../04_運用設計/index.md) |
| 将来対応 | [../05_future/index.md](../05_future/index.md) |

## 5. テスト観点

### 5.1 ユニットテスト

- KV キー命名規則バリデーション(英小文字 + ハイフン + コロン)
- TTL 設定値の確認(KV 値書込時に `expirationTtl` 指定)
- 機能フラグ KV キャッシュヒット・ミス

### 5.2 結合テスト(Miniflare)

- レート上書き → KV 書込 → 30 秒以内のメイン側参照で反映
- ハードゲート KV トグル → 60 秒以内に該当 action ハードゲート発動
- KV 値変更後の Invalidate 動作確認

### 5.3 E2E テスト

- 監視 KPI 閾値変更 → `monitoring.threshold.update` 監査記録
- サーキットブレーカ open / half_open / closed 遷移

### 5.4 運用テスト

- R2 Lifecycle Rule 30 日後の自動削除動作確認(月次運用テスト)
- バックアップ三層保持の最古ファイル参照可能性

## 6. 未確定事項・確認事項

| 確認事項ID | 確認内容 | 優先度 | ステータス |
|---|---|---|---|
| - | v1.0 リリース時点で全項目確定済み | 低 | 確認済 |
