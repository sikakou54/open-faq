<!-- portal-top -->
[設計ポータル](../../../README.md) ／ [基本設計](../../index.md) ／ [バックエンド設計](../index.md) ／ **システムイベント設計**
<!-- /portal-top -->

# システムイベント設計書

> **全システムイベント(`SEV-001`〜`SEV-068`)を対応システム別に一覧します。** 各システムイベントは [システム設計](../01_system/index.md)(`SYS-*`)の 1 処理に属し、複数のイベントが 1 つの業務ユースケースを実現します(システムイベント → 業務UC は多:1)。処理内容の正本は各システム設計 §6 です。

*版数 v1.0 ・ 更新 2026-06-23 ・ システムイベント 68 ・ ステータス ドラフト*

## 一覧(システム別)

### <span id="SYS-001"></span>SYS-001 メンバー数の上限接近・急増の検知と通知

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-001`](SEV-001.md#SEV-001) | メンバー数集計・しきい値評価 | [UC-049](../../../01_requirements/04_business_usecases/UC-049.md#UC-049) |
| [`SEV-002`](SEV-002.md#SEV-002) | アラート通知生成・記録 | [UC-049](../../../01_requirements/04_business_usecases/UC-049.md#UC-049) |

### <span id="SYS-002"></span>SYS-002 プロジェクト数急増検知通知

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-003`](SEV-003.md#SEV-003) | プロジェクト数集計・急増判定 | [UC-050](../../../01_requirements/04_business_usecases/UC-050.md#UC-050) |
| [`SEV-004`](SEV-004.md#SEV-004) | オーナー通知 | [UC-050](../../../01_requirements/04_business_usecases/UC-050.md#UC-050) |

### <span id="SYS-003"></span>SYS-003 参照FAQ記録・提示

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-005`](SEV-005.md#SEV-005) | 参照FAQ記録 | [UC-053](../../../01_requirements/04_business_usecases/UC-053.md#UC-053) |
| [`SEV-006`](SEV-006.md#SEV-006) | 参照FAQ提示 | [UC-053](../../../01_requirements/04_business_usecases/UC-053.md#UC-053) |

### <span id="SYS-004"></span>SYS-004 回答不可時の未解決質問登録・案内処理

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-007`](SEV-007.md#SEV-007) | 未解決質問登録 | [UC-054](../../../01_requirements/04_business_usecases/UC-054.md#UC-054) |
| [`SEV-008`](SEV-008.md#SEV-008) | 回答不可案内 | [UC-054](../../../01_requirements/04_business_usecases/UC-054.md#UC-054) |

### <span id="SYS-005"></span>SYS-005 未解決質問の記録

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-009`](SEV-009.md#SEV-009) | 未解決質問の記録 | [UC-055](../../../01_requirements/04_business_usecases/UC-055.md#UC-055) |

### <span id="SYS-006"></span>SYS-006 課金プロバイダ通知の受信・検証・取込

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-010`](SEV-010.md#SEV-010) | 受信検証 | [UC-061](../../../01_requirements/04_business_usecases/UC-061.md#UC-061) |
| [`SEV-011`](SEV-011.md#SEV-011) | 取込完了 | [UC-061](../../../01_requirements/04_business_usecases/UC-061.md#UC-061) |
| [`SEV-012`](SEV-012.md#SEV-012) | 取込失敗 | [UC-061](../../../01_requirements/04_business_usecases/UC-061.md#UC-061) |

### <span id="SYS-007"></span>SYS-007 許可ドメイン照合によるウィジェット起動可否判定

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-013`](SEV-013.md#SEV-013) | 許可ドメイン照合 | [UC-062](../../../01_requirements/04_business_usecases/UC-062.md#UC-062) |
| [`SEV-014`](SEV-014.md#SEV-014) | 許可ドメイン上での起動 | [UC-062](../../../01_requirements/04_business_usecases/UC-062.md#UC-062) |

### <span id="SYS-008"></span>SYS-008 アカウント認証関連通知のオプトアウト不可送信

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-015`](SEV-015.md#SEV-015) | オプトアウト不可判定 | [UC-069](../../../01_requirements/04_business_usecases/UC-069.md#UC-069) |
| [`SEV-016`](SEV-016.md#SEV-016) | 認証関連通知の送信 | [UC-069](../../../01_requirements/04_business_usecases/UC-069.md#UC-069) |

### <span id="SYS-009"></span>SYS-009 送信品質監視による通知送信抑制

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-017`](SEV-017.md#SEV-017) | 送信品質の評価 | [UC-070](../../../01_requirements/04_business_usecases/UC-070.md#UC-070) |
| [`SEV-018`](SEV-018.md#SEV-018) | 通知送信の抑制 | [UC-070](../../../01_requirements/04_business_usecases/UC-070.md#UC-070) |

### <span id="SYS-010"></span>SYS-010 契約単位レート制限の適用

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-019`](SEV-019.md#SEV-019) | 契約単位レート制限の評価 | [UC-076](../../../01_requirements/04_business_usecases/UC-076.md#UC-076) |
| [`SEV-020`](SEV-020.md#SEV-020) | 上限超過リクエストの抑制 | [UC-076](../../../01_requirements/04_business_usecases/UC-076.md#UC-076) |

### <span id="SYS-011"></span>SYS-011 外部露出箇所の入力サニタイズ

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-021`](SEV-021.md#SEV-021) | 外部露出箇所のサニタイズ完了 | [UC-077](../../../01_requirements/04_business_usecases/UC-077.md#UC-077) |

### <span id="SYS-012"></span>SYS-012 プロジェクト削除に伴うメンバー割当解除

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-022`](SEV-022.md#SEV-022) | メンバー割当の一括解除 | [UC-079](../../../01_requirements/04_business_usecases/UC-079.md#UC-079) |
| [`SEV-023`](SEV-023.md#SEV-023) | 利用根拠を失ったメンバーの利用停止 | [UC-079](../../../01_requirements/04_business_usecases/UC-079.md#UC-079) |

### <span id="SYS-013"></span>SYS-013 お知らせ閲覧範囲のアカウント利用者限定

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-024`](SEV-024.md#SEV-024) | お知らせ閲覧範囲の本人限定 | [UC-086](../../../01_requirements/04_business_usecases/UC-086.md#UC-086) |

### <span id="SYS-014"></span>SYS-014 お知らせ受信箱の利用者別保持と退会時削除

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-025`](SEV-025.md#SEV-025) | お知らせ受信箱の利用者別保持 | [UC-087](../../../01_requirements/04_business_usecases/UC-087.md#UC-087) |
| [`SEV-026`](SEV-026.md#SEV-026) | 退会・無効化確定時の受信箱削除 | [UC-087](../../../01_requirements/04_business_usecases/UC-087.md#UC-087) |

### <span id="SYS-015"></span>SYS-015 管理ダッシュボード遷移時の未読お知らせ件数取得・更新

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-027`](SEV-027.md#SEV-027) | 遷移時の未読件数取得・反映 | [UC-088](../../../01_requirements/04_business_usecases/UC-088.md#UC-088) |
| [`SEV-028`](SEV-028.md#SEV-028) | 滞在中の定期的な未読件数最新化 | [UC-088](../../../01_requirements/04_business_usecases/UC-088.md#UC-088) |

### <span id="SYS-016"></span>SYS-016 FAQ一括取り込みジョブ非同期実行

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-029`](SEV-029.md#SEV-029) | 行単位取り込み | [UC-051](../../../01_requirements/04_business_usecases/UC-051.md#UC-051) |
| [`SEV-030`](SEV-030.md#SEV-030) | 完了通知 | [UC-051](../../../01_requirements/04_business_usecases/UC-051.md#UC-051) |

### <span id="SYS-017"></span>SYS-017 AIしきい値変更の伝播・フォールバック

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-031`](SEV-031.md#SEV-031) | しきい値変更伝播 | [UC-052](../../../01_requirements/04_business_usecases/UC-052.md#UC-052) |
| [`SEV-032`](SEV-032.md#SEV-032) | フォールバックアラート通知 | [UC-052](../../../01_requirements/04_business_usecases/UC-052.md#UC-052) |

### <span id="SYS-018"></span>SYS-018 利用量リアルタイム集計・サマリ反映

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-033`](SEV-033.md#SEV-033) | 利用量集計・閾値判定 | [UC-056](../../../01_requirements/04_business_usecases/UC-056.md#UC-056) |
| [`SEV-034`](SEV-034.md#SEV-034) | 利用量サマリ反映 | [UC-056](../../../01_requirements/04_business_usecases/UC-056.md#UC-056) |

### <span id="SYS-019"></span>SYS-019 質問数上限アラート通知

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-035`](SEV-035.md#SEV-035) | 上限アラートお知らせ生成 | [UC-057](../../../01_requirements/04_business_usecases/UC-057.md#UC-057) |
| [`SEV-036`](SEV-036.md#SEV-036) | アラートメール送信・結果記録 | [UC-057](../../../01_requirements/04_business_usecases/UC-057.md#UC-057) |

### <span id="SYS-020"></span>SYS-020 上限到達ウィジェット受付停止

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-037`](SEV-037.md#SEV-037) | 受付停止 | [UC-058](../../../01_requirements/04_business_usecases/UC-058.md#UC-058) |
| [`SEV-038`](SEV-038.md#SEV-038) | 定型文応答 | [UC-058](../../../01_requirements/04_business_usecases/UC-058.md#UC-058) |

### <span id="SYS-021"></span>SYS-021 月次請求確定

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-039`](SEV-039.md#SEV-039) | 請求確定・記録 | [UC-059](../../../01_requirements/04_business_usecases/UC-059.md#UC-059) |
| [`SEV-040`](SEV-040.md#SEV-040) | 確定通知送信 | [UC-059](../../../01_requirements/04_business_usecases/UC-059.md#UC-059) |

### <span id="SYS-022"></span>SYS-022 決済失敗猶予・サスペンション移行

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-041`](SEV-041.md#SEV-041) | サスペンション移行 | [UC-060](../../../01_requirements/04_business_usecases/UC-060.md#UC-060) |
| [`SEV-042`](SEV-042.md#SEV-042) | 通常状態復帰 | [UC-060](../../../01_requirements/04_business_usecases/UC-060.md#UC-060) |

### <span id="SYS-023"></span>SYS-023 メール配信状態Webhook処理

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-043`](SEV-043.md#SEV-043) | 配信状態更新 | [UC-063](../../../01_requirements/04_business_usecases/UC-063.md#UC-063) |
| [`SEV-044`](SEV-044.md#SEV-044) | 送信停止リスト登録 | [UC-063](../../../01_requirements/04_business_usecases/UC-063.md#UC-063) |

### <span id="SYS-024"></span>SYS-024 運営お知らせ配信

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-045`](SEV-045.md#SEV-045) | 受信箱お知らせ生成 | [UC-064](../../../01_requirements/04_business_usecases/UC-064.md#UC-064) |
| [`SEV-046`](SEV-046.md#SEV-046) | 配信ログ記録 | [UC-064](../../../01_requirements/04_business_usecases/UC-064.md#UC-064) |

### <span id="SYS-025"></span>SYS-025 運用イベントのシステム通知自動生成

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-047`](SEV-047.md#SEV-047) | システム通知生成 | [UC-065](../../../01_requirements/04_business_usecases/UC-065.md#UC-065) |
| [`SEV-048`](SEV-048.md#SEV-048) | 通知メール送信・配信ログ記録 | [UC-065](../../../01_requirements/04_business_usecases/UC-065.md#UC-065) |

### <span id="SYS-026"></span>SYS-026 メンバー割当変更通知

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-049`](SEV-049.md#SEV-049) | 受信箱お知らせ生成 | [UC-066](../../../01_requirements/04_business_usecases/UC-066.md#UC-066) |
| [`SEV-050`](SEV-050.md#SEV-050) | 通知メール送信・配信記録 | [UC-066](../../../01_requirements/04_business_usecases/UC-066.md#UC-066) |

### <span id="SYS-027"></span>SYS-027 配信失敗通知の再送

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-051`](SEV-051.md#SEV-051) | 通知再送 | [UC-067](../../../01_requirements/04_business_usecases/UC-067.md#UC-067) |
| [`SEV-052`](SEV-052.md#SEV-052) | 配信状態更新 | [UC-067](../../../01_requirements/04_business_usecases/UC-067.md#UC-067) |

### <span id="SYS-028"></span>SYS-028 受信箱お知らせ重複集約

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-053`](SEV-053.md#SEV-053) | 既存お知らせへ集約 | [UC-068](../../../01_requirements/04_business_usecases/UC-068.md#UC-068) |
| [`SEV-054`](SEV-054.md#SEV-054) | お知らせ新規生成 | [UC-068](../../../01_requirements/04_business_usecases/UC-068.md#UC-068) |

### <span id="SYS-029"></span>SYS-029 90日経過データ物理削除

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-055`](SEV-055.md#SEV-055) | 依存順物理削除 | [UC-071](../../../01_requirements/04_business_usecases/UC-071.md#UC-071) |
| [`SEV-056`](SEV-056.md#SEV-056) | 監査記録 | [UC-071](../../../01_requirements/04_business_usecases/UC-071.md#UC-071) |

### <span id="SYS-030"></span>SYS-030 セッション失効判定・再認証誘導

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-057`](SEV-057.md#SEV-057) | セッション無効化 | [UC-072](../../../01_requirements/04_business_usecases/UC-072.md#UC-072) |
| [`SEV-058`](SEV-058.md#SEV-058) | 再ログイン誘導 | [UC-072](../../../01_requirements/04_business_usecases/UC-072.md#UC-072) |

### <span id="SYS-031"></span>SYS-031 ログイン失敗ロックアウト・解除

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-059`](SEV-059.md#SEV-059) | ロック発動 | [UC-073](../../../01_requirements/04_business_usecases/UC-073.md#UC-073) |
| [`SEV-060`](SEV-060.md#SEV-060) | ロック解除 | [UC-073](../../../01_requirements/04_business_usecases/UC-073.md#UC-073) |

### <span id="SYS-032"></span>SYS-032 契約停止時セッション一斉無効化

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-061`](SEV-061.md#SEV-061) | セッション一斉無効化 | [UC-074](../../../01_requirements/04_business_usecases/UC-074.md#UC-074) |
| [`SEV-062`](SEV-062.md#SEV-062) | 再認証・停止時制限適用 | [UC-074](../../../01_requirements/04_business_usecases/UC-074.md#UC-074) |

### <span id="SYS-033"></span>SYS-033 監査ログ整合性検証(日次)

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-063`](SEV-063.md#SEV-063) | 監査ログ整合性検証 | [UC-075](../../../01_requirements/04_business_usecases/UC-075.md#UC-075) |
| [`SEV-064`](SEV-064.md#SEV-064) | 整合性違反通知 | [UC-075](../../../01_requirements/04_business_usecases/UC-075.md#UC-075) |

### <span id="SYS-034"></span>SYS-034 保持期間超過データの自動論理削除

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-065`](SEV-065.md#SEV-065) | 保持期間超過データの論理削除 | — |
| [`SEV-066`](SEV-066.md#SEV-066) | 削除実行結果の記録 | — |

### <span id="SYS-035"></span>SYS-035 課金通知 取込失敗の再処理

| SEV-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`SEV-067`](SEV-067.md#SEV-067) | 取込失敗通知の再処理 | [UC-061](../../../01_requirements/04_business_usecases/UC-061.md#UC-061) |
| [`SEV-068`](SEV-068.md#SEV-068) | 再処理上限到達のエスカレーション | [UC-061](../../../01_requirements/04_business_usecases/UC-061.md#UC-061) |

---

<!-- portal-bottom -->
[← バックエンド設計](../index.md) ・ [基本設計](../../index.md) ・ [↑ 設計ポータル](../../../README.md)
<!-- /portal-bottom -->
