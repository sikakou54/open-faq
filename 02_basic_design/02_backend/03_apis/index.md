<!-- portal-top -->
[設計ポータル](../../../README.md) ／ [基本設計](../../index.md) ／ [バックエンド設計](../index.md) ／ **API設計**
<!-- /portal-top -->

# API 設計書

> **このページは、メインシステムが提供する全 59 エンドポイントの REST / 内部 IF API を、1 エンドポイント = 1 ファイル(`API-001` 〜 `API-059`)でフラット採番し索引する設計書です。** 各 API の詳細は個別ページ(基本情報 / 処理概要 / リクエスト / レスポンス / バリデーション / エラー / 利用テーブル)に展開しています。

*版数 v3.0 ・ 更新 2026-06-21 ・ API数 59 ・ 再構成 P4*

## <span id="conv"></span>0. API 設計の方針・共通仕様

全 API に共通する基本ルール・認証ヘッダ・エラー体系を定義します。各 API ページは本節を前提とし、差分のみを各ページに記載します。

### <span id="conv-policy"></span>0.1 方針

| 観点 | 方針 |
|---|---|
| ベースパス | `/api/v1` 配下に統一(ウィジェット系は `/widget/v1`) |
| データ形式 | JSON。日時は ISO 8601 + 末尾 Z(UTC)。ID は ULID(26 文字、Stripe ID 例外) |
| 認証方式 | 管理 API は Cookie セッション、更新系は CSRF トークン併用。ウィジェットは公開鍵 + ドメイン検証 |
| ページング | カーソル方式に統一(`cursor` / `limit` 50〜200、末尾 `nextCursor=null`) |
| エラー応答 | RFC 7807(`application/problem+json`)。`E-AUTH-*` / `E-AUTHZ-*` / `E-BIZ-*` / `E-INPUT-*` の ID 体系 |
| オーナー境界 | 全 API で `contract_id` による契約分離を強制。違反時は 404 偽装で存在を秘匿 |
| 冪等性 | 書き込み系 API は `Idempotency-Key` ヘッダ(ULID 推奨、24h 保管)を受け付ける |
| 論理削除 | `valid` カラムを持つテーブルへの GET 系は `WHERE valid=1` を強制(監査ログは対象外) |

### <span id="conv-headers"></span>0.2 認証ヘッダ

| ヘッダ | 用途 | 例 |
|---|---|---|
| `Cookie: session=<token>` | 利用者セッション | 管理 API |
| `Authorization: Bearer <wst_*>` | ウィジェットセッション | ウィジェット API |
| `X-CSRF-Token: <token>` | CSRF 対策 | 状態変更系 |
| `Idempotency-Key: <ULID>` | 冪等性 | 書き込み系 |

> [!NOTE]
> **レート制限・キャパシティ** API 層の警告 / 拒否レベルと超過時の挙動は、業務正本である [課金・請求設計書](../../05_billing-design.md) と各 FR / NFR を参照する(FAQ 件数 / 月間質問数 / 公開 API レート / ログイン失敗ロック 等)。

## <span id="list"></span>1. API 一覧(機能グループ別)

全 59 エンドポイントを 13 機能グループに整理します。API ID から個別ページへ移動します。

### <span id="g-1"></span>1.1 認証・セッション

サインアップ / ログイン / 再認証 / メール確認 / 招待 / プロフィール / 契約設定。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-001"></span>[`API-001`](API-001.md#API-001) | **新規登録** POST `/auth/signup` | —(公開) | `M_USER` `M_CONTRACT` `T_TERMS_AGREE` `T_ACCESS_TOKENS` |
| <span id="API-002"></span>[`API-002`](API-002.md#API-002) | **ログイン** POST `/auth/login` | —(公開) | `M_CONTRACT` `M_PRJ_USERS` `T_SESSIONS` |
| <span id="API-003"></span>[`API-003`](API-003.md#API-003) | **ログアウト** POST `/auth/logout` | 認証済み | `T_SESSIONS` |
| <span id="API-004"></span>[`API-004`](API-004.md#API-004) | **パスワード再設定要求** POST `/auth/password-reset-request` | —(公開) | `M_CONTRACT` `M_PRJ_USERS` `T_ACCESS_TOKENS` |
| <span id="API-005"></span>[`API-005`](API-005.md#API-005) | **再認証** POST `/auth/re-auth` | 認証済み | `M_CONTRACT` `M_PRJ_USERS` `T_ACCESS_TOKENS` |
| <span id="API-006"></span>[`API-006`](API-006.md#API-006) | **メール確認** POST `/auth/email-verifications/{token}` | — | `T_ACCESS_TOKENS` `M_CONTRACT` |
| <span id="API-007"></span>[`API-007`](API-007.md#API-007) | **招待トークン検証・プレビュー** POST `/auth/invitations/{token}/preview` | — | `T_ACCESS_TOKENS` `M_PROJECTS` `M_PRJ_USERS` `M_CONTRACT` |
| <span id="API-008"></span>[`API-008`](API-008.md#API-008) | **メンバーアカウント有効化** POST `/auth/invitations/{token}/activate` | — | `T_ACCESS_TOKENS` `M_USER` `M_PRJ_USERS` `T_TERMS_AGREE` `H_AUDIT_LOGS` |
| <span id="API-009"></span>[`API-009`](API-009.md#API-009) | **プロジェクト連絡先メール確認** POST `/auth/contact-verifications/{token}` | — | `T_ACCESS_TOKENS` `M_PROJECTS` `H_AUDIT_LOGS` |
| <span id="API-010"></span>[`API-010`](API-010.md#API-010) | **パスワード再設定確定** POST `/auth/password-reset` | —(公開) | `T_ACCESS_TOKENS` `M_CONTRACT` `M_PRJ_USERS` `T_SESSIONS` |
| <span id="API-011"></span>[`API-011`](API-011.md#API-011) | **連絡先確認メール再送** POST `/auth/contact-verifications/resend` | オーナー専有 | `M_PROJECTS` `T_ACCESS_TOKENS` `H_NOTIF_LOGS` |
| <span id="API-012"></span>[`API-012`](API-012.md#API-012) | **自己プロフィール更新** PATCH `/me/profile` | 認証済み | `M_CONTRACT` `M_PRJ_USERS` `T_ACCESS_TOKENS` |
| <span id="API-013"></span>[`API-013`](API-013.md#API-013) | **自己パスワード変更** PATCH `/me/password` | 認証済み | `T_ACCESS_TOKENS` `M_CONTRACT` `M_PRJ_USERS` |
| <span id="API-014"></span>[`API-014`](API-014.md#API-014) | **契約設定取得** GET `/owner/settings` | オーナー専有 | `M_CONTRACT` |
| <span id="API-015"></span>[`API-015`](API-015.md#API-015) | **契約設定更新** PATCH `/owner/settings` | オーナー専有 | `M_CONTRACT` |

### <span id="g-2"></span>1.2 プロジェクト

プロジェクト CRUD とウィジェット鍵ローテーション。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-016"></span>[`API-016`](API-016.md#API-016) | **プロジェクト一覧** GET `/projects` | **オーナー専有** | `M_PROJECTS` `M_FAQS` `M_ALLOWED_DOMAINS` |
| <span id="API-017"></span>[`API-017`](API-017.md#API-017) | **プロジェクト新規作成** POST `/projects` | **オーナー専有**(プロジェクト設定全般を含めオーナーのみ実行可) | `M_PROJECTS` `M_ALLOWED_DOMAINS` `M_PRJ_USERS` |
| <span id="API-018"></span>[`API-018`](API-018.md#API-018) | **プロジェクト更新・削除** PATCH / DELETE `/projects/{id}` | **オーナー専有** | `M_PROJECTS` `M_ALLOWED_DOMAINS` `M_PRJ_USERS` `T_SESSIONS` `T_ACCESS_TOKENS` `M_FAQS` `H_QUESTION_LOGS` `T_INQUIRIES` `H_AUDIT_LOGS` |
| <span id="API-019"></span>[`API-019`](API-019.md#API-019) | **ウィジェット鍵ローテーション** POST `/projects/{id}/widget-key/rotate` | オーナー専有 | `M_PROJECTS` |

### <span id="g-3"></span>1.3 メンバー

プロジェクト単位のメンバー招待 / 情報更新 / 離脱 / 再送。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-020"></span>[`API-020`](API-020.md#API-020) | **メンバー一覧** GET `/projects/{id}/members` | オーナー / 当該プロジェクトのメンバー | `M_PRJ_USERS` |
| <span id="API-021"></span>[`API-021`](API-021.md#API-021) | **メンバー招待** POST `/projects/{id}/members` | オーナー / 当該プロジェクトのメンバー | `M_USER` `M_PRJ_USERS` `T_ACCESS_TOKENS` `H_NOTIF_LOGS` |
| <span id="API-022"></span>[`API-022`](API-022.md#API-022) | **メンバー情報更新** PATCH `/projects/{id}/members/{userId}` | オーナー / 当該プロジェクトのメンバー | `M_PRJ_USERS` |
| <span id="API-023"></span>[`API-023`](API-023.md#API-023) | **プロジェクト割当解除** DELETE `/projects/{id}/members/{userId}` | オーナー / 当該プロジェクトのメンバー | `M_PRJ_USERS` `T_SESSIONS` `T_ACCESS_TOKENS` |
| <span id="API-024"></span>[`API-024`](API-024.md#API-024) | **招待メール再送** POST `/members/{id}/resend-invitation` | オーナー / 当該プロジェクトのメンバー | `M_PRJ_USERS` `T_ACCESS_TOKENS` `H_NOTIF_LOGS` |

### <span id="g-4"></span>1.4 FAQ

FAQ の CRUD・一括状態変更・CSV 入出力・全文検索・質問ログ検索。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-025"></span>[`API-025`](API-025.md#API-025) | **FAQ 一覧** GET `/faqs` | オーナー / 当該プロジェクトのメンバー | `M_FAQS` |
| <span id="API-026"></span>[`API-026`](API-026.md#API-026) | **FAQ 作成・更新・削除** POST / PATCH / DELETE `/faqs`, `/faqs/{id}` | オーナー / 当該プロジェクトのメンバー | `M_FAQS` |
| <span id="API-027"></span>[`API-027`](API-027.md#API-027) | **FAQ 一括状態変更** POST `/faqs/bulk-status` | オーナー / 当該プロジェクトのメンバー | `M_FAQS` |
| <span id="API-028"></span>[`API-028`](API-028.md#API-028) | **FAQ CSV インポート** POST `/faqs/import` | オーナー / 当該プロジェクトのメンバー | `M_FAQS` |
| <span id="API-029"></span>[`API-029`](API-029.md#API-029) | **FAQ インポートテンプレート** GET `/faqs/import/template` | オーナー / 当該プロジェクトのメンバー(API-022 と同一) | — |
| <span id="API-030"></span>[`API-030`](API-030.md#API-030) | **FAQ CSV エクスポート** GET `/faqs/export` | オーナー / 当該プロジェクトのメンバー | `M_FAQS` |
| <span id="API-031"></span>[`API-031`](API-031.md#API-031) | **FAQ 全文検索** GET `/projects/{id}/faqs/search` | オーナー / 当該プロジェクトのメンバー | `M_FAQS` `TP_FAQ_FTS` |
| <span id="API-032"></span>[`API-032`](API-032.md#API-032) | **質問ログ検索** GET `/projects/{id}/question-logs/search` | オーナー / 当該プロジェクトのメンバー | `H_QUESTION_LOGS` |
| <span id="API-033"></span>[`API-033`](API-033.md#API-033) | **FAQ 個別取得** GET `/faqs/{id}` | オーナー / 当該プロジェクトのメンバー | `M_FAQS` |

### <span id="g-5"></span>1.5 未解決質問

未解決質問の一覧・詳細・状況切替・CSV エクスポート。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-034"></span>[`API-034`](API-034.md#API-034) | **未解決質問一覧** GET `/inquiries` | オーナー / 当該プロジェクトのメンバー | `T_INQUIRIES` |
| <span id="API-035"></span>[`API-035`](API-035.md#API-035) | **未解決質問詳細・状況切替** GET / PATCH `/inquiries/{id}` | オーナー / 当該プロジェクトのメンバー | `T_INQUIRIES` |
| <span id="API-036"></span>[`API-036`](API-036.md#API-036) | **未解決質問 CSV エクスポート** GET `/inquiries/export` | オーナー / 当該プロジェクトのメンバー | `T_INQUIRIES` |

### <span id="g-6"></span>1.6 ウィジェット配信

エンドユーザー向けウィジェットの bootstrap / ask / 問い合わせ。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-037"></span>[`API-037`](API-037.md#API-037) | **ウィジェット起動** POST `/widget/v1/bootstrap` | end_user(公開キー) | `M_PROJECTS` `M_ALLOWED_DOMAINS` `M_CONTRACT` |
| <span id="API-038"></span>[`API-038`](API-038.md#API-038) | **ウィジェット質問送信** POST `/widget/v1/ask` | end_user(セッション) | `H_QUESTION_LOGS` `M_FAQS` `T_USAGE_METER` `T_INQUIRIES` |
| <span id="API-039"></span>[`API-039`](API-039.md#API-039) | **ウィジェット未解決質問登録** POST `/widget/v1/inquiries` | end_user(セッション) | `T_INQUIRIES` `H_QUESTION_LOGS` |

### <span id="g-7"></span>1.7 ダッシュボード

概要画面向けの集計サマリー。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-040"></span>[`API-040`](API-040.md#API-040) | **ダッシュボードサマリ** GET `/dashboard/summary` | オーナー / 当該プロジェクトのメンバー(`notification` ブロックの配信失敗・バウンス件数はオーナー専有) | `T_USAGE_METER` `H_QUESTION_LOGS` `T_INQUIRIES` `H_NOTIF_LOGS` |

### <span id="g-8"></span>1.8 利用量・課金

利用量・請求サマリー・請求書・支払方法・上限設定。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-041"></span>[`API-041`](API-041.md#API-041) | **利用量サマリ(プロジェクト)** GET `/usage` | オーナー / 当該プロジェクトのメンバー | `T_USAGE_METER` `M_FAQS` |
| <span id="API-042"></span>[`API-042`](API-042.md#API-042) | **利用量サマリ(契約)** GET `/owner/projects/usage` | オーナー専有 | `T_USAGE_METER` `M_FAQS` |
| <span id="API-043"></span>[`API-043`](API-043.md#API-043) | **請求サマリ** GET `/billing/summary` | オーナー専有 | `T_BILL_SUBS` `T_USAGE_METER` |
| <span id="API-044"></span>[`API-044`](API-044.md#API-044) | **請求書一覧** GET `/billing/invoices` | オーナー専有 | `T_BILL_INVOICES` |
| <span id="API-045"></span>[`API-045`](API-045.md#API-045) | **支払方法 取得・登録・更新** GET / PUT `/billing/payment-method` | **オーナー専有** | `T_BILL_SUBS` |
| <span id="API-046"></span>[`API-046`](API-046.md#API-046) | **プロジェクト上限・アラート取得** GET `/projects/{id}/quota-limits` | オーナー / 当該プロジェクトのメンバー(閲覧) | `M_PRJ_QUOTA_LIMITS` `T_USAGE_METER` |
| <span id="API-047"></span>[`API-047`](API-047.md#API-047) | **プロジェクト上限・アラート更新** PATCH `/projects/{id}/quota-limits/questions` | オーナー / 当該プロジェクトのメンバー | `M_PRJ_QUOTA_LIMITS` |

### <span id="g-9"></span>1.9 お知らせ受信箱

受信箱の取得・既読化・未読件数。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-048"></span>[`API-048`](API-048.md#API-048) | **お知らせ一覧** GET `/me/announcements` | オーナー / メンバー | `T_INBOX_MSG` |
| <span id="API-049"></span>[`API-049`](API-049.md#API-049) | **お知らせ個別既読** POST `/me/announcements/{id}/read` | オーナー / メンバー | `T_INBOX_MSG` |
| <span id="API-050"></span>[`API-050`](API-050.md#API-050) | **お知らせ一括既読** POST `/me/announcements/read` | オーナー / メンバー | `T_INBOX_MSG` `H_AUDIT_LOGS` |
| <span id="API-051"></span>[`API-051`](API-051.md#API-051) | **お知らせ未読件数** GET `/me/announcements/unread-summary` | オーナー / メンバー | `T_INBOX_MSG` |

### <span id="g-10"></span>1.10 規約・退会

規約 / プライバシー取得・同意・退会申請。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-052"></span>[`API-052`](API-052.md#API-052) | **利用規約 最新版取得** GET `/terms/current` | —(公開) | — |
| <span id="API-053"></span>[`API-053`](API-053.md#API-053) | **プライバシーポリシー 最新版取得** GET `/privacy/current` | —(公開) | — |
| <span id="API-054"></span>[`API-054`](API-054.md#API-054) | **利用規約 同意** POST `/terms/agree` | オーナー / メンバー | — |
| <span id="API-055"></span>[`API-055`](API-055.md#API-055) | **プライバシーポリシー 同意** POST `/privacy/agree` | オーナー / メンバー | — |
| <span id="API-056"></span>[`API-056`](API-056.md#API-056) | **退会申請** POST `/withdrawal-requests` | オーナー専有 | `T_WITHDRAW_REQ` `M_CONTRACT` |

### <span id="g-11"></span>1.11 AI 推論 IF

AI 推論連携インターフェース(外部 LLM)。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-057"></span>[`API-057`](API-057.md#API-057) | **AI 推論 IF(`AnswerProvider`)** | — | — |

### <span id="g-12"></span>1.12 メール配信 IF

トランザクションメール送信インターフェース。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-058"></span>[`API-058`](API-058.md#API-058) | **メール配信 IF(`EmailProvider`)** | — | — |

### <span id="g-13"></span>1.13 外部 Webhook

メール配信プロバイダ(Resend)からの Webhook 受信。

| API ID | API / エンドポイント | 認可 | 利用テーブル |
|---|---|---|---|
| <span id="API-059"></span>[`API-059`](API-059.md#API-059) | **外部 Webhook(Resend)** POST `/webhooks/resend` | —(署名検証のみ) | `H_NOTIF_LOGS` `M_EMAIL_SUPPRESS` `H_AUDIT_LOGS` |

## <span id="trace"></span>2. API ↔ UC / EVT / TBL 対応表

各 API を呼び出す画面イベント(EVT)・業務ユースケース(UC)と、参照・更新するテーブル(TBL)の結線一覧です。EVT・UC から逆引きできない API は MVP では画面イベント層に直接の呼び出しを持たない(内部 / 検索系)ことを示します。

| API ID | API名 | 対応EVT | 対応UC | 利用テーブル |
|---|---|---|---|---|
| [`API-001`](API-001.md#API-001) | 新規登録 | [EVT-016](../../01_frontend/02_screen_events/EVT-016.md#EVT-016) [EVT-152](../../01_frontend/02_screen_events/EVT-152.md#EVT-152) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) | `M_USER` `M_CONTRACT` `T_TERMS_AGREE` `T_ACCESS_TOKENS` |
| [`API-002`](API-002.md#API-002) | ログイン | [EVT-004](../../01_frontend/02_screen_events/EVT-004.md#EVT-004) | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) [UC-072](../../../01_requirements/04_business_usecases/UC-072.md#UC-072) [UC-073](../../../01_requirements/04_business_usecases/UC-073.md#UC-073) | `M_CONTRACT` `M_PRJ_USERS` `T_SESSIONS` |
| [`API-003`](API-003.md#API-003) | ログアウト | — | [UC-072](../../../01_requirements/04_business_usecases/UC-072.md#UC-072) [UC-074](../../../01_requirements/04_business_usecases/UC-074.md#UC-074) | `T_SESSIONS` |
| [`API-004`](API-004.md#API-004) | パスワード再設定要求 | [EVT-020](../../01_frontend/02_screen_events/EVT-020.md#EVT-020) [EVT-021](../../01_frontend/02_screen_events/EVT-021.md#EVT-021) [EVT-023](../../01_frontend/02_screen_events/EVT-023.md#EVT-023) | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) | `M_CONTRACT` `M_PRJ_USERS` `T_ACCESS_TOKENS` |
| [`API-005`](API-005.md#API-005) | 再認証 | [EVT-159](../../01_frontend/02_screen_events/EVT-159.md#EVT-159) [EVT-177](../../01_frontend/02_screen_events/EVT-177.md#EVT-177) [EVT-178](../../01_frontend/02_screen_events/EVT-178.md#EVT-178) | [UC-017](../../../01_requirements/04_business_usecases/UC-017.md#UC-017) [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) [UC-009](../../../01_requirements/04_business_usecases/UC-009.md#UC-009) [UC-010](../../../01_requirements/04_business_usecases/UC-010.md#UC-010) [UC-038](../../../01_requirements/04_business_usecases/UC-038.md#UC-038) | `M_CONTRACT` `M_PRJ_USERS` `T_ACCESS_TOKENS` |
| [`API-006`](API-006.md#API-006) | メール確認 | [EVT-151](../../01_frontend/02_screen_events/EVT-151.md#EVT-151) | [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) | `T_ACCESS_TOKENS` `M_CONTRACT` |
| [`API-007`](API-007.md#API-007) | 招待トークン検証・プレビュー | [EVT-181](../../01_frontend/02_screen_events/EVT-181.md#EVT-181) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) | `T_ACCESS_TOKENS` `M_PROJECTS` `M_PRJ_USERS` `M_CONTRACT` |
| [`API-008`](API-008.md#API-008) | メンバーアカウント有効化 | [EVT-190](../../01_frontend/02_screen_events/EVT-190.md#EVT-190) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) | `T_ACCESS_TOKENS` `M_USER` `M_PRJ_USERS` `T_TERMS_AGREE` `H_AUDIT_LOGS` |
| [`API-009`](API-009.md#API-009) | プロジェクト連絡先メール確認 | [EVT-194](../../01_frontend/02_screen_events/EVT-194.md#EVT-194) | [UC-007](../../../01_requirements/04_business_usecases/UC-007.md#UC-007) | `T_ACCESS_TOKENS` `M_PROJECTS` `H_AUDIT_LOGS` |
| [`API-010`](API-010.md#API-010) | パスワード再設定確定 | [EVT-025](../../01_frontend/02_screen_events/EVT-025.md#EVT-025) | [UC-005](../../../01_requirements/04_business_usecases/UC-005.md#UC-005) | `T_ACCESS_TOKENS` `M_CONTRACT` `M_PRJ_USERS` `T_SESSIONS` |
| [`API-011`](API-011.md#API-011) | 連絡先確認メール再送 | [EVT-040](../../01_frontend/02_screen_events/EVT-040.md#EVT-040) | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) | `M_PROJECTS` `T_ACCESS_TOKENS` `H_NOTIF_LOGS` |
| [`API-012`](API-012.md#API-012) | 自己プロフィール更新 | [EVT-177](../../01_frontend/02_screen_events/EVT-177.md#EVT-177) | [UC-009](../../../01_requirements/04_business_usecases/UC-009.md#UC-009) | `M_CONTRACT` `M_PRJ_USERS` `T_ACCESS_TOKENS` |
| [`API-013`](API-013.md#API-013) | 自己パスワード変更 | [EVT-178](../../01_frontend/02_screen_events/EVT-178.md#EVT-178) | [UC-010](../../../01_requirements/04_business_usecases/UC-010.md#UC-010) | `T_ACCESS_TOKENS` `M_CONTRACT` `M_PRJ_USERS` |
| [`API-014`](API-014.md#API-014) | 契約設定取得 | [EVT-215](../../01_frontend/02_screen_events/EVT-215.md#EVT-215) | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) | `M_CONTRACT` |
| [`API-015`](API-015.md#API-015) | 契約設定更新 | [EVT-217](../../01_frontend/02_screen_events/EVT-217.md#EVT-217) | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) | `M_CONTRACT` |
| [`API-016`](API-016.md#API-016) | プロジェクト一覧 | [EVT-028](../../01_frontend/02_screen_events/EVT-028.md#EVT-028) | [UC-014](../../../01_requirements/04_business_usecases/UC-014.md#UC-014) | `M_PROJECTS` `M_FAQS` `M_ALLOWED_DOMAINS` |
| [`API-017`](API-017.md#API-017) | プロジェクト新規作成 | [EVT-038](../../01_frontend/02_screen_events/EVT-038.md#EVT-038) | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) | `M_PROJECTS` `M_ALLOWED_DOMAINS` `M_PRJ_USERS` |
| [`API-018`](API-018.md#API-018) | プロジェクト更新・削除 | [EVT-034](../../01_frontend/02_screen_events/EVT-034.md#EVT-034) [EVT-039](../../01_frontend/02_screen_events/EVT-039.md#EVT-039) [EVT-042](../../01_frontend/02_screen_events/EVT-042.md#EVT-042) [EVT-105](../../01_frontend/02_screen_events/EVT-105.md#EVT-105) | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) [UC-017](../../../01_requirements/04_business_usecases/UC-017.md#UC-017) [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) | `M_PROJECTS` `M_ALLOWED_DOMAINS` `M_PRJ_USERS` `T_SESSIONS` `T_ACCESS_TOKENS` `M_FAQS` `H_QUESTION_LOGS` `T_INQUIRIES` `H_AUDIT_LOGS` |
| [`API-019`](API-019.md#API-019) | ウィジェット鍵ローテーション | [EVT-104](../../01_frontend/02_screen_events/EVT-104.md#EVT-104) | [UC-041](../../../01_requirements/04_business_usecases/UC-041.md#UC-041) | `M_PROJECTS` |
| [`API-020`](API-020.md#API-020) | メンバー一覧 | [EVT-115](../../01_frontend/02_screen_events/EVT-115.md#EVT-115) [EVT-116](../../01_frontend/02_screen_events/EVT-116.md#EVT-116) [EVT-117](../../01_frontend/02_screen_events/EVT-117.md#EVT-117) [EVT-124](../../01_frontend/02_screen_events/EVT-124.md#EVT-124) | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) [UC-048](../../../01_requirements/04_business_usecases/UC-048.md#UC-048) [UC-020](../../../01_requirements/04_business_usecases/UC-020.md#UC-020) [UC-066](../../../01_requirements/04_business_usecases/UC-066.md#UC-066) | `M_PRJ_USERS` |
| [`API-021`](API-021.md#API-021) | メンバー招待 | [EVT-126](../../01_frontend/02_screen_events/EVT-126.md#EVT-126) | [UC-019](../../../01_requirements/04_business_usecases/UC-019.md#UC-019) | `M_USER` `M_PRJ_USERS` `T_ACCESS_TOKENS` `H_NOTIF_LOGS` |
| [`API-022`](API-022.md#API-022) | メンバー情報更新 | [EVT-128](../../01_frontend/02_screen_events/EVT-128.md#EVT-128) | [UC-020](../../../01_requirements/04_business_usecases/UC-020.md#UC-020) | `M_PRJ_USERS` |
| [`API-023`](API-023.md#API-023) | プロジェクト割当解除 | [EVT-130](../../01_frontend/02_screen_events/EVT-130.md#EVT-130) | [UC-021](../../../01_requirements/04_business_usecases/UC-021.md#UC-021) | `M_PRJ_USERS` `T_SESSIONS` `T_ACCESS_TOKENS` |
| [`API-024`](API-024.md#API-024) | 招待メール再送 | [EVT-127](../../01_frontend/02_screen_events/EVT-127.md#EVT-127) | [UC-019](../../../01_requirements/04_business_usecases/UC-019.md#UC-019) | `M_PRJ_USERS` `T_ACCESS_TOKENS` `H_NOTIF_LOGS` |
| [`API-025`](API-025.md#API-025) | FAQ 一覧 | [EVT-062](../../01_frontend/02_screen_events/EVT-062.md#EVT-062) [EVT-063](../../01_frontend/02_screen_events/EVT-063.md#EVT-063) [EVT-064](../../01_frontend/02_screen_events/EVT-064.md#EVT-064) [EVT-065](../../01_frontend/02_screen_events/EVT-065.md#EVT-065) | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) [UC-027](../../../01_requirements/04_business_usecases/UC-027.md#UC-027) [UC-026](../../../01_requirements/04_business_usecases/UC-026.md#UC-026) | `M_FAQS` |
| [`API-026`](API-026.md#API-026) | FAQ 作成・更新・削除 | [EVT-071](../../01_frontend/02_screen_events/EVT-071.md#EVT-071) [EVT-081](../../01_frontend/02_screen_events/EVT-081.md#EVT-081) [EVT-082](../../01_frontend/02_screen_events/EVT-082.md#EVT-082) [EVT-084](../../01_frontend/02_screen_events/EVT-084.md#EVT-084) | [UC-026](../../../01_requirements/04_business_usecases/UC-026.md#UC-026) [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) [UC-026](../../../01_requirements/04_business_usecases/UC-026.md#UC-026) | `M_FAQS` |
| [`API-027`](API-027.md#API-027) | FAQ 一括状態変更 | [EVT-069](../../01_frontend/02_screen_events/EVT-069.md#EVT-069) [EVT-070](../../01_frontend/02_screen_events/EVT-070.md#EVT-070) | [UC-027](../../../01_requirements/04_business_usecases/UC-027.md#UC-027) | `M_FAQS` |
| [`API-028`](API-028.md#API-028) | FAQ CSV インポート | [EVT-093](../../01_frontend/02_screen_events/EVT-093.md#EVT-093) | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) [UC-051](../../../01_requirements/04_business_usecases/UC-051.md#UC-051) | `M_FAQS` |
| [`API-029`](API-029.md#API-029) | FAQ インポートテンプレート | [EVT-091](../../01_frontend/02_screen_events/EVT-091.md#EVT-091) | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) | — |
| [`API-030`](API-030.md#API-030) | FAQ CSV エクスポート | [EVT-074](../../01_frontend/02_screen_events/EVT-074.md#EVT-074) | [UC-029](../../../01_requirements/04_business_usecases/UC-029.md#UC-029) | `M_FAQS` |
| [`API-031`](API-031.md#API-031) | FAQ 全文検索 | — | — | `M_FAQS` `TP_FAQ_FTS` |
| [`API-032`](API-032.md#API-032) | 質問ログ検索 | — | — | `H_QUESTION_LOGS` |
| [`API-033`](API-033.md#API-033) | FAQ 個別取得 | [EVT-076](../../01_frontend/02_screen_events/EVT-076.md#EVT-076) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) | `M_FAQS` |
| [`API-034`](API-034.md#API-034) | 未解決質問一覧 | [EVT-046](../../01_frontend/02_screen_events/EVT-046.md#EVT-046) [EVT-047](../../01_frontend/02_screen_events/EVT-047.md#EVT-047) [EVT-048](../../01_frontend/02_screen_events/EVT-048.md#EVT-048) [EVT-051](../../01_frontend/02_screen_events/EVT-051.md#EVT-051) [EVT-052](../../01_frontend/02_screen_events/EVT-052.md#EVT-052) | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) | `T_INQUIRIES` |
| [`API-035`](API-035.md#API-035) | 未解決質問詳細・状況切替 | [EVT-054](../../01_frontend/02_screen_events/EVT-054.md#EVT-054) [EVT-056](../../01_frontend/02_screen_events/EVT-056.md#EVT-056) [EVT-057](../../01_frontend/02_screen_events/EVT-057.md#EVT-057) | [UC-031](../../../01_requirements/04_business_usecases/UC-031.md#UC-031) [UC-032](../../../01_requirements/04_business_usecases/UC-032.md#UC-032) | `T_INQUIRIES` |
| [`API-036`](API-036.md#API-036) | 未解決質問 CSV エクスポート | [EVT-049](../../01_frontend/02_screen_events/EVT-049.md#EVT-049) | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) | `T_INQUIRIES` |
| [`API-037`](API-037.md#API-037) | ウィジェット起動 | [EVT-223](../../01_frontend/02_screen_events/EVT-223.md#EVT-223) [EVT-229](../../01_frontend/02_screen_events/EVT-229.md#EVT-229) | [UC-042](../../../01_requirements/04_business_usecases/UC-042.md#UC-042) [UC-044](../../../01_requirements/04_business_usecases/UC-044.md#UC-044) | `M_PROJECTS` `M_ALLOWED_DOMAINS` `M_CONTRACT` |
| [`API-038`](API-038.md#API-038) | ウィジェット質問送信 | [EVT-226](../../01_frontend/02_screen_events/EVT-226.md#EVT-226) [EVT-227](../../01_frontend/02_screen_events/EVT-227.md#EVT-227) [EVT-228](../../01_frontend/02_screen_events/EVT-228.md#EVT-228) [EVT-229](../../01_frontend/02_screen_events/EVT-229.md#EVT-229) | [UC-043](../../../01_requirements/04_business_usecases/UC-043.md#UC-043) [UC-044](../../../01_requirements/04_business_usecases/UC-044.md#UC-044) | `H_QUESTION_LOGS` `M_FAQS` `T_USAGE_METER` `T_INQUIRIES` |
| [`API-039`](API-039.md#API-039) | ウィジェット未解決質問登録 | [EVT-227](../../01_frontend/02_screen_events/EVT-227.md#EVT-227) | [UC-044](../../../01_requirements/04_business_usecases/UC-044.md#UC-044) | `T_INQUIRIES` `H_QUESTION_LOGS` |
| [`API-040`](API-040.md#API-040) | ダッシュボードサマリ | [EVT-107](../../01_frontend/02_screen_events/EVT-107.md#EVT-107) [EVT-108](../../01_frontend/02_screen_events/EVT-108.md#EVT-108) | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) [UC-067](../../../01_requirements/04_business_usecases/UC-067.md#UC-067) [UC-056](../../../01_requirements/04_business_usecases/UC-056.md#UC-056) | `T_USAGE_METER` `H_QUESTION_LOGS` `T_INQUIRIES` `H_NOTIF_LOGS` |
| [`API-041`](API-041.md#API-041) | 利用量サマリ(プロジェクト) | [EVT-170](../../01_frontend/02_screen_events/EVT-170.md#EVT-170) [EVT-199](../../01_frontend/02_screen_events/EVT-199.md#EVT-199) | [UC-036](../../../01_requirements/04_business_usecases/UC-036.md#UC-036) [UC-034](../../../01_requirements/04_business_usecases/UC-034.md#UC-034) [UC-048](../../../01_requirements/04_business_usecases/UC-048.md#UC-048) [UC-056](../../../01_requirements/04_business_usecases/UC-056.md#UC-056) | `T_USAGE_METER` `M_FAQS` |
| [`API-042`](API-042.md#API-042) | 利用量サマリ(契約) | [EVT-170](../../01_frontend/02_screen_events/EVT-170.md#EVT-170) | [UC-036](../../../01_requirements/04_business_usecases/UC-036.md#UC-036) | `T_USAGE_METER` `M_FAQS` |
| [`API-043`](API-043.md#API-043) | 請求サマリ | [EVT-208](../../01_frontend/02_screen_events/EVT-208.md#EVT-208) | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) [UC-059](../../../01_requirements/04_business_usecases/UC-059.md#UC-059) | `T_BILL_SUBS` `T_USAGE_METER` |
| [`API-044`](API-044.md#API-044) | 請求書一覧 | [EVT-208](../../01_frontend/02_screen_events/EVT-208.md#EVT-208) | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) | `T_BILL_INVOICES` |
| [`API-045`](API-045.md#API-045) | 支払方法 取得・登録・更新 | [EVT-209](../../01_frontend/02_screen_events/EVT-209.md#EVT-209) [EVT-213](../../01_frontend/02_screen_events/EVT-213.md#EVT-213) | [UC-038](../../../01_requirements/04_business_usecases/UC-038.md#UC-038) [UC-060](../../../01_requirements/04_business_usecases/UC-060.md#UC-060) | `T_BILL_SUBS` |
| [`API-046`](API-046.md#API-046) | プロジェクト上限・アラート取得 | [EVT-199](../../01_frontend/02_screen_events/EVT-199.md#EVT-199) [EVT-202](../../01_frontend/02_screen_events/EVT-202.md#EVT-202) | [UC-034](../../../01_requirements/04_business_usecases/UC-034.md#UC-034) [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) [UC-057](../../../01_requirements/04_business_usecases/UC-057.md#UC-057) [UC-058](../../../01_requirements/04_business_usecases/UC-058.md#UC-058) | `M_PRJ_QUOTA_LIMITS` `T_USAGE_METER` |
| [`API-047`](API-047.md#API-047) | プロジェクト上限・アラート更新 | [EVT-206](../../01_frontend/02_screen_events/EVT-206.md#EVT-206) | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) | `M_PRJ_QUOTA_LIMITS` |
| [`API-048`](API-048.md#API-048) | お知らせ一覧 | [EVT-136](../../01_frontend/02_screen_events/EVT-136.md#EVT-136) [EVT-137](../../01_frontend/02_screen_events/EVT-137.md#EVT-137) [EVT-138](../../01_frontend/02_screen_events/EVT-138.md#EVT-138) [EVT-139](../../01_frontend/02_screen_events/EVT-139.md#EVT-139) [EVT-145](../../01_frontend/02_screen_events/EVT-145.md#EVT-145) [EVT-147](../../01_frontend/02_screen_events/EVT-147.md#EVT-147) | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) [UC-046](../../../01_requirements/04_business_usecases/UC-046.md#UC-046) [UC-064](../../../01_requirements/04_business_usecases/UC-064.md#UC-064) [UC-065](../../../01_requirements/04_business_usecases/UC-065.md#UC-065) | `T_INBOX_MSG` |
| [`API-049`](API-049.md#API-049) | お知らせ個別既読 | [EVT-141](../../01_frontend/02_screen_events/EVT-141.md#EVT-141) [EVT-147](../../01_frontend/02_screen_events/EVT-147.md#EVT-147) | [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) [UC-046](../../../01_requirements/04_business_usecases/UC-046.md#UC-046) | `T_INBOX_MSG` |
| [`API-050`](API-050.md#API-050) | お知らせ一括既読 | [EVT-142](../../01_frontend/02_screen_events/EVT-142.md#EVT-142) [EVT-143](../../01_frontend/02_screen_events/EVT-143.md#EVT-143) [EVT-144](../../01_frontend/02_screen_events/EVT-144.md#EVT-144) | [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) | `T_INBOX_MSG` `H_AUDIT_LOGS` |
| [`API-051`](API-051.md#API-051) | お知らせ未読件数 | [EVT-136](../../01_frontend/02_screen_events/EVT-136.md#EVT-136) | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) | `T_INBOX_MSG` |
| [`API-052`](API-052.md#API-052) | 利用規約 最新版取得 | [EVT-133](../../01_frontend/02_screen_events/EVT-133.md#EVT-133) [EVT-164](../../01_frontend/02_screen_events/EVT-164.md#EVT-164) | [UC-011](../../../01_requirements/04_business_usecases/UC-011.md#UC-011) [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) | — |
| [`API-053`](API-053.md#API-053) | プライバシーポリシー 最新版取得 | [EVT-164](../../01_frontend/02_screen_events/EVT-164.md#EVT-164) [EVT-196](../../01_frontend/02_screen_events/EVT-196.md#EVT-196) | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) [UC-012](../../../01_requirements/04_business_usecases/UC-012.md#UC-012) | — |
| [`API-054`](API-054.md#API-054) | 利用規約 同意 | [EVT-135](../../01_frontend/02_screen_events/EVT-135.md#EVT-135) [EVT-169](../../01_frontend/02_screen_events/EVT-169.md#EVT-169) | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) | — |
| [`API-055`](API-055.md#API-055) | プライバシーポリシー 同意 | [EVT-169](../../01_frontend/02_screen_events/EVT-169.md#EVT-169) | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) | — |
| [`API-056`](API-056.md#API-056) | 退会申請 | [EVT-159](../../01_frontend/02_screen_events/EVT-159.md#EVT-159) | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) | `T_WITHDRAW_REQ` `M_CONTRACT` |
| [`API-057`](API-057.md#API-057) | AI 推論 IF(`AnswerProvider`) | — | [UC-052](../../../01_requirements/04_business_usecases/UC-052.md#UC-052) | — |
| [`API-058`](API-058.md#API-058) | メール配信 IF(`EmailProvider`) | — | [UC-059](../../../01_requirements/04_business_usecases/UC-059.md#UC-059) [UC-064](../../../01_requirements/04_business_usecases/UC-064.md#UC-064) [UC-065](../../../01_requirements/04_business_usecases/UC-065.md#UC-065) [UC-066](../../../01_requirements/04_business_usecases/UC-066.md#UC-066) [UC-057](../../../01_requirements/04_business_usecases/UC-057.md#UC-057) [UC-067](../../../01_requirements/04_business_usecases/UC-067.md#UC-067) | — |
| [`API-059`](API-059.md#API-059) | 外部 Webhook(Resend) | — | [UC-063](../../../01_requirements/04_business_usecases/UC-063.md#UC-063) | `H_NOTIF_LOGS` `M_EMAIL_SUPPRESS` `H_AUDIT_LOGS` |

## <span id="reading"></span>3. 読み順

1. 本ページ §0 で共通仕様(認証ヘッダ・エラー体系・境界判定)を把握する。
2. §1 の機能グループ一覧で対象 API を特定し、API ID から個別ページへ移動する。
3. 個別ページの「項目」表で対応画面・対応UC・対応EVT をたどり、画面設計 / ユースケース設計と縦串で確認する。
4. §2 の対応表で API ↔ EVT / UC / TBL の結線を俯瞰する。

---

<!-- portal-bottom -->
[← バックエンド設計](../index.md) ・ [基本設計](../../index.md) ・ [↑ 設計ポータル](../../../README.md)
<!-- /portal-bottom -->
