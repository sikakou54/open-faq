<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [DB設計](index.md) ／ **TBL-T-009 T_ANNOUNCE_RCPT**
<!-- /portal-top -->

# TBL-T-009 T_ANNOUNCE_RCPT

トランザクション <span id="327-T_ANNOUNCE_RCPT"></span>

お知らせの実配信先・配信集計・監査情報を保持します。

### <span id="3271-概要"></span>概要

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
<td><code>T_ANNOUNCE_RCPT</code></td>
</tr>
<tr>
<td>論理名</td>
<td>お知らせ受信者</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>announcement_id</code> → <code>M_SERVICE_ANNOUNCE(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3272-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | お知らせ ID | `announcement_id` | TEXT | \- | NO |  | `M_SERVICE_ANNOUNCE(id)` |  |  |  |
| 3 | 契約 owner ID | `contract_id` | TEXT | \- | NO |  |  |  |  |  |
| 4 | 受信者種別 | `recipient_type` | TEXT | \- | NO |  |  |  |  | `recipient_type IN ('owner','project_user')` |
| 5 | 受信者 ID | `recipient_id` | TEXT | \- | NO |  |  |  |  | `recipient_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 6 | 送信日時 | `sent_at` | TEXT | \- | NO |  |  |  |  |  |
| 7 | 配信状態 | `delivery_status` | TEXT | \- | NO |  |  |  |  | `delivery_status IN ('pending','delivered','failed')` |
| 8 | 既読日時 | `read_at` | TEXT | \- | YES |  |  |  |  |  |

### <span id="3275-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_ar_announcement` | `announcement_id` |  | お知らせ別 |
| 2 | `idx_ar_owner_user` | `(contract_id, recipient_type, recipient_id)` |  | ユーザー別逆引き |

### <span id="3277-コード値区分値"></span>コード値・区分値

| カラム名          | 値          | 意味     |
|-------------------|-------------|----------|
| `delivery_status` | `pending`   | 配信待ち |
| `delivery_status` | `delivered` | 配信完了 |
| `delivery_status` | `failed`    | 配信失敗 |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-011](../01_screens/SCR-011.md) [SCR-012](../01_screens/SCR-012.md) **API** —

---

<!-- portal-bottom -->
[← DB設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
