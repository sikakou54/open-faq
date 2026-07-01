# システム仕様書(設計値の正本)

> **このページは、サービス提供に関わる設計値(しきい値・課金単価・無料枠・タイムアウト・保持期間・AI しきい値)を一元管理する正本です。** 各設計書は本書を参照する。値の業務的根拠は対応する RULE / FR / NFR を併記する。

## <span id="1-aiしきい値"></span>1. AI しきい値

回答可否判定(信頼度・関連度)のしきい値は、グローバル既定値とプロジェクト単位の設定値だけを持つ。推論時は対象プロジェクトの設定値が登録されていればその値を使用し、未登録の場合はグローバル既定値を使用する。

| 種別 | 適用条件 | 設定主体 | 既定値の有無 |
|----|----|----|----|
| `global`(グローバル既定値) | 対象プロジェクトの設定値が未登録の場合 | 運営 | 信頼度 0.60 / 関連度 0.50 を常時保持 |
| `project`(プロジェクト設定値) | 対象プロジェクトの設定値が登録済みの場合 | オーナー / 当該プロジェクトのメンバー | 未登録可(未登録時はグローバル既定値を使用) |

プロジェクト設定値は信頼度・関連度を 1 セットとして扱う。片方だけを登録してもう片方をグローバル既定値から補う部分的なフォールバックは行わない。プロジェクト設定値をリセットした場合は当該プロジェクトの設定行を削除し、未登録状態としてグローバル既定値を使用する。

| 項目 | 値 | 単位/条件 | 根拠 | 格納先 |
|----|----|----|----|----|
| 信頼度しきい値(グローバル既定) | 0.60 | 0.0〜1.0 | [RULE-012](../01_requirements/01_business_requirement/08_rule.md#RULE-012) | 定数(システム仕様書 / RULE-012) |
| 関連度しきい値(グローバル既定) | 0.50 | 0.0〜1.0 | [RULE-012](../01_requirements/01_business_requirement/08_rule.md#RULE-012) | 定数(システム仕様書 / RULE-012) |
| プロジェクト設定値 | 上書き値(未登録可) | 0.0〜1.0、信頼度・関連度を同時に保持 | [RULE-012](../01_requirements/01_business_requirement/08_rule.md#RULE-012) | [`TP_AI_THRESH_CACHE`](02_backend/04_database/TBL-031.md#TBL-031)(`project_id`) |
| AI 回答 候補 FAQ 件数 | 5 | 件(`published` かつ当該 `project_id` の FAQ を全文検索し一致スコア降順で上位 N=5 件を候補とする) | [FR-198](../01_requirements/02_functional_requirement/02_faq-ai-fr.md#FR-198) | 定数(AI 回答候補選定) |

> [!NOTE]
> **取得・更新・削除と伝播** プロジェクト設定値の取得・更新・削除は [API-067](02_backend/03_apis/API-067.md#API-067)、変更後の設定状態の AI 推論への伝播・取得失敗時のフォールバックは [SYS-015](02_backend/01_system/SYS-015.md#SYS-015) が担う。対象プロジェクトの設定値が未登録または取得不能の場合は、グローバル既定値で推論を継続する。取得不能時はアラートを上げる。

## <span id="2-課金利用量上限"></span>2. 課金・利用量・上限

完全従量課金 + 月次無料枠の単一モデルを全アカウントへ適用する。無料枠・月次上限はプロジェクト単位、レート制限はオーナー単位で判定する。質問数のみが月次上限件数による受付停止対象で、FAQ 件数は上限なしで従量課金を継続する。値の業務的根拠と判定ロジックは [課金・請求設計書](05_billing-design.md) を併せて参照する。

| 項目 | 値 | 単位/条件 | 根拠 | 格納先 |
|----|----|----|----|----|
| 質問数 無料枠 | 1,000 | 件 / 月(JST 暦月境界・毎月 1 日 00:00 JST リセット) | [RULE-015](../01_requirements/01_business_requirement/08_rule.md#RULE-015) / [課金・請求設計書](05_billing-design.md) | KV `usage-limit:free-default:question`(初期 1,000)・[`M_PRJ_QUOTA_LIMITS`](02_backend/04_database/TBL-009.md#TBL-009) `free_quota` |
| 質問数 超過単価 | 0.5 | 円 / 件 | [課金・請求設計書](05_billing-design.md) | 定数(課金ロジック) |
| FAQ 件数 無料枠 | 100 | 件 | [課金・請求設計書](05_billing-design.md) | KV `usage-limit:free-default:faq`(初期 100)・[`M_PRJ_QUOTA_LIMITS`](02_backend/04_database/TBL-009.md#TBL-009) `free_quota` |
| FAQ 件数 超過単価 | 5 | 円 / 件 / 月 | [課金・請求設計書](05_billing-design.md) | 定数(課金ロジック) |
| AI 利用コスト | MVP 吸収 | 社内可視化指標(課金対象外) | [課金・請求設計書](05_billing-design.md) | [`T_USAGE_METER`](02_backend/04_database/TBL-020.md#TBL-020) |
| 質問数 受付停止しきい値 | 100 | % 到達でウィジェット新規質問受付を停止 | [RULE-013](../01_requirements/01_business_requirement/08_rule.md#RULE-013) | [`M_PRJ_QUOTA_LIMITS`](02_backend/04_database/TBL-009.md#TBL-009) `threshold` |
| 質問数 最終ガード追加通知 | 125 | % 到達で追加アラート通知(集計遅延・誤差対策) | [RULE-013](../01_requirements/01_business_requirement/08_rule.md#RULE-013) | 定数(課金ロジック) |
| 質問数 アラート閾値 | 25 / 50 / 80 / 90 / 100 | %(複数選択可・当月初回到達時通知) | [RULE-014](../01_requirements/01_business_requirement/08_rule.md#RULE-014) | [`M_PRJ_QUOTA_LIMITS`](02_backend/04_database/TBL-009.md#TBL-009) `alert_thresholds`(JSON 配列) |
| FAQ 件数 警告しきい値 | 8,000 | 件 / プロジェクト | [RULE-010](../01_requirements/01_business_requirement/08_rule.md#RULE-010) | 定数(入力ガード) |
| FAQ 件数 強制拒否しきい値 | 12,000 | 件 / プロジェクト | [RULE-010](../01_requirements/01_business_requirement/08_rule.md#RULE-010) | 定数(入力ガード) |
| FAQ 件数 運用想定上限 | 10,000 | 件 / プロジェクト(負荷想定。利用は制限しない) | [RULE-010](../01_requirements/01_business_requirement/08_rule.md#RULE-010) / [NFR-068](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-068) | — |
| 利用量サマリ反映遅延 | 5 | 分以内 | [課金・請求設計書](05_billing-design.md) | [`T_USAGE_METER`](02_backend/04_database/TBL-020.md#TBL-020) |
| 質問数上限 入力ガード(最小/最大) | KV 値 | 件(上限設定の入力検証) | [課金・請求設計書](05_billing-design.md) | KV `usage-limit:min` / `usage-limit:max` |
| ダッシュボード期間切替 | 30 | 日(当月との切替表示) | [API-062](02_backend/03_apis/API-062.md#API-062) / [SCR-033](01_frontend/01_screens/SCR-033.md#SCR-033) | 定数(ダッシュボード集計) |
| 日次トレンド表示期間 | 14 | 日 | [API-040](02_backend/03_apis/API-040.md#API-040) | 定数(ダッシュボード表示) |
| ウィジェット許可ドメイン件数上限 | 20 | 件/プロジェクト | 設計判断(入力ガード) | 定数(入力ガード) |

> [!NOTE]
> **上限なしの対象** プロジェクト数・メンバー数・FAQ 件数は受付停止の対象とする上限値を持たない(プロジェクト数・メンバー数の目安は §5 を参照)。FAQ 件数は無料枠超過後も受付を止めず従量課金を継続する。

## <span id="3-タイムアウトセッション認証"></span>3. タイムアウト・セッション・認証

セッション・認証・推論に関わる時間しきい値を集約する。判定ロジックの正本は各 RULE。

| 項目 | 値 | 単位/条件 | 根拠 | 格納先 |
|----|----|----|----|----|
| ログイン失敗ロックアウト しきい値 | 5 | 回連続失敗でロック | [RULE-001](../01_requirements/01_business_requirement/08_rule.md#RULE-001) | 定数(認証ロジック) |
| ログイン失敗ロックアウト 時間 | 15 | 分(時間経過 / 運営解除で復旧) | [RULE-001](../01_requirements/01_business_requirement/08_rule.md#RULE-001) | 定数(認証ロジック) |
| 再認証の有効範囲 | 当該操作 1 回 / 15 分以内 | 重要操作の再認証有効範囲 | [RULE-002](../01_requirements/01_business_requirement/08_rule.md#RULE-002) | [`T_ACCESS_TOKENS`](02_backend/04_database/TBL-014.md#TBL-014)(`purpose='reauth'`) |
| 無操作タイムアウト | 30 | 分(無操作でセッション失効) | [RULE-004](../01_requirements/01_business_requirement/08_rule.md#RULE-004) | 定数(セッション管理) |
| 絶対タイムアウト | 12 | 時間(ログインから。1 営業日内に再認証) | [RULE-005](../01_requirements/01_business_requirement/08_rule.md#RULE-005) | 定数(セッション管理) |
| AI 推論タイムアウト | 8 | 秒(超過時は処理エラーとして打ち切り) | [RULE-020](../01_requirements/01_business_requirement/08_rule.md#RULE-020) | 定数(推論呼び出し) |
| 規約改定予告 | 30 | 日前に対象者へ通知 | [FR-010](../01_requirements/02_functional_requirement/01_account-fr.md#FR-010) | 定数(通知スケジュール) |
| 規約再同意期限 | 14 | 日(発効日から) | [FR-010](../01_requirements/02_functional_requirement/01_account-fr.md#FR-010) | 定数(規約同意ゲート) |
| 通知再送回数上限 | 3 | 回 | [NFR-039](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-039) | 定数(メール再送制御) |
| 通知再送バックオフ | 5 分 / 30 分 / 2 時間 | 失敗後の次回再送間隔 | [NFR-039](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-039) | 定数(メール再送制御) |
| お知らせ集約時間窓 | 60 | 分(同一プロジェクト・同一イベント種別の連続発火を 1 件へ集約) | [FR-160](../01_requirements/02_functional_requirement/05_notification-fr.md#FR-160) | 定数(受信箱お知らせ集約) |

## <span id="4-データ保持期間削除猶予"></span>4. データ保持期間・削除猶予

退会・論理削除・各種有効期限の保持・猶予値を集約する。

| 項目 | 値 | 単位/条件 | 根拠 | 格納先 |
|----|----|----|----|----|
| アカウント論理削除の猶予 | 90 | 日(最後の有効割当解除後に完全消去) | [RULE-008](../01_requirements/01_business_requirement/08_rule.md#RULE-008) / [NFR-048](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-048) | 定数(削除バッチ) |
| 退会後 請求関連データ保持 | 7 | 年(電帳法・国税法準拠。退会時刻起点) | [RULE-022](../01_requirements/01_business_requirement/08_rule.md#RULE-022) / [NFR-047](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-047) | [`M_BILLING_ACCOUNT`](02_backend/04_database/TBL-002.md#TBL-002) ほか請求データ |
| 退会後 運用データ削除 | 速やかに(猶予 0 日) | 退会成立と同時 | [RULE-022](../01_requirements/01_business_requirement/08_rule.md#RULE-022) / [NFR-047](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-047) | — |
| 招待リンク有効期限 | 7 | 日(期限切れ後は再送で新リンク) | [RULE-007](../01_requirements/01_business_requirement/08_rule.md#RULE-007) | 定数(招待トークン) |
| プロジェクト連絡先確認メール有効期限 | 24 | 時間 | [RULE-009](../01_requirements/01_business_requirement/08_rule.md#RULE-009) | 定数(確認トークン) |
| アカウントメール確認リンク有効期限 | 24 | 時間 | 設計判断(認証トークン管理) | 定数(メール確認トークン) |
| パスワード再設定リンク有効期限 | 1 | 時間 | [RULE-003](../01_requirements/01_business_requirement/08_rule.md#RULE-003) | 定数(パスワード再設定トークン) |
| 公開キーローテーション猶予 | 24 | 時間(旧キーの失効猶予。超過後は [SYS-032](02_backend/01_system/SYS-032.md#SYS-032) が物理削除) | [RULE-018](../01_requirements/01_business_requirement/08_rule.md#RULE-018) | 定数(公開キー管理) |
| 課金通知の受信履歴保持 | 30 | 日(直近の受信履歴) | [RULE-017](../01_requirements/01_business_requirement/08_rule.md#RULE-017) | 定数(Webhook 受信履歴) |
| 決済失敗の猶予 | 7 | 日(失敗確定通知受信時刻起点。経過でサスペンション) | [RULE-016](../01_requirements/01_business_requirement/08_rule.md#RULE-016) / [課金・請求設計書](05_billing-design.md) | [TBL-018](02_backend/04_database/TBL-018.md#TBL-018) `grace_started_at` |
| プロジェクト識別子の再利用 | 不可 | 物理削除完了後 | [NFR-051](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-051) | トムストーン保持 |
| 冪等性キー保持 | 24 | 時間 | [ERR-032](05_errors/ERR-032.md#ERR-032) | 定数(API冪等性管理) |
| 請求明細PDFダウンロード有効期限 | 30 | 日 | [MSG-007](06_messages/MSG-007.md#MSG-007) | 定数(請求ファイルURL発行) |
| 質問ログ・未解決質問の保持期間 | 1 | 年 | [NFR-045](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-045) | 定数(保持期間バッチ) |
| 通知ログ・お知らせ受信箱の保持期間 | 1 | 年 | [NFR-049](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-049) | 定数(保持期間バッチ) |
| 監査ログ(一般)の保持期間 | 1 | 年 | 設計判断(運用確認対象) | 定数(保持期間バッチ) |
| 監査ログ(課金)の保持期間 | 7 | 年 | [NFR-047](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-047) / [RULE-022](../01_requirements/01_business_requirement/08_rule.md#RULE-022) | 定数(保持期間バッチ) |
| 監査ログ整合性検証の実施頻度 | 日次 | 1 回/日 | [NFR-015](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-015) | 定数(監査整合性検証バッチ) |

## <span id="5-レート制限キャパシティ目安"></span>5. レート制限・キャパシティ目安

レート制限はオーナー単位で適用し、オーナー・機能種別の組合せで上書きできる。下表の初期既定値は提案値で、キャパシティ目安は負荷想定であり利用を制限する上限ではない。

| 項目 | 値 | 単位/条件 | 根拠 | 格納先 |
|----|----|----|----|----|
| 認証系レート(初期既定) | 10 | req/min(1 IP / アカウント) | [NFR-017](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-017) | 定数 / [`M_OWNER_QUOTA_OVR`](02_backend/04_database/TBL-008.md#TBL-008)(上書き) |
| ウィジェット質問送信レート(初期既定) | 30 | req/min(1 ウィジェットセッション) | [NFR-017](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-017) | 定数 / [`M_OWNER_QUOTA_OVR`](02_backend/04_database/TBL-008.md#TBL-008)(`widget_ask_per_min` 上書き) |
| 一般管理 API レート(初期既定) | 120 | req/min(1 セッション) | [NFR-017](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-017) | 定数 / [`M_OWNER_QUOTA_OVR`](02_backend/04_database/TBL-008.md#TBL-008)(`admin_api_per_min` 上書き) |
| 同時アクティブプロジェクト数 目安 | 200 | 件(負荷想定。上限ではない) | [NFR-067](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-067) | — |
| 1 アカウントあたりプロジェクト数 目安 | 50 | 件(負荷想定。上限ではない・超過しても制限しない) | [NFR-070](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-070) | — |
| 1 アカウントあたりメンバー数 目安 | 100 | 名(負荷想定。上限ではない・超過しても制限しない) | [NFR-070](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-070) | — |
| 1 プロジェクトあたり質問ログ件数 想定上限 | 100 万 | 件 / 月(負荷想定) | [NFR-069](../01_requirements/03_non_functional_requirement/07_nfr.md#NFR-069) | — |

> [!IMPORTANT]
> **目安は上限ではない** プロジェクト数・メンバー数・同時アクティブプロジェクト数・質問ログ件数はキャパシティ設計上の負荷想定であり、超過しても利用を制限しない(プロジェクト数・メンバー数の急増検知や上限は持たない)。レート制限の既定値はオーナー・機能種別ごとに [`M_OWNER_QUOTA_OVR`](02_backend/04_database/TBL-008.md#TBL-008) で上書きできる。

## <span id="6-個人情報piiマスキング"></span>6. 個人情報(PII)マスキング

AI 回答生成後、ウィジェット利用者へ回答を出力する前に、回答文に含まれる個人情報(PII)を検出し、種別ラベル付きの伏字へ置換して出力する。MVP の対象種別・マスキング形式・契機を集約する。氏名・住所は MVP 対象外で、将来対応 [FUT-07](../04_future/FUT-07.md#FUT-07) で扱う。

| 項目 | 値 | 単位/条件 | 根拠 | 格納先 |
|----|----|----|----|----|
| 検出対象種別(MVP) | メールアドレス / 電話番号 / クレジットカード番号 | 回答文中の該当箇所を検出 | [RULE-024](../01_requirements/01_business_requirement/08_rule.md#RULE-024) | 定数(マスキング処理) |
| マスキング形式 | 種別ラベル付き伏字([メールアドレス] / [電話番号] / [カード番号]) | 検出箇所を種別ラベルの伏字へ置換 | [RULE-024](../01_requirements/01_business_requirement/08_rule.md#RULE-024) | 定数(マスキング処理) |
| 実施契機 | 回答出力前 | AI 回答生成後・応答整形前(AnswerProvider の外=上位) | [RULE-024](../01_requirements/01_business_requirement/08_rule.md#RULE-024) | 定数(マスキング処理) |
| MVP 対象外種別 | 氏名 / 住所 | 将来対応で AI 判定により高度化 | [FUT-07](../04_future/FUT-07.md#FUT-07) | — |

## <span id="7-バッチ運用設計値"></span>7. バッチ・運用設計値

バッチ・非同期処理・監視処理の再試行回数・監視間隔・チャンクサイズ・Cron スケジュールを集約する。個々のジョブ仕様は対応する SYS を参照する。

| 項目 | 値 | 単位/条件 | 根拠 | 格納先 |
|----|----|----|----|----|
| 課金 Webhook 再処理 上限回数 | 5 | 回 | 設計判断(運用確認対象) | [`T_BILLING_WEBHOOK_LOG`](02_backend/04_database/TBL-032.md#TBL-032) `retry_count` |
| 課金 Webhook 再処理 周期 | 15 | 分 | 設計判断(運用確認対象) | 定数(再処理バッチ) |
| FAQ 取込ジョブ 滞留監視間隔 | 5 | 分 | 設計判断(運用確認対象) | 定数(監視バッチ) |
| FAQ 取込ジョブ 滞留判定しきい値 | 30 | 分(最終進捗更新からの経過) | 設計判断(運用確認対象) | 定数(監視バッチ) |
| FAQ 取込ジョブ 進捗記録間隔 | 50 | 行ごと | 設計判断(運用確認対象) | 定数(取込ジョブ) |
| FAQ 取込ジョブ 想定処理時間 | 1,000 件 / 10 分以内 | 目安値(非 SLA) | 設計判断(運用確認対象) | — |
| 保持期間バッチ 走査チャンクサイズ | 500 | 件 / 実行 | 設計判断(運用確認対象) | 定数(保持期間バッチ) |
| 保持期間バッチ 起動あたり最大チャンク数 | 20 | チャンク / 起動 | 設計判断(運用確認対象) | 定数(保持期間バッチ) |
| 保持期間バッチ カーソル永続化 | チャンク完了ごと | 再開可能(中断時は次回起動時にカーソルから再開) | 設計判断(運用確認対象) | 定数(保持期間バッチ) |
| 保持期間バッチ 長時間ジョブ保護待機ポーリング間隔 | 5 | 分 | 設計判断(運用確認対象) | 定数(保持期間バッチ) |
| 保持期間バッチ 長時間ジョブ保護待機上限 | 60 | 分 | 設計判断(運用確認対象) | 定数(保持期間バッチ) |
| 通知送信抑制しきい値 バウンス率 | 5 | %超(直近 24 時間ローリング) | 設計判断(ESP 慣行) | 定数(通知送信抑制) |
| 通知送信抑制しきい値 苦情率 | 0.3 | %超(直近 24 時間ローリング) | 設計判断(ESP 慣行) | 定数(通知送信抑制) |
| 通知送信抑制しきい値 評価対象下限件数 | 50 | 件(直近 24 時間の送信件数がこれ未満の場合は評価対象外) | 設計判断(ESP 慣行) | 定数(通知送信抑制) |
| 通知送信抑制しきい値 評価窓 | 直近 24 時間 | ローリングウィンドウ | 設計判断(ESP 慣行) | 定数(通知送信抑制) |
| 通知送信抑制解除しきい値 バウンス率 | 2 | %未満(直近 24 時間ローリング) | 設計判断(運用確認対象) | 定数(通知送信抑制) |
| 通知送信抑制解除しきい値 苦情率 | 0.1 | %未満(直近 24 時間ローリング) | 設計判断(運用確認対象) | 定数(通知送信抑制) |
| 通知送信抑制解除しきい値 評価窓 | 直近 24 時間 | ローリングウィンドウ | 設計判断(運用確認対象) | 定数(通知送信抑制) |
| 通知送信抑制解除しきい値 連続下回り回数 | 2 | 回連続で解除しきい値内 | 設計判断(運用確認対象) | 定数(通知送信抑制) |
| Cron スケジュール SYS-032 | 0 17 * * *(UTC、JST 02:00) | 削除系(032→027→034 の順序保証・先頭) | 設計判断(運用確認対象) | 定数(Cron 設定) |
| Cron スケジュール SYS-027 | 30 17 * * *(UTC、JST 02:30) | 削除系(032→027→034 の順序保証・中間) | 設計判断(運用確認対象) | 定数(Cron 設定) |
| Cron スケジュール SYS-034 | 0 18 * * *(UTC、JST 03:00) | 削除系(032→027→034 の順序保証・最終) | 設計判断(運用確認対象) | 定数(Cron 設定) |
| Cron スケジュール SYS-031 | 0 19 * * *(UTC、JST 04:00) | 日次バッチ | 設計判断(運用確認対象) | 定数(Cron 設定) |
| Cron スケジュール SYS-025 | */15 * * * *(UTC) | 15 分ごと | 設計判断(運用確認対象) | 定数(Cron 設定) |
| Cron スケジュール SYS-019 | 0 18 1 * *(UTC、JST 毎月 1 日 03:00) | 月次バッチ | 設計判断(運用確認対象) | 定数(Cron 設定) |
| Cron スケジュール SYS-007 | 通知送信時 + 0,30 * * * *(UTC) | 通知送信契機 + 毎時 0 分・30 分 | 設計判断(運用確認対象) | 定数(Cron 設定) |
