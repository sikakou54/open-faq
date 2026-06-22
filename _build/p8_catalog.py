#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P8 業務ユースケース統合カタログ(正本データ + クロスウォーク生成)。

操作粒度の旧 UC-001..281 を業務処理粒度の新 UC-001..088 へ完全分割する内容駆動マッピング。
本スクリプトは:
  1. 旧→新の被覆が「1..281 をちょうど 1 回ずつ」であることを assert で検証。
  2. 08_rule.md の `適用UC`(旧UC) を解析し RULE→新UC を導出。
  3. 99_management/uc_crosswalk_v2.json(old_to_new / new_to_old / meta)を出力。

実行: python3 _build/p8_catalog.py  (リポジトリルートで)
"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULEFILE = os.path.join(ROOT, "01_requirements", "01_BusinessRequirement", "08_rule.md")
OUT = os.path.join(ROOT, "99_management", "uc_crosswalk_v2.json")


def fr(*ns):
    return [f"FR-{n:03d}" for n in ns]


# 新UC定義(採番順 = 画面起点→システム起点→要件起点、各内で機能グループ順)。
# old = 構成元の旧UC番号(int)。
CATALOG = [
    # ---- 画面起点 / account (UC-001..023) ----
    dict(name="未認証ユーザーがログインする", actor="未認証ユーザー", group="account", kind="screen",
         fr=fr(4,7,37,40), old=[1,2,3,4,17,26,31,106]),
    dict(name="オーナーがアカウントを新規登録する", actor="未認証ユーザー", group="account", kind="screen",
         fr=fr(1,2,3,6,144,145,149,150), old=[6,7,8,9,10,11,12,13,14,15,16,18]),
    dict(name="オーナーが登録確認メールを検証する", actor="未認証ユーザー", group="account", kind="screen",
         fr=fr(1,3,149), old=[151,152,153,154,155]),
    dict(name="未認証ユーザーがパスワードの再設定を要求する", actor="未認証ユーザー", group="account", kind="screen",
         fr=fr(4), old=[5,19,20,21,23,27]),
    dict(name="未認証ユーザーが新しいパスワードを設定する", actor="未認証ユーザー", group="account", kind="screen",
         fr=fr(6), old=[22,24,25]),
    dict(name="招待メンバーがアカウントを有効化する", actor="メンバー", group="account", kind="screen",
         fr=fr(4,6,12,18,19,21,22,23,25,32,137,144,149), old=[181,182,183,184,185,186,187,188,189,190,191,192,193]),
    dict(name="対象ユーザーが連絡先メールアドレスを確認する", actor="アカウント利用者", group="account", kind="screen",
         fr=fr(43,44), old=[194,195]),
    dict(name="アカウント利用者が個人プロフィールを閲覧する", actor="アカウント利用者", group="account", kind="screen",
         fr=fr(1,4,5,9,190,191), old=[173,174,180]),
    dict(name="アカウント利用者が個人プロフィールを編集する", actor="アカウント利用者", group="account", kind="screen",
         fr=fr(1,5), old=[175,176,177,179]),
    dict(name="アカウント利用者が自身のパスワードを変更する", actor="アカウント利用者", group="account", kind="screen",
         fr=fr(5,6), old=[178]),
    dict(name="アカウント利用者が利用規約を閲覧する", actor="アカウント利用者", group="account", kind="screen",
         fr=fr(4,10,137,139), old=[133,134,198]),
    dict(name="アカウント利用者がプライバシーポリシーを閲覧する", actor="アカウント利用者", group="account", kind="screen",
         fr=fr(10,137,139), old=[196,197]),
    dict(name="アカウント利用者が改定文書へ再同意する", actor="アカウント利用者", group="account", kind="screen",
         fr=fr(10,137,139), old=[135,164,165,166,167,168,169]),
    dict(name="オーナーがプロジェクト一覧を閲覧する", actor="オーナー", group="account", kind="screen",
         fr=fr(37), old=[28,29,30,32]),
    dict(name="オーナーがプロジェクトを作成する", actor="オーナー", group="account", kind="screen",
         fr=fr(37,38), old=[33,35,36,37,38,44,252]),
    dict(name="オーナーがプロジェクトを編集する", actor="オーナー", group="account", kind="screen",
         fr=fr(37), old=[34,39,40,43,45]),
    dict(name="オーナーがプロジェクトを削除する", actor="オーナー", group="account", kind="screen",
         fr=fr(37), old=[41,42]),
    dict(name="管理者がメンバー一覧を閲覧する", actor="プロジェクト管理者", group="account", kind="screen",
         fr=fr(22,27,36), old=[115,116,117,118,119,120]),
    dict(name="管理者がメンバーを招待する", actor="プロジェクト管理者", group="account", kind="screen",
         fr=fr(19,21,22,23,28,32,36), old=[123,125,126,127,249]),
    dict(name="管理者がメンバー情報を編集する", actor="プロジェクト管理者", group="account", kind="screen",
         fr=fr(22,24,27,36), old=[124,128,131,132]),
    dict(name="管理者がメンバーをプロジェクトから外す", actor="プロジェクト管理者", group="account", kind="screen",
         fr=fr(24,26,27,29,30,31), old=[129,130]),
    dict(name="オーナーが契約設定を編集する", actor="オーナー", group="account", kind="screen",
         fr=fr(9,90,138), old=[215,216,217,218,220,221]),
    dict(name="オーナーが退会を申請する", actor="オーナー", group="account", kind="screen",
         fr=fr(1,5,9,138), old=[156,157,158,159,160,161,162,163]),
    # ---- 画面起点 / faq-ai (UC-024..032) ----
    dict(name="管理者がFAQ一覧を閲覧する", actor="プロジェクト管理者", group="faq-ai", kind="screen",
         fr=fr(169,173,174), old=[62,63,64,65,66,72]),
    dict(name="管理者がFAQを作成・編集する", actor="プロジェクト管理者", group="faq-ai", kind="screen",
         fr=fr(47,48,49,50,51,52,53,54,55,56,75,169,170,171,172,178), old=[61,67,68,75,76,77,78,79,80,81,82,85,86,88,89]),
    dict(name="管理者がFAQを削除する", actor="プロジェクト管理者", group="faq-ai", kind="screen",
         fr=fr(47,53,169,174), old=[71,83,84,87]),
    dict(name="管理者がFAQの公開状態を一括変更する", actor="プロジェクト管理者", group="faq-ai", kind="screen",
         fr=fr(169,173,174), old=[69,70]),
    dict(name="管理者がFAQをCSVでインポートする", actor="プロジェクト管理者", group="faq-ai", kind="screen",
         fr=fr(169,173,174), old=[73,90,91,92,93,94,95]),
    dict(name="管理者がFAQをCSVでエクスポートする", actor="プロジェクト管理者", group="faq-ai", kind="screen",
         fr=fr(169,173,174), old=[74]),
    dict(name="管理者が未解決質問一覧を閲覧する", actor="プロジェクト管理者", group="faq-ai", kind="screen",
         fr=fr(40,68,69), old=[46,47,48,49,51,52,53]),
    dict(name="管理者が未解決質問の詳細を確認する", actor="プロジェクト管理者", group="faq-ai", kind="screen",
         fr=fr(48,49,50,51,52,54,55,56,68,69,71,73,74,75,169,170,171,172,178), old=[50,54,59,60]),
    dict(name="管理者が未解決質問の対応状況を更新する", actor="プロジェクト管理者", group="faq-ai", kind="screen",
         fr=fr(68,72,73,74,75,80,101), old=[55,56,57,58,262,265]),
    # ---- 画面起点 / usage (UC-033..039) ----
    dict(name="管理者がプロジェクト概要ダッシュボードを閲覧する", actor="プロジェクト管理者", group="usage", kind="screen",
         fr=fr(4,7,68,88,90,100,102,103,105,109,169), old=[107,108,109,110,111,112,113,114,266,267,269]),
    dict(name="管理者が利用量と上限を閲覧する", actor="プロジェクト管理者", group="usage", kind="screen",
         fr=fr(88,89,92), old=[199,200]),
    dict(name="管理者が利用上限とアラート閾値を設定する", actor="プロジェクト管理者", group="usage", kind="screen",
         fr=fr(5,88,89,92,94), old=[202,203,204,205,206,207]),
    dict(name="オーナーが契約サマリーを閲覧する", actor="オーナー", group="usage", kind="screen",
         fr=fr(4,7,37,90,100), old=[170,171,172]),
    dict(name="オーナーが請求情報を閲覧する", actor="オーナー", group="usage", kind="screen",
         fr=fr(9,88,89,90), old=[208,210,211,212,219]),
    dict(name="オーナーが支払方法を登録・更新する", actor="オーナー", group="usage", kind="screen",
         fr=fr(90), old=[209,213]),
    dict(name="オーナーがプランを変更する", actor="オーナー", group="usage", kind="screen",
         fr=fr(89,90), old=[214]),
    # ---- 画面起点 / widget (UC-040..044) ----
    dict(name="管理者がウィジェット設定を編集する", actor="プロジェクト管理者", group="widget", kind="screen",
         fr=fr(40), old=[96,97,98,99,100,101,102,103,105]),
    dict(name="管理者がウィジェット公開キーを再発行する", actor="プロジェクト管理者", group="widget", kind="screen",
         fr=fr(40), old=[104]),
    dict(name="ウィジェット利用者がチャットを開く", actor="ウィジェット利用者", group="widget", kind="screen",
         fr=fr(57,61,68), old=[222,223,224]),
    dict(name="ウィジェット利用者がFAQを検索する", actor="ウィジェット利用者", group="widget", kind="screen",
         fr=fr(57,61), old=[225,226]),
    dict(name="ウィジェット利用者が未解決・制限・エラーの案内を受ける", actor="ウィジェット利用者", group="widget", kind="screen",
         fr=fr(57,58,59,61,65,66,67,68,96,135), old=[227,228,229,275]),
    # ---- 画面起点 / notification (UC-045..047) ----
    dict(name="アカウント利用者がお知らせ一覧を閲覧する", actor="アカウント利用者", group="notification", kind="screen",
         fr=fr(155,156,173), old=[136,137,138,139,140,145,146]),
    dict(name="アカウント利用者がお知らせの詳細を閲覧する", actor="アカウント利用者", group="notification", kind="screen",
         fr=fr(155,156,157,158), old=[147,148,149,150]),
    dict(name="アカウント利用者がお知らせを既読化する", actor="アカウント利用者", group="notification", kind="screen",
         fr=fr(156,167,174), old=[141,142,143,144,280]),
    # ---- 画面起点 / security (UC-048) ----
    dict(name="未割当ユーザーが権限不足ガードからダッシュボードへ戻る", actor="アカウント利用者", group="security", kind="screen",
         fr=fr(22,27,36,88,89), old=[121,122,201]),
    # ---- システム起点 / account (UC-049..050) ----
    dict(name="システムがメンバー数の上限接近・急増を検知して通知する", actor="システム", group="account", kind="system",
         fr=fr(33), old=[250]),
    dict(name="システムがプロジェクト数の急増を検知してオーナーへ通知する", actor="システム", group="account", kind="system",
         fr=fr(46), old=[256]),
    # ---- システム起点 / faq-ai (UC-051..055) ----
    dict(name="システムがFAQ一括取り込みジョブを非同期実行する", actor="システム", group="faq-ai", kind="system",
         fr=fr(169), old=[230]),
    dict(name="システムがAIしきい値変更を推論へ伝播する", actor="システム", group="faq-ai", kind="system",
         fr=fr(193), old=[245]),
    dict(name="システムが回答に利用したFAQを記録し参照提示する", actor="システム", group="faq-ai", kind="system",
         fr=fr(60), old=[257]),
    dict(name="システムが回答不可時に未解決質問を登録し案内する", actor="システム", group="faq-ai", kind="system",
         fr=fr(63,64,136), old=[259,260,276]),
    dict(name="システムが未解決質問に必要項目を記録する", actor="システム", group="faq-ai", kind="system",
         fr=fr(70), old=[261]),
    # ---- システム起点 / usage (UC-056..061) ----
    dict(name="システムが利用量をリアルタイム集計する", actor="システム", group="usage", kind="system",
         fr=fr(87,93), old=[239]),
    dict(name="システムが質問数上限アラートを通知する", actor="システム", group="usage", kind="system",
         fr=fr(34,93,94), old=[237,251]),
    dict(name="システムが上限到達時にウィジェット受付を停止する", actor="システム", group="usage", kind="system",
         fr=fr(87,89), old=[240]),
    dict(name="システムが月次請求を確定する", actor="システム", group="usage", kind="system",
         fr=fr(87,121), old=[233]),
    dict(name="システムが決済失敗から猶予を経てサスペンションへ移行する", actor="外部システム", group="usage", kind="system",
         fr=fr(91,97,98), old=[241]),
    dict(name="システムが課金プロバイダ通知を受信・検証・再処理する", actor="外部システム", group="usage", kind="system",
         fr=fr(99), old=[264]),
    # ---- システム起点 / widget (UC-062) ----
    dict(name="システムが許可ドメイン上でのみウィジェットを動作させる", actor="システム", group="widget", kind="system",
         fr=fr(127), old=[274]),
    # ---- システム起点 / notification (UC-063..070) ----
    dict(name="システムがメール配信状態のWebhookを処理する", actor="外部システム", group="notification", kind="system",
         fr=fr(115,124), old=[231]),
    dict(name="システムが運営お知らせを配信する", actor="システム", group="notification", kind="system",
         fr=fr(122,155), old=[234]),
    dict(name="システムが運用イベントの通知を自動生成する", actor="システム", group="notification", kind="system",
         fr=fr(113,123), old=[235]),
    dict(name="システムがメンバー割当変更を通知する", actor="システム", group="notification", kind="system",
         fr=fr(13,14,16,17,35,125), old=[236]),
    dict(name="システムが配信失敗通知を再送する", actor="システム", group="notification", kind="system",
         fr=fr(114,120), old=[238]),
    dict(name="システムが受信箱の重複お知らせを集約する", actor="システム", group="notification", kind="system",
         fr=fr(162,163,164), old=[246]),
    dict(name="システムがアカウント認証関連通知をオプトアウト不可で送信する", actor="システム", group="notification", kind="system",
         fr=fr(116), old=[270]),
    dict(name="システムが送信指標を監視して送信を抑制する", actor="システム", group="notification", kind="system",
         fr=fr(117), old=[271]),
    # ---- システム起点 / security (UC-071..077) ----
    dict(name="システムが90日経過データを物理削除する", actor="システム", group="security", kind="system",
         fr=fr(138), old=[232]),
    dict(name="システムがセッション失効を判定し再認証へ誘導する", actor="システム", group="security", kind="system",
         fr=fr(5,8), old=[242]),
    dict(name="システムがログイン失敗をロックアウトし解除する", actor="システム", group="security", kind="system",
         fr=fr(7), old=[243]),
    dict(name="システムが契約停止時にセッションを一斉無効化する", actor="システム", group="security", kind="system",
         fr=fr(8,11), old=[244]),
    dict(name="システムが監査ログの整合性を日次検証する", actor="システム", group="security", kind="system",
         fr=fr(147,151), old=[247]),
    dict(name="システムが契約単位のレート制限を適用する", actor="システム", group="security", kind="system",
         fr=fr(95), old=[263]),
    dict(name="システムがウィジェット入力を外部露出箇所からサニタイズする", actor="システム", group="security", kind="system",
         fr=fr(118), old=[272]),
    # ---- 要件起点 / account (UC-078..079) ----
    dict(name="オーナーが契約専有機能を実行する", actor="オーナー", group="account", kind="requirement",
         fr=fr(15), old=[248]),
    dict(name="システムがプロジェクト削除時にメンバー割当を解除する", actor="システム", group="account", kind="requirement",
         fr=fr(39), old=[253]),
    # ---- 要件起点 / faq-ai (UC-080..083) ----
    dict(name="管理者がプロジェクト範囲のFAQ・質問ログ・未解決質問を扱う", actor="プロジェクト管理者", group="faq-ai", kind="requirement",
         fr=fr(41), old=[254]),
    dict(name="利用者がプロジェクト削除時の関連データ取扱いを選択する", actor="オーナー", group="faq-ai", kind="requirement",
         fr=fr(45), old=[255]),
    dict(name="管理者が信頼度・関連度しきい値を3階層で調整する", actor="プロジェクト管理者", group="faq-ai", kind="requirement",
         fr=fr(62), old=[258]),
    dict(name="管理者がFAQ・質問ログを検索する", actor="プロジェクト管理者", group="faq-ai", kind="requirement",
         fr=fr(168), old=[281]),
    # ---- 要件起点 / notification (UC-084..088) ----
    dict(name="管理者が通知失敗・バウンス件数を確認する", actor="プロジェクト管理者", group="notification", kind="requirement",
         fr=fr(104), old=[268]),
    dict(name="管理者が通知配信状態を確認する", actor="プロジェクト管理者", group="notification", kind="requirement",
         fr=fr(119), old=[273]),
    dict(name="システムがお知らせをアカウント利用者のみに表示する", actor="システム", group="notification", kind="requirement",
         fr=fr(161), old=[277]),
    dict(name="システムがお知らせ受信箱を利用者ごとに保持し退会時に削除する", actor="システム", group="notification", kind="requirement",
         fr=fr(165), old=[278]),
    dict(name="システムが未読件数を遷移時に取得し更新する", actor="システム", group="notification", kind="requirement",
         fr=fr(166), old=[279]),
]


def uc(n):
    return f"UC-{n:03d}"


def parse_rule_applyuc():
    """08_rule.md を解析し RULE-NNN -> [旧UC番号...] を返す。"""
    t = open(RULEFILE, encoding="utf-8").read()
    blocks = re.split(r'(?=^###\s+<span id="RULE-)', t, flags=re.M)
    out = {}
    for b in blocks:
        m = re.search(r'id="(RULE-\d+)"', b)
        if not m:
            continue
        rid = m.group(1)
        nums = sorted({int(x) for x in re.findall(r'(?<![A-Za-z0-9])UC-(\d+)(?![0-9])', b)})
        out[rid] = nums
    return out


def main():
    # 1. クロスウォーク構築 + 被覆検証
    old_to_new, new_to_old, meta = {}, {}, {}
    for i, c in enumerate(CATALOG, start=1):
        nid = uc(i)
        new_to_old[nid] = [uc(o) for o in c["old"]]
        meta[nid] = dict(name=c["name"], actor=c["actor"], group=c["group"], kind=c["kind"], fr=c["fr"])
        for o in c["old"]:
            assert uc(o) not in old_to_new, f"旧 {uc(o)} が重複割当"
            old_to_new[uc(o)] = nid

    covered = sorted(int(k.split("-")[1]) for k in old_to_new)
    expected = list(range(1, 282))
    assert covered == expected, (
        f"被覆不一致: 欠落={sorted(set(expected)-set(covered))} / 余剰={sorted(set(covered)-set(expected))}")
    assert len(CATALOG) == 88, f"新UC件数 {len(CATALOG)} != 88"

    # 2. RULE -> 新UC
    rule_old = parse_rule_applyuc()
    new_rules = {nid: [] for nid in new_to_old}
    for rid, olds in rule_old.items():
        for o in olds:
            nid = old_to_new.get(uc(o))
            if nid and rid not in new_rules[nid]:
                new_rules[nid].append(rid)
    for nid in meta:
        meta[nid]["rule"] = sorted(new_rules[nid])

    # 3. 出力
    data = dict(version=2, count=len(CATALOG),
                old_to_new=old_to_new,
                new_to_old=new_to_old,
                meta=meta)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    # サマリ
    by_kind = {}
    for c in CATALOG:
        by_kind[c["kind"]] = by_kind.get(c["kind"], 0) + 1
    print(f"OK: {len(CATALOG)} business UCs cover old UC-001..281 exactly once")
    print("  kind:", by_kind)
    print("  RULE mapped:", sum(1 for nid in meta if meta[nid]["rule"]), "UCs have RULE")
    print("  output:", OUT)


if __name__ == "__main__":
    main()
