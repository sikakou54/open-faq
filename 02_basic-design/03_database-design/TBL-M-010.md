<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [データベース設計](index.md) ／ **TBL-M-010 M_SERVICE_ANNOUNCE**
<!-- /portal-top -->

# TBL-M-010 M_SERVICE_ANNOUNCE

マスタ <span id="325-M_SERVICE_ANNOUNCE"></span>

お知らせの本体を保持します。

### <span id="3251-概要"></span>概要

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
<td><code>M_SERVICE_ANNOUNCE</code></td>
</tr>
<tr>
<td>論理名</td>
<td>お知らせ(Control Plane)</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>created_by_type</code> + <code>created_by_id</code> → <code>M_CONTRACT(id)</code> / <code>M_PRJ_USERS(id)</code>(論理参照)</li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3252-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | タイトル | `title` | TEXT | \- | NO |  |  |  |  | `length(title) BETWEEN 1 AND 200` |
| 3 | 本文(HTML) | `body_html` | TEXT | \- | NO |  |  |  |  |  |
| 4 | 重要度 | `importance` | TEXT | \- | NO |  |  |  |  | `importance IN ('low','normal','high','critical')` |
| 5 | 公開日時 | `published_at` | TEXT | \- | NO |  |  |  |  |  |
| 6 | 取り下げ日時 | `retracted_at` | TEXT | \- | YES |  |  |  |  |  |
| 7 | 作成者種別 | `created_by_type` | TEXT | \- | YES |  |  |  |  | `created_by_type IN ('owner','project_user')` |
| 8 | 作成者 ID | `created_by_id` | TEXT | \- | YES |  |  |  |  | `created_by_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 9 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |

### <span id="3255-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `idx_announcements_published` | `published_at DESC` WHERE `retracted_at IS NULL` |  | 公開中の新着 |

### <span id="3257-コード値区分値"></span>コード値・区分値

| カラム名     | 値         | 意味         |
|--------------|------------|--------------|
| `importance` | `low`      | 低           |
| `importance` | `normal`   | 通常         |
| `importance` | `high`     | 高           |
| `importance` | `critical` | クリティカル |

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-011](../01_screen-design/SCR-011.md) [SCR-012](../01_screen-design/SCR-012.md) **API** —

---

<!-- portal-bottom -->
[← データベース設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
