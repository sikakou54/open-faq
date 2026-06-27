# メッセージ設計

> **このページは、メインシステムが送信する全メールテンプレート(`MSG-NNN`)の一覧と、メール共通基準・配信運用ルールの正本です。** 各テンプレートの件名・本文・変数・送信契機は個別 `MSG-NNN.md` が正本です。画面に表示する確認・完了・エラーメッセージの文言は各 [画面設計](../01_frontend/01_screens/index.md)(SCR の §4 / §6)、拒否時のエラーコードは [エラー設計](../05_errors/index.md) が正本です。

*ステータス ドラフト*

## <span id="reading"></span>読み順

画面設計(画面文言)/ API設計 / エラー設計 ＞ 本メッセージ設計(メールテンプレート)。配信宛先解決ロジックは [権限設計 PERM-011](../04_permissions/PERM-011.md#PERM-011) が正本です。

## <span id="list"></span>1. メッセージ(メールテンプレート)一覧(13)

メール送信を含む全テンプレートの索引です。件名 + 本文の全文は各 MSG ファイルを参照します。

| MSG ID | テンプレートID | 通知ID | 重要度 | 配信先 | 強制送信 | リンク有効期限 |
|----|----|----|----|----|----|----|
| <span id="MSG-001"></span>[MSG-001](MSG-001.md#MSG-001) | `TPL-EMAIL_VERIFY` | NOTIF-EMAIL_VERIFY | critical | 本人 | ◯ | 24h |
| <span id="MSG-002"></span>[MSG-002](MSG-002.md#MSG-002) | `TPL-PASSWORD_RESET` | NOTIF-PASSWORD_RESET | critical | 本人 | ◯ | 1h |
| <span id="MSG-003"></span>[MSG-003](MSG-003.md#MSG-003) | `TPL-MEMBER_INVITATION` | NOTIF-MEMBER_INVITATION | critical | 招待対象(登録済みユーザー) | ◯ | 7d |
| <span id="MSG-004"></span>[MSG-004](MSG-004.md#MSG-004) | `TPL-PROJECT_CONTACT_VERIFY` | (オーナー操作派生) | critical | プロジェクト連絡先 | ◯ | 24h |
| <span id="MSG-005"></span>[MSG-005](MSG-005.md#MSG-005) | `TPL-LOCKOUT_NOTIFY` | NOTIF-LOCKOUT_NOTIFY | critical | ロック本人 + オーナー + 全メンバー | ◯ | (リンクなし) |
| <span id="MSG-006"></span>[MSG-006](MSG-006.md#MSG-006) | `TPL-WITHDRAWAL_COMPLETED` | NOTIF-WITHDRAWAL_COMPLETED | high | 退会したアカウント本人 | ◯ | (リンクなし) |
| <span id="MSG-007"></span>[MSG-007](MSG-007.md#MSG-007) | `TPL-BILLING_INVOICE_ISSUED` | NOTIF-BILLING_INVOICE_ISSUED | high | オーナー | ◯ | 30d(PDF 再 DL) |
| <span id="MSG-008"></span>[MSG-008](MSG-008.md#MSG-008) | `TPL-BILLING_PAYMENT_FAILED` | NOTIF-BILLING_PAYMENT_FAILED | high | オーナー | ◯ | (再決済リンク) |
| <span id="MSG-009"></span>[MSG-009](MSG-009.md#MSG-009) | `TPL-BILLING_SUSPENSION` | NOTIF-BILLING_SUSPENSION | critical | オーナー + 全メンバー | ◯ | (リンクなし) |
| <span id="MSG-010"></span>[MSG-010](MSG-010.md#MSG-010) | `TPL-PAYMENT_METHOD_REQUIRED` | NOTIF-PAYMENT_METHOD_REQUIRED | critical | オーナー + 当該PJ有効メンバー | ◯ | (課金設定リンク) |
| <span id="MSG-011"></span>[MSG-011](MSG-011.md#MSG-011) | `TPL-TERMS_REVISION` | NOTIF-TERMS_REVISION | critical | オーナー + 全メンバー | ◯ | [システム仕様書 §3](../07_system-spec.md#3-タイムアウトセッション認証) の規約再同意期限 |
| <span id="MSG-012"></span>[MSG-012](MSG-012.md#MSG-012) | `TPL-SERVICE_ANNOUNCEMENT` | NOTIF-SERVICE_ANNOUNCEMENT | normal/high/critical | 範囲指定可 | 配信時に選択 | 入力 URL |
| <span id="MSG-013"></span>[MSG-013](MSG-013.md#MSG-013) | `TPL-SYSTEM_NOTICE` | NOTIF-SYSTEM_NOTICE | normal/high | 対象者 | 契機による | (画面内リンク) |

> [!NOTE]
> **本書の範囲と対象外** 本書は `MSG-*`(= `TPL-*`)各件の件名 / テキスト本文 / HTML 本文・送信契機(`NOTIF-*`)・配信先 / 重要度 / 添付 / リンク有効期限・メール共通要件(送信元・i18n・サニタイズ・配信信頼性)を扱います。`NOTIF-CHAT_HOLD_CHECK` はチャネルが `inbox` 限定(メール送信なし)のため対象外、画面文言は [画面設計](../01_frontend/01_screens/index.md) が正本です。

## <span id="common"></span>2. メール共通基準

全テンプレートに共通する送信元・件名・本文構造・文字コード・サニタイズ・配信失敗時挙動・添付の基準をまとめます。各小節は個別テンプレート(§4)が前提とする土台を定めるもので、テンプレート固有の差分のみを §4 側に記載します。

### <span id="21-送信元--reply-to--差出人表記"></span>2.1 送信元 / Reply-To / 差出人表記

差出人・返信先・認証情報の固定値を定めます。次の表は Envelope From(VERP)/ Header From / Reply-To / List-Unsubscribe / DMARC 等を並べたもので、なりすまし対策と到達性確保の基礎になります。

| 項目 | 値 |
|----|----|
| Envelope From | `bounces+<deliveryId>@<service-domain>` (VERP) |
| Header From | `open-faq <noreply@<service-domain>>` 固定 |
| Reply-To | 設定しない(NULL) |
| List-Unsubscribe | マーケティング系 `low` 通知にのみ設定 |
| DMARC / DKIM / SPF | 全テンプレートで pass を必須(送信ドメイン認証によるなりすまし対策・到達性確保) |

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

ウィジェット利用者の入力をメールに流用する際の安全策を定めます。次の各項目は、件名・送信元への流用禁止と本文埋め込み時のエスケープ・字数制限を定め、スパム埋め込みやなりすましを防ぎます(FR-117)。

- **ウィジェット利用者の入力文字列(質問本文等)を、メール件名・送信元(Header From / Envelope From)・Reply-To へそのまま使用しない**(FR-117。スパム埋め込み・なりすまし対策)。送信元は §2.1 のとおり `no-reply` 固定とする。
- ウィジェット利用者入力を本文に埋め込む場合に限り、HTML エスケープ + 200 字制限 + 末尾省略記号 `…` を付与する。
- 引用ブロックは罫線で視覚的に分離し、サービスからの文言と区別する。

### <span id="26-配信失敗時の挙動"></span>2.6 配信失敗時の挙動

送信失敗・バウンス・苦情時の再送方式の正本所在と、本書で定めるテンプレート単位の例外を示します。配信信頼性の方式そのものは 要件のセキュリティ NFR を正本とし、本書は `critical` 認証メールの再送続行など差分のみを定めます。

再送回数上限([システム仕様書 §3](../07_system-spec.md#3-タイムアウトセッション認証) の通知再送上限)・バウンス / 苦情検知・全ユーザー横断の送信停止リストといった**配信信頼性の方式は 要件のセキュリティ NFR を正本**とする(FR-113 / FR-114 / FR-119 / FR-123)。本書はテンプレート単位の挙動差のみを以下に定める。

- 恒久失敗(hard bounce)で送信停止リストに載った宛先でも、`critical` 重要度の `TPL-LOCKOUT_NOTIFY` のみ再送試行を続行する(認証関連の到達性最優先)。

### <span id="27-添付ファイル"></span>2.7 添付ファイル

添付ファイルを付けるテンプレートと形式・サイズ上限を定めます。次の表のとおり添付は請求明細 PDF のみに限定し、その他のテンプレートには添付を付けません。

| テンプレート | 添付ファイル | 形式 |
|----|----|----|
| `TPL-BILLING_INVOICE_ISSUED` | 請求明細 PDF | `invoice_{year}{month}.pdf`、≤ 1 MB |

その他のテンプレートには添付ファイルを付けない。

## <span id="ops"></span>3. 配信運用

テンプレートを実際に配信する際の宛先解決・強制送信ルール・重複抑止・配信ログ・テスト送信を定めます。各テンプレートが §4 で定めた件名・本文を、誰に・どの条件で・重複なく届けるかを以降の小節で示します。

### <span id="31-配信先解決ロジック"></span>3.1 配信先解決ロジック

テンプレートごとに配信先を決める解決ロジックを定めます。次の表は通知 ID と配信先解決方法を対応させたもので、ロックアウト・課金系の有効メンバー(`valid=1`)起点の網羅解決などを含みます。

| 通知 ID | 配信先解決 |
|----|----|
| TPL-EMAIL_VERIFY / PASSWORD_RESET | 操作者本人のメールアドレス(セッションから) |
| TPL-MEMBER_INVITATION | 招待対象(登録済みユーザー)のメールアドレス(`T_ACCESS_TOKENS.target_email`) |
| TPL-PROJECT_CONTACT_VERIFY | プロジェクト連絡先メールアドレス |
| TPL-LOCKOUT_NOTIFY | ロック対象者 + 対象プロジェクトのオーナー(`M_PROJECTS.owner_user_id` 由来) + 当該プロジェクトの有効メンバー(`M_PRJ_USERS.valid=1`)。ユーザーIDと正規化メールで重複排除(オーナー + 全メンバーを網羅) |
| TPL-WITHDRAWAL_COMPLETED | 退会したアカウント本人 |
| TPL-BILLING_INVOICE_ISSUED / BILLING_PAYMENT_FAILED | 対象プロジェクトのオーナー(`M_PROJECTS.owner_user_id` 由来。請求名義は当該オーナーの課金アカウント)のみ |
| TPL-PAYMENT_METHOD_REQUIRED / BILLING_SUSPENSION / TERMS_REVISION | 対象プロジェクトのオーナー(`M_PROJECTS.owner_user_id` 由来) + 当該プロジェクトの有効メンバー(`M_PRJ_USERS.valid=1`)。ユーザーIDと正規化メールで重複排除 |
| TPL-SERVICE_ANNOUNCEMENT | 配信時に指定する範囲(全ユーザー / 単一アカウント / 特定プロジェクト) |
| TPL-SYSTEM_NOTICE | `question_limit_threshold_reached` はオーナー + 当該プロジェクトの有効メンバー(`M_PRJ_USERS.valid=1`)。その他はサブ契機ごとに定義 |

### <span id="32-重要度別の強制送信ルール共有概念正本"></span>3.2 重要度別の強制送信ルール(共有概念正本)

通知重要度 4 値ごとにオプトアウト可否と強制送信の扱いを定めます。次の各項目は `critical` / `high` の強制送信と `normal` / `low` のオプトアウト方式を示し、重要度の正本ルールは [`M_BILLING_ACCOUNT`](../02_backend/04_database/TBL-002.md#TBL-002) に従います。

- `critical`: 受信オプトアウト不可、必ずメール送信。`TPL-EMAIL_VERIFY` / `PASSWORD_RESET` / `MEMBER_INVITATION` / `PROJECT_CONTACT_VERIFY` / `LOCKOUT_NOTIFY` / `BILLING_SUSPENSION` / `PAYMENT_METHOD_REQUIRED` / `TERMS_REVISION` / `SERVICE_ANNOUNCEMENT`(`critical` 選択時)
- `high`: 強制送信(オプトアウト不可)
- `normal`: 受信オプトアウト可能(プロジェクト関連通知トグルで一括制御)
- `low`: 個別オプトアウト + `List-Unsubscribe` ヘッダで RFC 8058 対応

### <span id="33-重複配信抑止"></span>3.3 重複配信抑止

同一イベントで同じ受信者へ多重配信しないための抑止条件を定めます。次の表は抑止対象・抑止窓・実装方針(冪等キー / ログ検索)を対応させたものです。

| 抑止対象 | 抑止窓 | 実装方針 |
|----|----|----|
| TPL-LOCKOUT_NOTIFY 同一受信者 | 60 分 | `H_NOTIF_LOGS(user_id, template_id, sent_at)` 検索 |
| TPL-BILLING_PAYMENT_FAILED 同一 invoice | Stripe Smart Retries 1 回につき 1 通 | `invoice_id` で重複検知 |
| TPL-SYSTEM_NOTICE 質問数上限アラート | 同一プロジェクト × 同一請求月 × 同一閾値につき1通/受信者 | 冪等キー `question-limit-alert:{projectId}:{yyyyMM}:{thresholdPercent}` + 受信者ID |

### <span id="34-配信ログ"></span>3.4 配信ログ

全送信を記録する配信ログの保存先・列構成・保持期間を定めます。次の各項目は `H_NOTIF_LOGS` に記録する内容を示し、テーブル定義は [データベース設計.md](../02_backend/04_database/index.md) が正本です。

- 全送信は `H_NOTIF_LOGS` に行を記録(03 テーブル設計参照)
- 列: `id` / `user_id` / `template_id` / `subject` / `recipient_email` / `sent_at` / `delivery_status`(`queued` / `sent` / `bounced` / `failed`)/ `provider_message_id` / `error_text`
- 保持期間: [システム仕様書 §4](../07_system-spec.md#4-データ保持期間削除猶予)（物理削除は SYS-032 が担当）

### <span id="35-テスト送信"></span>3.5 テスト送信

開発・ステージング環境での誤配信を防ぐ仕組みを定めます。次の各項目は全宛先の強制リダイレクトと件名プレフィックス付与を示します。

- 開発・ステージング環境では `MAIL_SAFE_SINK` 環境変数で全宛先を `dev-mail-sink@<internal-domain>` に強制リダイレクト
- 件名にプレフィックス `[STAGING]` / `[DEV]` を自動付与

## <span id="devflow"></span>4. テンプレート開発・運用フロー

テンプレートを新規追加 / 変更する際に同期すべき作業手順を定めます。本書・i18n キーなど複数箇所の整合を保つため、追加と変更それぞれの手順を以降に示します。

### <span id="41-新規テンプレート追加手順"></span>4.1 新規テンプレート追加手順

メールテンプレートを新規に追加する際の作業を順に定めます。次の手順は通知契機の登録から検証スクリプト実行までの一連を示します。

1.  通知契機を 本書 に追加(NOTIF-\* 行)
2.  本書 §3 索引 + §4 詳細にテンプレート行を追加
3.  テンプレート変数を確定し i18n キーファイル(`locales/ja/email_templates.yml`)に追加
4.  HTML / テキスト両版を実装し、ステージング `MAIL_SAFE_SINK` で目視確認
5.  `check-spec-sync.sh` を実行し SC-001〜SC-012 全パスを確認

### <span id="42-既存テンプレート変更手順"></span>4.2 既存テンプレート変更手順

既存テンプレートを変更する際の影響範囲を変更の大きさ別に定めます。次の各項目は、軽微な文言修正・件名 / CTA 変更・配信先 / 重要度変更ごとに同期すべきドキュメントを示します。

- 軽微な文言修正(誤字 / 表現変更): 本書 §4 のみ更新 + 変更履歴に記載
- 件名変更 / 主要 CTA 変更: 本書 §4 + ステージング再送テスト
- 配信先・重要度変更: 本書 §3.1 / §3.2 + [`M_BILLING_ACCOUNT`](../02_backend/04_database/TBL-002.md#TBL-002) の整合確認

## <span id="screen-msg"></span>5. 画面メッセージ(参照)

画面に表示する確認・完了・エラーメッセージ(`MSG-SCR-*` 相当)の文言は各画面設計が正本です。本書はメール文言の正本に限定します。

| メッセージ種別 | 正本 |
|----|----|
| 画面の入力検証・エラー表示文言 | 各 [画面設計](../01_frontend/01_screens/index.md) SCR の §4 画面項目定義 |
| 確認ダイアログ・完了トースト文言 | 各 [画面設計](../01_frontend/01_screens/index.md) SCR の §6 画面イベント一覧 |
| API エラーコード(HTTP / 分類) | [エラー設計](../05_errors/index.md) |
| お知らせ受信箱(`inbox`)メッセージ | 本書 `TPL-SYSTEM_NOTICE`([MSG-013](MSG-013.md#MSG-013))の `inbox` 生成 |
