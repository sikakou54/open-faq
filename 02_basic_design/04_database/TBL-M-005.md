<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [DB設計](index.md) ／ **TBL-M-005 M_ALLOWED_DOMAINS**
<!-- /portal-top -->

# TBL-M-005 M_ALLOWED_DOMAINS

マスタ <span id="38-M_ALLOWED_DOMAINS"></span>

ウィジェット埋め込みを許可するドメインを保持します。

### <span id="381-概要"></span>概要

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
<td><code>M_ALLOWED_DOMAINS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>許可ドメイン</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>project_id</code> → <code>M_PROJECTS(id)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="382-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | プロジェクト ID | `project_id` | TEXT | \- | NO |  | `M_PROJECTS(id)` |  |  |  |
| 3 | ドメイン | `domain` | TEXT | \- | NO |  |  |  |  |  |
| 4 | 有効フラグ | `valid` | INTEGER | \- | NO |  |  |  | `1` | `valid IN (0,1)` |
| 5 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  |  |  |
| 6 | 更新日時 | `updated_at` | TEXT | \- | NO |  |  |  | `datetime('now')` |  |

### <span id="385-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `uq_allowed_domains_project_domain` | `(project_id, domain)` WHERE `valid = 1` | ○ | プロジェクト内ドメイン一意(部分 UNIQUE) |
| 2 | `idx_allowed_domains_valid` | `valid` WHERE `valid = 0` |  | 論理削除対象抽出 |

### <span id="387-コード値区分値"></span>コード値・区分値

(なし)

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-005](../01_screens/SCR-005.md) [SCR-004](../01_screens/SCR-004.md) [SCR-011](../01_screens/SCR-011.md) [SCR-030](../01_screens/SCR-030.md) **API** [API-016](../03_apis/index.md#API-016) [API-017](../03_apis/index.md#API-017) [API-018](../03_apis/index.md#API-018) [API-037](../03_apis/index.md#API-037)

---

<!-- portal-bottom -->
[← DB設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
