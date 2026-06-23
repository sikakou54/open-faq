<!-- portal-top -->
[設計ポータル](../../../README.md) ／ [基本設計](../../index.md) ／ [バックエンド設計](../index.md) ／ **システム設計**
<!-- /portal-top -->

# システム設計書

> **メインシステムの全システム処理(`SYS-001`〜`SYS-015`)を一覧する独立設計書です。** 無人で動く処理(バッチ / Webhook / 非同期 / 監視 / 通知)を、画面設計の backend 版として 1 処理 = 1 ファイルで管理します。各処理は対応する業務ユースケース・[システムイベント](../02_system_events/index.md)(`SEV-*`)・API・テーブル・[シーケンス](../../03_sequences/index.md)へトレースします。

*版数 v1.0 ・ 更新 2026-06-23 ・ システム処理 15 ・ ステータス ドラフト*

## 一覧

| システムID | 処理名 | 種別 | トリガー | 対応業務UC |
|---|---|---|---|---|
| <span id="SYS-001"></span>[`SYS-001`](SYS-001.md#SYS-001) | メンバー数の上限接近・急増の検知と通知 | monitor | メンバー数の変動時 + 定期集計(日次) | [UC-049](../../../01_requirements/04_business_usecases/UC-049.md#UC-049) |
| <span id="SYS-002"></span>[`SYS-002`](SYS-002.md#SYS-002) | プロジェクト数急増検知通知 | monitor | プロジェクト作成時 + 定期監視 | [UC-050](../../../01_requirements/04_business_usecases/UC-050.md#UC-050) |
| <span id="SYS-003"></span>[`SYS-003`](SYS-003.md#SYS-003) | 参照FAQ記録・提示 | async | ウィジェット質問への AI 回答生成時 | [UC-053](../../../01_requirements/04_business_usecases/UC-053.md#UC-053) |
| <span id="SYS-004"></span>[`SYS-004`](SYS-004.md#SYS-004) | 回答不可時の未解決質問登録・案内処理 | async | FAQ ベースで回答不可と判定された時 | [UC-054](../../../01_requirements/04_business_usecases/UC-054.md#UC-054) |
| <span id="SYS-005"></span>[`SYS-005`](SYS-005.md#SYS-005) | 未解決質問の記録 | async | 未解決質問の登録時 | [UC-055](../../../01_requirements/04_business_usecases/UC-055.md#UC-055) |
| <span id="SYS-006"></span>[`SYS-006`](SYS-006.md#SYS-006) | 課金プロバイダ通知の受信・検証・取込 | webhook | 課金プロバイダからの HTTP 通知受信時 | [UC-061](../../../01_requirements/04_business_usecases/UC-061.md#UC-061) |
| <span id="SYS-007"></span>[`SYS-007`](SYS-007.md#SYS-007) | 許可ドメイン照合によるウィジェット起動可否判定 | guard | ウィジェットのロード・起動時 | [UC-062](../../../01_requirements/04_business_usecases/UC-062.md#UC-062) |
| <span id="SYS-008"></span>[`SYS-008`](SYS-008.md#SYS-008) | アカウント認証関連通知のオプトアウト不可送信 | notify | 認証関連イベント(メール確認・パスワード再設定・ロックアウト等)の発生時 | [UC-069](../../../01_requirements/04_business_usecases/UC-069.md#UC-069) |
| <span id="SYS-009"></span>[`SYS-009`](SYS-009.md#SYS-009) | 送信品質監視による通知送信抑制 | monitor | 通知送信時 + 定期の品質監視 | [UC-070](../../../01_requirements/04_business_usecases/UC-070.md#UC-070) |
| <span id="SYS-010"></span>[`SYS-010`](SYS-010.md#SYS-010) | 契約単位レート制限の適用 | guard | 機能リクエスト受信時(全 API 横断・ゲートウェイ層) | [UC-076](../../../01_requirements/04_business_usecases/UC-076.md#UC-076) |
| <span id="SYS-011"></span>[`SYS-011`](SYS-011.md#SYS-011) | 外部露出箇所の入力サニタイズ | guard | ウィジェット利用者の入力を含む通知の生成時 | [UC-077](../../../01_requirements/04_business_usecases/UC-077.md#UC-077) |
| <span id="SYS-012"></span>[`SYS-012`](SYS-012.md#SYS-012) | プロジェクト削除に伴うメンバー割当解除 | cascade | プロジェクト削除の確定時 | [UC-079](../../../01_requirements/04_business_usecases/UC-079.md#UC-079) |
| <span id="SYS-013"></span>[`SYS-013`](SYS-013.md#SYS-013) | お知らせ閲覧範囲のアカウント利用者限定 | guard | お知らせ表示のアクセス時 | [UC-086](../../../01_requirements/04_business_usecases/UC-086.md#UC-086) |
| <span id="SYS-014"></span>[`SYS-014`](SYS-014.md#SYS-014) | お知らせ受信箱の利用者別保持と退会時削除 | cascade | お知らせ受信時 + 退会/無効化の確定時 | [UC-087](../../../01_requirements/04_business_usecases/UC-087.md#UC-087) |
| <span id="SYS-015"></span>[`SYS-015`](SYS-015.md#SYS-015) | 管理ダッシュボード遷移時の未読お知らせ件数取得・更新 | async | 管理ダッシュボードへの遷移時 + 定期間隔 | [UC-088](../../../01_requirements/04_business_usecases/UC-088.md#UC-088) |

---

<!-- portal-bottom -->
[← バックエンド設計](../index.md) ・ [基本設計](../../index.md) ・ [↑ 設計ポータル](../../../README.md)
<!-- /portal-bottom -->
