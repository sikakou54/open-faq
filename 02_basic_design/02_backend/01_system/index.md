# システム設計書

> **メインシステムの全システム処理(`SYS-001`〜`SYS-034`)を一覧する独立設計書です。** 無人で動く処理(バッチ / Webhook / 非同期 / 監視 / 通知)を、画面設計の backend 版として 1 処理 = 1 ファイルで管理します。各処理の業務ユースケースIDを起点に、API・テーブル・シーケンスとの厳密な対応は [トレーサビリティ一覧](../../00_traceability/index.md) で一元管理します。

*版数 v1.1 ・ 更新 2026-06-25 ・ システム処理 34 ・ ステータス ドラフト*

## 一覧

| システムID | 処理名 | 種別 | トリガー | 業務ユースケースID |
|---|---|---|---|---|
| <span id="SYS-001"></span>[`SYS-001`](SYS-001.md#SYS-001) | 参照FAQ記録・提示 | async | ウィジェット質問への AI 回答生成時 | [UC-048](../../../01_requirements/04_business_usecases/UC-048.md#UC-048) |
| <span id="SYS-002"></span>[`SYS-002`](SYS-002.md#SYS-002) | 回答不可時の未解決質問登録・案内処理 | async | FAQ ベースで回答不可と判定された時 | [UC-049](../../../01_requirements/04_business_usecases/UC-049.md#UC-049) |
| <span id="SYS-003"></span>[`SYS-003`](SYS-003.md#SYS-003) | 未解決質問の記録 | async | 未解決質問の登録時 | [UC-050](../../../01_requirements/04_business_usecases/UC-050.md#UC-050) |
| <span id="SYS-004"></span>[`SYS-004`](SYS-004.md#SYS-004) | 課金プロバイダ通知の受信・検証・取込 | webhook | 課金プロバイダからの HTTP 通知受信時 | [UC-056](../../../01_requirements/04_business_usecases/UC-056.md#UC-056) |
| <span id="SYS-005"></span>[`SYS-005`](SYS-005.md#SYS-005) | 許可ドメイン照合によるウィジェット起動可否判定 | guard | ウィジェットのロード・起動時 | [UC-057](../../../01_requirements/04_business_usecases/UC-057.md#UC-057) |
| <span id="SYS-006"></span>[`SYS-006`](SYS-006.md#SYS-006) | アカウント認証関連通知のオプトアウト不可送信 | notify | 認証関連イベント(メール確認・パスワード再設定・ロックアウト等)の発生時 | [UC-064](../../../01_requirements/04_business_usecases/UC-064.md#UC-064) |
| <span id="SYS-007"></span>[`SYS-007`](SYS-007.md#SYS-007) | 送信品質監視による通知送信抑制 | monitor | 通知送信時 + 定期の品質監視 | [UC-065](../../../01_requirements/04_business_usecases/UC-065.md#UC-065) |
| <span id="SYS-008"></span>[`SYS-008`](SYS-008.md#SYS-008) | オーナー単位レート制限の適用 | guard | 機能リクエスト受信時(全 API 横断・ゲートウェイ層) | [UC-071](../../../01_requirements/04_business_usecases/UC-071.md#UC-071) |
| <span id="SYS-009"></span>[`SYS-009`](SYS-009.md#SYS-009) | 外部露出箇所の入力サニタイズ | guard | ウィジェット利用者の入力を含む通知の生成時 | [UC-072](../../../01_requirements/04_business_usecases/UC-072.md#UC-072) |
| <span id="SYS-010"></span>[`SYS-010`](SYS-010.md#SYS-010) | プロジェクト削除に伴うメンバー割当解除 | cascade | プロジェクト削除の確定時 | [UC-073](../../../01_requirements/04_business_usecases/UC-073.md#UC-073) |
| <span id="SYS-011"></span>[`SYS-011`](SYS-011.md#SYS-011) | お知らせ閲覧範囲のアカウント利用者限定 | guard | お知らせ表示のアクセス時 | [UC-078](../../../01_requirements/04_business_usecases/UC-078.md#UC-078) |
| <span id="SYS-012"></span>[`SYS-012`](SYS-012.md#SYS-012) | お知らせ受信箱の利用者別保持と退会時削除 | cascade | お知らせ受信時 + 退会/無効化の確定時 | [UC-079](../../../01_requirements/04_business_usecases/UC-079.md#UC-079) |
| <span id="SYS-013"></span>[`SYS-013`](SYS-013.md#SYS-013) | 管理ダッシュボード遷移時の未読お知らせ件数取得・更新 | async | 管理ダッシュボードへの遷移時 + 定期間隔 | [UC-080](../../../01_requirements/04_business_usecases/UC-080.md#UC-080) |
| <span id="SYS-014"></span>[`SYS-014`](SYS-014.md#SYS-014) | FAQ一括取り込みジョブ非同期実行 | async | FAQ 一括取り込み依頼の受付による取り込みジョブ起動 | [UC-046](../../../01_requirements/04_business_usecases/UC-046.md#UC-046) |
| <span id="SYS-015"></span>[`SYS-015`](SYS-015.md#SYS-015) | AIしきい値変更の伝播・フォールバック | cascade | 回答可否しきい値の変更検知 / 質問に伴う推論処理の発生 | [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) |
| <span id="SYS-016"></span>[`SYS-016`](SYS-016.md#SYS-016) | 利用量リアルタイム集計・サマリ反映 | async | ウィジェットへの質問がプロジェクトに到達した時 | [UC-051](../../../01_requirements/04_business_usecases/UC-051.md#UC-051) |
| <span id="SYS-017"></span>[`SYS-017`](SYS-017.md#SYS-017) | 質問数上限アラート通知 | async | 当月質問数が設定済みアラート閾値へ到達したことを検知したとき | [UC-052](../../../01_requirements/04_business_usecases/UC-052.md#UC-052) |
| <span id="SYS-018"></span>[`SYS-018`](SYS-018.md#SYS-018) | 上限到達ウィジェット受付停止 | monitor | ウィジェット利用者の質問送信を受け付けたとき(同期判定) | [UC-053](../../../01_requirements/04_business_usecases/UC-053.md#UC-053) |
| <span id="SYS-019"></span>[`SYS-019`](SYS-019.md#SYS-019) | 月次請求確定 | batch | 月初に前月分を対象として定期起動 | [UC-054](../../../01_requirements/04_business_usecases/UC-054.md#UC-054) |
| <span id="SYS-020"></span>[`SYS-020`](SYS-020.md#SYS-020) | 決済失敗猶予・サスペンション移行 | monitor | 決済失敗確定 / 再決済成功 / 解除の通知受信、および猶予経過を判定する定期起動 | [UC-055](../../../01_requirements/04_business_usecases/UC-055.md#UC-055) |
| <span id="SYS-021"></span>[`SYS-021`](SYS-021.md#SYS-021) | メール配信状態Webhook処理 | async | メール配信事業者から配信結果の通知を受信したとき | [UC-058](../../../01_requirements/04_business_usecases/UC-058.md#UC-058) |
| <span id="SYS-022"></span>[`SYS-022`](SYS-022.md#SYS-022) | 運営お知らせ配信 | batch | 配信予定日時の到来 / 運営による即時配信の指示 | [UC-059](../../../01_requirements/04_business_usecases/UC-059.md#UC-059) |
| <span id="SYS-023"></span>[`SYS-023`](SYS-023.md#SYS-023) | 運用イベントのシステム通知自動生成 | async | 運用イベント(利用上限接近・到達・通知失敗急増・サスペンション・復元・規約改定・価格改定 等)の発生時 | [UC-060](../../../01_requirements/04_business_usecases/UC-060.md#UC-060) |
| <span id="SYS-024"></span>[`SYS-024`](SYS-024.md#SYS-024) | メンバー割当変更通知 | async | メンバーのプロジェクト別役割割当の追加 / 変更 / 剥奪を契機に起動 | [UC-061](../../../01_requirements/04_business_usecases/UC-061.md#UC-061) |
| <span id="SYS-025"></span>[`SYS-025`](SYS-025.md#SYS-025) | 配信失敗通知の再送 | batch | 定期起動の再送処理(失敗分の検出) | [UC-062](../../../01_requirements/04_business_usecases/UC-062.md#UC-062) |
| <span id="SYS-026"></span>[`SYS-026`](SYS-026.md#SYS-026) | 受信箱お知らせ重複集約 | async | 受信箱お知らせの生成要求(プロジェクト / イベント種別)発生時 | [UC-063](../../../01_requirements/04_business_usecases/UC-063.md#UC-063) |
| <span id="SYS-027"></span>[`SYS-027`](SYS-027.md#SYS-027) | 退会済みアカウント・論理削除データの物理削除 | batch | 日次の実行スケジュールによる自動起動 | [UC-066](../../../01_requirements/04_business_usecases/UC-066.md#UC-066) |
| <span id="SYS-028"></span>[`SYS-028`](SYS-028.md#SYS-028) | セッション失効判定・再認証誘導 | monitor | アカウント利用者の操作リクエスト受付時 / 経過時間の上限を評価する定期的なタイミング | [UC-067](../../../01_requirements/04_business_usecases/UC-067.md#UC-067) |
| <span id="SYS-029"></span>[`SYS-029`](SYS-029.md#SYS-029) | ログイン失敗ロックアウト・解除 | monitor | ログイン試行の失敗 / ロック期間の経過判定スケジュール / 権限者による手動解除 | [UC-068](../../../01_requirements/04_business_usecases/UC-068.md#UC-068) |
| <span id="SYS-030"></span>[`SYS-030`](SYS-030.md#SYS-030) | アカウント停止時セッション一斉無効化 | cascade | 対象アカウントが停止(手動停止 / 規約違反停止)状態へ遷移した時 | [UC-069](../../../01_requirements/04_business_usecases/UC-069.md#UC-069) |
| <span id="SYS-031"></span>[`SYS-031`](SYS-031.md#SYS-031) | 監査ログ整合性検証(日次) | batch | 日次の定期処理(1 日 1 回・スケジューラ起動) | [UC-070](../../../01_requirements/04_business_usecases/UC-070.md#UC-070) |
| <span id="SYS-032"></span>[`SYS-032`](SYS-032.md#SYS-032) | 保持期間超過データの自動削除 | batch | 日次の定期処理 | [UC-066](../../../01_requirements/04_business_usecases/UC-066.md#UC-066) |
| <span id="SYS-033"></span>[`SYS-033`](SYS-033.md#SYS-033) | 課金通知 取込失敗の再処理 | batch | 定期スケジュール | [UC-056](../../../01_requirements/04_business_usecases/UC-056.md#UC-056) |
| <span id="SYS-034"></span>[`SYS-034`](SYS-034.md#SYS-034) | 保持期間経過アカウントの物理削除 | batch | 日次の実行スケジュールによる自動起動 | [UC-066](../../../01_requirements/04_business_usecases/UC-066.md#UC-066) |
