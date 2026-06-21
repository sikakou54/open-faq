# FAQ 設計ポータル 保守ルール

本書(CLAUDE.md)はリポジトリの**保守・運用ルールの正本**であり、エージェントが自動読込する指示ファイルである。

本リポジトリは「FAQ AI ウィジェット SaaS / メインシステム」の設計ドキュメントを **Markdown** で管理する。
かつての静的 HTML ポータル(`gen.py` による生成)を Markdown へ全面変換し、**Markdown を正本**とした。元の HTML サイトと同じディレクトリ構成・ポータル形式を維持しており、ルートの [`README.md`](README.md) がポータルのトップ(旧サイドバー相当の全文書索引)である。

---

## 構成

ファイル名はすべて英名(ASCII)。ページの表示タイトル・見出しは日本語。配置は旧 HTML サイトと同一(ルート直下に `01_〜03_`)。

```text
README.md                 # ポータルトップ(全文書ツリー = 旧サイドバー相当。自動生成)
CLAUDE.md                 # 保守ルール正本(本書)
01_requirements/          # 要件定義 : index.md + FR01.md〜FR21.md
02_basic-design/          # 基本設計 : index.md + 画面設計(SCR-*)/ API設計(API-*)/ DB設計(TBL-*)
                          #            + 01_screen-design 〜 07_auth-design.md
└── mocks/                #   画面モック: 画像 SCR-*.png と HTML ソース SCR-*.html(同名ペア)
03_future/                # 将来対応 : index.md + FUT01.md〜FUT06(-req/-detail).md
_build/                   # ツール(配信対象外)
├── html2md.py            #   HTML→Markdown 変換器(移行の記録 / provenance)
├── portal_nav.py         #   ポータルナビ付与 + README 生成器(下記)
├── imagify_mocks.py      #   画面モック(埋め込み HTML)を画像化し <details> に原本を残す
├── externalize_mocks.py  #   <details> 内のモック HTML を mocks/ へ外出し(移行時)
└── render_mocks.js       #   モック HTML を PNG へレンダリング(puppeteer-core + Chromium)
```

- ファイル名は ID ベースの英名(例 `FR01.md` / `SCR-001.md` / `TBL-M-001.md` / `API-auth.md` / `FUT06-detail.md`)。
- `02_basic-design/` は**フラット構成**(全ページ同一階層)。内部リンクは兄弟参照(例 `SCR-002.md` / `TBL-M-001.md`)。
- ページ間リンクはすべて `.md`。同一グループ内は兄弟参照、グループをまたぐ参照は相対パス(例 `../01_requirements/index.md`)。

> [!NOTE]
> 旧配信用 HTML(`index.html` / 生成された `01_〜03_` の HTML / `style.css`)と生成器 `gen.py` は廃止・削除済み。`_build/` 配下はツールであり閲覧対象ではない。

---

## ポータル形式(ナビゲーション)

HTML 時代のサイドバー / パンくず / 戻り導線を Markdown で再現する。

- **ポータルトップ** = ルート [`README.md`](README.md)。3 グループ(要件定義 / 基本設計 / 将来対応)の全文書を入れ子で索引する(基本設計は 画面設計 / API設計 / データベース設計 / 横断設計 に細分)。
- **各グループの一覧** = 各 `index.md`(および 基本設計の `01_screen-design.md` / `02_api-design.md` / `03_database-design.md` が画面/API/テーブルの一覧を兼ねる)。
- **各ページの上下ナビ** = 全ページの先頭にパンくず、末尾に戻り導線を、次のマーカで囲って埋め込む:
  - 先頭: `<!-- portal-top -->` 〜 `<!-- /portal-top -->`(例 `[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [画面設計](01_screen-design.md) ／ **SCR-001 ログイン**`)
  - 末尾: `<!-- portal-bottom -->` 〜 `<!-- /portal-bottom -->`(戻り導線)
- 右 TOC(「このページ」)はビューア(GitHub 等)が見出しから自動生成するため埋め込まない。見出しには相互参照アンカー(下記)が付く。

### ナビ・README の再生成

ナビとマーカ内・README は **`_build/portal_nav.py` が自動管理**する。ページを追加・削除・改題したら、ルートで再生成する(冪等):

```sh
python3 _build/portal_nav.py
```

- パンくず/フッターは `portal-top` / `portal-bottom` マーカ間を毎回入れ替える。**本文編集はマーカの外側**(`# タイトル` 以降)で行う。
- 並びはファイル名の自然順(親 `SCR-004` → 子 `SCR-004-001`)。API・テーブルは `portal_nav.py` 内の `API_ORDER` / `TBL_ORDER` の機能順。
- ラベルは各ページの `<h1>`(`#` 見出し)から取得する。

---

## 画面モックの画像化

GitHub は埋め込み HTML の `style=`/`class=` を除去するため、画面モック(`02_basic-design/SCR-*.md` の §3 画面レイアウト)は **PNG 画像で表示**する。HTML ソースは MD に埋め込まず、**`02_basic-design/mocks/<画面>-<n>.html`** に外出しして保持する(MD は画像 1 行のみ)。画像も同じ `02_basic-design/mocks/<画面>-<n>.png` に置き、各 SCR からは `mocks/<画面>-<n>.png`(子階層相対・`../` なし)で参照する。**`../` 親参照にすると Cursor / VS Code のプレビューが画像を読み込めない**ため、必ず各ページと同階層配下に置く。

`mocks/<画面>-<n>.html` は単体で開けて図と同じ見た目になる完結 HTML(クロップ用に `#wrap` を持つ)。**モックを変更するときはこの .html を直接編集**し、PNG を再生成する(ルートで):

```sh
node ~/.claude/skills/html-to-png/scripts/html_to_png.js 02_basic-design/mocks --selector "#wrap"
```

`mocks/*.html` → 同名 `mocks/*.png` を一括レンダリングする(html-to-png グローバルスキル / `puppeteer-core` + ローカル Chromium)。新規モックは `mocks/<画面>-<n>.html` を追加し、対応する SCR の §3 に `![…](mocks/<画面>-<n>.png)` を置いて上記で描画する。`mermaid` は画像化せず ` ```mermaid ` のまま(GitHub が描画)。

> 移行時のスクリプト `_build/imagify_mocks.py`(MD 埋め込み div を画像化)・`_build/externalize_mocks.py`(`<details>` ソースを外出し)・`_build/render_mocks.js`(manifest 描画)は provenance として残置。通常運用は上記スキルで足りる。

## ページ形式

各ページは**自己完結 Markdown**(ナビのマーカ + 本文)。

- 外部依存なし。図は ` ```mermaid ` コードフェンスで記述し、対応ビューア(GitHub 等)でそのまま描画される。
- **絵文字は使わない。**
- 画面モック(ワイヤーフレーム)は **PNG 画像で表示**し、元の HTML は同じ位置の `<details>` 内に ` ```html ` で保持する。GitHub は埋め込み HTML の CSS を除去するため、見た目を保つには画像化が必須(下記「画面モックの画像化」)。

### 相互参照アンカー(最重要)

定義箇所には `<span id="ID"></span>` を埋め込んでアンカーを保持する(例: 表セル先頭の `<span id="BR-028"></span>BR-028`、見出しの `## <span id="API-AUTH-001"></span>…`)。参照側は通常の Markdown リンクで送る。

- 同一ページ: `[FR-005](#FR-005)`
- 他ページ(同一グループ): `[API-AUTH-002](API-auth.md#API-AUTH-002)`
- 他グループ: `[NFR-304](../01_requirements/index.md#NFR-304)`(NFR の正本は要件定義 index)

新しい定義行・見出しを追加するときは、対応する `<span id="…"></span>` を必ず付ける。

### ページの編集・追加

Markdown が正本なので、**該当 `.md` の本文を直接編集する**(ナビのマーカ外)。ページ追加は当該グループのディレクトリに `.md` を追加し、`python3 _build/portal_nav.py` を実行してナビ・README を更新する。

---

## 記載スタイル標準(全ページ共通)

冒頭で全体像が掴め、結論が先に読め、ページ間で構成が揃うことを目的に、以下の固定骨格で書く。

1. **`#` タイトル** — ID 接頭辞 + 簡潔名(例 `# FR05: AI 回答`)。
2. **ページ要約(引用ブロック)** — タイトル直後。`> **このページは〜を定義します。**` の平易な要点(必要なら箇条書きを続ける)。
3. **文書メタ** — `*版数 v1.1 ・ 更新 2026-06-16 ・ ステータス 承認済*` のように 1 行(斜体)。
4. **本編(`##` 以降)** — 各層の定型(下記)。更新履歴は末尾 `## 更新履歴` + 表。

### 文章ルール

- 結論先出し。基本設計・画面設計は各 `##`/`###` 直後に 1〜2 文の説明(リード文)を置いてから表へ入る(**表をいきなり置かない**)。**要件定義層はリード文を置かない**。
- 一文一義・能動・平易。略語は初出で説明するか正本へリンク。
- 並列で属性 1 種なら箇条書き、2 列以上なら表。

### 注記(GitHub Alert)

callout は GitHub Alert 記法で表す。

| 用途 | 記法 |
|---|---|
| 補足・前提 | `> [!NOTE]` |
| 見落とすと困る正本ルール | `> [!IMPORTANT]` |
| 破壊的操作・誤りやすい点 | `> [!WARNING]` |
| 推奨・ベストプラクティス | `> [!TIP]` |

見出し+本文は `> [!NOTE]` の次行に `> **見出し** 本文` の形で書く。

### 表の作法

- 列順は「識別子 → 名称 → 説明 → 値 / 制約 → 参照」。
- コード値・ID・列名はインラインコード(`` `status` ``)。空欄は `—`(全角ダッシュ)。
- 原則 GitHub Flavored Markdown のパイプ表。**セル内に箇条書き・改行・行/列結合(rowspan/colspan)が必要な表は、生 HTML テーブルのまま記述する**(アンカーと構造を保持するため)。
- 正本でない値の再掲は禁止。リンクで正本へ送る。

### コード・図

- JSON / DDL 等は ` ```json ` / ` ```sql ` 等のコードフェンス。
- フロー・シーケンス・ER 図は ` ```mermaid ` フェンス(`flowchart` / `sequenceDiagram` / `erDiagram`)。リクエストには応答線を対で描く。

---

## 各層テンプレート

### 要件定義(`01_requirements/FRxx.md`)

- 骨格: `# FRxx: 名称` → 要約(引用ブロック)→ 文書メタ(版数 / 更新 / 機能グループ / 優先度 / ステータス)→ `## 1. 業務要件` → `## 2. 機能要件` → 未確定事項(callout)→ 更新履歴。**リード文は置かない。**
- **業務要件**: 表(列 = `ID(BR) / 観点 / ステークホルダ / 業務要件 / 関連 NFR`)。ID = `BR-###` 連番、定義セルは `<span id="BR-###"></span>BR-###`。主語はステークホルダ列へ。役割で内容が異なる場合は箇条書き。関連は NFR のみ。
- **機能要件**: 表(列 = `ID(FR) / 要件 / 関連業務要件 / 優先度`)。ID = `FR-###`、定義セルは `<span id="FR-###"></span>FR-###`。優先度は `P0` / `P1` / `P2`。長い要件は番号付き箇条書きで整理。
- **FR-ID / BR-ID は欠番のない連番を維持する。** 要件を削除したら後続 ID を詰めて再採番し、**全層の参照を一括更新する**(`(?<![A-Za-z0-9])(FR|BR)-\d+(?![0-9])` を旧→新マッピングで 1 パス置換 → `_build/portal_nav.py` → リンク/アンカー検証で壊れ件数が増えないこと)。定義(`<span id>`)の文書出現順に `001` から採番する。
- **NFR-ID も欠番のない通し連番を維持する。** `01_requirements/index.md` の NFR カタログ定義の出現順に `NFR-001` から採番する(かつてのカテゴリ別番号帯 `1xx`/`2xx`/`3xx`… は廃止。範囲行は `NFR-029〜033` のように連続範囲で、旧 `NFR-602a/b/c` の接尾辞は通し番号へ展開済み)。NFR の正本は同 index。FR/BR と同じく削除時は後続を詰めて再採番し全層の参照を一括更新する。

### 基本設計の文書(`02_basic-design/0x_*-design.md`、API-*、TBL-*)

- 各節は **タイトル → 説明(リード文)→ 表 → 補足(callout)** の順。
- **内容は原則すべて表**。散文・箇条書きは最小限。
- フロー解説はシーケンス図(mermaid)。DDL・API スキーマ等はコードフェンス。

### 画面設計(`02_basic-design/SCR-*.md`、1 画面 = 1 ファイル)

- 親画面 `SCR-<番号>.md`、従属画面・モーダル `SCR-<番号>-NNN.md`(3 桁連番)。
- 6 セクション固定: `1. 画面概要` / `2. 画面遷移図`(mermaid flowchart)/ `3. 画面レイアウト`(モック = **PNG 画像のみ**。HTML ソースは `mocks/<画面>-<n>.html` に外出し、MD には非表示)/ `4. 画面項目定義`(項目 ID `IT-01`…)/ `5. 入出力一覧`(CRUD マトリクス)/ `6. 画面イベント一覧`(列 = `イベント ID` / `項目 ID` / `イベント` / `処理`。イベント ID `EV-01`…。`項目 ID` で §4 の `IT-` に **1 対 1** で紐づけ、対応する項目が無いイベント(`初期表示`・遷移系など)はブランク `—`。イベント名は操作単位(`初期表示` / `…を押下` / `…を入力` 等)、`処理` の成功時 / 失敗時の分岐は箇条書きで定義)。
- 意味のある状態・入力・業務ロジックを持つモーダルは独立 SCR ファイルにする。単純な確認ダイアログは独立させない。

### テーブル設計(`02_basic-design/TBL-*.md`、1 テーブル = 1 ファイル)

- ファイル名 `TBL-<分類>-<連番>.md`。分類接頭辞は **`M_`(マスタ)/ `T_`(トランザクション)/ `H_`(履歴)/ `TP_`(ワーク・一時)**。
- 各テーブルは 概要 / カラム定義 / 主キー / 外部キー / インデックス / 制約 / コード値 の構成で表記する。
- **データモデルの正本は `02_basic-design/03_database-design.md` および各 `TBL-*`**。利用者モデルは `M_USER`(利用者マスタ)+ `M_CONTRACT`(契約マスタ)を中核とする。

### 将来対応(`03_future/FUTxx.md`)

- MVP 後の候補・バックログ。FUT カテゴリ別。要件定義テンプレートに準じる。

---

## ID・用語

- ID 体系: `FR-###` / `BR-###` / `NFR-###`(要件)、`SCR-<番号>(-NNN)`(画面)、`IT-##` / `EV-##`(画面内連番)、`API-*`(API)、`TBL-<分類>-<連番>`(テーブル)、`FUT##`(将来対応)。
- 定義箇所は `<span id="ID"></span>`(アンカー)。参照は定義へリンク(同一ページ `#ID`、他ページ `相対パス.md#ID`、NFR は `../01_requirements/index.md#NFR-###`)。
- 用語: ログイン可能なアカウント保有者は「アカウント利用者」、ウィジェットのエンドユーザーは「ウィジェット利用者」と区別する。

---

## 検証

ページを編集・追加したら、`python3 _build/portal_nav.py` でナビ・README を更新したうえで、**移行範囲内の壊れリンク・壊れアンカーが無い**ことを確認する。ルートで次を実行:

```sh
python3 - <<'PY'
import os,re,glob,html
files=sorted(set(glob.glob("0[123]_*/*.md")+["README.md"]))
ids={f:set(re.findall(r'id="([^"]+)"',open(f,encoding="utf-8").read())) for f in files}
def links(s):
    for m in re.finditer(r'\]\(([^)\s]+)\)',s): yield m.group(1)
    for m in re.finditer(r'href="([^"]+)"',s): yield m.group(1)
bf=[]; ba=[]
for p in files:
    d=os.path.dirname(p); s=open(p,encoding="utf-8").read()
    for raw in links(s):
        h=html.unescape(raw)
        if h.startswith(("http","mailto:")): continue
        path,_,frag=h.partition("#")
        if path=="":
            if frag and frag not in ids[p]: ba.append((p,h)); continue
        else:
            t=os.path.normpath(os.path.join(d,path))
            if not os.path.exists(t): bf.append((p,h))
            elif frag and t in ids and frag not in ids[t]: ba.append((p,h))
print("broken file links:",len(bf))
for x in bf: print("  F",*x)
print("broken anchor links:",len(ba))
for x in ba: print("  A",*x)
PY
```

> [!NOTE]
> 旧基本設計世代(`M_OWNERS` モデル・11 文書体系)から移行した本文には、現構成に存在しない旧ドキュメント(詳細設計 / 運用設計 / エラー設計 / メッセージ一覧 / 共有概念 等)への参照や、元から定義されていなかったアンカー(`01_requirements/index.md#NFR-3xx` の多く、`02_api-design.md#API-*` / `03_database-design.md#TBL-*` 等)が残る。これらは中身を忠実保持した結果のリンク切れであり、**HTML 時点から壊れていたもの**。整合を取る場合は参照先を現構成へ張り替えるか、リンクをテキスト化する。

---

## 注意

- Markdown が正本。本文変更は該当 `.md` の本文(ナビのマーカ外)を直接編集する。ナビ・README は `_build/portal_nav.py` で再生成する。
- 定義行・見出しを追加したら `<span id="…"></span>` を必ず付ける。削除・改名した識別子(FR ID・列挙値・列名・画面/項目ラベル等)は、`01_〜03_` 内を検索して取りこぼしを修正する。
- 運用ルールの更新は本書 `CLAUDE.md` を直接編集する。
