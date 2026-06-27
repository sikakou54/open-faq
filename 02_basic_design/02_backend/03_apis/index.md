# API 設計書

> **このページは、メインシステムが提供する全 68 エンドポイント(`API-001`〜`API-068`)を、機能グループ別に一覧する索引です。** 各行は `API ID` / `API名` / `METHOD` / `エンドポイント` を示し、詳細は各 API 個別ページ(項目 / 処理概要 / リクエスト(認証ヘッダ含む) / レスポンス / バリデーション / エラー / 利用テーブル)を参照します。共通の入出力・エラー規約は次の「§0 共通仕様」を正本とします。

## <span id="common"></span>0. 共通仕様(全 API 共通)

各 API の「リクエスト / レスポンス / エラー」で `(共通仕様)` と記す箇所は本節を正本とする。各 API のエラー表には**当該 API 固有の異常系のみ**を記載し、下記の共通エラー(401 / 403 / 429)は全 API に暗黙で適用される。

### <span id="common-auth"></span>0.1 認証・認可エラー(共通)

認証必須 API はセッション(Cookie)を要し、状態変更系(POST / PATCH / DELETE)は CSRF トークンを要する(各 API の「認証ヘッダ」節を参照)。

| 条件 | HTTP | エラーコード |
|---|---|---|
| 未認証 / セッション失効 | 401 | `SESSION_EXPIRED` → [ERR-033](../../05_errors/ERR-033.md#ERR-033) |
| 再認証が必要(重要操作) | 401 | `REAUTH_REQUIRED` → [ERR-013](../../05_errors/ERR-013.md#ERR-013) |
| 認可なし(オーナー専有) | 403 | `OWNER_ONLY` → [ERR-015](../../05_errors/ERR-015.md#ERR-015) |
| 認可なし(権限不足) | 403 | `PERMISSION_DENIED` → [ERR-030](../../05_errors/ERR-030.md#ERR-030) |

### <span id="common-paging"></span>0.2 ページング(カーソル方式・共通)

一覧取得 API のリクエスト `cursor` / `limit` と レスポンス `nextCursor` は本仕様に従う。

| 項目 | 規定 |
|---|---|
| 方式 | カーソルベース(オフセット不可)。`cursor` はサーバが Base64URL でエンコードした不透明トークン(最終キー + 並び順)。復号不能・改ざん時は 400 `VALIDATION_ERROR` → [ERR-001](../../05_errors/ERR-001.md#ERR-001)。 |
| `limit` | 既定 20 件 / 最大 100 件。範囲外は 400 `VALIDATION_ERROR`。 |
| 並び順 | 各 API が既定の並び順(原則 `created_at` 降順)を明示する。`sort` を持つ API は列挙値で指定する。 |
| `nextCursor` | 次ページがあれば返し、末尾は `null`。 |

### <span id="common-idem"></span>0.3 冪等性(状態変更系・共通)

| 項目 | 規定 |
|---|---|
| ヘッダ | `Idempotency-Key: <ULID>`(POST / PATCH / DELETE で任意)。 |
| 挙動 | 同一キーの再送は初回結果(同一ステータス・ボディ)を再現する。保持期間は 24 時間。キー一致でボディ不一致の場合は 409 `IDEMPOTENT_REPLAY` → [ERR-032](../../05_errors/ERR-032.md#ERR-032)。 |

### <span id="common-rate"></span>0.4 レート制限(共通)

オーナー単位(`owner_user_id`)のレート制限(`SYS-008`)を超過した場合は 429 `RATE_LIMITED` → [ERR-009](../../05_errors/ERR-009.md#ERR-009) を返し、`Retry-After` ヘッダで再試行可能時刻を示す。

## <span id="g-1"></span>認証・セッション

サインアップ(独立) / ログイン / 再認証 / メール確認 / 招待(登録済みユーザー限定) / プロフィール / アカウント設定。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-001"></span>[`API-001`](API-001.md#API-001) | 新規登録 | POST | `/auth/signup` |
| <span id="API-002"></span>[`API-002`](API-002.md#API-002) | ログイン | POST | `/auth/login` |
| <span id="API-003"></span>[`API-003`](API-003.md#API-003) | ログアウト | POST | `/auth/logout` |
| <span id="API-004"></span>[`API-004`](API-004.md#API-004) | パスワード再設定要求 | POST | `/auth/password-reset-request` |
| <span id="API-005"></span>[`API-005`](API-005.md#API-005) | 再認証 | POST | `/auth/re-auth` |
| <span id="API-006"></span>[`API-006`](API-006.md#API-006) | メール確認 | POST | `/auth/email-verifications/{token}` |
| <span id="API-007"></span>[`API-007`](API-007.md#API-007) | 招待トークン検証・プレビュー | POST | `/auth/invitations/{token}/preview` |
| <span id="API-008"></span>[`API-008`](API-008.md#API-008) | 招待受諾(割当有効化) | POST | `/projects/invitations/{token}/accept` |
| <span id="API-009"></span>[`API-009`](API-009.md#API-009) | プロジェクト連絡先メール確認 | POST | `/auth/contact-verifications/{token}` |
| <span id="API-010"></span>[`API-010`](API-010.md#API-010) | パスワード再設定確定 | POST | `/auth/password-reset` |
| <span id="API-011"></span>[`API-011`](API-011.md#API-011) | 連絡先確認メール再送 | POST | `/auth/contact-verifications/resend` |
| <span id="API-012"></span>[`API-012`](API-012.md#API-012) | 自己プロフィール更新 | PATCH | `/me/profile` |
| <span id="API-013"></span>[`API-013`](API-013.md#API-013) | 自己パスワード変更 | PATCH | `/me/password` |
| <span id="API-064"></span>[`API-064`](API-064.md#API-064) | 自己プロフィール取得 | GET | `/me/profile` |
| <span id="API-014"></span>[`API-014`](API-014.md#API-014) | オーナー設定取得 | GET | `/owner/settings` |
| <span id="API-015"></span>[`API-015`](API-015.md#API-015) | セキュリティ設定更新 | PATCH | `/me/settings` |

## <span id="g-2"></span>プロジェクト

プロジェクト CRUD とウィジェット鍵ローテーション。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-016"></span>[`API-016`](API-016.md#API-016) | プロジェクト一覧 | GET | `/projects` |
| <span id="API-017"></span>[`API-017`](API-017.md#API-017) | プロジェクト新規作成 | POST | `/projects` |
| <span id="API-018"></span>[`API-018`](API-018.md#API-018) | プロジェクト更新・削除 | PATCH / DELETE | `/projects/{id}` |
| <span id="API-065"></span>[`API-065`](API-065.md#API-065) | プロジェクト範囲データ概要取得 | GET | `/projects/{id}/overview` |
| <span id="API-066"></span>[`API-066`](API-066.md#API-066) | プロジェクト削除影響プレビュー取得 | GET | `/projects/{id}/deletion-impact` |
| <span id="API-019"></span>[`API-019`](API-019.md#API-019) | ウィジェット鍵ローテーション | POST | `/projects/{id}/widget-key/rotate` |

## <span id="g-3"></span>メンバー

プロジェクト単位のメンバー招待 / 情報更新 / 離脱 / 再送。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-020"></span>[`API-020`](API-020.md#API-020) | メンバー一覧 | GET | `/projects/{id}/members` |
| <span id="API-021"></span>[`API-021`](API-021.md#API-021) | メンバー招待 | POST | `/projects/{id}/members` |
| <span id="API-022"></span>[`API-022`](API-022.md#API-022) | メンバー情報更新 | PATCH | `/projects/{id}/members/{userId}` |
| <span id="API-023"></span>[`API-023`](API-023.md#API-023) | プロジェクト割当解除 | DELETE | `/projects/{id}/members/{userId}` |
| <span id="API-024"></span>[`API-024`](API-024.md#API-024) | 招待メール再送 | POST | `/members/{id}/resend-invitation` |

## <span id="g-4"></span>FAQ

FAQ の CRUD・一括状態変更・CSV 入出力・全文検索・質問ログ検索。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-025"></span>[`API-025`](API-025.md#API-025) | FAQ 一覧 | GET | `/faqs` |
| <span id="API-026"></span>[`API-026`](API-026.md#API-026) | FAQ 作成・更新・削除 | POST / PATCH / DELETE | `/faqs`・`/faqs/{id}` |
| <span id="API-027"></span>[`API-027`](API-027.md#API-027) | FAQ 一括状態変更 | POST | `/faqs/bulk-status` |
| <span id="API-028"></span>[`API-028`](API-028.md#API-028) | FAQ CSV インポート | POST | `/faqs/import` |
| <span id="API-068"></span>[`API-068`](API-068.md#API-068) | FAQ取込ジョブ状態取得 | GET | `/faqs/import/{jobId}` |
| <span id="API-029"></span>[`API-029`](API-029.md#API-029) | FAQ インポートテンプレート | GET | `/faqs/import/template` |
| <span id="API-030"></span>[`API-030`](API-030.md#API-030) | FAQ CSV エクスポート | GET | `/faqs/export` |
| <span id="API-031"></span>[`API-031`](API-031.md#API-031) | FAQ 全文検索 | GET | `/projects/{id}/faqs/search` |
| <span id="API-032"></span>[`API-032`](API-032.md#API-032) | 質問ログ検索 | GET | `/projects/{id}/question-logs/search` |
| <span id="API-033"></span>[`API-033`](API-033.md#API-033) | FAQ 個別取得 | GET | `/faqs/{id}` |

## <span id="g-5"></span>未解決質問

未解決質問の一覧・詳細・状況切替・CSV エクスポート。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-034"></span>[`API-034`](API-034.md#API-034) | 未解決質問一覧 | GET | `/inquiries` |
| <span id="API-035"></span>[`API-035`](API-035.md#API-035) | 未解決質問詳細・状況切替 | GET / PATCH | `/inquiries/{id}` |
| <span id="API-036"></span>[`API-036`](API-036.md#API-036) | 未解決質問 CSV エクスポート | GET | `/inquiries/export` |

## <span id="g-6"></span>ウィジェット配信

エンドユーザー向けウィジェットの bootstrap / ask / 問い合わせ。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-037"></span>[`API-037`](API-037.md#API-037) | ウィジェット起動 | POST | `/widget/v1/bootstrap` |
| <span id="API-038"></span>[`API-038`](API-038.md#API-038) | ウィジェット質問送信 | POST | `/widget/v1/ask` |
| <span id="API-039"></span>[`API-039`](API-039.md#API-039) | ウィジェット未解決質問登録 | POST | `/widget/v1/inquiries` |
| <span id="API-067"></span>[`API-067`](API-067.md#API-067) | AIしきい値設定取得・更新 | GET / PUT | `/projects/{id}/ai-thresholds` |

## <span id="g-7"></span>ダッシュボード

概要画面向けの集計サマリー。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-040"></span>[`API-040`](API-040.md#API-040) | ダッシュボードサマリ | GET | `/dashboard/summary` |
| <span id="API-062"></span>[`API-062`](API-062.md#API-062) | ダッシュボード集計取得 | GET | `/dashboard/overview` |
| <span id="API-063"></span>[`API-063`](API-063.md#API-063) | セットアップ進捗取得 | GET | `/onboarding/progress` |

## <span id="g-8"></span>利用量・課金

利用量・請求サマリー・請求書・支払方法・上限設定。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-041"></span>[`API-041`](API-041.md#API-041) | 利用量サマリ(プロジェクト) | GET | `/usage` |
| <span id="API-042"></span>[`API-042`](API-042.md#API-042) | 利用量サマリ(オーナー全プロジェクト) | GET | `/owner/projects/usage` |
| <span id="API-043"></span>[`API-043`](API-043.md#API-043) | 請求サマリ | GET | `/billing/summary` |
| <span id="API-044"></span>[`API-044`](API-044.md#API-044) | 請求書一覧 | GET | `/billing/invoices` |
| <span id="API-045"></span>[`API-045`](API-045.md#API-045) | 支払方法 取得・登録・更新 | GET / PUT | `/billing/payment-method` |
| <span id="API-046"></span>[`API-046`](API-046.md#API-046) | プロジェクト上限・アラート取得 | GET | `/projects/{id}/quota-limits` |
| <span id="API-047"></span>[`API-047`](API-047.md#API-047) | プロジェクト上限・アラート更新 | PATCH | `/projects/{id}/quota-limits/questions` |

## <span id="g-9"></span>お知らせ受信箱

受信箱の取得・既読化・未読件数・通知配信状態。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-048"></span>[`API-048`](API-048.md#API-048) | お知らせ一覧 | GET | `/me/announcements` |
| <span id="API-049"></span>[`API-049`](API-049.md#API-049) | お知らせ個別既読 | POST | `/me/announcements/{id}/read` |
| <span id="API-050"></span>[`API-050`](API-050.md#API-050) | お知らせ一括既読 | POST | `/me/announcements/read` |
| <span id="API-051"></span>[`API-051`](API-051.md#API-051) | お知らせ未読件数 | GET | `/me/announcements/unread-summary` |
| <span id="API-061"></span>[`API-061`](API-061.md#API-061) | 通知配信状態サマリ | GET | `/notifications/delivery-status` |

## <span id="g-10"></span>規約・退会

規約 / プライバシー取得・同意・退会(アカウント単位・即時)。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-052"></span>[`API-052`](API-052.md#API-052) | 利用規約 最新版取得 | GET | `/terms/current` |
| <span id="API-053"></span>[`API-053`](API-053.md#API-053) | プライバシーポリシー 最新版取得 | GET | `/privacy/current` |
| <span id="API-054"></span>[`API-054`](API-054.md#API-054) | 利用規約 同意 | POST | `/terms/agree` |
| <span id="API-055"></span>[`API-055`](API-055.md#API-055) | プライバシーポリシー 同意 | POST | `/privacy/agree` |
| <span id="API-056"></span>[`API-056`](API-056.md#API-056) | 退会(アカウント単位・即時) | POST | `/withdrawals` |

## <span id="g-11"></span>AI 推論 IF

AI 推論連携インターフェース(外部 LLM)。HTTP エンドポイントを持たない内部抽象 IF。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-057"></span>[`API-057`](API-057.md#API-057) | AI 推論 IF(`AnswerProvider`) | — | — |

## <span id="g-12"></span>メール配信 IF

トランザクションメール送信インターフェース。HTTP エンドポイントを持たない内部抽象 IF。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-058"></span>[`API-058`](API-058.md#API-058) | メール配信 IF(`EmailProvider`) | — | — |

## <span id="g-13"></span>外部 Webhook

メール配信プロバイダ(Resend)・課金プロバイダ(Stripe)からの Webhook 受信。

| API ID | API名 | METHOD | エンドポイント |
|---|---|---|---|
| <span id="API-059"></span>[`API-059`](API-059.md#API-059) | 外部 Webhook(Resend) | POST | `/webhooks/resend` |
| <span id="API-060"></span>[`API-060`](API-060.md#API-060) | 課金プロバイダ Webhook 受信 | POST | `/webhooks/billing` |
