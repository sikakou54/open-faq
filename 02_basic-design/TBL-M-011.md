<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-M-011 M_ANNOUNCE_AUD**
<!-- /portal-top -->

# TBL-M-011 M_ANNOUNCE_AUD

マスタ <span id="326-M_ANNOUNCE_AUD"></span>

お知らせの配信先オーナーを限定指定する M:N テーブルです。

### <span id="3261-概要"></span>概要

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
<td><code>M_ANNOUNCE_AUD</code></td>
</tr>
<tr>
<td>論理名</td>
<td>お知らせ配信対象(M:N)</td>
</tr>
<tr>
<td>主キー</td>
<td><ul>
<li><code>announcement_id</code></li>
<li><code>contract_id</code></li>
</ul></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>announcement_id</code> → <code>M_SERVICE_ANNOUNCE(id)</code></li>
<li><code>contract_id</code> → <code>M_CONTRACT(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3262-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | お知らせ ID | `announcement_id` | TEXT | \- | NO | ① | `M_SERVICE_ANNOUNCE(id)` |  |  |  |
| 2 | 契約 owner ID | `contract_id` | TEXT | \- | NO | ② | `M_CONTRACT(id)` |  |  |  |
| 3 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3265-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_announcement_audiences_owner` | `(contract_id, announcement_id)` |  | 契約別逆引き |

### <span id="3267-コード値区分値"></span>コード値・区分値

(なし)

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** — **API** —

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
