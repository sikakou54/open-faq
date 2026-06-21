#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P6b: 削除する 07_auth-design.md / 06_mail-design.md への全リンクを新移管先へ張替える。
- 認証・認可設計書(07_auth-design.md)→ 06_permissions/(PERM)
- メール設計書(06_mail-design.md)→ 08_messages/(MSG / index)
リポジトリ全 .md(削除対象自身は除く)を走査して置換する。冪等。ルートで実行する。
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

AUTH = "07_auth-design.md"
MAIL = "06_mail-design.md"
PERM_DIR = "02_basic_design/06_permissions"
MSG_DIR = "02_basic_design/08_messages"

# auth-design のアンカー → PERM 移管先(ファイル名 + アンカー)
AUTH_ANCHOR = {
    "57-契約状態によるアクセス制限": ("06_permissions/PERM-009.md", "PERM-009"),
    "41-ログイン失敗ロックアウト":   ("06_permissions/PERM-007.md", "PERM-007"),
    "42-失効の優先順位":             ("06_permissions/PERM-007.md", "PERM-007"),
    "4-セッション設計":              ("06_permissions/PERM-007.md", "PERM-007"),
    "2-再認証":                      ("06_permissions/PERM-006.md", "PERM-006"),
    "5-認可モデルと判定フロー":       ("06_permissions/index.md", None),
    "53-認可判定の順序":             ("06_permissions/PERM-002.md", "PERM-002"),
    "54-オーナー保護自己操作最後の管理者保護": ("06_permissions/PERM-004.md", "PERM-004"),
    "55-通知宛先解決":               ("06_permissions/PERM-011.md", "PERM-011"),
    "6-規約再同意の認可割込み":       ("06_permissions/PERM-010.md", "PERM-010"),
}
AUTH_LABEL = {  # 移管先の表示ラベル(リンクテキスト差し替え用、§ 記述は権限設計へ)
    "PERM-002": "権限設計 PERM-002 認可判定の順序",
    "PERM-004": "権限設計 PERM-004 オーナー保護・自己操作禁止",
    "PERM-006": "権限設計 PERM-006 重要操作の再認証",
    "PERM-007": "権限設計 PERM-007 セッションとログイン失敗ロックアウト",
    "PERM-009": "権限設計 PERM-009 契約状態によるアクセス制限",
    "PERM-010": "権限設計 PERM-010 規約再同意の認可割込み",
    "PERM-011": "権限設計 PERM-011 critical 通知の宛先解決",
}

def rel(frm_dir, to):
    return os.path.relpath(to, frm_dir).replace(os.sep, "/")

LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]*?)(07_auth-design\.md|06_mail-design\.md)(#[^)]*)?\)')

def rewrite_file(path):
    s = open(path, encoding="utf-8").read()
    d = os.path.dirname(path)
    changed = False

    def repl(m):
        nonlocal changed
        label, prefix, target, frag = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        anchor = frag[1:] if frag else ""
        if target == AUTH:
            if anchor in AUTH_ANCHOR:
                tofile, toanchor = AUTH_ANCHOR[anchor]
            else:
                tofile, toanchor = "06_permissions/index.md", None
            newlabel = label
            if toanchor and AUTH_LABEL.get(toanchor):
                # 「認証・認可設計書 §x.y」というラベルを権限設計の対応ラベルへ
                if "認証・認可設計書" in label or "認証" in label:
                    newlabel = AUTH_LABEL[toanchor]
            else:
                if "認証・認可設計書" in label:
                    newlabel = "権限設計"
            newpath = rel(d, tofile)
            newfrag = f"#{toanchor}" if toanchor else ""
        else:  # MAIL
            tofile = "08_messages/index.md"
            toanchor = None
            newlabel = label
            if "メール設計書" in label:
                newlabel = "メッセージ設計"
            newpath = rel(d, tofile)
            newfrag = ""
        changed = True
        return f"[{newlabel}]({newpath}{newfrag})"

    s2 = LINK_RE.sub(repl, s)
    if s2 != s:
        open(path, "w", encoding="utf-8").write(s2)
        return True
    return False

def main():
    files = []
    for g in ("01_requirements", "02_basic_design", "03_future"):
        files += glob.glob(f"{g}/**/*.md", recursive=True)
    files.append("README.md")
    files = sorted(set(files))
    n = 0
    for f in files:
        bn = os.path.basename(f)
        if bn in (AUTH, MAIL):
            continue  # 削除対象自身はスキップ
        if rewrite_file(f):
            n += 1
            print("relinked:", f)
    print("files relinked:", n)

if __name__ == "__main__":
    main()
