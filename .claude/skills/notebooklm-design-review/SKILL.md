---
name: notebooklm-design-review
description: '要件定義・基本設計・詳細設計をNotebookLMでレビューし、設計粒度・整合性・重複・落とし込み漏れ・責務分離・トレーサビリティを検証し、課題をObsidianで管理するためのスキル。「設計レビュー」「NotebookLMレビュー」「整合性チェック」「詳細設計レビュー」「落とし込み確認」「トレーサビリティ確認」「全層フルレビュー」「設計書全体のレビュー」と言われたら使う。リモートリポジトリ(uithub URL)からの取得・分割・レビューノートブック作成も対応。'
argument-hint: 'レビュー種別(省略時は全体構成レビューから開始): 全体構成 / 成果物別 / 処理フロー / バッチフロー / 共通定義 / 状態遷移 / Obsidian課題管理 / 再レビュー'
---

# NotebookLM設計レビュー Skill

## 目的

要件定義・基本設計・詳細設計をNotebookLMを外部レビュー担当として活用し、以下を確認する。

- 要件定義 → 基本設計 → 詳細設計 の落とし込み漏れ
- 上位設計に存在しない仕様の混入
- 設計書ごとの粒度分離
- 設計書間の重複記載
- 要件定義の逆参照（下位設計IDの混入）
- UI → API → モジュール → SQL → DB の追跡性
- バッチ → モジュール → SQL → DB の追跡性
- 状態値・区分値・閾値・設定値の共通定義への一元管理
- 詳細設計が実装に入れる粒度になっているか
- 発見された課題のObsidian管理

**NotebookLMは修正担当ではなく、外部レビュー担当として扱う。**

---

## NotebookLMの役割

```
あなたは、要件定義・基本設計・詳細設計の整合性を確認する外部レビュー担当です。

設計書を修正するのではなく、設計書の不整合・漏れ・重複・粒度不適切・責務混在・トレーサビリティ不備を指摘してください。

指摘は、必ず根拠となるドキュメント・該当箇所・理由を示してください。
根拠が不明な内容は、断定せず「要確認」として扱ってください。
```

### やらせないこと

- 設計書本文の勝手な修正・補完・推測追加
- 指摘根拠のない断定
- 単なる感想・一般論・観点外の改善提案
- 課題を設計書本文に直接混ぜ込む
- 未確定事項を確定仕様として扱う

---

## スクリプト・プロンプトの場所

```bash
SK=.claude/skills/notebooklm-design-review/scripts
PROMPTS=.claude/skills/notebooklm-design-review/prompts
```

CLI リファレンス: [nlm-reference.md](./references/nlm-reference.md)

---

## § 0. 前提チェック（初回のみ）

```bash
export PATH="$HOME/.local/bin:$PATH"
nlm --version
nlm doctor   # Cookies present + Account を確認
nlm list notebooks --json
```

セッションは約20分で自動回復する。`Cookies have expired` が出たら `nlm login`。

---

## レビュー手順

### Step 1: ソースを準備する（3バンドル取得）

`remote-bundles.json` に定義された3つのURLをそれぞれ取得し、NotebookLMソースファイルを生成する。

```bash
export UITHUB_TOKEN="<your-uithub-token>"   # 認証が必要な場合

python3 $SK/fetch_and_bundle.py \
    --config .claude/skills/notebooklm-design-review/remote-bundles.json \
    --out _nlm/bundles \
    --cache-dir _nlm/cache   # 再実行時にfetchをスキップ
```

出力される3ファイルがNotebookLMのソースになる:

| ファイル | URL |
|---|---|
| `_nlm/bundles/01_requirements.md` | `01_requirements/` 以下全体 |
| `_nlm/bundles/02_basic_design.md` | `02_basic_design/` 以下全体 |
| `_nlm/bundles/03_detail_design.md` | `03_detail_design/` 以下全体 |

### Step 2: レビュー単位を選択

引数で指定されたレビュー種別、または以下の順で実施する。

1. **全体構成レビュー** — ドキュメント構成・粒度・読み順・責務分離・トレーサビリティ全体
2. **成果物別レビュー** — 各成果物の責務・落とし込み・実装粒度
3. **処理フローレビュー** — UI → API → モジュール → SQL → DB
4. **バッチフローレビュー** — バッチ → モジュール → SQL → DB
5. **共通定義レビュー** — 状態値・区分値・閾値の一元管理
6. **状態遷移レビュー** — 状態遷移図・共通定義・DB・API・モジュール・SQLの整合
7. **Obsidian課題管理レビュー** — 課題保存状況の確認
8. **再レビュー** — 前回指摘の解消確認

各レビュー単位の対象と目的 → [レビュー実施単位](./references/01_review-units.md)

### Step 3: レビューごとに新規ノートブックを作成してバンドルを同期

**レビューごとに専用の新規ノートブックを作成する。既存ノートブックを使い回さない。**

```bash
REVIEW_KIND="全体構成"   # 実施するレビュー種別
REVIEW_DATE=$(date +%F)
NB_TITLE="FAQ open-faq ${REVIEW_KIND}レビュー ${REVIEW_DATE}"
NB_ALIAS="review-$(date +%Y%m%d)-${REVIEW_KIND}"

python3 $SK/nlm_sync.py \
    --notebook "$NB_ALIAS" \
    --create "$NB_TITLE" \
    --bundles-dir _nlm/bundles \
    --ids-out "_nlm/source_ids_${NB_ALIAS}.json"
```

> **失敗した場合の手動ループ**:
> ```bash
> NB=<notebook-id-from-create>
> for f in 01_requirements 02_basic_design 03_detail_design; do
>   out=$(nlm source add "$NB" --file "_nlm/bundles/$f.md" --wait)
>   sid=$(echo "$out" | grep -oE '[a-f0-9-]{12,}' | head -1)
>   python3 -c "import json,os;p='_nlm/source_ids.json';m=json.load(open(p)) if os.path.exists(p) else {};m['$f']='$sid';json.dump(m,open(p,'w'),ensure_ascii=False,indent=2)"
> done
> ```

### Step 4: NotebookLMにプロンプトを投入

各レビュー種別対応のプロンプト → [NotebookLMプロンプト集](./references/03_nlm-prompts.md)

プロンプトはレビュー単位ごとに分割して投入する。一度に全体をまとめて投入しない。

`nlm_ask.py` で自動投入する場合:

```bash
python3 $SK/nlm_ask.py --notebook "$NB_ALIAS" \
    --prompt-file $PROMPTS/xref_mismatch.md \
    --sources requirements,usecases,traceability,crosscut \
    --ids-map "_nlm/source_ids_${NB_ALIAS}.json" \
    --out _nlm/results/xref
```

### Step 5: 決定的チェック（機械的事実の正本）

NotebookLMの出力を以下の形式へ正規化する。

```
# REVIEW-XXX_レビュー名

## 1. レビュー対象

| 項目 | 内容 |
|---|---|
| レビューID | REVIEW-XXX |
| レビュー種別 | |
| 対象ドキュメント | |
| 実施日 | |
| 実施者 | NotebookLM |
| 整理担当 | レビュー統括Agent |

## 2. レビュー結果サマリー

| 項目 | 件数 |
|---|---|
| 指摘総数 | |
| 高 | |
| 中 | |
| 低 | |
| 要確認 | |
| Obsidian課題化対象 | |

## 3. 指摘一覧

| 指摘ID | 重要度 | 指摘分類 | 対象ドキュメント | 対象ID | 指摘内容 | 根拠 | 推奨対応 | Obsidian課題化要否 | 担当統括Agent | ステータス |
|---|---|---|---|---|---|---|---|---|---|---|

## 4. 重要指摘の詳細

## 5. 要確認事項

| 要確認ID | 内容 | 理由 | 推奨確認先 | Obsidian課題化要否 | ステータス |
|---|---|---|---|---|---|

## 6. Obsidian課題化対象

| 課題候補ID | 関連指摘ID | 課題名 | 課題化理由 | 担当統括Agent |
|---|---|---|---|---|

## 7. 次アクション

| No | アクション | 担当 | 期限目安 | 備考 |
|---|---|---|---|---|
```

### Step 5: 決定的チェック（機械的事実の正本）

NotebookLM とは独立に、スクリプトで機械的事実を確定する。NotebookLM の指摘がこれらと矛盾する場合は**スクリプトが正しい**。

```bash
# 壊れリンク/アンカー=0 / 系列別欠番なし / 同一ファイル内dup アンカー=0
python3 $SK/structure_check.py .

# UC<->TR 1:1 / TBL逆引き整合
python3 $SK/trace_consistency.py .

# SCR フォーマット規約 (FORMAT VIOLATIONS TOTAL = 0)
python3 $SK/format_check.py .

# 系列ごとのカバレッジ（定義済みだがトレースされていないID）
python3 $SK/id_coverage.py --prefix UC \
    --defs '01_requirements/04_business_usecases/UC-*.md' \
    --refs 02_basic_design/00_traceability/index.md
```

### Step 6: 結果の正規化・重要度判定

レビュー統括Agentが整理・分類する。NotebookLMの指摘をそのまま確定しない。

**重要度基準**

| 重要度 | 基準 |
|---|---|
| 高 | 実装不能・仕様矛盾・要件漏れ・上位設計にない仕様追加・重大なトレーサビリティ不備 |
| 中 | 実装時に迷う・責務混在・粒度不適切・参照漏れ・重複記載・共通定義参照漏れ |
| 低 | 表現改善・記載位置調整・補足説明不足・表記ゆれ・軽微な整合性問題 |

**指摘分類** → [指摘分類・レビュー観点一覧](./references/02_review-perspectives.md)

正規化フォーマット:

```
# REVIEW-XXX_レビュー名

## 1. レビュー対象

| 項目 | 内容 |
|---|---|
| レビューID | REVIEW-XXX |
| レビュー種別 | |
| 対象ドキュメント | |
| 実施日 | |
| 実施者 | NotebookLM |
| 整理担当 | レビュー統括Agent |

## 2. レビュー結果サマリー

| 項目 | 件数 |
|---|---|
| 指摘総数 | |
| 高 | |
| 中 | |
| 低 | |
| 要確認 | |
| Obsidian課題化対象 | |

## 3. 指摘一覧

| 指摘ID | 重要度 | 指摘分類 | 対象ドキュメント | 対象ID | 指摘内容 | 根拠 | 推奨対応 | Obsidian課題化要否 | 担当統括Agent | ステータス |
|---|---|---|---|---|---|---|---|---|---|---|
```

### Step 7: Obsidian課題化

以下の条件に該当する指摘は Obsidian 課題として保存する。

| 条件 | 課題メモ化 |
|---|---|
| すぐ修正できる軽微な表記ゆれ | 不要 |
| 単純な参照漏れ | 必要に応じて |
| 上位設計にない仕様が見つかった | **必須** |
| 落とし込み漏れが見つかった | **必須** |
| 成果物間で設計方針が衝突 | **必須** |
| 共通定義にすべき値が未定義 | **必須** |
| 状態遷移が不明 | **必須** |
| DB制約と業務ルールが矛盾 | **必須** |
| 再レビューでも未解消 | **必須** |
| Obsidian保存漏れ | **必須** |

Obsidian保存ルール・テンプレート → [Obsidianルール・テンプレート](./references/04_obsidian-rules.md)

### Step 8: 修正・再レビュー

- 重要度「高」「中」の指摘を対応する
- 対応後は Step 3 の**再レビュー用プロンプト**で解消確認を行う
- 指摘が無くなるまで繰り返す（1回で打ち切らない）

### Step 9: 最終出力

最終出力形式 → [最終出力フォーマット](./references/05_output-formats.md)

---

## Agent構成

「統括Agent + 作業Agent」構成で実行する。1人のAgentだけで完結させない。

| 役割 | 担当 |
|---|---|
| 統括Agent | 方針決定・作業分解・進捗管理・成果物統合 |
| NoteBookLM管理Agent | NotebookLMへの依頼受け渡し・結果整理・返却 |
| レビュー統括Agent | 指摘の正規化・分類・Obsidian課題化判断 |
| 課題管理Agent | Obsidian課題一覧の登録・更新 |

---

## 完了条件

- 指定されたレビュー単位でNotebookLMレビューを実施
- レビュー指摘が正規化された一覧表になっている
- 各指摘に重要度・分類・根拠・推奨対応が記載されている
- 指摘ごとに担当統括Agentが割り当てられている
- 重要度「高」「中」の指摘が対応済み、またはObsidian上で課題管理されている
- 再レビューにより指摘解消状況を確認している
- レビュー結果がObsidianに保存されている
- 未解決課題が `99_obsidian_context/04_issues_and_solutions/` に保存されている
- `INDEX_課題一覧.md` が作成・更新されている
- 要件定義 → 基本設計 → 詳細設計 の整合性が説明できる
- UI → API → モジュール → SQL → DB の流れが追跡できる
- バッチ → モジュール → SQL → DB の流れが追跡できる
- 共通定義 → 各詳細設計書 の参照関係が追跡できる
- NotebookLMレビューで得られた重要なコンテキストがObsidianに残っている
