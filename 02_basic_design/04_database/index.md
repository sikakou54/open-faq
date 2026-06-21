<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ **DB設計**
<!-- /portal-top -->

# データベース設計書

**メインシステムのデータベース(Cloudflare D1 / SQLite)全 31 テーブルを機能ドメイン別に定義する設計書です。** 全ユーザーは `M_USER`、契約は `M_CONTRACT`(オーナー判定 + プロジェクトの親)で管理します。各テーブルの詳細はテーブル名のリンクから辿れます。

*版数 v3.6 ・ 更新 2026-06-21 ・ テーブル数 31 ・ 独立設計書*

## <span id="store"></span>1.データストア構成

<div class="card-grid cols-3">
<div class="card"><div class="lead-ico">D1</div><h4>Cloudflare D1(SQLite)</h4><p>全 31 テーブル。契約境界は <code>contract_id</code>(<code>M_CONTRACT.id</code>)で表す。</p></div>
<div class="card"><div class="lead-ico">KV</div><h4>Workers KV</h4><p>セッション / トークン / レート制限のキャッシュ。</p></div>
<div class="card"><div class="lead-ico">R2</div><h4>R2 オブジェクト</h4><p>CSV 添付・ウィジェット静的アセット。</p></div>
</div>

## <span id="map"></span>2.テーブル一覧

全 31 テーブルを 7 ドメインに分類しています。テーブル名は個別ページ(概要 / カラム定義 / インデックス / コード値)へのリンクです。

#### 認証・アカウント・契約 (7)

全ユーザーの認証(M_USER)、契約とオーナー判定(M_CONTRACT)、プロジェクトメンバー割当、セッション・トークン・規約。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-001"></span>[`M_USER`](TBL-001.md) | ユーザーマスタ | マスタ | オーナー・メンバーを含む全ユーザーの認証情報を一元保持。 |
| <span id="TBL-002"></span>[`M_CONTRACT`](TBL-002.md) | 契約マスタ | マスタ | 契約を管理。id が契約境界キー、user_id でオーナーを判定。プロジェクトの親。 |
| <span id="TBL-003"></span>[`M_PRJ_USERS`](TBL-003.md) | プロジェクトメンバー(割当) | マスタ | ユーザーをプロジェクトへ割り当て(役割差は持たない)。 |
| <span id="TBL-013"></span>[`T_SESSIONS`](TBL-013.md) | セッション | トランザクション | 複数デバイス対応のログインセッション。 |
| <span id="TBL-014"></span>[`T_ACCESS_TOKENS`](TBL-014.md) | アクセストークン | トランザクション | 招待・パスワード再設定・メール確認などの短期トークン。 |
| <span id="TBL-012"></span>[`M_TERMS_VER`](TBL-012.md) | 規約版数 | マスタ | 利用規約・プライバシーポリシーの版。 |
| <span id="TBL-024"></span>[`T_TERMS_AGREE`](TBL-024.md) | 規約同意 | トランザクション | 利用者ごとの規約同意履歴。 |

#### プロジェクト・ウィジェット (3)

FAQ プロジェクト本体(契約の子)、許可ドメイン、ウィジェット鍵。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-004"></span>[`M_PROJECTS`](TBL-004.md) | プロジェクト | マスタ | FAQ プロジェクトとウィジェット設定。契約(M_CONTRACT)の子テーブル。 |
| <span id="TBL-005"></span>[`M_ALLOWED_DOMAINS`](TBL-005.md) | 許可ドメイン | マスタ | ウィジェット埋め込みを許可するドメイン。 |
| <span id="TBL-015"></span>[`T_PRJ_LEGACY_KEYS`](TBL-015.md) | レガシー API キー | トランザクション | 鍵ローテーション時に旧キーを 24 時間だけ有効化。 |

#### FAQ・質問・未解決 (6)

FAQ 本体と全文検索、質問ログ、参照 FAQ、未解決質問、FAQ 化履歴。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-006"></span>[`M_FAQS`](TBL-006.md) | FAQ | マスタ | FAQ 本体(質問・回答・公開状態)。契約境界は project_id で導出。 |
| <span id="TBL-030"></span>[`TP_FAQ_FTS`](TBL-030.md) | FAQ 全文検索 | ワーク | FTS5 仮想テーブル(trigram)。 |
| <span id="TBL-025"></span>[`H_QUESTION_LOGS`](TBL-025.md) | 質問ログ | 履歴 | ウィジェット利用者の質問と AI 推論結果。 |
| <span id="TBL-016"></span>[`T_QLOG_FAQ_REFS`](TBL-016.md) | 参照 FAQ(M:N) | トランザクション | 質問ログと参照 FAQ の中間テーブル。 |
| <span id="TBL-017"></span>[`T_INQUIRIES`](TBL-017.md) | 未解決質問 | トランザクション | FAQ 登録前の未解決質問。 |
| <span id="TBL-029"></span>[`H_INQUIRY_FAQ`](TBL-029.md) | 未解決質問 FAQ 化履歴 | 履歴 | 未解決質問から FAQ への移行履歴(データコピー方式)。 |

#### 利用量・課金・上限 (5)

利用量計測、サブスク・請求書(7 年保持)、利用上限・無料枠。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-020"></span>[`T_USAGE_METER`](TBL-020.md) | 利用量計測 | トランザクション 課金7年 | 質問数・FAQ 件数をプロジェクト単位で計測し契約単位で集計。 |
| <span id="TBL-018"></span>[`T_BILL_SUBS`](TBL-018.md) | 課金サブスクリプション | トランザクション 課金7年 | Stripe サブスクと連動。 |
| <span id="TBL-019"></span>[`T_BILL_INVOICES`](TBL-019.md) | 請求書 | トランザクション 課金7年 | 月次請求書(電子帳簿保存法 7 年)。 |
| <span id="TBL-009"></span>[`M_PRJ_QUOTA_LIMITS`](TBL-009.md) | プロジェクト別利用設定 | マスタ | 質問数の月次上限・無料枠・アラート。 |
| <span id="TBL-008"></span>[`M_OWNER_QUOTA_OVR`](TBL-008.md) | 契約別レート上書き | マスタ | 契約単位のレート制限上書き(contract 単位)。 |

#### お知らせ・通知 (5)

運営お知らせ、配信対象、受信者集計、受信箱、メール通知ログ。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-010"></span>[`M_SERVICE_ANNOUNCE`](TBL-010.md) | お知らせ(Control Plane) | マスタ | お知らせ本体。 |
| <span id="TBL-011"></span>[`M_ANNOUNCE_AUD`](TBL-011.md) | お知らせ配信対象(M:N) | マスタ | 配信先を限定指定。 |
| <span id="TBL-021"></span>[`T_ANNOUNCE_RCPT`](TBL-021.md) | お知らせ受信者 | トランザクション | 実配信先・配信集計・監査。 |
| <span id="TBL-022"></span>[`T_INBOX_MSG`](TBL-022.md) | 受信箱(Tenant Plane) | トランザクション | 利用者が受け取る通知の既読状態。 |
| <span id="TBL-026"></span>[`H_NOTIF_LOGS`](TBL-026.md) | 通知ログ | 履歴 | メール通知の送信履歴。 |

#### 退会・データ管理 (1)

退会申請(90 日猶予)とデータ削除モード。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-023"></span>[`T_WITHDRAW_REQ`](TBL-023.md) | 退会申請 | トランザクション | 退会申請レコード(90 日猶予)。 |

#### システム・ログ・運用 (4)

監査ログ、エラーログ、メールサプレス、AI しきい値キャッシュ。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-027"></span>[`H_AUDIT_LOGS`](TBL-027.md) | 監査ログ | 履歴 一部課金 | メイン側 API 操作ログ。 |
| <span id="TBL-028"></span>[`H_ERROR_LOGS`](TBL-028.md) | エラーログ | 履歴 | サーバーエラー記録。 |
| <span id="TBL-007"></span>[`M_EMAIL_SUPPRESS`](TBL-007.md) | メールサプレスリスト | マスタ | バウンス・苦情アドレス(全契約横断)。 |
| <span id="TBL-031"></span>[`TP_AI_THRESH_CACHE`](TBL-031.md) | AI しきい値キャッシュ | ワーク | 3 階層しきい値の永続キャッシュ。 |

## <span id="er"></span>3.ER 図(親子関係)

全 31 テーブルの親子関係を、機能ドメイン別の ER 図で示します。

**(1) アカウント・契約・メンバー**

```mermaid
erDiagram
  M_USER {
    TEXT id PK
  }
  M_CONTRACT {
    TEXT id PK
    TEXT user_id FK "→M_USER.id"
  }
  M_PROJECTS {
    TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
  }
  M_PRJ_USERS {
    TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id"
    TEXT user_id FK "→M_USER.id"
  }
  M_USER ||--o| M_CONTRACT : "オーナー"
  M_USER ||--o{ M_PRJ_USERS : "参加"
  M_CONTRACT ||--o{ M_PROJECTS : "保有"
  M_PROJECTS ||--o{ M_PRJ_USERS : "割当先"
```

**(2) 認証 — セッション**

```mermaid
erDiagram
  M_USER { TEXT id PK }
  T_SESSIONS {
    TEXT id PK
    TEXT user_id FK "→M_USER.id"
  }
  M_USER ||--o{ T_SESSIONS : "ユーザー"
```

**(3) 認証 — トークン**

```mermaid
erDiagram
  M_USER { TEXT id PK }
  T_ACCESS_TOKENS {
    TEXT id PK
    TEXT user_id FK "→M_USER.id"
  }
  M_USER ||--o{ T_ACCESS_TOKENS : "ユーザー"
```

**(4) 認証 — 規約同意**

```mermaid
erDiagram
  M_USER { TEXT id PK }
  M_TERMS_VER {
    TEXT doc_type PK
    TEXT version PK
  }
  T_TERMS_AGREE {
    TEXT id PK
    TEXT user_id FK "→M_USER.id"
    TEXT terms_version FK "→M_TERMS_VER"
  }
  M_USER ||--o{ T_TERMS_AGREE : "ユーザー"
  M_TERMS_VER ||--o{ T_TERMS_AGREE : "版"
```

**(5) プロジェクト・ウィジェット**

```mermaid
erDiagram
  M_CONTRACT { TEXT id PK }
  M_PROJECTS { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id" }
  M_ALLOWED_DOMAINS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  T_PRJ_LEGACY_KEYS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  M_CONTRACT ||--o{ M_PROJECTS : "保有"
  M_PROJECTS ||--o{ M_ALLOWED_DOMAINS : "許可ドメイン"
  M_PROJECTS ||--o{ T_PRJ_LEGACY_KEYS : "旧鍵"
```

**(6) FAQ**

```mermaid
erDiagram
  M_FAQS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  H_INQUIRY_FAQ { TEXT id PK
    TEXT inquiry_id FK "→T_INQUIRIES.id"
    TEXT faq_id FK "→M_FAQS.id" }
  M_PROJECTS { TEXT id PK }
  T_INQUIRIES { TEXT id PK }
  M_PROJECTS ||--o{ M_FAQS : "FAQ"
  T_INQUIRIES ||--o{ H_INQUIRY_FAQ : "FAQ化"
  M_FAQS ||--o{ H_INQUIRY_FAQ : "FAQ化履歴"
```

**(7) 質問ログ・参照 FAQ**

```mermaid
erDiagram
  H_QUESTION_LOGS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  T_QLOG_FAQ_REFS { TEXT id PK
    TEXT question_log_id FK "→H_QUESTION_LOGS.id"
    TEXT faq_id FK "→M_FAQS.id" }
  M_PROJECTS { TEXT id PK }
  M_FAQS { TEXT id PK }
  T_INQUIRIES { TEXT id PK
    TEXT question_log_id FK "→H_QUESTION_LOGS.id" }
  M_PROJECTS ||--o{ H_QUESTION_LOGS : "質問ログ"
  H_QUESTION_LOGS ||--o{ T_QLOG_FAQ_REFS : "参照FAQ"
  M_FAQS ||--o{ T_QLOG_FAQ_REFS : "被参照"
  H_QUESTION_LOGS ||--o| T_INQUIRIES : "未解決化"
```

**(8) 未解決質問**

```mermaid
erDiagram
  T_INQUIRIES { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id"
    TEXT question_log_id FK "→H_QUESTION_LOGS.id" }
  M_PROJECTS { TEXT id PK }
  H_QUESTION_LOGS { TEXT id PK }
  M_FAQS { TEXT id PK }
  H_INQUIRY_FAQ { TEXT id PK
    TEXT inquiry_id FK "→T_INQUIRIES.id"
    TEXT faq_id FK "→M_FAQS.id" }
  M_PROJECTS ||--o{ T_INQUIRIES : "未解決"
  H_QUESTION_LOGS ||--o| T_INQUIRIES : "未解決化"
  T_INQUIRIES ||--o{ H_INQUIRY_FAQ : "FAQ化"
  M_FAQS ||--o{ H_INQUIRY_FAQ : "FAQ化履歴"
```

**(9) 利用量・課金・上限**

```mermaid
erDiagram
  M_CONTRACT { TEXT id PK }
  M_PROJECTS { TEXT id PK }
  T_BILL_SUBS { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id" }
  T_BILL_INVOICES { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id" }
  T_USAGE_METER { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  M_PRJ_QUOTA_LIMITS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  M_OWNER_QUOTA_OVR { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id" }
  M_CONTRACT ||--o{ T_BILL_SUBS : "サブスク"
  M_CONTRACT ||--o{ T_BILL_INVOICES : "請求書"
  M_PROJECTS ||--o{ T_USAGE_METER : "計測"
  M_PROJECTS ||--o{ M_PRJ_QUOTA_LIMITS : "上限設定"
  M_CONTRACT ||--o| M_OWNER_QUOTA_OVR : "レート上書き"
```

**(10) お知らせ・通知**

```mermaid
erDiagram
  M_CONTRACT { TEXT id PK }
  M_SERVICE_ANNOUNCE { TEXT id PK }
  M_ANNOUNCE_AUD { TEXT announcement_id FK "→M_SERVICE_ANNOUNCE.id"
    TEXT contract_id FK "→M_CONTRACT.id" }
  T_ANNOUNCE_RCPT { TEXT id PK
    TEXT announcement_id FK "→M_SERVICE_ANNOUNCE.id" }
  T_INBOX_MSG { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
    TEXT recipient_id FK "→M_CONTRACT/M_PRJ_USERS" }
  H_NOTIF_LOGS { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
    TEXT inquiry_id FK "→T_INQUIRIES.id" }
  T_INQUIRIES { TEXT id PK }
  M_SERVICE_ANNOUNCE ||--o{ M_ANNOUNCE_AUD : "配信対象"
  M_CONTRACT ||--o{ M_ANNOUNCE_AUD : "対象契約"
  M_SERVICE_ANNOUNCE ||--o{ T_ANNOUNCE_RCPT : "fan-out"
  M_CONTRACT ||--o{ T_INBOX_MSG : "受信箱"
  M_CONTRACT ||--o{ H_NOTIF_LOGS : "通知ログ"
  T_INQUIRIES ||--o{ H_NOTIF_LOGS : "問合せ通知"
```

**(11) 退会・データ管理**

```mermaid
erDiagram
  M_CONTRACT { TEXT id PK }
  T_WITHDRAW_REQ { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
    TEXT applied_by_id FK "→M_CONTRACT/M_PRJ_USERS" }
  M_CONTRACT ||--o{ T_WITHDRAW_REQ : "退会申請"
```

**(12) システム・ログ・運用**

```mermaid
erDiagram
  M_CONTRACT { TEXT id PK }
  M_PROJECTS { TEXT id PK }
  H_AUDIT_LOGS { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
    TEXT actor_id FK "→M_CONTRACT/M_PRJ_USERS" }
  TP_AI_THRESH_CACHE { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
    TEXT project_id FK "→M_PROJECTS.id" }
  M_CONTRACT ||--o{ H_AUDIT_LOGS : "監査"
  M_CONTRACT ||--o{ TP_AI_THRESH_CACHE : "しきい値"
  M_PROJECTS ||--o{ TP_AI_THRESH_CACHE : "PJしきい値"
```


<!-- p5-cross -->
## <span id="cross"></span>4.テーブル↔API / 業務UC 対応表(逆引き)

各テーブルを読み書きする API と、参照する業務ユースケースの逆引きです。API は `## 利用テーブル`、UC は `関連テーブルID` から決定論的に集計しています。個別の対応は各テーブルページの「項目」セクションを参照してください。

| テーブル | API 数 | 利用API | 対応業務UC |
|---|---:|---|---|
| [`M_USER`](#TBL-001) | 3 | [API-001](../03_apis/API-001.md#API-001) [API-008](../03_apis/API-008.md#API-008) [API-021](../03_apis/API-021.md#API-021) | 4 件(例 [UC-016](../../01_requirements/02_business_usecases/UC-016.md#UC-016) [UC-042](../../01_requirements/02_business_usecases/UC-042.md#UC-042) [UC-190](../../01_requirements/02_business_usecases/UC-190.md#UC-190)…) |
| [`M_CONTRACT`](#TBL-002) | 13 | [API-001](../03_apis/API-001.md#API-001) [API-002](../03_apis/API-002.md#API-002) [API-004](../03_apis/API-004.md#API-004) [API-005](../03_apis/API-005.md#API-005) [API-006](../03_apis/API-006.md#API-006) [API-007](../03_apis/API-007.md#API-007) [API-010](../03_apis/API-010.md#API-010) [API-012](../03_apis/API-012.md#API-012) [API-013](../03_apis/API-013.md#API-013) [API-014](../03_apis/API-014.md#API-014) [API-015](../03_apis/API-015.md#API-015) [API-037](../03_apis/API-037.md#API-037) [API-056](../03_apis/API-056.md#API-056) | 19 件(例 [UC-001](../../01_requirements/02_business_usecases/UC-001.md#UC-001) [UC-004](../../01_requirements/02_business_usecases/UC-004.md#UC-004) [UC-016](../../01_requirements/02_business_usecases/UC-016.md#UC-016)…) |
| [`M_PRJ_USERS`](#TBL-003) | 15 | [API-002](../03_apis/API-002.md#API-002) [API-004](../03_apis/API-004.md#API-004) [API-005](../03_apis/API-005.md#API-005) [API-007](../03_apis/API-007.md#API-007) [API-008](../03_apis/API-008.md#API-008) [API-010](../03_apis/API-010.md#API-010) [API-012](../03_apis/API-012.md#API-012) [API-013](../03_apis/API-013.md#API-013) [API-017](../03_apis/API-017.md#API-017) [API-018](../03_apis/API-018.md#API-018) [API-020](../03_apis/API-020.md#API-020) [API-021](../03_apis/API-021.md#API-021) [API-022](../03_apis/API-022.md#API-022) [API-023](../03_apis/API-023.md#API-023) [API-024](../03_apis/API-024.md#API-024) | 21 件(例 [UC-001](../../01_requirements/02_business_usecases/UC-001.md#UC-001) [UC-004](../../01_requirements/02_business_usecases/UC-004.md#UC-004) [UC-020](../../01_requirements/02_business_usecases/UC-020.md#UC-020)…) |
| [`T_SESSIONS`](#TBL-013) | 5 | [API-002](../03_apis/API-002.md#API-002) [API-003](../03_apis/API-003.md#API-003) [API-010](../03_apis/API-010.md#API-010) [API-018](../03_apis/API-018.md#API-018) [API-023](../03_apis/API-023.md#API-023) | 5 件(例 [UC-001](../../01_requirements/02_business_usecases/UC-001.md#UC-001) [UC-004](../../01_requirements/02_business_usecases/UC-004.md#UC-004) [UC-025](../../01_requirements/02_business_usecases/UC-025.md#UC-025)…) |
| [`T_ACCESS_TOKENS`](#TBL-014) | 15 | [API-001](../03_apis/API-001.md#API-001) [API-004](../03_apis/API-004.md#API-004) [API-005](../03_apis/API-005.md#API-005) [API-006](../03_apis/API-006.md#API-006) [API-007](../03_apis/API-007.md#API-007) [API-008](../03_apis/API-008.md#API-008) [API-009](../03_apis/API-009.md#API-009) [API-010](../03_apis/API-010.md#API-010) [API-011](../03_apis/API-011.md#API-011) [API-012](../03_apis/API-012.md#API-012) [API-013](../03_apis/API-013.md#API-013) [API-018](../03_apis/API-018.md#API-018) [API-021](../03_apis/API-021.md#API-021) [API-023](../03_apis/API-023.md#API-023) [API-024](../03_apis/API-024.md#API-024) | 6 件(例 [UC-126](../../01_requirements/02_business_usecases/UC-126.md#UC-126) [UC-127](../../01_requirements/02_business_usecases/UC-127.md#UC-127) [UC-130](../../01_requirements/02_business_usecases/UC-130.md#UC-130)…) |
| [`M_TERMS_VER`](#TBL-012) | 0 | — | 3 件(例 [UC-133](../../01_requirements/02_business_usecases/UC-133.md#UC-133) [UC-164](../../01_requirements/02_business_usecases/UC-164.md#UC-164) [UC-196](../../01_requirements/02_business_usecases/UC-196.md#UC-196)) |
| [`T_TERMS_AGREE`](#TBL-024) | 2 | [API-001](../03_apis/API-001.md#API-001) [API-008](../03_apis/API-008.md#API-008) | 5 件(例 [UC-133](../../01_requirements/02_business_usecases/UC-133.md#UC-133) [UC-135](../../01_requirements/02_business_usecases/UC-135.md#UC-135) [UC-169](../../01_requirements/02_business_usecases/UC-169.md#UC-169)…) |
| [`M_PROJECTS`](#TBL-004) | 8 | [API-007](../03_apis/API-007.md#API-007) [API-009](../03_apis/API-009.md#API-009) [API-011](../03_apis/API-011.md#API-011) [API-016](../03_apis/API-016.md#API-016) [API-017](../03_apis/API-017.md#API-017) [API-018](../03_apis/API-018.md#API-018) [API-019](../03_apis/API-019.md#API-019) [API-037](../03_apis/API-037.md#API-037) | 12 件(例 [UC-028](../../01_requirements/02_business_usecases/UC-028.md#UC-028) [UC-034](../../01_requirements/02_business_usecases/UC-034.md#UC-034) [UC-038](../../01_requirements/02_business_usecases/UC-038.md#UC-038)…) |
| [`M_ALLOWED_DOMAINS`](#TBL-005) | 4 | [API-016](../03_apis/API-016.md#API-016) [API-017](../03_apis/API-017.md#API-017) [API-018](../03_apis/API-018.md#API-018) [API-037](../03_apis/API-037.md#API-037) | 4 件(例 [UC-028](../../01_requirements/02_business_usecases/UC-028.md#UC-028) [UC-034](../../01_requirements/02_business_usecases/UC-034.md#UC-034) [UC-038](../../01_requirements/02_business_usecases/UC-038.md#UC-038)…) |
| [`T_PRJ_LEGACY_KEYS`](#TBL-015) | 0 | — | 2 件(例 [UC-096](../../01_requirements/02_business_usecases/UC-096.md#UC-096) [UC-104](../../01_requirements/02_business_usecases/UC-104.md#UC-104)) |
| [`M_FAQS`](#TBL-006) | 12 | [API-016](../03_apis/API-016.md#API-016) [API-018](../03_apis/API-018.md#API-018) [API-025](../03_apis/API-025.md#API-025) [API-026](../03_apis/API-026.md#API-026) [API-027](../03_apis/API-027.md#API-027) [API-028](../03_apis/API-028.md#API-028) [API-030](../03_apis/API-030.md#API-030) [API-031](../03_apis/API-031.md#API-031) [API-033](../03_apis/API-033.md#API-033) [API-038](../03_apis/API-038.md#API-038) [API-041](../03_apis/API-041.md#API-041) [API-042](../03_apis/API-042.md#API-042) | 13 件(例 [UC-054](../../01_requirements/02_business_usecases/UC-054.md#UC-054) [UC-062](../../01_requirements/02_business_usecases/UC-062.md#UC-062) [UC-063](../../01_requirements/02_business_usecases/UC-063.md#UC-063)…) |
| [`TP_FAQ_FTS`](#TBL-030) | 1 | [API-031](../03_apis/API-031.md#API-031) | 6 件(例 [UC-063](../../01_requirements/02_business_usecases/UC-063.md#UC-063) [UC-069](../../01_requirements/02_business_usecases/UC-069.md#UC-069) [UC-070](../../01_requirements/02_business_usecases/UC-070.md#UC-070)…) |
| [`H_QUESTION_LOGS`](#TBL-025) | 5 | [API-018](../03_apis/API-018.md#API-018) [API-032](../03_apis/API-032.md#API-032) [API-038](../03_apis/API-038.md#API-038) [API-039](../03_apis/API-039.md#API-039) [API-040](../03_apis/API-040.md#API-040) | 1 件(例 [UC-054](../../01_requirements/02_business_usecases/UC-054.md#UC-054)) |
| [`T_QLOG_FAQ_REFS`](#TBL-016) | 0 | — | — |
| [`T_INQUIRIES`](#TBL-017) | 7 | [API-018](../03_apis/API-018.md#API-018) [API-034](../03_apis/API-034.md#API-034) [API-035](../03_apis/API-035.md#API-035) [API-036](../03_apis/API-036.md#API-036) [API-038](../03_apis/API-038.md#API-038) [API-039](../03_apis/API-039.md#API-039) [API-040](../03_apis/API-040.md#API-040) | 12 件(例 [UC-046](../../01_requirements/02_business_usecases/UC-046.md#UC-046) [UC-047](../../01_requirements/02_business_usecases/UC-047.md#UC-047) [UC-048](../../01_requirements/02_business_usecases/UC-048.md#UC-048)…) |
| [`H_INQUIRY_FAQ`](#TBL-029) | 0 | — | — |
| [`T_USAGE_METER`](#TBL-020) | 6 | [API-038](../03_apis/API-038.md#API-038) [API-040](../03_apis/API-040.md#API-040) [API-041](../03_apis/API-041.md#API-041) [API-042](../03_apis/API-042.md#API-042) [API-043](../03_apis/API-043.md#API-043) [API-046](../03_apis/API-046.md#API-046) | 10 件(例 [UC-107](../../01_requirements/02_business_usecases/UC-107.md#UC-107) [UC-108](../../01_requirements/02_business_usecases/UC-108.md#UC-108) [UC-170](../../01_requirements/02_business_usecases/UC-170.md#UC-170)…) |
| [`T_BILL_SUBS`](#TBL-018) | 2 | [API-043](../03_apis/API-043.md#API-043) [API-045](../03_apis/API-045.md#API-045) | 5 件(例 [UC-170](../../01_requirements/02_business_usecases/UC-170.md#UC-170) [UC-208](../../01_requirements/02_business_usecases/UC-208.md#UC-208) [UC-209](../../01_requirements/02_business_usecases/UC-209.md#UC-209)…) |
| [`T_BILL_INVOICES`](#TBL-019) | 1 | [API-044](../03_apis/API-044.md#API-044) | 3 件(例 [UC-208](../../01_requirements/02_business_usecases/UC-208.md#UC-208) [UC-210](../../01_requirements/02_business_usecases/UC-210.md#UC-210) [UC-233](../../01_requirements/02_business_usecases/UC-233.md#UC-233)) |
| [`M_PRJ_QUOTA_LIMITS`](#TBL-009) | 2 | [API-046](../03_apis/API-046.md#API-046) [API-047](../03_apis/API-047.md#API-047) | 8 件(例 [UC-170](../../01_requirements/02_business_usecases/UC-170.md#UC-170) [UC-199](../../01_requirements/02_business_usecases/UC-199.md#UC-199) [UC-202](../../01_requirements/02_business_usecases/UC-202.md#UC-202)…) |
| [`M_OWNER_QUOTA_OVR`](#TBL-008) | 0 | — | — |
| [`M_SERVICE_ANNOUNCE`](#TBL-010) | 0 | — | 10 件(例 [UC-136](../../01_requirements/02_business_usecases/UC-136.md#UC-136) [UC-137](../../01_requirements/02_business_usecases/UC-137.md#UC-137) [UC-138](../../01_requirements/02_business_usecases/UC-138.md#UC-138)…) |
| [`M_ANNOUNCE_AUD`](#TBL-011) | 0 | — | — |
| [`T_ANNOUNCE_RCPT`](#TBL-021) | 0 | — | 10 件(例 [UC-136](../../01_requirements/02_business_usecases/UC-136.md#UC-136) [UC-137](../../01_requirements/02_business_usecases/UC-137.md#UC-137) [UC-138](../../01_requirements/02_business_usecases/UC-138.md#UC-138)…) |
| [`T_INBOX_MSG`](#TBL-022) | 4 | [API-048](../03_apis/API-048.md#API-048) [API-049](../03_apis/API-049.md#API-049) [API-050](../03_apis/API-050.md#API-050) [API-051](../03_apis/API-051.md#API-051) | 6 件(例 [UC-233](../../01_requirements/02_business_usecases/UC-233.md#UC-233) [UC-234](../../01_requirements/02_business_usecases/UC-234.md#UC-234) [UC-235](../../01_requirements/02_business_usecases/UC-235.md#UC-235)…) |
| [`H_NOTIF_LOGS`](#TBL-026) | 5 | [API-011](../03_apis/API-011.md#API-011) [API-021](../03_apis/API-021.md#API-021) [API-024](../03_apis/API-024.md#API-024) [API-040](../03_apis/API-040.md#API-040) [API-059](../03_apis/API-059.md#API-059) | 7 件(例 [UC-231](../../01_requirements/02_business_usecases/UC-231.md#UC-231) [UC-233](../../01_requirements/02_business_usecases/UC-233.md#UC-233) [UC-234](../../01_requirements/02_business_usecases/UC-234.md#UC-234)…) |
| [`T_WITHDRAW_REQ`](#TBL-023) | 1 | [API-056](../03_apis/API-056.md#API-056) | 2 件(例 [UC-159](../../01_requirements/02_business_usecases/UC-159.md#UC-159) [UC-232](../../01_requirements/02_business_usecases/UC-232.md#UC-232)) |
| [`H_AUDIT_LOGS`](#TBL-027) | 5 | [API-008](../03_apis/API-008.md#API-008) [API-009](../03_apis/API-009.md#API-009) [API-018](../03_apis/API-018.md#API-018) [API-050](../03_apis/API-050.md#API-050) [API-059](../03_apis/API-059.md#API-059) | 3 件(例 [UC-231](../../01_requirements/02_business_usecases/UC-231.md#UC-231) [UC-232](../../01_requirements/02_business_usecases/UC-232.md#UC-232) [UC-247](../../01_requirements/02_business_usecases/UC-247.md#UC-247)) |
| [`H_ERROR_LOGS`](#TBL-028) | 0 | — | — |
| [`M_EMAIL_SUPPRESS`](#TBL-007) | 1 | [API-059](../03_apis/API-059.md#API-059) | 1 件(例 [UC-231](../../01_requirements/02_business_usecases/UC-231.md#UC-231)) |
| [`TP_AI_THRESH_CACHE`](#TBL-031) | 0 | — | — |

## <span id="readorder"></span>5.読み順

1. 本ページ §2 テーブル一覧でドメイン全体像を把握する。
2. §3 ER 図で親子(契約境界 `M_CONTRACT` → `M_PROJECTS` → 各テーブル)を確認する。
3. §4 対応表で対象テーブルの利用 API / 業務UC を逆引きする。
4. 各テーブルページ(`TBL-NNN.md`)で 項目 / カラム定義 / 制約 / インデックス / コード値 を確認する。
<!-- /p5-cross -->

## <span id="rule"></span>6.命名・分類規約

| 接頭辞 | 分類             | 用途                 |
|--------|------------------|----------------------|
| `M_`   | マスタ           | マスタ・設定         |
| `T_`   | トランザクション | トランザクション     |
| `H_`   | 履歴             | 履歴・ログ(追記専用) |
| `TP_`  | ワーク           | ワーク・派生         |

---

<!-- portal-bottom -->
[基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
