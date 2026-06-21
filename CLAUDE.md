# FAQ 設計ポータル 保守ルール

本書(CLAUDE.md)はリポジトリの**保守・運用ルールの正本**であり、エージェントが自動読込する指示ファイルである。

本リポジトリは「FAQ AI ウィジェット SaaS / メインシステム」の **要件定義書**・**基本設計書** を **Markdown** で管理する。1 つの識別子(要件 / UC / 画面 / イベント / API / テーブル …)= 1 ファイルの**個別ページ構成**を正本とし、ルートの [`README.md`](README.md) がポータルのトップ(全文書索引)である。各識別子はフラット連番でゼロ詰め 3 桁・欠番なし。

> [!IMPORTANT]
> **読み順(正本)** 要件定義 ＞ 業務ユースケース ＞ 画面設計 ＞ 画面イベント ＞ API設計 ＞ DB設計 ＞ シーケンス ＞ 権限 / エラー / メッセージ。各層は前層を実現する関係で、`要件 ↔ UC ↔ SCR ↔ EVT ↔ API ↔ TBL` を双方向にトレースする。

---

## 構成

ファイル名はすべて英名(ASCII / ID ベース)。ページの表示タイトル・見出しは日本語。トップは 3 グループ(`01_requirements` / `02_basic_design` / `03_future`)。各セクションはフォルダ(`index.md` + 配下の個別ページ)で構成する。

```text
README.md                          # ポータルトップ(全文書ツリー = 旧サイドバー相当。自動生成)
CLAUDE.md                          # 保守ルール正本(本書)
01_requirements/                   # 要件定義
├── index.md                       #   システム概要 / 背景・目的 / スコープ / 利用者・ロール / 制約・前提 / 読み順 / 要件仕様・業務UCへのポインタ
├── 01_specifications/             #   要件仕様 : index.md + BR-001.. / FR-001.. / NFR-001.. / RULE-001..(1 要件 = 1 ファイル)
├── 02_business_usecases/          #   業務ユースケース : index.md + UC-001..(UC-001.. = 画面起点 / 末尾の連番 = システム起点)
└── 99_restructure_result.md       #   再構成結果サマリ(要件定義視点)
02_basic_design/                   # 基本設計
├── index.md                       #   基本設計トップ
├── 01_screens/                    #   画面設計 : index.md + SCR-001..(§6 にイベント列、§1 に対応UC)
│   └── mocks/                     #     画面モック: 画像 *.png と HTML ソース *.html(同名ペア)
├── 02_screen_events/              #   画面イベント設計 : index.md + EVT-001..(対応UC / SCR / 呼出API)
├── 03_apis/                       #   API設計 : index.md + API-001..(1 エンドポイント = 1 ファイル)
├── 04_database/                   #   DB設計 : index.md + TBL-001..(1 テーブル = 1 ファイル)
├── 05_sequences/                  #   シーケンス設計 : index.md + SEQ-001..(対応UC、図中の画面は新 SCR-ID)
├── 06_permissions/                #   権限設計 : index.md + PERM-001..
├── 07_errors/                     #   エラー設計 : index.md + ERR-001..
├── 08_messages/                   #   メッセージ設計 : index.md + MSG-001..(メールテンプレ)
├── 05_billing-design.md           #   横断設計(課金。単独ファイルで存置)
└── 99_restructure_result.md       #   再構成結果サマリ(基本設計視点)
03_future/                         # 将来対応 : index.md + FUT*
_build/                            # ツール(配信対象外。portal_nav.py / 再構成スクリプト等)
```

- ファイル名は ID 1 件 = 1 ファイル(例 `FR-001.md` / `BR-001.md` / `NFR-001.md` / `RULE-001.md` / `UC-001.md` / `SCR-001.md` / `EVT-001.md` / `API-001.md` / `TBL-001.md` / `SEQ-001.md` / `PERM-001.md` / `ERR-001.md` / `MSG-001.md`)。
- ページ間リンクはすべて `.md`。同一フォルダ内は兄弟参照、フォルダ / グループをまたぐ参照は相対パス(下記「相互参照アンカー」)。

### 採番ルール(最重要)

各系列は**フラット連番・ゼロ詰め 3 桁・欠番なし**。番号はその系列の**文書出現順**(定義の `<span id>` 出現順)に `001` から採番する。

| 系列 | 接頭辞 | 範囲(現状) | 備考 |
|----|----|----|----|
| 業務要件 | `BR-` | `BR-001`〜 | 要件仕様 |
| 機能要件 | `FR-` | `FR-001`〜 | 要件仕様 |
| 非機能要件 | `NFR-` | `NFR-001`〜 | 要件仕様(分類別ではなく通し連番) |
| 業務ルール | `RULE-` | `RULE-001`〜 | FR / BR から抽出した定量しきい値・ポリシー |
| 業務ユースケース | `UC-` | `UC-001`〜 | 前半 = 画面起点 / 後半 = システム起点(バッチ・Webhook・非同期) |
| 画面 | `SCR-` | `SCR-001`〜 | 1 画面 = 1 ファイル(フラット。`-NNN` 従属は廃止) |
| 画面イベント | `EVT-` | `EVT-001`〜 | UC と原則 1:1 |
| API | `API-` | `API-001`〜 | 1 エンドポイント = 1 ファイル |
| テーブル | `TBL-` | `TBL-001`〜 | 分類接頭辞(`M_`/`T_`/`H_`/`TP_`)は物理名に残し ID は通し連番 |
| シーケンス | `SEQ-` | `SEQ-001`〜 | UC 単位 |
| 権限 | `PERM-` | `PERM-001`〜 | |
| エラー | `ERR-` | `ERR-001`〜 | API エラーコードを正規化・採番 |
| メッセージ | `MSG-` | `MSG-001`〜 | メールテンプレ |
| 将来対応 | `FUT` | `FUT*` | MVP 後バックログ |

> [!WARNING]
> **欠番を作らない。** 識別子を削除したら後続を詰めて再採番し、**全層の参照を 1 パスで一括張替**する(例 `(?<![A-Za-z0-9])FR-\d+(?![0-9])` を旧→新マッピングで置換)→ `python3 _build/portal_nav.py` → 検証スクリプトで壊れ件数が **0 / 0** のままであることを確認する。

---

## ポータル形式(ナビゲーション)

サイドバー / パンくず / 戻り導線を Markdown で再現する。

- **ポータルトップ** = ルート [`README.md`](README.md)。3 グループの全文書を入れ子で索引する(自動生成)。
- **各セクションの一覧** = 各フォルダの `index.md`(要件仕様 / 業務UC / 画面 / 画面イベント / API / テーブル / シーケンス / 権限 / エラー / メッセージ の一覧を兼ねる)。
- **各ページの上下ナビ** = 全ページの先頭にパンくず、末尾に戻り導線を、次のマーカで囲って埋め込む:
  - 先頭: `<!-- portal-top -->` 〜 `<!-- /portal-top -->`(例 `[設計ポータル](../../README.md) ／ [要件定義](../index.md) ／ [要件仕様](index.md) ／ **FR-001: …**`)
  - 末尾: `<!-- portal-bottom -->` 〜 `<!-- /portal-bottom -->`(戻り導線)
- 右 TOC(「このページ」)はビューア(GitHub 等)が見出しから自動生成するため埋め込まない。

### ナビ・README の再生成

ナビとマーカ内・README は **`_build/portal_nav.py`(入れ子対応・汎用版)が自動管理**する。ページを追加・削除・改題したら、ルートで再生成する(冪等):

```sh
python3 _build/portal_nav.py
```

- パンくず / フッターは `portal-top` / `portal-bottom` マーカ間を毎回入れ替える。**本文編集はマーカの外側**(`# タイトル` 以降)で行う。
- 並びはファイル名の自然順(`FR-001` → `FR-002` …)。
- ラベルは各ページの `<h1>`(`#` 見出し)から取得する。

---

## 画面モックの画像化

GitHub は埋め込み HTML の `style=`/`class=` を除去するため、画面モック(`02_basic_design/01_screens/SCR-*.md` の §3 画面レイアウト)は **PNG 画像で表示**する。HTML ソースは MD に埋め込まず、**`02_basic_design/01_screens/mocks/<画面>-<n>.html`** に外出しして保持する(MD は画像 1 行のみ)。画像も同じ `02_basic_design/01_screens/mocks/<画面>-<n>.png` に置き、各 SCR からは `mocks/<画面>-<n>.png`(子階層相対・`../` なし)で参照する。**`../` 親参照にすると Cursor / VS Code のプレビューが画像を読み込めない**ため、必ず各ページと同階層配下に置く。

`mocks/<画面>-<n>.html` は単体で開けて図と同じ見た目になる完結 HTML(クロップ用に `#wrap` を持つ)。**モックを変更するときはこの .html を直接編集**し、PNG を再生成する(ルートで):

```sh
node ~/.claude/skills/html-to-png/scripts/html_to_png.js 02_basic_design/01_screens/mocks --selector "#wrap"
```

`mocks/*.html` → 同名 `mocks/*.png` を一括レンダリングする(html-to-png グローバルスキル / `puppeteer-core` + ローカル Chromium)。`mermaid` は画像化せず ` ```mermaid ` のまま(GitHub が描画)。

## ページ形式

各ページは**自己完結 Markdown**(ナビのマーカ + 本文)。

- 外部依存なし。図は ` ```mermaid ` コードフェンスで記述し、対応ビューア(GitHub 等)でそのまま描画される。
- **絵文字は使わない。**
- 画面モック(ワイヤーフレーム)は **PNG 画像で表示**する(上記「画面モックの画像化」)。

### 相互参照アンカー(最重要)

定義箇所には `<span id="ID"></span>` を埋め込んでアンカーを保持する(例: 見出しの `# <span id="FR-001"></span>FR-001: …`、表セル先頭の `<span id="TBL-001"></span>`)。参照側は通常の Markdown リンクで送る。

- 同一ページ: `[FR-001](#FR-001)`
- 同一フォルダの他ページ: `[FR-007](FR-007.md#FR-007)`(要件仕様フォルダ内)/ `[SCR-002](SCR-002.md#SCR-002)`(画面フォルダ内)
- 基本設計の別フォルダ: 画面イベント → 画面 `[SCR-001](../01_screens/SCR-001.md#SCR-001)` / API → テーブル `[TBL-001](../04_database/TBL-001.md#TBL-001)` / シーケンス → API `[API-002](../03_apis/API-002.md#API-002)`
- グループをまたぐ: 業務UC → 要件 `[FR-001](../01_specifications/FR-001.md#FR-001)` / 画面 → 業務UC `[UC-001](../../01_requirements/02_business_usecases/UC-001.md#UC-001)` / API → 業務UC `[UC-016](../../01_requirements/02_business_usecases/UC-016.md#UC-016)`

新しい定義行・見出しを追加するときは、対応する `<span id="…"></span>` を必ず付ける。

### ページの編集・追加

Markdown が正本なので、**該当 `.md` の本文を直接編集する**(ナビのマーカ外)。ページ追加は当該フォルダに `<ID>.md` を追加し、`python3 _build/portal_nav.py` を実行してナビ・README を更新する。

---

## 記載スタイル標準(全ページ共通)

冒頭で全体像が掴め、結論が先に読め、ページ間で構成が揃うことを目的に、以下の固定骨格で書く。

1. **`#` タイトル** — `# <span id="ID"></span>ID: 簡潔名`(例 `# <span id="FR-001"></span>FR-001: 管理者はアカウント登録`)。
2. **ページ要約(引用ブロック)** — タイトル直後。`> **この〜は「…」を定義します。**` の平易な要点。
3. **文書メタ** — `*種別 機能要件 ・ 優先度 P0 ・ ステータス ドラフト*` のように 1 行(斜体)。
4. **本編(`##` 以降)** — 各層の定型(下記)。

### 文章ルール

- 結論先出し。基本設計層は各 `##`/`###` 直後に 1〜2 文のリード文を置いてから表へ入る(**表をいきなり置かない**)。**要件定義層はリード文を置かない**(要約 + メタ + 要件 + 関連の簡潔構成)。
- 一文一義・能動・平易。略語は初出で説明するか正本へリンク。
- 並列で属性 1 種なら箇条書き、2 列以上なら表。

### 注記(GitHub Alert)

callout は GitHub Alert 記法で表す。見出し+本文は次行に `> **見出し** 本文` の形で書く。

| 用途 | 記法 |
|---|---|
| 補足・前提 | `> [!NOTE]` |
| 見落とすと困る正本ルール | `> [!IMPORTANT]` |
| 破壊的操作・誤りやすい点 | `> [!WARNING]` |
| 推奨・ベストプラクティス | `> [!TIP]` |

### 表の作法

- 列順は「識別子 → 名称 → 説明 → 値 / 制約 → 参照」。
- コード値・ID・列名はインラインコード(`` `status` ``)。空欄は `—`(全角ダッシュ)。
- 原則 GitHub Flavored Markdown のパイプ表。**セル内に箇条書き・改行・行/列結合が必要な表は、生 HTML テーブルのまま記述する**(アンカーと構造を保持するため)。
- 正本でない値の再掲は禁止。リンクで正本へ送る。

### コード・図

- JSON / DDL 等は ` ```json ` / ` ```sql ` 等のコードフェンス。
- フロー・シーケンス・ER 図は ` ```mermaid ` フェンス。リクエストには応答線を対で描く。

---

## 各層テンプレート

### 要件仕様(`01_requirements/01_specifications/`)

BR / FR / NFR / RULE を**1 要件 = 1 ファイル**で定義する。骨格は共通: タイトル → 要約 → メタ → `## 要件`(RULE は `## ルール`)→ `## 関連`。**リード文は置かない。**

- **業務要件 `BR-*`**: `## 関連` 表(列 = `観点 / ステークホルダ / 関連 NFR / 対応業務UC`)。要件本文は役割別の箇条書き可。
- **機能要件 `FR-*`**: `## 関連` 表(列 = `関連業務要件 / 優先度 / 対応業務UC`)。優先度 `P0`/`P1`/`P2`。
- **非機能要件 `NFR-*`**: メタに `分類`。`## 関連` に分類を記す。**分類別番号帯は使わず通し連番**。
- **業務ルール `RULE-*`**: FR / BR 文中の定量しきい値・ポリシーを抽出。`## ルール` + `## 由来`(由来要件へリンク)。
- **対応業務UC** 欄は各 UC の `対応要件ID` からの逆引きで結線する(UC が無ければ `(該当UCなし=ギャップ)`)。

### 業務ユースケース(`01_requirements/02_business_usecases/`)

**1 UC = 1 ファイル**。前半が画面起点(画面イベント由来)、後半がシステム起点(バッチ・Webhook・非同期ジョブ)。**15 項目**を満たす:

1. 業務ユースケースID / 2. 業務ユースケース名 / 3. 対応要件ID(FR へリンク)/ 4. 主アクター / 5. 目的 / 6. 事前条件 / 7. トリガー / 8. 基本フロー / 9. 代替フロー / 10. 例外フロー / 11. 事後条件 / 12〜15. 関連(関連画面ID `SCR` / 関連画面イベントID `EVT` / 関連API ID `API` / 関連テーブルID `TBL`)+ 備考。

- 詳細シーケンスは持たず、SEQ 層へトレースする。基本フローは画面・API・テーブルレベルの抽象度で書き、SQL・クラス / メソッド名は書かない。

### 画面設計(`02_basic_design/01_screens/`)

**1 画面 = 1 ファイル(フラット `SCR-NNN`)**。6 セクション固定:

1. 画面概要(画面 ID 表 + `関連`(FR/BR)+ `対応業務UC` 行)/ 2. 画面遷移図(mermaid flowchart)/ 3. 画面レイアウト(モック = **PNG 画像のみ**。HTML は `mocks/` に外出し)/ 4. 画面項目定義(項目 ID `IT-01`…)/ 5. 入出力一覧(CRUD マトリクス)/ **6. 画面イベント一覧**(列に **EVT 列**(`EVT-NNN` へリンク)/ イベント ID `EV-01`… / 項目 ID(§4 の `IT-` に対応、無ければ `—`)/ イベント / 処理)。

### 画面イベント設計(`02_basic_design/02_screen_events/`)

**1 イベント = 1 ファイル(`EVT-NNN`)**。`## 項目`(画面イベントID / イベント名 / 対応画面ID `SCR` / 対応業務UC `UC` / 対象項目ID `IT` / 呼出API `API` / 遷移先 `SCR`)+ `## 処理`(正本は SCR §6)+ 備考。UC と原則 1:1。

### API設計(`02_basic_design/03_apis/`)

**1 エンドポイント = 1 ファイル(`API-NNN`)**。骨格: `## 項目`(API ID / API名 / 対応業務UC / 対応画面ID / 対応画面イベントID / エンドポイント / HTTPメソッド / 認証 / 認可)/ 処理概要 / リクエスト / レスポンス / バリデーション / エラー(エラーコードセルに `ERR-NNN` 併記)/ 利用テーブル(`TBL-NNN` へリンク)/ 備考。

### DB設計(`02_basic_design/04_database/`)

**1 テーブル = 1 ファイル(`TBL-NNN`)**。物理名に分類接頭辞 `M_`(マスタ)/ `T_`(トランザクション)/ `H_`(履歴)/ `TP_`(ワーク・一時)を残す。骨格: H1 アンカー `# <span id="TBL-NNN"></span><物理名>(<論理名>)` → リード文 → `### 項目`(テーブルID / 物理名 / 論理名 / 概要 / 主キー(PK)/ 論理削除 / 監査項目 / 対応業務UC(逆引き)/ 利用API(逆引き))→ 概要 / カラム定義(PK / FK / UK / index / NULL / DEFAULT / 制約)/ コード値。データモデルの正本は `04_database/index.md` および各 `TBL-*`。

### シーケンス設計(`02_basic_design/05_sequences/`)

**UC 単位 1 ファイル(`SEQ-NNN`)**。`## 項目`(SEQ ID / 対応業務ユースケース `UC` / 関連画面 `SCR` / 関連 API `API` / 関連テーブル `TBL`)+ `## シーケンス図`(mermaid `sequenceDiagram`)。抽象度は `利用者 / 画面 / API / DB / 外部・バッチ・通知`、`テーブル名(CRUD)` 表記。**SQL・クラス / メソッド名・ORM・ループは書かない。** 図中の画面は新 `SCR-NNN`。

### 権限 / エラー / メッセージ

- **権限 `PERM-*`**(`06_permissions/`): ロール別操作可否 + 認可判定 + `対応 UC / SCR / EVT / API` 結線 + 由来要件。
- **エラー `ERR-*`**(`07_errors/`): エラーコード定義(HTTP ステータス・分類・メッセージ)+ `対応 API / EVT` 結線。
- **メッセージ `MSG-*`**(`08_messages/`): メールテンプレ(メタ・件名・本文・変数)+ `対応画面 / EVT / ERR` 結線。共通基準は各 index が正本。

### 将来対応(`03_future/FUTxx.md`)

- MVP 後の候補・バックログ。FUT カテゴリ別。要件定義テンプレートに準じる。

---

## トレーサビリティ規約

`要件(FR/BR/NFR/RULE) ↔ 業務UC ↔ 画面SCR ↔ 画面イベントEVT ↔ API ↔ テーブルTBL` を**双方向**に結線する。

- **順引き**: 各ページの `関連` / `項目` 表で下流(UC は SCR/EVT/API/TBL、SCR §1 は UC、API は UC/SCR/EVT/TBL、TBL は UC/API)へリンク。
- **逆引き**: 上流(FR/BR の `対応業務UC`、TBL の `対応業務UC / 利用API`)は下流側の参照を機械集計して結線する。
- 結線できない場合は `(該当UCなし=ギャップ)` 等を明記し、放置せず課題管理へ載せる(下記)。
- 一気通貫マトリクスは再構成期間中 `99_management/02_traceability_matrix.md` に保持(完了後は本書記載のトレース規約が正本)。

---

## 検証

ページを編集・追加したら、`python3 _build/portal_nav.py` でナビ・README を更新したうえで、**壊れリンク・壊れアンカーが無い**ことを確認する。ルートで次を実行:

```sh
python3 - <<'PY'
import os,re,glob,html
files=sorted(set(glob.glob("01_requirements/**/*.md",recursive=True)+glob.glob("02_basic_design/**/*.md",recursive=True)
                 +glob.glob("03_future/**/*.md",recursive=True)+["README.md"]))
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

> [!IMPORTANT]
> **壊れリンク・壊れアンカーは 0 / 0 を維持する。** 検証 glob は `01_requirements/**` + `02_basic_design/**` + `03_future/**` + `README.md`。一覧 / 索引ページ(各 `index.md`)は各項目に `<span id>` を付与し、`#FR-*` / `#UC-*` / `#SCR-*` / `#EVT-*` / `#API-*` / `#TBL-*` / `#SEQ-*` / `#PERM-*` / `#ERR-*` / `#MSG-*` の参照が解決すること。編集後は必ず本スクリプトで確認する。

---

## 課題管理(GitHub Issue)

作業中に発生した課題は GitHub Issue に登録し、解決したらクローズする。記録を残さないまま放置しない。

- **登録**: その場で解決できない課題・仕様とドキュメントの矛盾・トレーサビリティギャップ・環境制約が生じたら `gh issue create` で起票する。設計再構成由来の課題は表題に `[設計再構成][区分]`(区分 = `traceability` / `design-gap` / `needs-review` / `migration` / `cleanup` 等)を付ける。本文に **背景 / 対応(具体手順)/ 完了条件** を書く。
- **クローズ**: 解決コミット本文に `Closes #<番号>` を入れるか `gh issue close <番号>` でクローズする。
- 再構成の残課題は当面 `99_management/06_remaining_issues.md` に集約し、GitHub 再接続後に起票する。

---

## ID・用語

- ID 体系(全フラット連番・3 桁): `BR-###` / `FR-###` / `NFR-###` / `RULE-###`(要件)、`UC-###`(業務UC)、`SCR-###`(画面)、`IT-##` / `EV-##`(画面内連番)、`EVT-###`(画面イベント)、`API-###`(API)、`TBL-###`(テーブル)、`SEQ-###`(シーケンス)、`PERM-###` / `ERR-###` / `MSG-###`、`FUT##`(将来対応)。
- 定義箇所は `<span id="ID"></span>`(アンカー)。参照は定義へリンク(同一ページ `#ID`、他ページ `相対パス.md#ID`)。
- 用語: ログイン可能なアカウント保有者は「アカウント利用者」、ウィジェットのエンドユーザーは「ウィジェット利用者」と区別する。

---

## 注意

- Markdown が正本。本文変更は該当 `.md` の本文(ナビのマーカ外)を直接編集する。ナビ・README は `_build/portal_nav.py` で再生成する。
- 定義行・見出しを追加したら `<span id="…"></span>` を必ず付ける。削除・改名した識別子は、`01_requirements` / `02_basic_design`(配下フォルダ含む)/ `03_future` を検索して取りこぼしを修正する。
- 運用ルールの更新は本書 `CLAUDE.md` を直接編集する。
