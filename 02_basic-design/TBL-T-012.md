<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [データベース設計](03_database-design.md) ／ **TBL-T-012 T_TERMS_AGREE**
<!-- /portal-top -->

# TBL-T-012 T_TERMS_AGREE

トランザクション <span id="331-T_TERMS_AGREE"></span>

利用者ごとの規約同意履歴を保持します。

### <span id="3311-概要"></span>概要

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
<td><code>T_TERMS_AGREE</code></td>
</tr>
<tr>
<td>論理名</td>
<td>規約同意</td>
</tr>
<tr>
<td>主キー</td>
<td><code>id</code></td>
</tr>
<tr>
<td>外部キー</td>
<td><ul>
<li><code>actor_type</code> + <code>actor_id</code> → <code>M_CONTRACT(id)</code> / <code>M_PRJ_USERS(id)</code>(論理参照)</li>
<li><code>(doc_type, terms_version)</code> → <code>M_TERMS_VER(doc_type, version)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3312-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | 操作者種別 | `actor_type` | TEXT | \- | NO |  |  | ① |  | `actor_type IN ('owner','project_user')` |
| 3 | 操作者 ID | `actor_id` | TEXT | \- | NO |  |  | ① |  | `actor_type` に応じ `M_CONTRACT(id)` / `M_PRJ_USERS(id)` を指す(論理参照) |
| 4 | 文書種別 | `doc_type` | TEXT | \- | NO |  | `M_TERMS_VER(doc_type)` | ① |  |  |
| 5 | 規約版 | `terms_version` | TEXT | \- | NO |  | `M_TERMS_VER(version)` | ① |  |  |
| 6 | 同意日時 | `agreed_at` | TEXT | \- | NO |  |  |  |  |  |
| 7 | 同意 IP(マスク済) | `agreed_ip_masked` | TEXT | \- | YES |  |  |  |  |  |

### <span id="3315-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `uq_terms_actor_doc_version` | `(actor_type, actor_id, doc_type, terms_version)` | ○ | 操作者 × 文書 × 版で一意 |

### <span id="3317-コード値区分値"></span>コード値・区分値

(なし)

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-002](SCR-002.md) [SCR-010](SCR-010.md) [SCR-015](SCR-015.md) [SCR-018](SCR-018.md) [SCR-020](SCR-020.md) **API** [API-AUTH-001](02_api-design.md#API-AUTH-001) [API-AUTH-008](02_api-design.md#API-AUTH-008)

---

---

---

<!-- portal-bottom -->
[← データベース設計](03_database-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
