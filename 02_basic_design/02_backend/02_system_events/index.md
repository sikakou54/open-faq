<!-- portal-top -->
[設計ポータル](../../../README.md) ／ [基本設計](../../index.md) ／ [バックエンド設計](../index.md) ／ **システムイベント設計**
<!-- /portal-top -->

# システムイベント設計書

> **全システムイベント(`SEV-001`〜`SEV-028`)を対応システム別に一覧します。** 各システムイベントは [システム設計](../01_system/index.md)(`SYS-*`)の 1 処理に属し、複数のイベントが 1 つの業務ユースケースを実現します(システムイベント → 業務UC は多:1)。処理内容の正本は各システム設計 §6 です。

*版数 v1.0 ・ 更新 2026-06-23 ・ システムイベント 28 ・ ステータス ドラフト*

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

---

<!-- portal-bottom -->
[← バックエンド設計](../index.md) ・ [基本設計](../../index.md) ・ [↑ 設計ポータル](../../../README.md)
<!-- /portal-bottom -->
