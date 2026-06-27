---
name: full-layer-review
description: Run a change-agnostic, WHOLE-CORPUS full-layer quality review of THIS FAQ design-doc repo (要件定義 + 基本設計 + 関連設計 + 将来対応) — not a diff review. Bundles every layer, drives Google NotebookLM as the external reviewer across 7 dimensions (取り違え/整合性/逆参照/粒度/画面フォーマット適合/抜け漏れ/総合), runs deterministic link/anchor/numbering/trace + SCR-format(format_check.py) checks as the source of truth, grep-verifies every NotebookLM finding, fixes, and re-reviews until convergence. Use when asked for a 全層フルレビュー / 設計書全体のレビュー / "review the whole doc set" (not just the changes). Also handles focused NotebookLM QA over any local document subset when asked. All scripts, prompts, and nlm CLI primitives are self-contained under this skill's directory.
---

# 全層フルレビュー（変更差分ではなくコーパス全体を対象）

FAQリポジトリの設計書全体を **Google NotebookLM**（外部判定者）と **決定的チェックスクリプト**（機械的事実の正本）の両輪でレビューする。NotebookLM は文書品質（粒度／逆参照／取り違え／抜け漏れ）を判定し、スクリプトはカウントできる事実（壊れリンク・ID 欠番・トレース完全性）を確定する。どちらか一方だけでは不十分。レビュアーは NotebookLM の代わりに自分で判断せず、プロンプトを組み、**全指摘を grep で検証**し、修正して再レビューする。

> スコープ原則: 差分ではなく観察（コーパス全体）でレビューする。既存の問題もスコープ内。

全スクリプトは `scripts/`、プロンプトテンプレートは `prompts/`、`nlm` CLI チートシートは [reference.md](reference.md) に格納。

```bash
SK=.claude/skills/full-layer-review/scripts
PROMPTS=.claude/skills/full-layer-review/prompts
```

## § 0. 前提チェック（初回のみ）

```bash
export PATH="$HOME/.local/bin:$PATH"     # nlm (uv tool) のインストール先
nlm --version            # インストール確認
nlm doctor               # 認証確認 (Cookies present + Account)
nlm list notebooks --json
```

- セッションは約 20 分で自動回復する。"Cookies have expired" が出たら `nlm login`。
- CLI の全コマンドリファレンス: `nlm --ai`。簡易チートシート: [reference.md](reference.md)。

## § 1. 決定的チェックを最初に実行（機械的事実の正本）

毎回の編集の前後に必ず実行する。NotebookLM ではなくこのスクリプト群が機械的事実を決定する。

```bash
# 壊れリンク/アンカー=0 / 系列別欠番=[] / 同一ファイル内dup アンカー=0
# （EVT/EM/EV はページローカルなので系列欠番チェックから除外）
python3 $SK/structure_check.py .

# UC<->TR 1:1 / TBL逆引きリスト==行列DBカラム / 孤立（TBL-011将来予約のみ許容）
python3 $SK/trace_consistency.py .

# SCR フォーマット規約 (FORMAT VIOLATIONS TOTAL = 0):
#   §4 種類≠div(label) / フォーマット外[!NOTE]・補足なし / §4 stray箇条書きなし
#   EVTページローカル(EVT-01..N) / mermaid フェンス整形済み
#   EVT参照は画面修飾(SCR-NNN EVT-MM) / SCR本文に詳細設計粒度なし
python3 $SK/format_check.py .

# 系列ごとのカバレッジ（定義済みだがトレースされていないID）
python3 $SK/id_coverage.py --prefix UC  --defs '01_requirements/04_business_usecases/UC-*.md'        --refs 02_basic_design/00_traceability/index.md
# 同様に --prefix SCR/SYS/API/TBL を繰り返す
```

NotebookLM の指摘がこれらのスクリプトと矛盾する場合は**スクリプトが正しい**（ファイルを grep して確認）。NotebookLM は大きなトレーサビリティ行列や HTML/パイプ表を `<cited_table>` に潰すため、カウントできる事実は hallucinate する。

## § 2. コーパスをレイヤー別にバンドル

11 レイヤー。編集後は名前指定で対象レイヤーだけ再実行できる。`**` グロブは再帰的に展開される。

```bash
python3 $SK/nlm_bundle.py --root . --out _nlm/bundles \
  --bundle rules='CLAUDE.md' \
  --bundle requirements='01_requirements/index.md,01_requirements/01_business_requirement/**/*.md,01_requirements/02_functional_requirement/**/*.md,01_requirements/03_non_functional_requirement/**/*.md' \
  --bundle usecases='01_requirements/04_business_usecases/**/*.md' \
  --bundle traceability='02_basic_design/00_traceability/**/*.md' \
  --bundle screens='02_basic_design/01_frontend/01_screens/*.md' \
  --bundle system='02_basic_design/02_backend/01_system/**/*.md' \
  --bundle apis='02_basic_design/02_backend/03_apis/**/*.md' \
  --bundle database='02_basic_design/02_backend/04_database/**/*.md' \
  --bundle sequences='02_basic_design/03_sequences/**/*.md' \
  --bundle crosscut='02_basic_design/index.md,02_basic_design/05_billing-design.md,02_basic_design/04_permissions/**/*.md,02_basic_design/05_errors/**/*.md,02_basic_design/06_messages/**/*.md' \
  --bundle future='03_future/**/*.md'
```

`screens` は `*.md`（トップレベル）で `mocks/*.html` を除外する。`rules`（CLAUDE.md）を必ず含め、NotebookLM が規約に照らして判定できるようにする。

バンドルは多数のファイルを少数のソースにまとめる（NotebookLM はソース数に上限があるため）。`===== <path> =====` セパレータでファイルごとの出典を保持する。レイヤー単位で分割しておくと、変更されたレイヤーだけ再同期できる。

## § 3. 新規ノートブックへ同期

```bash
python3 $SK/nlm_sync.py --notebook fullreview --create "FAQ 全層フルレビュー $(date +%F)" \
  --bundles-dir _nlm/bundles --ids-out _nlm/source_ids.json
```

**既知のバグ**: `nlm_sync.py` はノートブック作成直後の `source list --json` パースで不安定に落ちることがある。その場合は手動ループでバンドルを1件ずつ追加し、ids-map を自分で組み立てる（ノートブック ID は create 時に表示される; `nlm source add ... --wait` は `Source ID:` を確実に出力する）:

```bash
NB=<notebook-id-from-create>
for f in rules requirements usecases traceability screens system apis database sequences crosscut future; do
  out=$(nlm source add "$NB" --file "_nlm/bundles/$f.md" --wait)
  sid=$(echo "$out" | grep -oE '[a-f0-9-]{12,}' | head -1)
  python3 -c "import json,os;p='_nlm/source_ids.json';m=json.load(open(p)) if os.path.exists(p) else {};m['$f']='$sid';json.dump(m,open(p,'w'),ensure_ascii=False,indent=2)"
done
```

（`nlm chat configure --response-length longer` が NOT_FOUND を返す場合はスキップし、プロンプト内で網羅性を要求する。）

## § 4. 7 次元のレビューを実行（次元ごとにスコープを絞る）

プロンプトテンプレートは `prompts/` 配下。`nlm_ask.py` で NotebookLM に問い合わせる:

```bash
python3 $SK/nlm_ask.py --notebook "$NB" --prompt-file $PROMPTS/xref_mismatch.md \
  --sources requirements,usecases,traceability,crosscut --ids-map _nlm/source_ids.json --out _nlm/results/xref
```

出力: `_nlm/results/<次元>.json`（生データ）+ `_nlm/results/<次元>_answer.md`（回答 + 引用根拠）。

| 次元 | プロンプトファイル | `--sources` |
|----|----|----|
| 相互参照取り違え | `xref_mismatch.md` | requirements,usecases,traceability,crosscut |
| 整合性 | `consistency.md` | （全ソース） |
| 逆参照・委譲 | `reverse_reference.md` | rules,requirements,usecases |
| 構成・記載粒度 | `granularity.md` | rules,system,sequences,apis,database |
| 画面フォーマット適合 | `format_conformance.md` | rules,screens |
| 抜け漏れ | `gaps.md` | （全ソース）— ただし機械的カバレッジは §1 スクリプトが正本 |
| 総合/再レビュー | `overall.md` | （全ソース） |

**再採番済みコーパスで最も高い収益** = 相互参照取り違え（セマンティックな ID↔タイトル不一致。リンクチェッカーでは検出不可）。

**画面フォーマット適合** は `format_check.py` が機械的に検出できない「判断を要する適合」を見る: §1 概要が箇条書きか / §7 が業務的結果のみか（呼び出す API は記載する・画面内部の変数管理や処理手順は書かない）/ フォーマット外記述がないか / リード文が定型を超えていないか / データパターンが表で定義されているか / 詳細設計粒度の本文転記がないか。

### レビュープロンプトの書き方

- 「提供されたソースのみに基づいて回答し、`===== <path> =====` セパレータからの相対パスを引用し、推測しない」と明示する（「実在する ID・記述を根拠に挙げ、無ければ『指摘なし』」）。
- 結果をパースしやすいよう固定の**表形式**で出力させる。
- 大きなレビューは**焦点を絞ったクエリ**（1クエリ1観点、`--sources` でスコープ限定）に分割する。メガプロンプト 1 本より網羅性が上がり hallucination が減る。

## § 5. 全指摘を grep で検証してから対応判断

各指摘につき: 引用テキストが実在するか確認し、主張のスコープを正本で確認し、確定 / 偽陽性 / 要決定 に分類する。**このリポジトリで繰り返し発生する偽陽性:**

- **「API 利用テーブルが空欄」** — パイプ表の誤読。テーブルは実際には入力済み。`grep -A6 '## 利用テーブル' <api>` で確認。
- **BR vs RULE 列の混同** — 要件行列の BR / FR / RULE は別列。NotebookLM は列を潰して「BR-x は RULE-y にすべき」と言うことがあるが、BR-x が BR 列に正しく入っているだけの場合がある。実際の行を確認する。
- **存在しない変更履歴 / ID** — 例:「管理者は v2.2 で廃止」（そのような履歴は無く 管理者 は現役ロール）、「NFR-905」（現在の最大は NFR-079）。`grep -rn` で実在を確認する。
- **過剰一般化された要件** — 要件が定めていないフィールド/ガードの欠如を指摘。追加すると要件の捏造になる。要件の実際のスコープを確認する。

**NotebookLM が本当に得意な領域**（検証しつつ活用する）: セマンティック ID↔タイトル不一致（取り違え）、逆参照／委譲フレーズ、UC 本文への UI 文言／ボタン名混入、要件への HTTP コード／実装メソッド流入。

指摘を黙って捨てない、検証せずに適用しない。確定 / 偽陽性 / 要決定と理由を必ず記録する。

## § 6. 修正 → 変更レイヤーを再同期 → 再レビューを収束まで繰り返す

1. 確定済み・根拠のある指摘を修正する。要件が支持しない仕様は捏造しない。支持されない Gap は 要確認/design-decision とする。
2. 変更されたレイヤーだけ再バンドルし（位置引数で名前指定）、ソースを再追加する（手動ループで可。`_nlm/source_ids.json` を新 ID で更新する）。
3. 「今回の修正概要」前置きを添えて（`prompts/overall.md` のコメント参照）、更新されたソース ID に絞って **総合** を再実行する。
4. 編集のたびに §1 スクリプトを再実行する（リンク/アンカー 0/0、欠番なし、トレース整合）。
5. 総合が「指摘なし」または設計判断項目のみになるまで繰り返す。

**採番削除を伴う場合の手順**: 系列の旧→新マッピングを組み、プレースホルダーパス（`PFX-NNN` → トークン → 新番号）で衝突を避けながら置換し、§1 スクリプトで欠番 0 / 壊れ参照 0 を確認する。

**大規模コーパスや生成的修正の場合**: カテゴリ／サブシステムごとに並列 Agent を展開し、各 Agent が要件ファイル＋UC＋行列を読んで機械可読マッピング（`REQ-ID | MAP/CROSSCUT/GAP | UC-IDs | reason`）を返す。MAP（特定の UC が実現）/ CROSSCUT（横断的品質属性。行列に無理に入れず注釈する）/ GAP（設計が存在しない。Issue に回す）を正直に分類する。

## § 7. 記録管理

- `_nlm/findings/<次元>_findings.md` — 各次元の NotebookLM 生回答を表形式に整理 ＋ 検証結果 ＋ 対応要否。
- `_nlm/correspondence.md` — 次元横断マスター: 各指摘 → 修正 → 状態（対応済み / 一部対応 / 対応不要 / 要確認）＋ 却下理由。
- `_nlm/STATUS.md` — 次元別進捗 ＋ 最終判定（合格 / 条件付き合格 / 要追加対応）。

## § 8. 判断待ち・Gap → GitHub Issue（CLAUDE.md 課題管理に従う）

ステークホルダーの判断が必要なもの（設計方針・スコープ・複数ファイルにわたる変更）は `gh issue create` で起票する。タイトルに `[design-gap]`/`[needs-review]`/`[traceability]` の区分を付け、概要/背景/影響/提案/確認したいこと/関連ドキュメントを平易な日本語で書き、具体的な提案を添える。ドキュメント更新・双方向影響調査完了・§1 スクリプト クリーン・NotebookLM 再レビュー クリーン のすべてを満たしてから Close する。

## § 9. 最終報告

次元別結果、修正一覧（根拠 ID 付き）、却下した NotebookLM 指摘と理由、残存課題 / 起票済み Issue、および最終判定（合格 / 条件付き合格 / 要追加対応）をまとめる。監査証跡として `_nlm/findings/`・`_nlm/correspondence.md`・`_nlm/STATUS.md` を保持する。
