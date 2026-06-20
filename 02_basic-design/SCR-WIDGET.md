<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ [画面設計](01_screen-design.md) ／ **WIDGET エンドユーザー向け FAQ ウィジェット**
<!-- /portal-top -->

# WIDGET エンドユーザー向け FAQ ウィジェット

> **このページは、ウィジェット利用者(エンドユーザー)が顧客サイト上で FAQ 検索・AI 回答・問い合わせを行う埋め込み UI を定義します(固有の SCR ID を持たない状態定義)。** 画面概要 / 画面遷移図 / 画面レイアウト / 画面項目定義 / 入出力一覧 / 画面イベント一覧 の 6 セクションで記述します。

*版数 v1.0 ・ 更新 2026-06-17 ・ 承認済*

## <span id="1-画面概要"></span>1. 画面概要

ウィジェット利用者(エンドユーザー)が顧客サイトに埋め込まれたウィジェットから FAQ 検索・AI 回答の確認・未解決時の連絡先確認を、同じ会話欄で行う UI です。初期表示は右下固定の丸型ランチャーバッジで、操作でチャット UI を展開します。

| 画面 ID | 画面名 | 機能概要 |
|----|----|----|
| <span id="WIDGET"></span>`WIDGET` | エンドユーザー向け FAQ ウィジェット | エンドユーザーが FAQ 検索・AI 回答・問い合わせを行うウィジェット |

| 関連 | 内容 |
|----|----|
| FR / BR | FR-050〜FR-057, FR-070〜FR-077, FR-122, FR-136, FR-150〜FR-156 / BR(ウィジェット) |
| 関連画面 | [`SCR-007` ウィジェット設定](SCR-007.md)(管理コンソール側でタイトル・連絡先メール等を設定) |

| ステークホルダ                     | 対象 |
|------------------------------------|------|
| ウィジェット利用者(エンドユーザー) | ◯    |

> [!NOTE]
> **補足** 本 UI は管理コンソールではなく顧客サイトへ埋め込まれるウィジェットです。固有の SCR ID は持たず、開閉状態と会話内容の状態を分けて管理する状態定義として扱います。管理用の問い合わせ ID はウィジェットに表示しません。配信・公開 API の詳細は DD12 を正本とします。

## <span id="2-画面遷移図"></span>2. 画面遷移図

本ウィジェットの状態遷移を、状態名と契機(操作・結果)で示します。固有 SCR ID を持たないため、開閉状態と会話状態を遷移ノードとして表します。

```mermaid
flowchart LR
  W0["起動前（丸型ランチャーバッジ）"]
  W1["展開中 / 通常（質問受付）"]
  W2["未解決（連絡先表示）"]
  W3["制限中（受付停止 / 429）"]
  W0 -->|バッジをクリック / Enter / Space| W1
  W1 -->|閉じるボタン| W0
  W1 -->|AI 回答 type=unanswered| W2
  W2 -->|別の質問を送信| W1
  W2 -->|閉じるボタン| W0
  W1 -->|質問数上限 / 支払ゲート（429）| W3
  W3 -->|閉じるボタン| W0
```

## <span id="3-画面レイアウト"></span>3. 画面レイアウト

<div style="background:#f5f6f8;padding:24px;border-radius:12px;font-family:'Noto Sans JP',-apple-system,BlinkMacSystemFont,'Hiragino Kaku Gothic ProN',Meiryo,sans-serif;color:#3a3f46;-webkit-font-smoothing:antialiased;--accent:#5e6ad2">
<div style="max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:32px">

  

  <div style="display:flex;gap:28px;align-items:flex-start;flex-wrap:wrap">

    <!-- 展開時 -->
    <section style="flex:1;min-width:560px">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:13px"><span style="font-size:11px;font-weight:700;color:var(--accent,#5e6ad2);background:color-mix(in srgb,var(--accent,#5e6ad2) 10%,#fff);border-radius:6px;padding:3px 8px">状態 1</span><span style="font-size:13.5px;font-weight:600;color:#16191d">展開時 — 回答 + フィードバック</span></div>
      <div style="height:600px;border:1px solid #e6e8eb;border-radius:14px;box-shadow:0 1px 2px rgba(16,24,40,.04),0 6px 20px rgba(16,24,40,.05);overflow:hidden;position:relative;background:linear-gradient(160deg,#eef1f6,#e3e7ef)">
        <!-- fake host site -->
        <div style="position:absolute;inset:0;padding:24px">
          <div style="width:160px;height:14px;border-radius:4px;background:rgba(22,25,29,.12);margin-bottom:18px"></div>
          <div style="width:70%;height:9px;border-radius:4px;background:rgba(22,25,29,.08);margin-bottom:10px"></div>
          <div style="width:60%;height:9px;border-radius:4px;background:rgba(22,25,29,.08);margin-bottom:10px"></div>
          <div style="width:65%;height:9px;border-radius:4px;background:rgba(22,25,29,.08)"></div>
        </div>
        <!-- widget -->
        <div style="position:absolute;right:24px;bottom:24px;width:360px;background:#fff;border-radius:18px;box-shadow:0 18px 50px rgba(16,24,40,.22);overflow:hidden;display:flex;flex-direction:column;max-height:524px">
          <div style="background:var(--accent,#5e6ad2);padding:16px 18px;color:#fff;display:flex;align-items:center;justify-content:between;gap:10px"><div style="flex:1"><div style="font-size:15px;font-weight:700">何かお困りですか?</div><div style="font-size:11.5px;opacity:.85;margin-top:2px">FAQ から自動でお答えします</div></div><span style="width:26px;height:26px;border-radius:7px;background:rgba(255,255,255,.18);display:flex;align-items:center;justify-content:center;cursor:pointer"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path></svg></span></div>
          <div style="flex:1;overflow:auto;padding:16px;display:flex;flex-direction:column;gap:12px;background:#fbfbfc">
            <div style="align-self:flex-end;max-width:82%;background:var(--accent,#5e6ad2);color:#fff;border-radius:14px 14px 4px 14px;padding:10px 13px;font-size:12.5px;line-height:1.55">料金プランの変更方法を教えてください</div>
            <div style="align-self:flex-start;max-width:88%;display:flex;flex-direction:column;gap:8px">
              <div style="background:#fff;border:1px solid #eef0f2;border-radius:14px 14px 14px 4px;padding:12px 14px;font-size:12.5px;color:#16191d;line-height:1.7">プランの変更は、管理画面の<b>「請求」→「プランを変更」</b>から行えます。変更は次回請求日から適用されます。</div>
              <div style="display:flex;align-items:center;gap:8px;padding-left:4px"><span style="font-size:11px;color:#9aa0a8">この回答は役に立ちましたか?</span><span style="width:28px;height:28px;border-radius:8px;border:1px solid #e6e8eb;background:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#1a7f37" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M7 11v9H4a1 1 0 0 1-1-1v-7a1 1 0 0 1 1-1z"></path><path d="M7 11l4-8a2 2 0 0 1 3 1.8V8h4.5a2 2 0 0 1 2 2.3l-1.2 7A2 2 0 0 1 17.3 19H7"></path></svg></span><span style="width:28px;height:28px;border-radius:8px;border:1px solid #e6e8eb;background:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#9aa0a8" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M17 13V4h3a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1z"></path><path d="M17 13l-4 8a2 2 0 0 1-3-1.8V16H5.5a2 2 0 0 1-2-2.3l1.2-7A2 2 0 0 1 6.7 5H17"></path></svg></span></div>
            </div>
            <div style="align-self:flex-start;display:flex;flex-wrap:wrap;gap:6px;padding-top:2px">
              <span style="padding:6px 11px;border:1px solid #e6e8eb;border-radius:999px;background:#fff;font-size:11.5px;color:var(--accent,#5e6ad2);font-weight:600;cursor:pointer">支払い方法を変更したい</span>
              <span style="padding:6px 11px;border:1px solid #e6e8eb;border-radius:999px;background:#fff;font-size:11.5px;color:var(--accent,#5e6ad2);font-weight:600;cursor:pointer">領収書がほしい</span>
            </div>
          </div>
          <div style="border-top:1px solid #eef0f2;padding:12px 14px;display:flex;align-items:center;gap:8px;background:#fff"><div style="flex:1;height:38px;border:1px solid #e6e8eb;border-radius:999px;background:#fbfbfc;display:flex;align-items:center;padding:0 14px;font-size:12px;color:#b5bac0">メッセージを入力…</div><span style="width:38px;height:38px;border-radius:999px;background:var(--accent,#5e6ad2);display:flex;align-items:center;justify-content:center;flex:none;cursor:pointer"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 14-7-7 14-2-5z"></path></svg></span></div>
        </div>
      </div>
    </section>

    <!-- 最小化時 -->
    <section style="flex:none;width:340px">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:13px"><span style="font-size:11px;font-weight:700;color:var(--accent,#5e6ad2);background:color-mix(in srgb,var(--accent,#5e6ad2) 10%,#fff);border-radius:6px;padding:3px 8px">状態 2</span><span style="font-size:13.5px;font-weight:600;color:#16191d">最小化時 — 起動ボタン</span></div>
      <div style="height:600px;border:1px solid #e6e8eb;border-radius:14px;box-shadow:0 1px 2px rgba(16,24,40,.04),0 6px 20px rgba(16,24,40,.05);overflow:hidden;position:relative;background:linear-gradient(160deg,#eef1f6,#e3e7ef)">
        <div style="position:absolute;inset:0;padding:24px">
          <div style="width:140px;height:14px;border-radius:4px;background:rgba(22,25,29,.12);margin-bottom:18px"></div>
          <div style="width:80%;height:9px;border-radius:4px;background:rgba(22,25,29,.08);margin-bottom:10px"></div>
          <div style="width:72%;height:9px;border-radius:4px;background:rgba(22,25,29,.08)"></div>
        </div>
        <div style="position:absolute;right:24px;bottom:24px;display:flex;flex-direction:column;align-items:flex-end;gap:12px">
          <div style="background:#fff;border:1px solid #eef0f2;border-radius:14px;box-shadow:0 8px 24px rgba(16,24,40,.14);padding:11px 14px;font-size:12.5px;color:#16191d;max-width:220px;line-height:1.5">ご質問はこちらから 👋</div>
          <span style="width:60px;height:60px;border-radius:999px;background:var(--accent,#5e6ad2);box-shadow:0 10px 26px color-mix(in srgb,var(--accent,#5e6ad2) 45%,transparent);display:flex;align-items:center;justify-content:center;cursor:pointer"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8z"></path></svg></span>
        </div>
      </div>
    </section>

  </div>
</div>
</div>

## <span id="4-画面項目定義"></span>4. 画面項目定義

本ウィジェットの入出力項目(ランチャーバッジ・ヘッダー・会話履歴・入力・送信・連絡先表示)を定義します。項目の正本は本表です。管理用の問い合わせ ID は描画しません。

| 項目 ID | 項目 | 説明 | 種類 | 表示条件 | 表示 |
|----|----|----|----|----|----|
| <span id="IT-01"></span>`IT-01` | 丸型ランチャーバッジ | 右下固定・直径 56px のバッジでチャット UI を開く。`aria-label="FAQチャットを開く"` | ボタン | — | チャットアイコン |
| <span id="IT-02"></span>`IT-02` | ヘッダー | ウィジェットタイトル・現在状態・閉じるボタンを表示する。利用規約等の導線は表示しない | 見出し | — | タイトル、状態(オンライン / 質問受付中 / 新しい質問の受付を停止中 等) |
| <span id="IT-03"></span>`IT-03` | 閉じるボタン | チャット UI を閉じてバッジ表示へ戻る。`aria-label="FAQチャットを閉じる"` | アイコンボタン | — | 閉じるアイコン |
| <span id="IT-04"></span>`IT-04` | 会話履歴 | 質問・AI 回答・システム返信を時系列で表示する | タイムライン | — | 質問 / AI 回答 / システム返信の時系列 |
| <span id="IT-05"></span>`IT-05` | 質問入力 | FAQ 質問のテキストを入力する。通常状態・未解決表示後は入力可 | テキストエリア | 受付制限中(質問数上限到達または支払方法ゲート)の場合は無効化 | — |
| <span id="IT-06"></span>`IT-06` | 送信 | 入力した質問を送信する。通常状態・未解決表示後は活性 | ボタン | 受付制限中(質問数上限到達または支払方法ゲート)の場合は無効化 | 送信 |
| <span id="IT-07"></span>`IT-07` | AI 回答 | 登録 FAQ に基づく回答を同じ会話欄に追加表示する | ラベル | — | AI 回答文 |
| <span id="IT-08"></span>`IT-08` | 連絡先メール表示 | 未解決・制限中に確認済みプロジェクト連絡先メールを案内表示する | ラベル | 未解決・制限中、かつ連絡先設定済みの場合のみ表示 | 「必要に応じて、下記のお問い合わせ先までメールでご連絡ください。」+ 連絡先メールアドレス |
| <span id="IT-09"></span>`IT-09` | 受付停止メッセージ | 受付停止と問い合わせ先を表示する(連絡先未設定時は再試行案内に差し替え) | アラート | 受付制限中の場合に表示 | 「ただいま新しいご質問をお受けできません。お手数ですが、下記のお問い合わせ先までメールでご連絡ください。」+ 連絡先メールアドレス |

## <span id="5-入出力一覧"></span>5. 入出力一覧

本ウィジェットが呼び出す公開 API の一覧です。公開 API のベースは `/widget/v1/...`、正本は [02_API設計 §5.5(ウィジェット API 群)](02_api-design.md)です(各 API の節は下表の行リンク先を正とします)。ウィジェットはサーバ経由でテーブルへアクセスし、直接の永続更新は行いません。

<table>
<thead>
<tr>
<th rowspan="2">入出力名</th>
<th rowspan="2">説明</th>
<th rowspan="2">種別</th>
<th rowspan="2">I/O</th>
<th colspan="4">アクセス種別(CRUD)</th>
<th rowspan="2">備考</th>
</tr>
<tr>
<th>C</th>
<th>R</th>
<th>U</th>
<th>D</th>
</tr>
</thead>
<tbody>
<tr>
<td>ウィジェット起動</td>
<td>セッションを確立しウィジェット設定を取得する</td>
<td>API</td>
<td>入力</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td><code>POST /widget/v1/bootstrap</code>(<a href="02_api-design.md#API-WGT-001">API 設計 5.5.1</a>)</td>
</tr>
<tr>
<td>質問送信</td>
<td>質問を送信し AI 回答を取得する(<code>type=unanswered</code> で未解決遷移)</td>
<td>API</td>
<td>入出力</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td><code>POST /widget/v1/ask</code>(<a href="02_api-design.md">API 設計 5.5.2</a>)</td>
</tr>
<tr>
<td>未解決質問登録</td>
<td>未解決時に質問ログ・未解決質問を登録する(問い合わせ ID は非表示)</td>
<td>API</td>
<td>出力</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td><code>POST /widget/v1/inquiries</code>(<a href="02_api-design.md">API 設計 5.5.3</a>)</td>
</tr>
</tbody>
</table>

## <span id="6-画面イベント一覧"></span>6. 画面イベント一覧

本ウィジェットで発生するイベントと発生タイミング・概要の一覧です。

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr>
<th>イベント ID</th>
<th>イベント</th>
<th>トリガー</th>
<th>処理</th>
<th>関連項目</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>EV-01</code></td>
<td>チャット UI を開く</td>
<td>ランチャーバッジのクリック / Enter / Space 時</td>
<td><ul>
<li>バッジを非表示にしチャット UI を展開</li>
<li><code>POST /widget/v1/bootstrap</code> でセッション・設定を取得</li>
</ul></td>
<td><a href="#IT-01">IT-01</a>, <a href="#IT-02">IT-02</a></td>
</tr>
<tr>
<td><code>EV-02</code></td>
<td>チャット UI を閉じる</td>
<td>ヘッダー閉じるボタン押下時</td>
<td><ul>
<li>チャット UI を閉じバッジへ戻る</li>
<li>会話履歴・入力内容・受付状態は保持</li>
</ul></td>
<td><a href="#IT-03">IT-03</a>, <a href="#IT-04">IT-04</a></td>
</tr>
<tr>
<td><code>EV-03</code></td>
<td>質問送信(通常)</td>
<td>送信ボタン押下時</td>
<td><ul>
<li><code>POST /widget/v1/ask</code> で質問送信</li>
<li>AI 回答を同じ会話欄に追加</li>
</ul></td>
<td><a href="#IT-05">IT-05</a>, <a href="#IT-06">IT-06</a>, <a href="#IT-07">IT-07</a></td>
</tr>
<tr>
<td><code>EV-04</code></td>
<td>未解決応答</td>
<td>AI 回答が <code>type=unanswered</code> の時</td>
<td><ul>
<li>回答不可の旨と確認済み連絡先メールをシステム返信で表示</li>
<li>問い合わせ ID は非表示で別質問は継続可能</li>
</ul></td>
<td><a href="#IT-07">IT-07</a>, <a href="#IT-08">IT-08</a></td>
</tr>
<tr>
<td><code>EV-05</code></td>
<td>受付停止(制限中)</td>
<td>質問数上限 100% 到達時、または支払方法ゲート(無料枠超過 + 支払方法未登録)による受付停止時(いずれも 429 応答)</td>
<td><ul>
<li>受付停止と問い合わせ先をシステム返信で表示し、入力欄と送信ボタンを無効化する</li>
<li><strong>いずれの契機も契約は <code>active</code> のままで、ウィジェット新規質問受付のみを停止する 429 系</strong>(質問数上限は <code>E-QUOTA-QUESTIONS-LIMIT</code>)</li>
<li>決済失敗等によるサスペンション(契約 <code>suspended</code> / 423)とは別状態(10_課金・請求設計 §4 支払方法ゲート)</li>
</ul></td>
<td><a href="#IT-05">IT-05</a>, <a href="#IT-06">IT-06</a>, <a href="#IT-09">IT-09</a></td>
</tr>
</tbody>
</table>

---

---

<!-- portal-bottom -->
[← 画面設計](01_screen-design.md) ・ [基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
