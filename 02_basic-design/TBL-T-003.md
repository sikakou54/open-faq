<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-T-003 T_PRJ_LEGACY_KEYS**
<!-- /portal-top -->

# TBL-T-003 T_PRJ_LEGACY_KEYS

トランザクション <span id="37-T_PRJ_LEGACY_KEYS"></span>

ウィジェット鍵ローテーション時に旧キーを 24 時間だけ有効にするためのレガシー API キーを保持します。

### <span id="371-概要"></span>概要

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
<td><code>T_PRJ_LEGACY_KEYS</code></td>
</tr>
<tr>
<td>論理名</td>
<td>レガシー API キー</td>
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

### <span id="372-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | プロジェクト ID | `project_id` | TEXT | \- | NO |  | `M_PROJECTS(id)` |  |  |  |
| 3 | 公開鍵 | `public_key` | TEXT | \- | NO |  |  |  |  |  |
| 4 | 猶予期限 | `grace_until` | TEXT | \- | NO |  |  |  |  |  |
| 5 | 作成日時 | `created_at` | TEXT | \- | NO |  |  |  | `datetime('now')` |  |

### <span id="375-インデックス"></span>インデックス

|  No | インデックス名        | 対象カラム   | UNIQUE | 用途     |
|----:|-----------------------|--------------|--------|----------|
|   1 | `idx_legacy_keys_key` | `public_key` |        | 旧鍵検索 |

### <span id="377-コード値区分値"></span>コード値・区分値

(なし)

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-007](SCR-007.md) **API** —

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
