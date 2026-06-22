ip="02_basic_design/08_messages/index.md"
s=open(ip,encoding="utf-8").read()
reps=[
 ('id="51-配信先解決ロジック"></span>5.1 ','id="31-配信先解決ロジック"></span>3.1 '),
 ('id="52-重要度別の強制送信ルール共有概念正本"></span>5.2 ','id="32-重要度別の強制送信ルール共有概念正本"></span>3.2 '),
 ('id="53-重複配信抑止"></span>5.3 ','id="33-重複配信抑止"></span>3.3 '),
 ('id="54-配信ログ"></span>5.4 ','id="34-配信ログ"></span>3.4 '),
 ('id="55-テスト送信"></span>5.5 ','id="35-テスト送信"></span>3.5 '),
 ('id="61-新規テンプレート追加手順"></span>6.1 ','id="41-新規テンプレート追加手順"></span>4.1 '),
 ('id="62-既存テンプレート変更手順"></span>6.2 ','id="42-既存テンプレート変更手順"></span>4.2 '),
 ('本書 §5.1 / §5.2 +','本書 §3.1 / §3.2 +'),
]
for a,b in reps:
    assert a in s, f"MISS: {a}"
    s=s.replace(a,b)
open(ip,"w",encoding="utf-8").write(s)
# MSG-012 textual ref
mp="02_basic_design/08_messages/MSG-012.md"
m=open(mp,encoding="utf-8").read()
assert "§5.2 のルールに従う" in m
open(mp,"w",encoding="utf-8").write(m.replace("§5.2 のルールに従う","§3.2 のルールに従う"))
print("MSG renumber done")
