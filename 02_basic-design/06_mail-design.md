<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ **メール設計書**
<!-- /portal-top -->

# メール設計書

> **このページは、メインシステム(利用者向け FAQ ウィジェット SaaS)が送信する全メールの件名・本文・テンプレート変数・送信契機を集中定義する正本です。**

*版数 v1.3 ・ 更新 2026-06-20 ・ 承認済*

> [!NOTE]
> **本書の範囲と対象外** 本書は §4 のテンプレート ID `TPL-*` 全件の件名 / テキスト本文 / HTML 本文・送信契機(`NOTIF-*`)・配信先 / 重要度 / 添付 / リンク有効期限・メール共通要件(送信元・i18n・サニタイズ・配信信頼性)を扱います。アプリ内お知らせ受信箱(`inbox` 限定の `NOTIF-CHAT_HOLD_CHECK` 等)は 本書、画面文言(`MSG-SCR-*`)は [画面設計.md](01_screen-design.md) が正本です。配信信頼性(DMARC 等)は 要件のセキュリティ NFR、通知契機・配信先は 本書 が正本です。

## <span id="2-共通基準"></span>2. 共通基準

全テンプレートに共通する送信元・件名・本文構造・文字コード・サニタイズ・配信失敗時挙動・添付の基準をまとめます。各小節は個別テンプレート(§4)が前提とする土台を定めるもので、テンプレート固有の差分のみを §4 側に記載します。

### <span id="21-送信元--reply-to--差出人表記"></span>2.1 送信元 / Reply-To / 差出人表記

差出人・返信先・認証情報の固定値を定めます。次の表は Envelope From(VERP)/ Header From / Reply-To / List-Unsubscribe / DMARC 等を並べたもので、なりすまし対策と到達性確保の基礎になります。

| 項目 | 値 |
|----|----|
| Envelope From | `bounces+<deliveryId>@<service-domain>` (VERP) |
| Header From | `open-faq <noreply@<service-domain>>` 固定 |
| Reply-To | 設定しない(NULL) |
| List-Unsubscribe | マーケティング系 `low` 通知にのみ設定 |
| DMARC / DKIM / SPF | 全テンプレートで pass を必須(NFR-905、09 セキュリティ §11.3) |

「このメールに直接返信せず、お問い合わせ画面または各プロジェクトのお問い合わせ先からご返信ください」のフッタ文言を必ず本文末尾に付与する。

### <span id="22-件名規則"></span>2.2 件名規則

件名の長さ・プレフィックス・プレースホルダの扱いを統一します。次の各項目は、モバイル一覧での折り返し回避と `critical` 規約改定通知の `【重要】` 付与ルールを定めます。

- 件名長: 半角換算 70 文字以内(モバイル一覧で折り返しが発生しない目安)
- プレースホルダ `{...}` は本書 §4 各テンプレートの変数表で定義
- `critical` 重要度の利用規約改定通知のみ `【重要】` プレフィックスを付与
- `【open-faq】` のサービス名プレフィックスは付けない(`Header From` で識別可能なため)

### <span id="23-本文構造"></span>2.3 本文構造

本文を構成する固定ブロックの順序を定めます。全テンプレートは宛名から共通フッタまでの 6 ブロックを共通の骨格とし、読者がどのメールでも同じ位置で同じ情報を読めるようにします。

全テンプレートは以下の 6 ブロックで構成される:

1.  宛名(`{recipient_display_name} 様` / 不明時は `お客様`)
2.  一段落の状況説明(何が起きたか)
3.  行動を促す主要 CTA(リンクまたはボタン)
4.  副次情報(失効日時・対象ID等のメタデータ表)
5.  不審な操作の場合の連絡先案内(`critical` テンプレートのみ)
6.  共通フッタ(返信不可注意 / サービス名 / 配信元署名)

### <span id="24-文字コード--言語--時刻"></span>2.4 文字コード / 言語 / 時刻

文字コード・配信形式・対応言語・時刻表記の前提を定めます。次の各項目は UTF-8 / multipart 配信 / i18n キー化 / JST 固定表記を共通仕様として固定します。

- 文字コード: UTF-8
- HTML 版とテキスト版を両方生成し、`multipart/alternative` で送信
- 全文 i18n キー化必須。MVP 対応言語: 日本語(`ja`)
- 本文内の時刻表記は **JST 固定** で `YYYY-MM-DD HH:mm`(秒は含めない)。タイムゾーンを `(JST)` と明示

### <span id="25-サニタイズ"></span>2.5 サニタイズ

ウィジェット利用者の入力をメールに流用する際の安全策を定めます。次の各項目は、件名・送信元への流用禁止と本文埋め込み時のエスケープ・字数制限を定め、スパム埋め込みやなりすましを防ぎます(FR-087)。

- **ウィジェット利用者の入力文字列(質問本文等)を、メール件名・送信元(Header From / Envelope From)・Reply-To へそのまま使用しない**(FR-087。スパム埋め込み・なりすまし対策)。送信元は §2.1 のとおり `no-reply` 固定とする。
- ウィジェット利用者入力を本文に埋め込む場合に限り、HTML エスケープ + 200 字制限 + 末尾省略記号 `…` を付与する。
- 引用ブロックは罫線で視覚的に分離し、サービスからの文言と区別する。

### <span id="26-配信失敗時の挙動"></span>2.6 配信失敗時の挙動

送信失敗・バウンス・苦情時の再送方式の正本所在と、本書で定めるテンプレート単位の例外を示します。配信信頼性の方式そのものは 要件のセキュリティ NFR を正本とし、本書は `critical` 認証メールの再送続行など差分のみを定めます。

再送回数上限(24 時間内に最大 3 回)・バウンス / 苦情検知・全契約横断の送信停止リストといった**配信信頼性の方式は 要件のセキュリティ NFR を正本**とする(FR-083 / FR-084 / FR-089 / FR-091b)。本書はテンプレート単位の挙動差のみを以下に定める。

- 恒久失敗(hard bounce)で送信停止リストに載った宛先でも、`critical` 重要度の `TPL-LOCKOUT_NOTIFY` のみ再送試行を続行する(認証関連の到達性最優先)。

### <span id="27-添付ファイル"></span>2.7 添付ファイル

添付ファイルを付けるテンプレートと形式・サイズ上限を定めます。次の表のとおり添付は請求明細 PDF のみに限定し、その他のテンプレートには添付を付けません。

| テンプレート | 添付ファイル | 形式 |
|----|----|----|
| `TPL-BILLING_INVOICE_ISSUED` | 請求明細 PDF | `invoice_{year}{month}.pdf`、≤ 1 MB |

その他のテンプレートには添付ファイルを付けない。

## <span id="3-テンプレート一覧"></span>3. テンプレート一覧

メール送信を含む全 13 テンプレートを索引します。次の表はテンプレート ID・通知 ID・重要度・配信先・強制送信可否・リンク有効期限を一覧化したもので、件名 + 本文の全文は §4 を参照します。メンバー招待は §4.3 の共通メンバー招待(`TPL-ADMIN_USER_REGISTER`)に一本化する。

| \# | テンプレートID | 通知ID | 重要度 | 配信先 | 強制送信 | リンク有効期限 |
|----|----|----|----|----|----|----|
| 1 | TPL-EMAIL_VERIFY | NOTIF-EMAIL_VERIFY | critical | 本人 | ◯ | 24h |
| 2 | TPL-PASSWORD_RESET | NOTIF-PASSWORD_RESET | critical | 本人 | ◯ | 1h |
| 3 | TPL-ADMIN_USER_REGISTER | NOTIF-ADMIN_USER_REGISTER | critical | 招待対象 | ◯ | 7d |
| 4 | TPL-PROJECT_CONTACT_VERIFY | (オーナー操作派生) | critical | プロジェクト連絡先 | ◯ | 24h |
| 5 | TPL-LOCKOUT_NOTIFY | NOTIF-LOCKOUT_NOTIFY | critical | ロック本人 + オーナー + 全メンバー | ◯ | (リンクなし) |
| 6 | TPL-DELETION_REMINDER | NOTIF-DELETION_REMINDER | high | オーナー | ◯ | 退会発効日まで |
| 7 | TPL-BILLING_INVOICE_ISSUED | NOTIF-BILLING_INVOICE_ISSUED | high | オーナー | ◯ | 30d(PDF 再 DL) |
| 8 | TPL-BILLING_PAYMENT_FAILED | NOTIF-BILLING_PAYMENT_FAILED | high | オーナー | ◯ | (再決済リンク) |
| 9 | TPL-BILLING_SUSPENSION | NOTIF-BILLING_SUSPENSION | critical | オーナー + 全メンバー | ◯ | (リンクなし) |
| 10 | TPL-PAYMENT_METHOD_REQUIRED | NOTIF-PAYMENT_METHOD_REQUIRED | critical | オーナー | ◯ | (課金設定リンク) |
| 11 | TPL-TERMS_REVISION | NOTIF-TERMS_REVISION | critical | オーナー + 全メンバー | ◯ | 発効日 + 14d |
| 12 | TPL-SERVICE_ANNOUNCEMENT | NOTIF-SERVICE_ANNOUNCEMENT | normal/high/critical | 範囲指定可 | 配信時に選択 | 入力 URL |
| 13 | TPL-SYSTEM_NOTICE | NOTIF-SYSTEM_NOTICE | normal/high | 対象者 | 契機による | (画面内リンク) |

`NOTIF-CHAT_HOLD_CHECK` はチャネルが `inbox` 限定(メール送信なし)のため本書の対象外。`NOTIF-SYSTEM_NOTICE` は inbox/email 兼用で、サブ契機ごとに動的に件名・本文を組み立てるメタテンプレートとして定義する。

## <span id="4-テンプレート詳細"></span>4. テンプレート詳細

各テンプレートの発火条件・テンプレート変数・件名・本文(テキスト / HTML 版)・備考を 1 件ずつ定義します。本文の件名・テキストは送信される文言そのものの正本です。各テンプレートは以下のセクション構造で記載します。

各テンプレートは以下のセクション構造で記載する:

- **発火条件**: どの操作・イベントで送信されるか
- **テンプレート変数**: 本文中の `{...}` 変数
- **件名**: 件名(JA)
- **本文(テキスト版)**: プレーンテキスト本文
- **本文(HTML 版)**: HTML 版の構造(本文要素を箇条書きで定義)
- **備考**: 注意事項

### <span id="41-tpl-email_verifyアカウント登録-メール確認"></span>4.1 TPL-EMAIL_VERIFY(アカウント登録: メール確認)

新規登録直後の本人到達を確認する `critical` メールです。確認 URL(24h 有効)とリクエスト元 IP を提示し、本人以外の登録試行を見分けられるようにします。

**発火条件**: SCR-002 新規登録の「アカウント作成」ボタン押下直後、`T_ACCESS_TOKENS.purpose='email_verify'` 発行時。

**テンプレート変数**:

| 変数 | 説明 | 例 |
|----|----|----|
| `{recipient_display_name}` | 受信者の表示名(未設定時は空文字) | 佐藤 太郎 |
| `{verify_url}` | 確認 URL(24h 有効) | https://app.example.com/auth/verify?token=... |
| `{expire_at_jst}` | 失効日時(JST、`YYYY-MM-DD HH:mm`) | 2026-05-20 14:30 |
| `{requester_ip}` | リクエスト元 IP(国情報を補助表記) | 203.0.113.42(JP) |

**件名**: `メール確認をお願いします`

**本文(テキスト版)**:

```json
{recipient_display_name} 様

open-faq へのご登録ありがとうございます。
以下のリンクからメールアドレスの確認を完了してください。

▶ メールを確認する
{verify_url}

このリンクは {expire_at_jst}(JST) まで有効です。

リクエスト元:
  - IP: {requester_ip}

ご自身でこの操作を行っていない場合は、本メールを破棄してください。第三者が
あなたのメールアドレスで登録を試みた可能性がありますが、リンクをクリックし
ない限り、アカウントは作成されません。

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: テキスト版と同等の段落構造 + 「メールを確認する」プライマリボタン(リンク `{verify_url}`)。失効日時とリクエスト元 IP は背景色 `#f5f5f5` のメタデータ表で表示。

**備考**: 失敗(リンク有効期限切れ等)時はログインページで `E-AUTH-EMAIL_VERIFY-EXPIRED` を表示し、再送導線を提供。

------------------------------------------------------------------------

### <span id="42-tpl-password_resetパスワード再設定"></span>4.2 TPL-PASSWORD_RESET(パスワード再設定)

パスワード再設定リクエストを受け付けた本人へ送る `critical` メールです。再設定 URL(1h 有効)とリクエスト元 IP / 端末を提示し、心当たりのない要求への注意喚起を含めます。

**発火条件**: SCR-003 パスワード再設定の「再設定リンクを送信する」ボタン押下時、`T_ACCESS_TOKENS.purpose='password_reset'` 発行時。

**テンプレート変数**:

| 変数                       | 説明                                  |
|----------------------------|---------------------------------------|
| `{recipient_display_name}` | 受信者の表示名                        |
| `{reset_url}`              | 再設定 URL(1h 有効)                   |
| `{expire_at_jst}`          | 失効日時(JST)                         |
| `{requester_ip}`           | リクエスト元 IP                       |
| `{requester_ua_summary}`   | User-Agent 要約(ブラウザ名 + OS のみ) |

**件名**: `パスワード再設定のご案内`

**本文(テキスト版)**:

```json
{recipient_display_name} 様

open-faq のパスワード再設定リクエストを受け付けました。
以下のリンクから新しいパスワードを設定してください。

▶ パスワードを再設定する
{reset_url}

このリンクは {expire_at_jst}(JST) まで有効です(発行から 1 時間)。

リクエスト元:
  - IP: {requester_ip}
  - 端末: {requester_ua_summary}

ご自身で操作を行っていない場合は、本メールを破棄しアカウントの不正利用を
ご確認ください。心当たりのないリクエストが続く場合はサポートまでご連絡く
ださい。

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: プライマリボタン「パスワードを再設定する」+ リクエスト元のメタデータ表 + 警告ボックス(背景色 `#fff3cd`)で「心当たりのないリクエストの場合」案内。

**備考**: 連続失敗ロックアウト(FR-007)発動時は本テンプレートは送信せず `TPL-LOCKOUT_NOTIFY` に切り替わる。

------------------------------------------------------------------------

### <span id="43-tpl-admin_user_registerメンバー招待再送-共通"></span>4.3 TPL-ADMIN_USER_REGISTER(メンバー招待・再送 共通)

メンバー招待および招待再送で共通利用する `critical` メールです。プロジェクトへのメンバー招待はすべて本テンプレートに一本化する。アクティベーション URL(7d 有効)と招待内容(プロジェクト・招待元)を提示し、着地ページで氏名・初回パスワード・規約同意を入力させます。

**発火条件**: SCR-009-001 メンバー招待モーダルの「招待メールを送信する」/「招待メールを再送する」ボタン押下時、`T_ACCESS_TOKENS.purpose='activation'` 発行時。

**テンプレート変数**:

| 変数 | 説明 |
|----|----|
| `{recipient_email}` | 招待対象のメールアドレス(招待時点で `M_PRJ_USERS.name=NULL` のため宛先表示は email を用いる。FR-013e) |
| `{inviter_owner_name}` | 招待元オーナーの表示名 |
| `{inviter_admin_name}` | 招待操作者の表示名(オーナー以外のメンバーの場合) |
| `{project_name}` | 招待対象プロジェクト名 |
| `{activation_url}` | アクティベーション URL(7d 有効、SCR-018 メンバーアカウント有効化ページに着地) |
| `{expire_at_jst}` | 失効日時(JST) |

**件名**: `open-faq のメンバー登録を完了してください`

**本文(テキスト版)**:

```json
{recipient_email} 様

{inviter_owner_name} 様の open-faq アカウントから、{project_name} のメン
バーとして招待を受けました。以下のリンクからお名前(表示名)と初回パスワー
ドを設定し、利用規約・プライバシーポリシーに同意のうえ、アカウント登録を
完了してください。

▶ アカウント登録を完了する
{activation_url}

このリンクは {expire_at_jst}(JST) まで有効です(発行から 7 日)。
失効後に登録する場合は、招待元のメンバーへ再送をご依頼ください。

招待内容:
  - プロジェクト: {project_name}
  - 招待元オーナー: {inviter_owner_name}
  - 招待操作者: {inviter_admin_name}

心当たりがない場合は本メールを破棄してください。リンクをクリックしない限
りアカウントは有効化されません。

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: 招待内容を背景色 `#eef6ff` のパネルで表示 + プライマリボタン「アカウント登録を完了する」+ 失効日時を強調表示。本文の必須項目に「氏名(表示名)入力 + 初回パスワード設定 + 利用規約・プライバシーポリシー同意」を含める。

**着地ページ**: SCR-018 メンバーアカウント有効化([画面設計書](01_screen-design.md))。

**備考**: 再送時は **旧 `T_ACCESS_TOKENS` を失効させ新トークンを発行** したうえで本テンプレートで再送信(`MSG-SCR-009-001-TOAST-002` と整合)。本文は新規招待時と同一で、差出人による文脈は本文中の「招待操作者」フィールドで補足する。氏名は招待時点で未登録のため、宛先表示は `{recipient_email}` を用いる。

------------------------------------------------------------------------

### <span id="45-tpl-project_contact_verifyプロジェクト連絡先メール確認"></span>4.5 TPL-PROJECT_CONTACT_VERIFY(プロジェクト連絡先メール確認)

プロジェクトのお問い合わせ先メールアドレスをウィジェット表示前に確認する `critical` メールです。確認 URL(24h 有効)を提示し、受信者はアカウントを持たない第三者でも構いません。

**発火条件**: SCR-004-001 プロジェクト作成・編集モーダルで連絡先メールアドレスが新規入力 / 変更された時、ウィジェット上での表示前確認用に送信。

**テンプレート変数**:

| 変数              | 説明                         |
|-------------------|------------------------------|
| `{project_name}`  | プロジェクト名               |
| `{verify_url}`    | 確認 URL(24h 有効)           |
| `{expire_at_jst}` | 失効日時(JST)                |
| `{owner_name}`    | 設定操作したオーナーの表示名 |

**件名**: `{project_name} のお問い合わせ先メールアドレスを確認してください`

**本文(テキスト版)**:

```
お客様

{owner_name} 様が open-faq の {project_name} のお問い合わせ先メー
ルアドレスとしてこのアドレスを登録しました。FAQ ウィジェット上でお問い合
わせ先として表示するため、以下のリンクから確認をお願いします。

▶ メールアドレスを確認する
{verify_url}

このリンクは {expire_at_jst}(JST) まで有効です(発行から 24 時間)。

確認が完了するまで、FAQ ウィジェット上にお問い合わせ先は表示されません。

心当たりがない場合は本メールを破棄してください。

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: プロジェクト名を強調 + 確認用プライマリボタン + 確認前は非表示である旨を注記。

**着地ページ**: **SCR-019 プロジェクト連絡先メール確認完了**([画面設計書](01_screen-design.md)、共通領域、未認証可)。トークン検証成功時に `M_PROJECTS.contact_verified_at=now()` をセットし、結果(完了 / 期限切れ / 既使用)を表示する。

**備考**: 受信者はオーナーやメンバーである必要はなく、第三者(例: サポート窓口担当者の共有メールアドレス)でも構わない。アカウント作成や認証は不要で、トークン保有者のみが本フローを進められる。トークンは `T_ACCESS_TOKENS.purpose='contact_verify'`(24 時間)、`meta` に `projectId` を JSON 保持(FR-022a)。

------------------------------------------------------------------------

### <span id="46-tpl-lockout_notifyログインロックアウト発動"></span>4.6 TPL-LOCKOUT_NOTIFY(ログインロックアウト発動)

連続ログイン失敗でロックアウトが発動したことを本人とオーナー / 全メンバーへ知らせる `critical` メールです。ロック詳細と不正試行が疑われる場合の対応を提示します。

**発火条件**: FR-007 連続ログイン失敗閾値到達時。宛先は本人 + **オーナー(`M_CONTRACT` 由来)** + **当該スコープの有効メンバー(`M_PRJ_USERS.valid=1`)**。正規化メールで重複排除する(オーナーはメンバー行も自動保持するため両方に出る)。

**テンプレート変数**:

| 変数 | 説明 |
|----|----|
| `{recipient_display_name}` | 受信者の表示名 |
| `{locked_account_email}` | ロックされたアカウントのメールアドレス |
| `{lockout_started_at_jst}` | ロックアウト開始日時(JST) |
| `{lockout_window_minutes}` | 自動解除までの分数(MVP: 15、FR-007) |
| `{requester_ip}` | 最後の失敗試行 IP |
| `{requester_geo}` | IP からの推定国・地域(IP geolocation) |
| `{contact_url}` | サポート問い合わせ URL(**サービス提供者が運用する外部サポートページ**、環境変数 `SUPPORT_CONTACT_URL` 等で設定可能) |

**件名**: `【セキュリティ】ログインロックアウトが発動しました`

**本文(テキスト版)**:

```json
{recipient_display_name} 様

open-faq のアカウントで連続ログイン失敗を検知し、ロックアウトが発動しまし
た。

  - 対象アカウント: {locked_account_email}
  - ロックアウト開始: {lockout_started_at_jst}(JST)
  - 自動解除: {lockout_window_minutes} 分後
  - 最終試行元: {requester_ip}({requester_geo})

ご自身による試行の場合、自動解除後に正しいパスワードでログインしてくださ
い。パスワードを失念した場合は SCR-003 パスワード再設定をご利用ください。

ご自身による試行でない場合、第三者が認証情報を試行している可能性がありま
す。直ちに以下を実施してください:

  1. パスワードを再設定する
  2. 心当たりのないログイン履歴がないか確認する
  3. 必要に応じて以下からサポートへ連絡する
     {contact_url}

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: 警告アイコン + 赤系背景 `#fff5f5` のヘッダ + 「ロック詳細」「ご自身による試行の場合」「不正試行が疑われる場合」の 3 ブロック。

**着地ページ**: `{contact_url}` は **外部サポートページ**(管理画面外、本書 SCR 体系の対象外)。SCR ID は付与しない。

**備考**: 同一インシデントで同一受信者に短時間で複数回送信されないよう、`H_NOTIF_LOGS` で 60 分以内の重複配信を抑止。

------------------------------------------------------------------------

### <span id="47-tpl-deletion_reminder退会猶予期間案内"></span>4.7 TPL-DELETION_REMINDER(退会猶予期間案内)

退会申請後の節目(発効 7 日前 / 発効当日 / 完全削除 3 日前)で送る `high` メールです。`{withdrawal_phase}` でフェーズ別に件名・本文を出し分ける単一テンプレートです。

**発火条件**: SCR-014 退会申請後、退会発効日(申請当月末)の 7 日前 / 当日 / データ完全削除 3 日前の 3 回送信。退会発効(サービス停止)からデータ完全削除までの猶予は 90 日(FR-009 / 削除データ保持期間 90 日)。

**テンプレート変数**:

| 変数 | 説明 |
|----|----|
| `{recipient_display_name}` | オーナー表示名 |
| `{withdrawal_phase}` | フェーズ(`pre7d` / `effective` / `pre3d_purge`) |
| `{service_stop_at_jst}` | サービス停止日時(申請当月末日 23:59 JST) |
| `{data_purge_at_jst}` | 完全削除日時(停止 + 90 日) |
| `{cancel_withdrawal_url}` | 退会取消 URL(発効前のみ) |

**件名**:

- pre7d: `退会まで残り 7 日: サービス停止のご案内`
- effective: `退会が発効しました: データ完全削除のご案内`
- pre3d_purge: `【最終案内】データ完全削除まで残り 3 日`

**本文(テキスト版・pre7d)**:

```json
{recipient_display_name} 様

open-faq へのご退会申請ありがとうございました。
{service_stop_at_jst}(JST) にサービス利用が停止されます。

退会を取り消す場合は発効日まで以下のリンクからキャンセル可能です。

▶ 退会を取り消す
{cancel_withdrawal_url}

データ完全削除予定日: {data_purge_at_jst}(JST、サービス停止から 90 日)
完全削除後は復元できません。

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: フェーズに応じてヘッダ色を変える(pre7d: 黄、effective: 橙、pre3d_purge: 赤)+ 退会取消リンクは `pre7d` フェーズのみ表示。

**備考**: フェーズごとに件名・本文を分岐させる単一テンプレート。`{withdrawal_phase}` で本文セクションの出し分けを行う。

------------------------------------------------------------------------

### <span id="48-tpl-billing_invoice_issued月次請求確定通知"></span>4.8 TPL-BILLING_INVOICE_ISSUED(月次請求確定通知)

月次請求の確定をオーナーへ通知する `high` メールです。請求サマリと明細 PDF(添付 + DL URL 30d)・請求画面 deeplink を提示します。

**発火条件**: FR-090 月次請求確定バッチ完了時、当該契約のオーナーへ送信。

**テンプレート変数**:

| 変数                       | 説明                            |
|----------------------------|---------------------------------|
| `{recipient_display_name}` | オーナー表示名                  |
| `{billing_period_label}`   | 対象期間(`2026 年 4 月`)        |
| `{invoice_amount_jpy}`     | 請求金額(¥1,234)                |
| `{question_count}`         | 質問数                          |
| `{overage_amount_jpy}`     | 上限超過分(¥0 の場合は記載省略) |
| `{invoice_pdf_url}`        | 明細 PDF DL URL(30d 有効)       |
| `{billing_screen_url}`     | SCR-022 請求 deeplink           |

**件名**: `{billing_period_label} の請求書が発行されました(¥{invoice_amount_jpy})`

**本文(テキスト版)**:

```json
{recipient_display_name} 様

open-faq の {billing_period_label} ご利用分の請求書を発行しました。

  - 請求金額: ¥{invoice_amount_jpy}
  - 対象期間: {billing_period_label}
  - 質問数: {question_count}
  - 上限超過分: ¥{overage_amount_jpy}

明細 PDF を添付しています。また以下からも DL いただけます(30 日間有効)。

▶ 請求明細 PDF を開く
{invoice_pdf_url}

請求書一覧および過去の請求は以下からご確認いただけます。

▶ 請求画面を開く
{billing_screen_url}

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: 請求サマリ表 + プライマリボタン「請求画面を開く」+ PDF DL セカンダリボタン。

**備考**: PDF は §2.7 のとおり必ず添付。`{overage_amount_jpy}` が `0` の場合は当該行を出力しない。

------------------------------------------------------------------------

### <span id="49-tpl-billing_payment_failed支払い失敗通知"></span>4.9 TPL-BILLING_PAYMENT_FAILED(支払い失敗通知)

支払い失敗(Stripe Smart Retries 継続中)をオーナーへ通知する `high` メールです。失敗理由・再試行回数・次回再試行・サスペンション予定を提示し、支払い方法更新へ誘導します。

**発火条件**: Stripe Webhook で支払い失敗(`invoice.payment_failed`)を受信、Smart Retries が継続中の場合に送信。

**テンプレート変数**:

| 変数 | 説明 |
|----|----|
| `{recipient_display_name}` | オーナー表示名 |
| `{billing_period_label}` | 対象期間 |
| `{invoice_amount_jpy}` | 請求金額 |
| `{failure_reason}` | Stripe 失敗理由(`card_declined` 等の人間可読版) |
| `{retry_count}` | 再試行回数(1〜3) |
| `{next_retry_at_jst}` | 次回再試行日時(JST、最終再試行時は「再試行なし」) |
| `{payment_method_url}` | SCR-022 請求の支払い方法変更 URL |
| `{suspension_at_jst}` | サスペンション開始予定日時(最終再試行失敗時) |

**件名**: `【重要】請求のお支払いに失敗しました({billing_period_label})`

**本文(テキスト版)**:

```json
{recipient_display_name} 様

open-faq {billing_period_label} 分(¥{invoice_amount_jpy})のお支払いに失敗
しました。

  - 失敗理由: {failure_reason}
  - 再試行回数: {retry_count} / 3
  - 次回再試行: {next_retry_at_jst}(JST)
  - サスペンション予定: {suspension_at_jst}(JST)

支払い方法の更新で多くの場合解決できます。以下から速やかにご確認・ご更新
ください。

▶ 支払い方法を更新する
{payment_method_url}

最終再試行も失敗した場合、サスペンションが発動しサービス利用が制限されま
すのでご注意ください。

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: 警告色背景 + 再試行回数を視覚的に表示 + プライマリボタン。

**備考**: Stripe Smart Retries のスケジュール(発生から 3 / 5 / 7 日後)に従い最大 3 回送信。失敗理由テキストは英→日変換マップを用意。

------------------------------------------------------------------------

### <span id="410-tpl-billing_suspensionサスペンション開始解除"></span>4.10 TPL-BILLING_SUSPENSION(サスペンション開始/解除)

未払いによるサービス停止の開始 / 解除を通知する `critical` メールです。`{suspension_event}` が `start` / `release` のいずれかで件名・本文を分岐し、オーナー + 全メンバーへ配信します。

**発火条件**: Stripe Smart Retries 最終失敗時のサスペンション開始、または支払い完了時の解除。

**テンプレート変数**:

| 変数                       | 説明                                      |
|----------------------------|-------------------------------------------|
| `{recipient_display_name}` | 受信者表示名                              |
| `{suspension_event}`       | `start` / `release`                       |
| `{suspension_at_jst}`      | サスペンション開始日時(JST、`start` 時)   |
| `{released_at_jst}`        | サスペンション解除日時(JST、`release` 時) |
| `{billing_period_label}`   | 対象期間                                  |
| `{invoice_amount_jpy}`     | 請求金額(`start` 時)                      |
| `{payment_method_url}`     | 支払い方法変更 URL(`start` 時)            |

**件名**:

- start: `【重要】サービス利用が停止されました(請求未払い)`
- release: `サービス利用が再開されました`

**本文(テキスト版・start)**:

```json
{recipient_display_name} 様

{billing_period_label} 分(¥{invoice_amount_jpy})のお支払いが完了しなかっ
たため、{suspension_at_jst}(JST) より open-faq の管理画面および FAQ ウィ
ジェットの利用を停止しました。

サービスを再開するには支払い方法を更新し、未払い分を決済してください。

▶ 支払い方法を更新する
{payment_method_url}

ご不明な点はサポートまでご連絡ください。

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(テキスト版・release)**:

```json
{recipient_display_name} 様

{released_at_jst}(JST) にサービス利用が再開されました。
ご対応ありがとうございました。引き続きどうぞよろしくお願いいたします。

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: `start` は赤系警告 + 停止範囲リスト、`release` は緑系 + 簡潔な解除通知。

**備考**: オーナー + 全メンバー(当該スコープの `M_PRJ_USERS.valid=1`)へ配信(`critical`)。正規化メールで重複排除する。

------------------------------------------------------------------------

### <span id="411-tpl-payment_method_required無料枠超過支払方法登録要請通知"></span>4.11 TPL-PAYMENT_METHOD_REQUIRED(無料枠超過・支払方法登録要請通知)

支払方法未登録のままプロジェクトが質問数無料枠を超過し、ウィジェットの質問受付を停止した時に送る `critical` メールです。停止対象プロジェクトと支払方法登録導線を提示します。

**発火条件**: 支払方法未登録の契約の **いずれかのプロジェクト** が質問数無料枠を超過し、支払方法ゲート(FR-073)により当該プロジェクトのウィジェットの新規質問受付を停止した時点で送信。FAQ 件数の無料枠超過は本テンプレートの停止契機にしない。

**テンプレート変数**:

| 変数                        | 説明                                        |
|-----------------------------|---------------------------------------------|
| `{recipient_display_name}`  | 受信者表示名(オーナー)     |
| `{project_name}`            | 無料枠を超過したプロジェクト名              |
| `{exceeded_resource_label}` | 超過した無料枠の種別(`質問数` / `FAQ 件数`) |
| `{stopped_at_jst}`          | ウィジェット質問受付停止日時(JST)           |
| `{billing_setup_url}`       | 請求 URL(SCR-022)                           |

**件名**: `【重要】{project_name} が無料枠を超過しました — お支払い方法の登録が必要です`

**本文(テキスト版)**:

```json
{recipient_display_name} 様

open-faq のプロジェクト「{project_name}」の月次無料枠({exceeded_resource_label})を超過しました。
お支払い方法が未登録のため、{stopped_at_jst}(JST) より当該プロジェクトのウィジェットの
新規質問受付を停止しています(管理画面は引き続きご利用いただけます)。

ウィジェットの質問受付を再開するには、お支払い方法を登録してください。
登録後ただちに再開し、超過分は事後課金となります。

▶ 支払い方法を登録する
{billing_setup_url}

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: 超過種別カード + ウィジェット停止の案内 + プライマリボタン(支払い方法を登録する)。

------------------------------------------------------------------------

### <span id="412-tpl-terms_revision利用規約改定告知"></span>4.12 TPL-TERMS_REVISION(利用規約改定告知)

利用規約・プライバシーポリシー改定の発効 30 日前にオーナー + 全メンバーへ送る `critical` メールです。改定要約・新規約 URL・同意期限(発効日 + 14d)・再同意 deeplink を提示します。

**発火条件**: 利用規約・プライバシーポリシー改定の発効日 30 日前に送信(FR-010)。オーナー + 全メンバー(当該スコープの `M_PRJ_USERS.valid=1`)へ配信し、正規化メールで重複排除する。

**テンプレート変数**:

| 変数                       | 説明                              |
|----------------------------|-----------------------------------|
| `{recipient_display_name}` | 受信者表示名                      |
| `{effective_at_jst}`       | 改定発効日時(JST)                 |
| `{summary_text}`           | 改定要約(HTML sanitize 済)        |
| `{new_terms_url}`          | 新規約 URL                        |
| `{consent_deadline_jst}`   | 同意期限(発効日 + 14d、JST)       |
| `{consent_screen_url}`     | SCR-015 規約再同意割込み deeplink |

**件名**: `【重要】利用規約改定のお知らせ(発効日: {effective_at_jst})`

**本文(テキスト版)**:

```json
{recipient_display_name} 様

open-faq の利用規約を {effective_at_jst}(JST) より改定いたします。

改定要約:
{summary_text}

新しい利用規約全文は以下をご確認ください。

▶ 新しい利用規約を読む
{new_terms_url}

ご利用継続のためには、{consent_deadline_jst}(JST、発効日 + 14 日) までに
管理画面で再同意をお願いいたします。期限を過ぎると一部機能の利用が制限さ
れる場合があります。

▶ 管理画面で再同意する
{consent_screen_url}

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: 改定要約をパネル表示 + 「新規約を読む」「再同意する」の 2 プライマリボタン。`critical` 重要度のため強制送信。

------------------------------------------------------------------------

### <span id="413-tpl-service_announcement運営からのお知らせ"></span>4.13 TPL-SERVICE_ANNOUNCEMENT(運営からのお知らせ)

サービス運営側から配信トリガーされるお知らせメールです。重要度(`normal` / `high` / `critical`)は配信時に選択し、本書はメインシステム側の受信時表現を定めます。

**発火条件**: お知らせの配信がトリガーされた時。重要度 `normal` / `high` / `critical` は配信時に選択。

**テンプレート変数**:

| 変数                       | 説明                              |
|----------------------------|-----------------------------------|
| `{recipient_display_name}` | 受信者表示名                      |
| `{announcement_title}`     | お知らせタイトル                  |
| `{announcement_body_html}` | お知らせ本文(HTML sanitize 済)    |
| `{signature}`              | 配信元署名(`open-faq 運営事務局`) |

**件名**: `{announcement_title}`(`critical` の場合は `【重要】` プレフィックスを自動付与)

**本文(テキスト版)**:

```json
{recipient_display_name} 様

open-faq 運営事務局よりお知らせいたします。

{announcement_body_html}

──────────────────────────────────────────────
このメールに直接返信しないでください。
{signature}
```

**本文(HTML 版)**: お知らせ本文は HTML 版でリッチテキスト(リスト・太字・リンクのみ許可)で表示。

**強制送信**: 規約改定・価格改定・重要セキュリティに該当するお知らせは重要度 `critical` を選択して配信し、受信者はオプトアウトできない(FR-091 / BR-078。利用規約改定そのものは専用の `TPL-TERMS_REVISION` を用いる)。それ以外の `normal` / `high` は §5.2 のルールに従う。

**備考**: 本書ではメインシステム側の受信時表現を定義する。

------------------------------------------------------------------------

### <span id="414-tpl-system_noticeサブ契機ごとの定型文--メタテンプレート"></span>4.14 TPL-SYSTEM_NOTICE(サブ契機ごとの定型文 = メタテンプレート)

質問数の選択アラート閾値到達や契約上書き反映など運用系イベントを通知するメタテンプレートです。サブ契機(`event_type`)ごとに件名・本文を動的に組み立て、AI 利用上限到達などメール対象外の契機は受信箱のみで通知します。

**発火条件**: 質問数の選択アラート閾値到達、契約上書き反映等の運用系イベント(FR-071 / FR-091a)。サブ契機ごとに別 i18n キーを持つ。質問数上限関連(25% / 50% / 80% / 90% / 100% 閾値到達)はメール送信対象。

**メール対象外**: AI 利用上限到達(FR-091a / FR-125 のシステム通知契機)は MVP ではメールを送信せず、お知らせ受信箱(`inbox` チャネル)のみで通知する。受信箱側の生成は 本書 を正本とする。

**テンプレート変数(共通)**:

| 変数 | 説明 |
|----|----|
| `{recipient_display_name}` | 受信者表示名 |
| `{event_type}` | サブ契機名(`question_limit_threshold_reached` / `quota_override_applied` 等) |
| `{event_at_jst}` | 発生日時(JST) |
| `{related_resource}` | 関連リソース名(プロジェクト名)。上限系はプロジェクト単位 |
| `{threshold_percent}` | 到達したアラート閾値(`25` / `50` / `80` / `90` / `100`) |
| `{used_count}` | 到達時点の当月質問数 |
| `{limit_count}` | 設定中の当月質問数上限 |
| `{action_url}` | 対応画面 URL(上限系は SCR-021、請求系は SCR-022、個人設定は SCR-017) |

**件名**: サブ契機ごとに以下のマッピング(上限系はプロジェクト名を含める):

| event_type | 件名 |
|----|----|
| question_limit_threshold_reached | {related_resource}: 当月の質問数が上限の {threshold_percent}% に達しました |
| quota_override_applied | プロジェクト上限が更新されました |

> 質問数上限アラートの配信先はオーナー + 当該プロジェクトの有効メンバー(`M_PRJ_USERS.valid=1`)。画面上で送信先は変更できず、ユーザーIDと正規化メールアドレスで重複排除する。

**本文(テキスト版・テンプレート骨格)**:

```json
{recipient_display_name} 様

(event_type 別の定型文。例: question_limit_threshold_reached)
{event_at_jst}(JST) 時点で、プロジェクト「{related_resource}」の当月の質問数が
設定上限件数の {threshold_percent}% に達しました。

  - 対象: {related_resource}
  - 当月の質問数: {used_count} 件
  - 今月の利用上限: {limit_count} 件
  - 到達割合: {threshold_percent}%
  - 発生日時: {event_at_jst}(JST)

詳細・対応方法は以下からご確認ください。

▶ 詳細を見る
{action_url}

──────────────────────────────────────────────
このメールに直接返信しないでください。
open-faq <noreply@<service-domain>>
```

**本文(HTML 版)**: サブ契機ごとに色を変える(警告系: 黄、超過系: 赤、情報系: 青)。

**備考**: 新規イベント追加時は本書 + 本書 + i18n キー定義の 3 か所を同期更新する。

## <span id="5-配信運用"></span>5. 配信運用

テンプレートを実際に配信する際の宛先解決・強制送信ルール・重複抑止・配信ログ・テスト送信を定めます。各テンプレートが §4 で定めた件名・本文を、誰に・どの条件で・重複なく届けるかを以降の小節で示します。

### <span id="51-配信先解決ロジック"></span>5.1 配信先解決ロジック

テンプレートごとに配信先を決める解決ロジックを定めます。次の表は通知 ID と配信先解決方法を対応させたもので、ロックアウト・課金系の有効メンバー(`valid=1`)起点の網羅解決などを含みます。

| 通知 ID | 配信先解決 |
|----|----|
| TPL-EMAIL_VERIFY / PASSWORD_RESET | 操作者本人のメールアドレス(セッションから) |
| TPL-ADMIN_USER_REGISTER | 招待時に入力されたメールアドレス(`T_ACCESS_TOKENS.target_email`) |
| TPL-PROJECT_CONTACT_VERIFY | プロジェクト連絡先メールアドレス |
| TPL-LOCKOUT_NOTIFY | ロック対象者 + オーナー(`M_CONTRACT` 由来) + 当該スコープの有効メンバー(`M_PRJ_USERS.valid=1`)。正規化メールで重複排除(オーナー + 全メンバーを網羅) |
| TPL-DELETION_REMINDER / PAYMENT_METHOD_REQUIRED / BILLING_INVOICE_ISSUED / BILLING_PAYMENT_FAILED | 契約のオーナー(`M_CONTRACT` 由来)のみ |
| TPL-BILLING_SUSPENSION / TERMS_REVISION | オーナー(`M_CONTRACT` 由来) + 当該スコープの有効メンバー(`M_PRJ_USERS.valid=1`)。正規化メールで重複排除 |
| TPL-SERVICE_ANNOUNCEMENT | 配信時に指定する範囲(全契約 / 単一契約 / 特定プロジェクト) |
| TPL-SYSTEM_NOTICE | `question_limit_threshold_reached` はオーナー + 当該プロジェクトの有効メンバー(`M_PRJ_USERS.valid=1`)。その他はサブ契機ごとに定義 |

### <span id="52-重要度別の強制送信ルール共有概念正本"></span>5.2 重要度別の強制送信ルール(共有概念正本)

通知重要度 4 値ごとにオプトアウト可否と強制送信の扱いを定めます。次の各項目は `critical` / `high` の強制送信と `normal` / `low` のオプトアウト方式を示し、重要度の正本ルールは [`M_CONTRACT`](TBL-M-002.md) に従います。

- `critical`: 受信オプトアウト不可、必ずメール送信。`TPL-EMAIL_VERIFY` / `PASSWORD_RESET` / `ADMIN_USER_REGISTER` / `PROJECT_CONTACT_VERIFY` / `LOCKOUT_NOTIFY` / `BILLING_SUSPENSION` / `PAYMENT_METHOD_REQUIRED` / `TERMS_REVISION` / `SERVICE_ANNOUNCEMENT`(`critical` 選択時)
- `high`: 強制送信(オプトアウト不可)
- `normal`: 受信オプトアウト可能(プロジェクト関連通知トグルで一括制御)
- `low`: 個別オプトアウト + `List-Unsubscribe` ヘッダで RFC 8058 対応

### <span id="53-重複配信抑止"></span>5.3 重複配信抑止

同一イベントで同じ受信者へ多重配信しないための抑止条件を定めます。次の表は抑止対象・抑止窓・実装方針(冪等キー / ログ検索)を対応させたものです。

| 抑止対象 | 抑止窓 | 実装方針 |
|----|----|----|
| TPL-LOCKOUT_NOTIFY 同一受信者 | 60 分 | `H_NOTIF_LOGS(user_id, template_id, sent_at)` 検索 |
| TPL-BILLING_PAYMENT_FAILED 同一 invoice | Stripe Smart Retries 1 回につき 1 通 | `invoice_id` で重複検知 |
| TPL-SYSTEM_NOTICE 質問数上限アラート | 同一プロジェクト × 同一請求月 × 同一閾値につき1通/受信者 | 冪等キー `question-limit-alert:{projectId}:{yyyyMM}:{thresholdPercent}` + 受信者ID |

### <span id="54-配信ログ"></span>5.4 配信ログ

全送信を記録する配信ログの保存先・列構成・保持期間を定めます。次の各項目は `H_NOTIF_LOGS` に記録する内容を示し、テーブル定義は [データベース設計.md](03_database-design.md) が正本です。

- 全送信は `H_NOTIF_LOGS` に行を記録(03 テーブル設計参照)
- 列: `id` / `user_id` / `template_id` / `subject` / `recipient_email` / `sent_at` / `delivery_status`(`queued` / `sent` / `bounced` / `failed`)/ `provider_message_id` / `error_text`
- 保持期間: 90 日(NFR-059 一般ログ準拠)

### <span id="55-テスト送信"></span>5.5 テスト送信

開発・ステージング環境での誤配信を防ぐ仕組みを定めます。次の各項目は全宛先の強制リダイレクトと件名プレフィックス付与を示します。

- 開発・ステージング環境では `MAIL_SAFE_SINK` 環境変数で全宛先を `dev-mail-sink@<internal-domain>` に強制リダイレクト
- 件名にプレフィックス `[STAGING]` / `[DEV]` を自動付与

## <span id="6-テンプレート開発運用フロー"></span>6. テンプレート開発・運用フロー

テンプレートを新規追加 / 変更する際に同期すべき作業手順を定めます。本書・i18n キーなど複数箇所の整合を保つため、追加と変更それぞれの手順を以降に示します。

### <span id="61-新規テンプレート追加手順"></span>6.1 新規テンプレート追加手順

メールテンプレートを新規に追加する際の作業を順に定めます。次の手順は通知契機の登録から検証スクリプト実行までの一連を示します。

1.  通知契機を 本書 に追加(NOTIF-\* 行)
2.  本書 §3 索引 + §4 詳細にテンプレート行を追加
3.  テンプレート変数を確定し i18n キーファイル(`locales/ja/email_templates.yml`)に追加
4.  HTML / テキスト両版を実装し、ステージング `MAIL_SAFE_SINK` で目視確認
5.  `check-spec-sync.sh` を実行し SC-001〜SC-012 全パスを確認

### <span id="62-既存テンプレート変更手順"></span>6.2 既存テンプレート変更手順

既存テンプレートを変更する際の影響範囲を変更の大きさ別に定めます。次の各項目は、軽微な文言修正・件名 / CTA 変更・配信先 / 重要度変更ごとに同期すべきドキュメントを示します。

- 軽微な文言修正(誤字 / 表現変更): 本書 §4 のみ更新 + 変更履歴に記載
- 件名変更 / 主要 CTA 変更: 本書 §4 + ステージング再送テスト
- 配信先・重要度変更: 本書 §5.1 / §5.2 + [`M_CONTRACT`](TBL-M-002.md) の整合確認

## <span id="更新履歴"></span>更新履歴

| 版数 | 日付 | 変更内容 |
|----|----|----|
| v1.3 | 2026-06-20 | ユーザー種別をオーナー/メンバーの2種へ統合(プロジェクト管理者を廃止)。`TPL-PROJECT_ADMIN_INVITE`(プロジェクト管理者招待)を廃止し、メンバー招待を `TPL-ADMIN_USER_REGISTER`(共通メンバー招待)へ一本化。`{assigned_role_label}` 変数と「付与ロール」記載を削除。契約横断 critical 通知(LOCKOUT_NOTIFY / BILLING_SUSPENSION / TERMS_REVISION / 質問数上限アラート)の宛先を「オーナー + 全プロジェクト管理者」から「オーナー(`M_CONTRACT` 由来) + 当該スコープの有効メンバー(`M_PRJ_USERS.valid=1`、正規化メールで重複排除)」へ更新。 |
| v1.2 | 2026-06-17 | 記載スタイル標準(設計書シンプルテンプレ v2)へ移行。旧「1. 文書概要(目的 / 対象範囲 / 版数表 / 関連ドキュメント表)」を要約ブロック(`ps-lead`)+ `doc-meta` + 範囲 callout へ集約。各 `<h2>` / `<h3>` 直後に `section-lead` を追加。テンプレート ID(`TPL-*`)・通知 ID(`NOTIF-*`)・件名 / 本文テンプレート全文・配信契機・変数・配信運用ルールは一切改変せず保持。 |
| v1.2 | 2026-06-17 | (旧履歴)プロジェクト管理者招待(`TPL-PROJECT_ADMIN_INVITE`)・無料枠超過支払方法登録要請(`TPL-PAYMENT_METHOD_REQUIRED`)等を含むテンプレート群を整備。 |

---

<!-- portal-bottom -->
[基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
