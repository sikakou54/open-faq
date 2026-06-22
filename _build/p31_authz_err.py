import re
E="02_basic_design/07_errors"
# 1. taxonomy in individual ERR files
tax={"015":"E-AUTH-REAUTH-REQUIRED","019":"E-AUTHZ-OWNER-BOUNDARY","021":"E-AUTHZ-PROJECT-DENIED"}
for n,code in tax.items():
    p=f"{E}/ERR-{n}.md"; s=open(p,encoding="utf-8").read()
    s2=s.replace("| 分類コード(taxonomy) | — |", f"| 分類コード(taxonomy) | `{code}` |",1)
    assert s2!=s, n
    open(p,"w",encoding="utf-8").write(s2)
# 2. create ERR-036 SESSION_EXPIRED
err036='''<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [エラー設計](index.md) ／ **ERR-036: SESSION_EXPIRED**
<!-- /portal-top -->

# <span id="ERR-036"></span>ERR-036: SESSION_EXPIRED

> **このページは API レスポンスで返すエラー `SESSION_EXPIRED` の HTTP ステータス・分類・メッセージ・対応 API / EVT を定義します。**

*種別 エラー定義 ・ 分類 認証 ・ ステータス ドラフト*

## <span id="def"></span>1. 定義

| 項目 | 値 |
|----|----|
| エラーコード | `SESSION_EXPIRED` |
| 分類コード(taxonomy) | `E-AUTH-SESSION-EXPIRED` |
| HTTP ステータス | 401 |
| エラー分類 | 認証 |

## <span id="msg"></span>2. メッセージ

セッションの有効期限が切れました。再度ログインしてください。

## <span id="trace"></span>3. 対応 API / EVT

認可ミドルウェアのセッション検証段（[PERM-002](../06_permissions/PERM-002.md#PERM-002) 段1）が全認証保護 API 共通で返す。特定 API / EVT には紐づかない横断エラー。

| 観点 | 結線 |
|----|----|
| 対応 API | 全認証保護 API 共通（横断） |
| 対応 EVT | — |

---

<!-- portal-bottom -->
[← エラー設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
'''
open(f"{E}/ERR-036.md","w",encoding="utf-8").write(err036)
# 3. update index: taxonomy in rows + count + ERR-036 row + mapping note
ip=f"{E}/index.md"; s=open(ip,encoding="utf-8").read()
s=s.replace("`REAUTH_REQUIRED` | — |","`REAUTH_REQUIRED` | `E-AUTH-REAUTH-REQUIRED` |")
s=s.replace("`NOT_FOUND` | — | オーナー境界違反偽装","`NOT_FOUND` | `E-AUTHZ-OWNER-BOUNDARY` | オーナー境界違反偽装")
s=s.replace("`PROJECT_ACCESS_DENIED` | — |","`PROJECT_ACCESS_DENIED` | `E-AUTHZ-PROJECT-DENIED` |")
s=s.replace("## <span id=\"list\"></span>1. エラーコード一覧(35)","## <span id=\"list\"></span>1. エラーコード一覧(36)")
# append ERR-036 row after ERR-035 row
row035=[l for l in s.splitlines() if l.startswith("| <span id=\"ERR-035\">")][0]
row036='| <span id="ERR-036"></span>[ERR-036](ERR-036.md#ERR-036) | 認証 | 401 | `SESSION_EXPIRED` | `E-AUTH-SESSION-EXPIRED` | セッション期限切れ(再ログインへ) |'
s=s.replace(row035, row035+"\n"+row036)
open(ip,"w",encoding="utf-8").write(s)
print("done. ERR-036 created, taxonomy set, index updated.")
