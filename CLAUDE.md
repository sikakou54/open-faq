# FAQ 設計ポータル 保守ルール

本書(CLAUDE.md)はリポジトリの**保守・運用ルールの正本**であり、エージェントが自動読込する指示ファイルである。運用ルールは本書に集約し、ポータル(設計書 HTML 群)とは独立して維持する(ポータル内にルールの HTML ページは置かない)。

本リポジトリは「FAQ AI ウィジェット SaaS / メインシステム」の設計ドキュメントを **new 形式の静的ポータル**として管理する。リポジトリルートがそのままサイトで、`index.html` が入口、`file://` でも動作する。

---

## 構成(リポジトリルート)

ファイル名はすべて英名(ASCII)。ページの表示タイトル・サイドバーのラベルは日本語のまま。

```text
CLAUDE.md            # 保守ルール正本(本書 / 唯一の Markdown)
index.html           # ポータルトップ(00 概要)
style.css            # 唯一の共通スタイルシート
01_requirements/     # 要件定義  : index.html + FR01.html〜FR21.html
02_basic-design/     # 基本設計  : index + 画面設計(SCR-*) / API設計(API-*) / DB設計(TBL-*)
                     #             + 01_screen-design 〜 07_auth-design.html
03_future/           # 将来対応  : index.html + FUT01.html〜FUT06(-req/-detail).html
_build/              # ビルド資材(配信対象外。下記参照)
├── gen.py           #   静的ジェネレータ
└── src/             #   生成元ソース(自己完結。外部フォルダに依存しない)
    ├── requirements/ #     FR*.html(本文ソース)
    ├── basic-design/ #     SCR*/API*/TBL*/0x_*-design.html(本文ソース)
    ├── future/       #     FUT*.html(本文ソース)
    └── webhook.html
```

- ファイル名は ID ベースの英名(例 `FR01.html` / `FUT06-detail.html` / `01_screen-design.html`)。表示タイトル・ナビラベルは各ページの `<h1>`(日本語)から生成する。
- `02_basic-design/` は**フラット構成**(全ページ同一階層)。内部リンクは兄弟参照(例 `SCR-002.html` / `TBL-M-USER.html`)。
- `_build/` 配下はツール・生成元であり**配信(閲覧)対象ではない**。サイト本体は `index.html` / `style.css` / `01_〜03_` のみ。

---

## ページ形式(new 形式・最重要)

各ページは**自己完結 HTML**である。共通シェル(サイドバー / パンくず / 右 TOC / フッター / スクリプト)を各ページに**焼き込む**(旧 `portal.js` 注入方式は廃止)。

- 共通スタイルは**ルートの `style.css` のみ**。各ページは `../style.css?v=N` を参照する。
- 外部依存は CDN のみ:Noto Sans JP / Bootstrap Icons / lucide(画面モック)/ mermaid(図)。**ローカル画像・追加 JS/CSS は持たない。**
- **絵文字は使わない。** アイコンは Bootstrap Icons(`<i class="bi bi-...">`)、画面モックは lucide(`<i data-lucide="...">`)。
- ページ間リンクはすべて `.html`。

### ページの編集・追加(生成フロー)

サイト本体(`01_〜03_`)は `_build/gen.py` が `_build/src/` から生成する。**生成物を直接手編集しない**(再生成で上書きされる)。

1. **本文を編集**: `_build/src/<グループ>/<ファイル>.html` の `<article class="content">…</article>` の中身を編集する。
2. **ページを追加**: 同じ `_build/src/<グループ>/` に本文 HTML を追加する(`<article class="content">` を持つ形。既存ソースに倣う)。サイドバーの並びはファイル名昇順・ID 順。
3. **再生成**: リポジトリルートで次を実行する。

   ```sh
   python3 _build/gen.py
   ```

   要件定義 + 基本設計 + 将来対応の全ページを統一シェルで再生成する(冪等)。サイドバー・右 TOC・パンくず・カレント表示・mermaid/lucide の読込はジェネレータが自動付与する。
4. CSS を変更したら `_build/gen.py` 内の `?v=N` を上げてキャッシュを無効化する。

> ジェネレータは `_build/src/` のみを参照し、外部フォルダに依存しない。リポジトリ単体で再生成できる。

---

## ナビゲーション(左ペイン)

トップメニューは **要件定義 / 基本設計 / 将来対応** の 3 グループ。`基本設計` は入れ子で、配下に `画面設計(→SCR)` / `API設計(→API)` / `データベース設計(→TBL)` のサブセクションと `04 ユースケース` 〜 `07 認証認可` のリーフを持つ。

- 現在地のパスは自動展開し、カレント項目とグループ見出しをアクティブ表示する。
- 展開状態(localStorage)とスクロール位置(sessionStorage)はページ遷移後も保持する。
- ナビ定義はジェネレータが `_build/src/basic-design/` のサイドバー構造を解析して自動生成する(手書きの nav 定義ファイルは持たない)。

---

## 記載スタイル標準(全ページ共通)

`<article class="content">` 内のみを対象に、以下の固定骨格で書く。目的は「冒頭で全体像が掴め、結論が先に読め、ページ間で構成が揃う」こと。

1. **`<h1>` タイトル** — ID 接頭辞 + 簡潔名(例 `FR05: AI 回答`)。
2. **ページ要約 `aside.page-summary`** — H1 直後。`<p class="ps-lead"><strong>このページは〜を定義します。</strong></p>` の平易な要点。要約内のラベルは見出しタグではなく `<p class="ps-label">` を使う(目次を汚さない)。
3. **文書メタ `<p class="doc-meta">`** — `版数 / 更新 / ステータス` 等を 1 行。
4. **本編(`<h2>` 以降)** — 各層の定型(下記)。更新履歴は末尾 `<h2>更新履歴</h2>` + 表。

### 文章ルール

- 結論先出し。基本設計・画面設計は各 `<h2>`/`<h3>` 直後に `<p class="section-lead">` で 1〜2 文の説明を置いてから表へ入る(**表をいきなり置かない**)。**要件定義層は section-lead を置かない**。
- 一文一義・能動・平易。略語は初出で説明するか正本へリンク。
- 並列で属性 1 種なら箇条書き、2 列以上なら表。

### 注記(callout)

`<div class="callout 種別"><i class="bi bi-..."></i><div><span class="c-title">見出し</span>本文</div></div>`

| 種別 | クラス | アイコン | 用途 |
|---|---|---|---|
| 補足 | `callout note` | `bi-info-circle` | 補足・前提 |
| 重要 | `callout important` | `bi-pin-angle` | 見落とすと困る正本ルール |
| 注意 | `callout warning` | `bi-exclamation-triangle` | 破壊的操作・誤りやすい点 |
| ヒント | `callout tip` | `bi-lightbulb` | 推奨・ベストプラクティス |

### 表の作法

- 列順は「識別子 → 名称 → 説明 → 値 / 制約 → 参照」。
- コード値・ID・列名は `<code>`。空欄は `—`(全角ダッシュ)。
- 正本でない値の再掲は禁止。`<a href="...html">` で正本へ送る。

---

## 各層テンプレート

### 要件定義(`01_requirements/FRxx.html`)

- 骨格: `<h1>FRxx: 名称` → `aside.page-summary`(`ps-lead` + 概要 `<ul>`)→ `doc-meta`(版数 / 更新 / 機能グループ / 優先度 / ステータス)→ `1. 業務要件` → `2. 機能要件` → 未確定事項(callout)→ 更新履歴。**section-lead は置かない。**
- **業務要件**: 表 `<table class="br-table">`(列 = `ID(BR) / 観点 / ステークホルダ / 業務要件 / 関連 NFR`)。ID = `BR-###` 連番、定義セルは `<td id="BR-###">`(アンカーのみ非リンク)。主語は本文に書かずステークホルダ列へ。役割で内容が異なる場合は `<ul class="role-req">`。関連は NFR のみ。
- **機能要件**: 表 `<table class="req-table">`(列 = `ID(FR) / 要件 / 関連業務要件 / 優先度`)。ID = `FR-###`、定義セルは `<td id="FR-###">`。優先度はバッジ(`<span class="badge badge-p0">P0</span>` / `badge-p1` / `badge-p2`)。長い要件は `<ol class="alpha">`((a)(b)(c)、入れ子は `<ol class="alpha-sub">`=(a-1))で整理。
- ID は連番。欠番(廃番)は再利用しない。**FR-ID は全層で多数が相互参照するため機械的な全面リナンバリングは行わない**(参照整合が壊れる)。

### 基本設計の文書(`02_basic-design/0x_*-design.html`、API-*、TBL-*)

- 各節は **タイトル → 説明(`section-lead`)→ 表 → 補足(callout)** の順。概要は `ps-lead` の目的 1 文 + `doc-meta` のみ。
- **内容は原則すべて表**。散文・箇条書きは最小限。
- **フロー解説はシーケンス図(mermaid)** で示す: `<pre class="mermaid">sequenceDiagram …</pre>`(矢印は HTML エスケープ `-&gt;&gt;` / `--&gt;&gt;`)。リクエストには応答線を対で描く。DDL・API スキーマ等は `<pre><code>` で保持。

### 画面設計(`02_basic-design/SCR-*.html`、1 画面 = 1 ファイル)

- 親画面 `SCR-<番号>.html`、従属画面・モーダル `SCR-<番号>-NNN.html`(3 桁連番。`-M` サフィックスは使わない)。
- 6 セクション固定: `1. 画面概要` / `2. 画面遷移図`(mermaid flowchart)/ `3. 画面レイアウト`(`<div class="scr-mock">` のワイヤーフレーム。lucide アイコン)/ `4. 画面項目定義`(項目 ID `IT-01`…)/ `5. 入出力一覧`(CRUD マトリクス)/ `6. 画面イベント一覧`(イベント ID `EV-01`…、`関連項目` で §4 の `IT-` に紐づけ)。
- 意味のある状態・入力・業務ロジックを持つモーダルは独立 SCR ファイルにする。単純な確認ダイアログは独立させない。

### テーブル設計(`02_basic-design/TBL-*.html`、1 テーブル = 1 ファイル)

- ファイル名 `TBL-<分類>-<連番>.html`。分類接頭辞は **`M_`(マスタ)/ `T_`(トランザクション)/ `H_`(履歴)/ `TP_`(ワーク・一時)**。
- 各テーブルは 概要 / カラム定義 / 主キー / 外部キー / インデックス / 制約 / コード値の構成で表記する。
- **データモデルの正本は `02_basic-design/03_database-design.html` および各 `TBL-*`**。利用者モデルは `M_USER`(利用者マスタ)+ `M_CONTRACT`(契約マスタ)を中核とする。詳細・最新は当該設計書を参照(本書には再掲しない)。

### 将来対応(`03_future/FUTxx.html`)

- MVP 後の候補・バックログ。FUT カテゴリ別。要件定義テンプレートに準じる。

---

## ID・用語

- ID 体系: `FR-###` / `BR-###` / `NFR-###`(要件)、`SCR-<番号>(-NNN)`(画面)、`IT-##` / `EV-##`(画面内連番)、`API-*`(API)、`TBL-<分類>-<連番>`(テーブル)、`FUT##`(将来対応)。
- 定義セルはアンカーのみ(非リンク)。参照は定義へリンク(同一ページ `#ID`、他ページ `相対パス#ID`、NFR は `01_requirements/index.html#NFR-###`)。
- 用語: ログイン可能なアカウント保有者は「アカウント利用者」、ウィジェットのエンドユーザーは「ウィジェット利用者」と区別する。

---

## 検証

ページを編集・再生成したら、配信ポータル(`_build` を除く)に**移行範囲内の壊れリンクが無い**ことを確認する。ルートで次を実行:

```sh
python3 - <<'PY'
import os,re,html
files=[os.path.join(r,f) for r,_,fs in os.walk(".")
       if "/_build" not in r and "/.git" not in r and not r.startswith("./.git")
       for f in fs if f.endswith(".html")]
broken=[]
for p in files:
    root=os.path.dirname(p); s=open(p,encoding="utf-8").read()
    for m in re.finditer(r'href="([^"]+)"', s):
        h=html.unescape(m.group(1))
        if h.startswith(("http","#","mailto:")): continue
        path=h.split("#")[0].split("?")[0]
        if not path or path.endswith(".css"): continue
        if not os.path.exists(os.path.normpath(os.path.join(root,path))):
            broken.append((os.path.relpath(p,"."), h))
print("broken:", len(broken))
for x in broken: print("  ", x)
PY
```

旧基本設計世代(`M_OWNERS` モデル・11 文書体系)から移行した要件定義本文には、現構成に存在しない旧ドキュメント(詳細設計 / 運用設計 / 共有概念 / 旧基本設計の一部)への参照が残ることがある。これらは中身を忠実保持した結果のリンク切れであり、整合を取る場合は参照先を現構成へ張り替えるか、リンクをテキスト化する。

---

## 注意

- 生成物(`01_〜03_` の HTML)を直接編集しない。本文変更は `_build/src/` を編集して `python3 _build/gen.py` で再生成する。
- 変更により削除・改名した識別子(FR ID・列挙値・列名・画面/項目ラベル等)は、ソース内を検索して取りこぼしを修正する。
- 運用ルールの更新は本書 `CLAUDE.md` を直接編集する(ポータルには展開しない)。
