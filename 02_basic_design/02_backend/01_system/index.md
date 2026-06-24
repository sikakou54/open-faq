# システム設計書

> **メインシステムの全システム処理(`SYS-001`〜`SYS-035`)を一覧する独立設計書です。** 無人で動く処理(バッチ / Webhook / 非同期 / 監視 / 通知)を、画面設計の backend 版として 1 処理 = 1 ファイルで管理します。各処理のトレーサビリティID(TR)から関連する業務UC・API・テーブル・[シーケンス](../../03_sequences/index.md)を [トレーサビリティ一覧](../../00_traceability/index.md) で辿れます。

*版数 v1.0 ・ 更新 2026-06-23 ・ システム処理 35 ・ ステータス ドラフト*

## 一覧

| システムID | 処理名 | 種別 | トリガー | トレーサビリティID |
|---|---|---|---|---|
| <span id="SYS-001"></span>[`SYS-001`](SYS-001.md#SYS-001) | メンバー数の上限接近・急増の検知と通知 | monitor | メンバー数の変動時 + 定期集計(日次) | [TR-048](../../00_traceability/index.md#TR-048) |
| <span id="SYS-002"></span>[`SYS-002`](SYS-002.md#SYS-002) | プロジェクト数急増検知通知 | monitor | プロジェクト作成時 + 定期監視 | [TR-049](../../00_traceability/index.md#TR-049) |
| <span id="SYS-003"></span>[`SYS-003`](SYS-003.md#SYS-003) | 参照FAQ記録・提示 | async | ウィジェット質問への AI 回答生成時 | [TR-052](../../00_traceability/index.md#TR-052) |
| <span id="SYS-004"></span>[`SYS-004`](SYS-004.md#SYS-004) | 回答不可時の未解決質問登録・案内処理 | async | FAQ ベースで回答不可と判定された時 | [TR-053](../../00_traceability/index.md#TR-053) |
| <span id="SYS-005"></span>[`SYS-005`](SYS-005.md#SYS-005) | 未解決質問の記録 | async | 未解決質問の登録時 | [TR-054](../../00_traceability/index.md#TR-054) |
| <span id="SYS-006"></span>[`SYS-006`](SYS-006.md#SYS-006) | 課金プロバイダ通知の受信・検証・取込 | webhook | 課金プロバイダからの HTTP 通知受信時 | [TR-060](../../00_traceability/index.md#TR-060) |
| <span id="SYS-007"></span>[`SYS-007`](SYS-007.md#SYS-007) | 許可ドメイン照合によるウィジェット起動可否判定 | guard | ウィジェットのロード・起動時 | [TR-061](../../00_traceability/index.md#TR-061) |
| <span id="SYS-008"></span>[`SYS-008`](SYS-008.md#SYS-008) | アカウント認証関連通知のオプトアウト不可送信 | notify | 認証関連イベント(メール確認・パスワード再設定・ロックアウト等)の発生時 | [TR-068](../../00_traceability/index.md#TR-068) |
| <span id="SYS-009"></span>[`SYS-009`](SYS-009.md#SYS-009) | 送信品質監視による通知送信抑制 | monitor | 通知送信時 + 定期の品質監視 | [TR-069](../../00_traceability/index.md#TR-069) |
| <span id="SYS-010"></span>[`SYS-010`](SYS-010.md#SYS-010) | 契約単位レート制限の適用 | guard | 機能リクエスト受信時(全 API 横断・ゲートウェイ層) | [TR-075](../../00_traceability/index.md#TR-075) |
| <span id="SYS-011"></span>[`SYS-011`](SYS-011.md#SYS-011) | 外部露出箇所の入力サニタイズ | guard | ウィジェット利用者の入力を含む通知の生成時 | [TR-076](../../00_traceability/index.md#TR-076) |
| <span id="SYS-012"></span>[`SYS-012`](SYS-012.md#SYS-012) | プロジェクト削除に伴うメンバー割当解除 | cascade | プロジェクト削除の確定時 | [TR-077](../../00_traceability/index.md#TR-077) |
| <span id="SYS-013"></span>[`SYS-013`](SYS-013.md#SYS-013) | お知らせ閲覧範囲のアカウント利用者限定 | guard | お知らせ表示のアクセス時 | [TR-084](../../00_traceability/index.md#TR-084) |
| <span id="SYS-014"></span>[`SYS-014`](SYS-014.md#SYS-014) | お知らせ受信箱の利用者別保持と退会時削除 | cascade | お知らせ受信時 + 退会/無効化の確定時 | [TR-085](../../00_traceability/index.md#TR-085) |
| <span id="SYS-015"></span>[`SYS-015`](SYS-015.md#SYS-015) | 管理ダッシュボード遷移時の未読お知らせ件数取得・更新 | async | 管理ダッシュボードへの遷移時 + 定期間隔 | [TR-086](../../00_traceability/index.md#TR-086) |
| <span id="SYS-016"></span>[`SYS-016`](SYS-016.md#SYS-016) | FAQ一括取り込みジョブ非同期実行 | async | FAQ 一括取り込み依頼の受付による取り込みジョブ起動 | [TR-050](../../00_traceability/index.md#TR-050) |
| <span id="SYS-017"></span>[`SYS-017`](SYS-017.md#SYS-017) | AIしきい値変更の伝播・フォールバック | cascade | 回答可否しきい値の変更検知 / 質問に伴う推論処理の発生 | [TR-051](../../00_traceability/index.md#TR-051) |
| <span id="SYS-018"></span>[`SYS-018`](SYS-018.md#SYS-018) | 利用量リアルタイム集計・サマリ反映 | async | ウィジェットへの質問がプロジェクトに到達した時 | [TR-055](../../00_traceability/index.md#TR-055) |
| <span id="SYS-019"></span>[`SYS-019`](SYS-019.md#SYS-019) | 質問数上限アラート通知 | async | 当月質問数が設定済みアラート閾値へ到達したことを検知したとき | [TR-056](../../00_traceability/index.md#TR-056) |
| <span id="SYS-020"></span>[`SYS-020`](SYS-020.md#SYS-020) | 上限到達ウィジェット受付停止 | monitor | ウィジェット利用者の質問送信を受け付けたとき(同期判定) | [TR-057](../../00_traceability/index.md#TR-057) |
| <span id="SYS-021"></span>[`SYS-021`](SYS-021.md#SYS-021) | 月次請求確定 | batch | 月初に前月分を対象として定期起動 | [TR-058](../../00_traceability/index.md#TR-058) |
| <span id="SYS-022"></span>[`SYS-022`](SYS-022.md#SYS-022) | 決済失敗猶予・サスペンション移行 | monitor | 決済失敗確定 / 再決済成功 / 解除の通知受信、および猶予経過を判定する定期起動 | [TR-059](../../00_traceability/index.md#TR-059) |
| <span id="SYS-023"></span>[`SYS-023`](SYS-023.md#SYS-023) | メール配信状態Webhook処理 | async | メール配信事業者から配信結果の通知を受信したとき | [TR-062](../../00_traceability/index.md#TR-062) |
| <span id="SYS-024"></span>[`SYS-024`](SYS-024.md#SYS-024) | 運営お知らせ配信 | batch | 配信予定日時の到来 / 運営による即時配信の指示 | [TR-063](../../00_traceability/index.md#TR-063) |
| <span id="SYS-025"></span>[`SYS-025`](SYS-025.md#SYS-025) | 運用イベントのシステム通知自動生成 | async | 運用イベント(利用上限接近・到達・通知失敗急増・サスペンション・復元・規約改定・価格改定 等)の発生時 | [TR-064](../../00_traceability/index.md#TR-064) |
| <span id="SYS-026"></span>[`SYS-026`](SYS-026.md#SYS-026) | メンバー割当変更通知 | async | メンバーのプロジェクト別役割割当の追加 / 変更 / 剥奪を契機に起動 | [TR-065](../../00_traceability/index.md#TR-065) |
| <span id="SYS-027"></span>[`SYS-027`](SYS-027.md#SYS-027) | 配信失敗通知の再送 | batch | 定期起動の再送処理(失敗分の検出) | [TR-066](../../00_traceability/index.md#TR-066) |
| <span id="SYS-028"></span>[`SYS-028`](SYS-028.md#SYS-028) | 受信箱お知らせ重複集約 | async | 受信箱お知らせの生成要求(契約 / イベント種別)発生時 | [TR-067](../../00_traceability/index.md#TR-067) |
| <span id="SYS-029"></span>[`SYS-029`](SYS-029.md#SYS-029) | 90日経過データ物理削除 | batch | 日次の実行スケジュールによる自動起動 | [TR-070](../../00_traceability/index.md#TR-070) |
| <span id="SYS-030"></span>[`SYS-030`](SYS-030.md#SYS-030) | セッション失効判定・再認証誘導 | monitor | アカウント利用者の操作リクエスト受付時 / 経過時間の上限を評価する定期的なタイミング | [TR-071](../../00_traceability/index.md#TR-071) |
| <span id="SYS-031"></span>[`SYS-031`](SYS-031.md#SYS-031) | ログイン失敗ロックアウト・解除 | monitor | ログイン試行の失敗 / ロック期間の経過判定スケジュール / 権限者による手動解除 | [TR-072](../../00_traceability/index.md#TR-072) |
| <span id="SYS-032"></span>[`SYS-032`](SYS-032.md#SYS-032) | 契約停止時セッション一斉無効化 | cascade | 対象契約が停止(手動停止 / 規約違反停止)状態へ遷移した時 | [TR-073](../../00_traceability/index.md#TR-073) |
| <span id="SYS-033"></span>[`SYS-033`](SYS-033.md#SYS-033) | 監査ログ整合性検証(日次) | batch | 日次の定期処理(1 日 1 回・スケジューラ起動) | [TR-074](../../00_traceability/index.md#TR-074) |
| <span id="SYS-034"></span>[`SYS-034`](SYS-034.md#SYS-034) | 保持期間超過データの自動論理削除 | batch | 日次の定期処理 | — |
| <span id="SYS-035"></span>[`SYS-035`](SYS-035.md#SYS-035) | 課金通知 取込失敗の再処理 | batch | 定期スケジュール | [TR-060](../../00_traceability/index.md#TR-060) |
