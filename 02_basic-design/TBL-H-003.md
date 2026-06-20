<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-H-003 H_NOTIF_LOGS**
<!-- /portal-top -->

# TBL-H-003 H_NOTIF_LOGS

履歴 <span id="315-H_NOTIF_LOGS"></span>

メール通知の送信履歴を保持します。

### <span id="3151-概要"></span>概要

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th>項目</th>
<th>内容</th>
</tr>
</thead>
<tbody>
<tr>
<td>テーブル名</td>
<td><code>H_NOTIF_LOGS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>通知ログ</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>contract_id</code> → <code>M_CONTRACT(id)</code></li>
<li><code>inquiry_id</code> → <code>T_INQUIRIES(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3152-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | 契約 owner ID | `contract_id` | TEXT | \- | NO |  | `M_CONTRACT(id)` |  |  |  |
| 3 | 案件 ID | `inquiry_id` | TEXT | \- | YES |  | `T_INQUIRIES(id)` |  |  |  |
| 4 | 受信者メール HMAC | `recipient_hmac` | TEXT | \- | YES |  |  |  |  |  |
| 5 | 通知種別 | `notification_type` | TEXT | \- | NO |  |  |  |  |  |
| 6 | 配信状態 | `delivery_state` | TEXT | \- | NO |  |  |  |  | `delivery_state IN ('queued','sending','sent','delivered','failed','bounced','complained','suppressed')` |
| 7 | メッセージ ID | `message_id` | TEXT | \- | YES |  |  |  |  |  |
| 8 | 試行回数 | `attempt_count` | INTEGER | \- | NO |  |  |  | `0` |  |
| 9 | 送信日時 | `sent_at` | TEXT | \- | YES |  |  |  |  |  |
| 10 | 配信日時 | `delivered_at` | TEXT | \- | YES |  |  |  |  |  |
| 11 | 失敗日時 | `failed_at` | TEXT | \- | YES |  |  |  |  |  |
| 12 | 失敗理由 | `fail_reason` | TEXT | \- | YES |  |  |  |  |  |
| 13 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3155-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_nlog_owner_created` | `(contract_id, created_at DESC)` |  | オーナー別新着 |
| 2 | `idx_nlog_message_id` | `message_id` |  | Webhook 紐付け |
| 3 | `idx_nlog_state` | `delivery_state` |  | 状態別集計 |

### <span id="3157-コード値区分値"></span>コード値・区分値

| カラム名         | 値           | 意味                   |
|------------------|--------------|------------------------|
| `delivery_state` | `queued`     | Queue 投入済み         |
| `delivery_state` | `sending`    | 送信中                 |
| `delivery_state` | `sent`       | 送信成功               |
| `delivery_state` | `delivered`  | 配信成功               |
| `delivery_state` | `failed`     | 失敗                   |
| `delivery_state` | `bounced`    | バウンス               |
| `delivery_state` | `complained` | スパム報告             |
| `delivery_state` | `suppressed` | サプレスリスト追加済み |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-008](SCR-008.md) [SCR-009-001](SCR-009-001.md) **API** [API-DASH-001](02_api-design.md#API-DASH-001) [API-MBR-002](02_api-design.md#API-MBR-002) [API-MBR-005](02_api-design.md#API-MBR-005) [API-WHK-001](02_api-design.md#API-WHK-001)

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
