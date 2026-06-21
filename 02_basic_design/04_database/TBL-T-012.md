<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [DB設計](index.md) ／ **TBL-T-012 T_TERMS_AGREE**
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
<li><code>user_id → M_USER(id)</code></li>
<li><code>(doc_type, terms_version)</code> → <code>M_TERMS_VER(doc_type, version)</code></li>
</ul></td>
</tr>
</tbody>
</table>

### <span id="3312-カラム定義"></span>カラム定義

| No | 論理名 | 物理名 | データ型 | 桁数 | NULL | PK | FK | UNIQUE | DEFAULT | 制約 |
|---:|----|----|----|---:|----|----|----|----|----|----|
| 1 | ID | `id` | TEXT | \- | NO | ○ |  |  |  |  |
| 2 | ユーザーID | `user_id` | TEXT | \- | NO |  | `M_USER(id)` | ① |  |  |
| 3 | 文書種別 | `doc_type` | TEXT | \- | NO |  | `M_TERMS_VER(doc_type)` | ① |  |  |
| 4 | 規約版 | `terms_version` | TEXT | \- | NO |  | `M_TERMS_VER(version)` | ① |  |  |
| 5 | 同意日時 | `agreed_at` | TEXT | \- | NO |  |  |  |  |  |
| 6 | 同意 IP(マスク済) | `agreed_ip_masked` | TEXT | \- | YES |  |  |  |  |  |

### <span id="3315-インデックス"></span>インデックス

| No | インデックス名 | 対象カラム | UNIQUE | 用途 |
|---:|----|----|----|----|
| 1 | `uq_terms_user_doc_version` | `(user_id, doc_type, terms_version)` | ○ | ユーザー × 文書 × 版で一意 |

### <span id="3317-コード値区分値"></span>コード値・区分値

(なし)

### <span id="usedby"></span>使用元(画面 / API)

このテーブルを読み書きする画面と API です(逆引き)。

**画面** [SCR-002](../01_screens/SCR-002.md) [SCR-015](../01_screens/SCR-015.md) [SCR-020](../01_screens/SCR-020.md) [SCR-023](../01_screens/SCR-023.md) [SCR-025](../01_screens/SCR-025.md) **API** [API-001](../03_apis/index.md#API-001) [API-008](../03_apis/index.md#API-008)

---

<!-- portal-bottom -->
[← DB設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
