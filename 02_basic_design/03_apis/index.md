<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ **API設計**
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
> **レート制限・キャパシティ** API 層の警告 / 拒否レベルと超過時の挙動は、業務正本である [課金・請求設計書](../05_billing-design.md) と各 FR / NFR を参照する(FAQ 件数 / 月間質問数 / 公開 API レート / ログイン失敗ロック 等)。

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
| [`API-001`](API-001.md#API-001) | 新規登録 | [EVT-016](../02_screen_events/EVT-016.md#EVT-016) [EVT-152](../02_screen_events/EVT-152.md#EVT-152) | [UC-016](../../01_requirements/02_business_usecases/UC-016.md#UC-016) [UC-152](../../01_requirements/02_business_usecases/UC-152.md#UC-152) | `M_USER` `M_CONTRACT` `T_TERMS_AGREE` `T_ACCESS_TOKENS` |
| [`API-002`](API-002.md#API-002) | ログイン | [EVT-004](../02_screen_events/EVT-004.md#EVT-004) | [UC-001](../../01_requirements/02_business_usecases/UC-001.md#UC-001) [UC-004](../../01_requirements/02_business_usecases/UC-004.md#UC-004) [UC-242](../../01_requirements/02_business_usecases/UC-242.md#UC-242) [UC-243](../../01_requirements/02_business_usecases/UC-243.md#UC-243) | `M_CONTRACT` `M_PRJ_USERS` `T_SESSIONS` |
| [`API-003`](API-003.md#API-003) | ログアウト | — | [UC-242](../../01_requirements/02_business_usecases/UC-242.md#UC-242) [UC-244](../../01_requirements/02_business_usecases/UC-244.md#UC-244) | `T_SESSIONS` |
| [`API-004`](API-004.md#API-004) | パスワード再設定要求 | [EVT-020](../02_screen_events/EVT-020.md#EVT-020) [EVT-021](../02_screen_events/EVT-021.md#EVT-021) [EVT-023](../02_screen_events/EVT-023.md#EVT-023) | [UC-020](../../01_requirements/02_business_usecases/UC-020.md#UC-020) [UC-021](../../01_requirements/02_business_usecases/UC-021.md#UC-021) [UC-023](../../01_requirements/02_business_usecases/UC-023.md#UC-023) | `M_CONTRACT` `M_PRJ_USERS` `T_ACCESS_TOKENS` |
| [`API-005`](API-005.md#API-005) | 再認証 | [EVT-159](../02_screen_events/EVT-159.md#EVT-159) [EVT-177](../02_screen_events/EVT-177.md#EVT-177) [EVT-178](../02_screen_events/EVT-178.md#EVT-178) | [UC-042](../../01_requirements/02_business_usecases/UC-042.md#UC-042) [UC-159](../../01_requirements/02_business_usecases/UC-159.md#UC-159) [UC-177](../../01_requirements/02_business_usecases/UC-177.md#UC-177) [UC-178](../../01_requirements/02_business_usecases/UC-178.md#UC-178) [UC-209](../../01_requirements/02_business_usecases/UC-209.md#UC-209) [UC-213](../../01_requirements/02_business_usecases/UC-213.md#UC-213) | `M_CONTRACT` `M_PRJ_USERS` `T_ACCESS_TOKENS` |
| [`API-006`](API-006.md#API-006) | メール確認 | [EVT-151](../02_screen_events/EVT-151.md#EVT-151) | [UC-151](../../01_requirements/02_business_usecases/UC-151.md#UC-151) | `T_ACCESS_TOKENS` `M_CONTRACT` |
| [`API-007`](API-007.md#API-007) | 招待トークン検証・プレビュー | [EVT-181](../02_screen_events/EVT-181.md#EVT-181) | [UC-181](../../01_requirements/02_business_usecases/UC-181.md#UC-181) | `T_ACCESS_TOKENS` `M_PROJECTS` `M_PRJ_USERS` `M_CONTRACT` |
| [`API-008`](API-008.md#API-008) | メンバーアカウント有効化 | [EVT-190](../02_screen_events/EVT-190.md#EVT-190) | [UC-190](../../01_requirements/02_business_usecases/UC-190.md#UC-190) | `T_ACCESS_TOKENS` `M_USER` `M_PRJ_USERS` `T_TERMS_AGREE` `H_AUDIT_LOGS` |
| [`API-009`](API-009.md#API-009) | プロジェクト連絡先メール確認 | [EVT-194](../02_screen_events/EVT-194.md#EVT-194) | [UC-194](../../01_requirements/02_business_usecases/UC-194.md#UC-194) | `T_ACCESS_TOKENS` `M_PROJECTS` `H_AUDIT_LOGS` |
| [`API-010`](API-010.md#API-010) | パスワード再設定確定 | [EVT-025](../02_screen_events/EVT-025.md#EVT-025) | [UC-022](../../01_requirements/02_business_usecases/UC-022.md#UC-022) [UC-025](../../01_requirements/02_business_usecases/UC-025.md#UC-025) | `T_ACCESS_TOKENS` `M_CONTRACT` `M_PRJ_USERS` `T_SESSIONS` |
| [`API-011`](API-011.md#API-011) | 連絡先確認メール再送 | [EVT-040](../02_screen_events/EVT-040.md#EVT-040) | [UC-040](../../01_requirements/02_business_usecases/UC-040.md#UC-040) | `M_PROJECTS` `T_ACCESS_TOKENS` `H_NOTIF_LOGS` |
| [`API-012`](API-012.md#API-012) | 自己プロフィール更新 | [EVT-177](../02_screen_events/EVT-177.md#EVT-177) | [UC-177](../../01_requirements/02_business_usecases/UC-177.md#UC-177) | `M_CONTRACT` `M_PRJ_USERS` `T_ACCESS_TOKENS` |
| [`API-013`](API-013.md#API-013) | 自己パスワード変更 | [EVT-178](../02_screen_events/EVT-178.md#EVT-178) | [UC-178](../../01_requirements/02_business_usecases/UC-178.md#UC-178) | `T_ACCESS_TOKENS` `M_CONTRACT` `M_PRJ_USERS` |
| [`API-014`](API-014.md#API-014) | 契約設定取得 | [EVT-215](../02_screen_events/EVT-215.md#EVT-215) | [UC-215](../../01_requirements/02_business_usecases/UC-215.md#UC-215) | `M_CONTRACT` |
| [`API-015`](API-015.md#API-015) | 契約設定更新 | [EVT-217](../02_screen_events/EVT-217.md#EVT-217) | [UC-217](../../01_requirements/02_business_usecases/UC-217.md#UC-217) | `M_CONTRACT` |
| [`API-016`](API-016.md#API-016) | プロジェクト一覧 | [EVT-028](../02_screen_events/EVT-028.md#EVT-028) | [UC-028](../../01_requirements/02_business_usecases/UC-028.md#UC-028) | `M_PROJECTS` `M_FAQS` `M_ALLOWED_DOMAINS` |
| [`API-017`](API-017.md#API-017) | プロジェクト新規作成 | [EVT-038](../02_screen_events/EVT-038.md#EVT-038) | [UC-038](../../01_requirements/02_business_usecases/UC-038.md#UC-038) | `M_PROJECTS` `M_ALLOWED_DOMAINS` `M_PRJ_USERS` |
| [`API-018`](API-018.md#API-018) | プロジェクト更新・削除 | [EVT-034](../02_screen_events/EVT-034.md#EVT-034) [EVT-039](../02_screen_events/EVT-039.md#EVT-039) [EVT-042](../02_screen_events/EVT-042.md#EVT-042) [EVT-105](../02_screen_events/EVT-105.md#EVT-105) | [UC-034](../../01_requirements/02_business_usecases/UC-034.md#UC-034) [UC-039](../../01_requirements/02_business_usecases/UC-039.md#UC-039) [UC-042](../../01_requirements/02_business_usecases/UC-042.md#UC-042) [UC-096](../../01_requirements/02_business_usecases/UC-096.md#UC-096) [UC-105](../../01_requirements/02_business_usecases/UC-105.md#UC-105) | `M_PROJECTS` `M_ALLOWED_DOMAINS` `M_PRJ_USERS` `T_SESSIONS` `T_ACCESS_TOKENS` `M_FAQS` `H_QUESTION_LOGS` `T_INQUIRIES` `H_AUDIT_LOGS` |
| [`API-019`](API-019.md#API-019) | ウィジェット鍵ローテーション | [EVT-104](../02_screen_events/EVT-104.md#EVT-104) | [UC-104](../../01_requirements/02_business_usecases/UC-104.md#UC-104) | `M_PROJECTS` |
| [`API-020`](API-020.md#API-020) | メンバー一覧 | [EVT-115](../02_screen_events/EVT-115.md#EVT-115) [EVT-116](../02_screen_events/EVT-116.md#EVT-116) [EVT-117](../02_screen_events/EVT-117.md#EVT-117) [EVT-124](../02_screen_events/EVT-124.md#EVT-124) | [UC-115](../../01_requirements/02_business_usecases/UC-115.md#UC-115) [UC-116](../../01_requirements/02_business_usecases/UC-116.md#UC-116) [UC-117](../../01_requirements/02_business_usecases/UC-117.md#UC-117) [UC-121](../../01_requirements/02_business_usecases/UC-121.md#UC-121) [UC-124](../../01_requirements/02_business_usecases/UC-124.md#UC-124) [UC-236](../../01_requirements/02_business_usecases/UC-236.md#UC-236) | `M_PRJ_USERS` |
| [`API-021`](API-021.md#API-021) | メンバー招待 | [EVT-126](../02_screen_events/EVT-126.md#EVT-126) | [UC-126](../../01_requirements/02_business_usecases/UC-126.md#UC-126) | `M_USER` `M_PRJ_USERS` `T_ACCESS_TOKENS` `H_NOTIF_LOGS` |
| [`API-022`](API-022.md#API-022) | メンバー情報更新 | [EVT-128](../02_screen_events/EVT-128.md#EVT-128) | [UC-128](../../01_requirements/02_business_usecases/UC-128.md#UC-128) | `M_PRJ_USERS` |
| [`API-023`](API-023.md#API-023) | プロジェクト割当解除 | [EVT-130](../02_screen_events/EVT-130.md#EVT-130) | [UC-130](../../01_requirements/02_business_usecases/UC-130.md#UC-130) | `M_PRJ_USERS` `T_SESSIONS` `T_ACCESS_TOKENS` |
| [`API-024`](API-024.md#API-024) | 招待メール再送 | [EVT-127](../02_screen_events/EVT-127.md#EVT-127) | [UC-127](../../01_requirements/02_business_usecases/UC-127.md#UC-127) | `M_PRJ_USERS` `T_ACCESS_TOKENS` `H_NOTIF_LOGS` |
| [`API-025`](API-025.md#API-025) | FAQ 一覧 | [EVT-062](../02_screen_events/EVT-062.md#EVT-062) [EVT-063](../02_screen_events/EVT-063.md#EVT-063) [EVT-064](../02_screen_events/EVT-064.md#EVT-064) [EVT-065](../02_screen_events/EVT-065.md#EVT-065) | [UC-062](../../01_requirements/02_business_usecases/UC-062.md#UC-062) [UC-063](../../01_requirements/02_business_usecases/UC-063.md#UC-063) [UC-064](../../01_requirements/02_business_usecases/UC-064.md#UC-064) [UC-065](../../01_requirements/02_business_usecases/UC-065.md#UC-065) [UC-069](../../01_requirements/02_business_usecases/UC-069.md#UC-069) [UC-070](../../01_requirements/02_business_usecases/UC-070.md#UC-070) [UC-071](../../01_requirements/02_business_usecases/UC-071.md#UC-071) | `M_FAQS` |
| [`API-026`](API-026.md#API-026) | FAQ 作成・更新・削除 | [EVT-071](../02_screen_events/EVT-071.md#EVT-071) [EVT-081](../02_screen_events/EVT-081.md#EVT-081) [EVT-082](../02_screen_events/EVT-082.md#EVT-082) [EVT-084](../02_screen_events/EVT-084.md#EVT-084) | [UC-071](../../01_requirements/02_business_usecases/UC-071.md#UC-071) [UC-081](../../01_requirements/02_business_usecases/UC-081.md#UC-081) [UC-082](../../01_requirements/02_business_usecases/UC-082.md#UC-082) [UC-084](../../01_requirements/02_business_usecases/UC-084.md#UC-084) | `M_FAQS` |
| [`API-027`](API-027.md#API-027) | FAQ 一括状態変更 | [EVT-069](../02_screen_events/EVT-069.md#EVT-069) [EVT-070](../02_screen_events/EVT-070.md#EVT-070) | [UC-069](../../01_requirements/02_business_usecases/UC-069.md#UC-069) [UC-070](../../01_requirements/02_business_usecases/UC-070.md#UC-070) | `M_FAQS` |
| [`API-028`](API-028.md#API-028) | FAQ CSV インポート | [EVT-093](../02_screen_events/EVT-093.md#EVT-093) | [UC-093](../../01_requirements/02_business_usecases/UC-093.md#UC-093) [UC-230](../../01_requirements/02_business_usecases/UC-230.md#UC-230) | `M_FAQS` |
| [`API-029`](API-029.md#API-029) | FAQ インポートテンプレート | [EVT-091](../02_screen_events/EVT-091.md#EVT-091) | [UC-091](../../01_requirements/02_business_usecases/UC-091.md#UC-091) | — |
| [`API-030`](API-030.md#API-030) | FAQ CSV エクスポート | [EVT-074](../02_screen_events/EVT-074.md#EVT-074) | [UC-074](../../01_requirements/02_business_usecases/UC-074.md#UC-074) | `M_FAQS` |
| [`API-031`](API-031.md#API-031) | FAQ 全文検索 | — | — | `M_FAQS` `TP_FAQ_FTS` |
| [`API-032`](API-032.md#API-032) | 質問ログ検索 | — | — | `H_QUESTION_LOGS` |
| [`API-033`](API-033.md#API-033) | FAQ 個別取得 | [EVT-076](../02_screen_events/EVT-076.md#EVT-076) | [UC-076](../../01_requirements/02_business_usecases/UC-076.md#UC-076) | `M_FAQS` |
| [`API-034`](API-034.md#API-034) | 未解決質問一覧 | [EVT-046](../02_screen_events/EVT-046.md#EVT-046) [EVT-047](../02_screen_events/EVT-047.md#EVT-047) [EVT-048](../02_screen_events/EVT-048.md#EVT-048) [EVT-051](../02_screen_events/EVT-051.md#EVT-051) [EVT-052](../02_screen_events/EVT-052.md#EVT-052) | [UC-046](../../01_requirements/02_business_usecases/UC-046.md#UC-046) [UC-047](../../01_requirements/02_business_usecases/UC-047.md#UC-047) [UC-048](../../01_requirements/02_business_usecases/UC-048.md#UC-048) [UC-051](../../01_requirements/02_business_usecases/UC-051.md#UC-051) [UC-052](../../01_requirements/02_business_usecases/UC-052.md#UC-052) | `T_INQUIRIES` |
| [`API-035`](API-035.md#API-035) | 未解決質問詳細・状況切替 | [EVT-054](../02_screen_events/EVT-054.md#EVT-054) [EVT-056](../02_screen_events/EVT-056.md#EVT-056) [EVT-057](../02_screen_events/EVT-057.md#EVT-057) | [UC-054](../../01_requirements/02_business_usecases/UC-054.md#UC-054) [UC-056](../../01_requirements/02_business_usecases/UC-056.md#UC-056) [UC-057](../../01_requirements/02_business_usecases/UC-057.md#UC-057) | `T_INQUIRIES` |
| [`API-036`](API-036.md#API-036) | 未解決質問 CSV エクスポート | [EVT-049](../02_screen_events/EVT-049.md#EVT-049) | [UC-049](../../01_requirements/02_business_usecases/UC-049.md#UC-049) | `T_INQUIRIES` |
| [`API-037`](API-037.md#API-037) | ウィジェット起動 | [EVT-223](../02_screen_events/EVT-223.md#EVT-223) [EVT-229](../02_screen_events/EVT-229.md#EVT-229) | [UC-223](../../01_requirements/02_business_usecases/UC-223.md#UC-223) [UC-229](../../01_requirements/02_business_usecases/UC-229.md#UC-229) | `M_PROJECTS` `M_ALLOWED_DOMAINS` `M_CONTRACT` |
| [`API-038`](API-038.md#API-038) | ウィジェット質問送信 | [EVT-226](../02_screen_events/EVT-226.md#EVT-226) [EVT-227](../02_screen_events/EVT-227.md#EVT-227) [EVT-228](../02_screen_events/EVT-228.md#EVT-228) [EVT-229](../02_screen_events/EVT-229.md#EVT-229) | [UC-226](../../01_requirements/02_business_usecases/UC-226.md#UC-226) [UC-228](../../01_requirements/02_business_usecases/UC-228.md#UC-228) [UC-229](../../01_requirements/02_business_usecases/UC-229.md#UC-229) | `H_QUESTION_LOGS` `M_FAQS` `T_USAGE_METER` `T_INQUIRIES` |
| [`API-039`](API-039.md#API-039) | ウィジェット未解決質問登録 | [EVT-227](../02_screen_events/EVT-227.md#EVT-227) | [UC-227](../../01_requirements/02_business_usecases/UC-227.md#UC-227) | `T_INQUIRIES` `H_QUESTION_LOGS` |
| [`API-040`](API-040.md#API-040) | ダッシュボードサマリ | [EVT-107](../02_screen_events/EVT-107.md#EVT-107) [EVT-108](../02_screen_events/EVT-108.md#EVT-108) | [UC-107](../../01_requirements/02_business_usecases/UC-107.md#UC-107) [UC-108](../../01_requirements/02_business_usecases/UC-108.md#UC-108) [UC-238](../../01_requirements/02_business_usecases/UC-238.md#UC-238) [UC-239](../../01_requirements/02_business_usecases/UC-239.md#UC-239) | `T_USAGE_METER` `H_QUESTION_LOGS` `T_INQUIRIES` `H_NOTIF_LOGS` |
| [`API-041`](API-041.md#API-041) | 利用量サマリ(プロジェクト) | [EVT-170](../02_screen_events/EVT-170.md#EVT-170) [EVT-199](../02_screen_events/EVT-199.md#EVT-199) | [UC-170](../../01_requirements/02_business_usecases/UC-170.md#UC-170) [UC-199](../../01_requirements/02_business_usecases/UC-199.md#UC-199) [UC-201](../../01_requirements/02_business_usecases/UC-201.md#UC-201) [UC-239](../../01_requirements/02_business_usecases/UC-239.md#UC-239) | `T_USAGE_METER` `M_FAQS` |
| [`API-042`](API-042.md#API-042) | 利用量サマリ(契約) | [EVT-170](../02_screen_events/EVT-170.md#EVT-170) | [UC-170](../../01_requirements/02_business_usecases/UC-170.md#UC-170) | `T_USAGE_METER` `M_FAQS` |
| [`API-043`](API-043.md#API-043) | 請求サマリ | [EVT-208](../02_screen_events/EVT-208.md#EVT-208) | [UC-208](../../01_requirements/02_business_usecases/UC-208.md#UC-208) [UC-233](../../01_requirements/02_business_usecases/UC-233.md#UC-233) | `T_BILL_SUBS` `T_USAGE_METER` |
| [`API-044`](API-044.md#API-044) | 請求書一覧 | [EVT-208](../02_screen_events/EVT-208.md#EVT-208) | [UC-208](../../01_requirements/02_business_usecases/UC-208.md#UC-208) [UC-210](../../01_requirements/02_business_usecases/UC-210.md#UC-210) | `T_BILL_INVOICES` |
| [`API-045`](API-045.md#API-045) | 支払方法 取得・登録・更新 | [EVT-209](../02_screen_events/EVT-209.md#EVT-209) [EVT-213](../02_screen_events/EVT-213.md#EVT-213) | [UC-209](../../01_requirements/02_business_usecases/UC-209.md#UC-209) [UC-213](../../01_requirements/02_business_usecases/UC-213.md#UC-213) [UC-241](../../01_requirements/02_business_usecases/UC-241.md#UC-241) | `T_BILL_SUBS` |
| [`API-046`](API-046.md#API-046) | プロジェクト上限・アラート取得 | [EVT-199](../02_screen_events/EVT-199.md#EVT-199) [EVT-202](../02_screen_events/EVT-202.md#EVT-202) | [UC-199](../../01_requirements/02_business_usecases/UC-199.md#UC-199) [UC-202](../../01_requirements/02_business_usecases/UC-202.md#UC-202) [UC-237](../../01_requirements/02_business_usecases/UC-237.md#UC-237) [UC-240](../../01_requirements/02_business_usecases/UC-240.md#UC-240) | `M_PRJ_QUOTA_LIMITS` `T_USAGE_METER` |
| [`API-047`](API-047.md#API-047) | プロジェクト上限・アラート更新 | [EVT-206](../02_screen_events/EVT-206.md#EVT-206) | [UC-206](../../01_requirements/02_business_usecases/UC-206.md#UC-206) | `M_PRJ_QUOTA_LIMITS` |
| [`API-048`](API-048.md#API-048) | お知らせ一覧 | [EVT-136](../02_screen_events/EVT-136.md#EVT-136) [EVT-137](../02_screen_events/EVT-137.md#EVT-137) [EVT-138](../02_screen_events/EVT-138.md#EVT-138) [EVT-139](../02_screen_events/EVT-139.md#EVT-139) [EVT-145](../02_screen_events/EVT-145.md#EVT-145) [EVT-147](../02_screen_events/EVT-147.md#EVT-147) | [UC-136](../../01_requirements/02_business_usecases/UC-136.md#UC-136) [UC-137](../../01_requirements/02_business_usecases/UC-137.md#UC-137) [UC-138](../../01_requirements/02_business_usecases/UC-138.md#UC-138) [UC-139](../../01_requirements/02_business_usecases/UC-139.md#UC-139) [UC-142](../../01_requirements/02_business_usecases/UC-142.md#UC-142) [UC-143](../../01_requirements/02_business_usecases/UC-143.md#UC-143) [UC-144](../../01_requirements/02_business_usecases/UC-144.md#UC-144) [UC-145](../../01_requirements/02_business_usecases/UC-145.md#UC-145) [UC-147](../../01_requirements/02_business_usecases/UC-147.md#UC-147) [UC-234](../../01_requirements/02_business_usecases/UC-234.md#UC-234) [UC-235](../../01_requirements/02_business_usecases/UC-235.md#UC-235) | `T_INBOX_MSG` |
| [`API-049`](API-049.md#API-049) | お知らせ個別既読 | [EVT-141](../02_screen_events/EVT-141.md#EVT-141) [EVT-147](../02_screen_events/EVT-147.md#EVT-147) | [UC-141](../../01_requirements/02_business_usecases/UC-141.md#UC-141) [UC-147](../../01_requirements/02_business_usecases/UC-147.md#UC-147) | `T_INBOX_MSG` |
| [`API-050`](API-050.md#API-050) | お知らせ一括既読 | [EVT-142](../02_screen_events/EVT-142.md#EVT-142) [EVT-143](../02_screen_events/EVT-143.md#EVT-143) [EVT-144](../02_screen_events/EVT-144.md#EVT-144) | [UC-142](../../01_requirements/02_business_usecases/UC-142.md#UC-142) [UC-143](../../01_requirements/02_business_usecases/UC-143.md#UC-143) [UC-144](../../01_requirements/02_business_usecases/UC-144.md#UC-144) | `T_INBOX_MSG` `H_AUDIT_LOGS` |
| [`API-051`](API-051.md#API-051) | お知らせ未読件数 | [EVT-136](../02_screen_events/EVT-136.md#EVT-136) | [UC-136](../../01_requirements/02_business_usecases/UC-136.md#UC-136) | `T_INBOX_MSG` |
| [`API-052`](API-052.md#API-052) | 利用規約 最新版取得 | [EVT-133](../02_screen_events/EVT-133.md#EVT-133) [EVT-164](../02_screen_events/EVT-164.md#EVT-164) | [UC-133](../../01_requirements/02_business_usecases/UC-133.md#UC-133) [UC-164](../../01_requirements/02_business_usecases/UC-164.md#UC-164) | — |
| [`API-053`](API-053.md#API-053) | プライバシーポリシー 最新版取得 | [EVT-164](../02_screen_events/EVT-164.md#EVT-164) [EVT-196](../02_screen_events/EVT-196.md#EVT-196) | [UC-164](../../01_requirements/02_business_usecases/UC-164.md#UC-164) [UC-196](../../01_requirements/02_business_usecases/UC-196.md#UC-196) | — |
| [`API-054`](API-054.md#API-054) | 利用規約 同意 | [EVT-135](../02_screen_events/EVT-135.md#EVT-135) [EVT-169](../02_screen_events/EVT-169.md#EVT-169) | [UC-135](../../01_requirements/02_business_usecases/UC-135.md#UC-135) [UC-169](../../01_requirements/02_business_usecases/UC-169.md#UC-169) | — |
| [`API-055`](API-055.md#API-055) | プライバシーポリシー 同意 | [EVT-169](../02_screen_events/EVT-169.md#EVT-169) | [UC-169](../../01_requirements/02_business_usecases/UC-169.md#UC-169) | — |
| [`API-056`](API-056.md#API-056) | 退会申請 | [EVT-159](../02_screen_events/EVT-159.md#EVT-159) | [UC-159](../../01_requirements/02_business_usecases/UC-159.md#UC-159) | `T_WITHDRAW_REQ` `M_CONTRACT` |
| [`API-057`](API-057.md#API-057) | AI 推論 IF(`AnswerProvider`) | — | [UC-245](../../01_requirements/02_business_usecases/UC-245.md#UC-245) | — |
| [`API-058`](API-058.md#API-058) | メール配信 IF(`EmailProvider`) | — | [UC-233](../../01_requirements/02_business_usecases/UC-233.md#UC-233) [UC-234](../../01_requirements/02_business_usecases/UC-234.md#UC-234) [UC-235](../../01_requirements/02_business_usecases/UC-235.md#UC-235) [UC-236](../../01_requirements/02_business_usecases/UC-236.md#UC-236) [UC-237](../../01_requirements/02_business_usecases/UC-237.md#UC-237) [UC-238](../../01_requirements/02_business_usecases/UC-238.md#UC-238) | — |
| [`API-059`](API-059.md#API-059) | 外部 Webhook(Resend) | — | [UC-231](../../01_requirements/02_business_usecases/UC-231.md#UC-231) | `H_NOTIF_LOGS` `M_EMAIL_SUPPRESS` `H_AUDIT_LOGS` |

## <span id="reading"></span>3. 読み順

1. 本ページ §0 で共通仕様(認証ヘッダ・エラー体系・境界判定)を把握する。
2. §1 の機能グループ一覧で対象 API を特定し、API ID から個別ページへ移動する。
3. 個別ページの「項目」表で対応画面・対応UC・対応EVT をたどり、画面設計 / ユースケース設計と縦串で確認する。
4. §2 の対応表で API ↔ EVT / UC / TBL の結線を俯瞰する。

---

<!-- portal-bottom -->
[基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
