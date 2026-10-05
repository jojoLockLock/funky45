import json,base64,io,html
from PIL import Image
from data import ROWS
from picks import YT, SP, SIDE_NOTE
rel=json.load(open("releases.json")); ch=json.load(open("chosen.json")); oe=json.load(open("oembed.json"))
IMG={1:1,2:0,3:1,4:0,5:0,6:2,7:1,8:0,9:1,10:0,11:1,12:0,13:0,14:0,15:0,16:1,17:0,18:0,19:1,20:2,21:0,22:1,23:0,24:0,25:1,26:0,27:1,28:0,29:0,30:0,31:0,32:0,33:1,34:0,35:0,36:0,37:1,38:1,39:1,40:0,41:1,42:0,43:0,44:1,45:0,46:0,47:1}
MATCHNOTE={
1:"Discogs：拆分单曲 Abraham And The Metronomes / Illinois Connection – Party / Po' Boy's Dream (FUNK45.020)",
15:"YouTube：Melting Pot Music 官方自动生成的 “On the Run · Imperial Breed”（已确认）",
18:"YouTube：该视频来自 D-W 6901 版本的 “Zip-A-Doe-Do-Dah”（同为 2:30），推测为同一录音",
19:"Discogs B 面全名：My Baby (Just Told Me She Loves Me)",
24:"Discogs B 面：We Must Be In Love",
26:"Discogs 编号为 K67M17（书中 #K76M17）；视频标注 1976 录音",
27:"Discogs 编号：K76M17A / K76M19A",
29:"Discogs 无编号，matrix VMFRP-1289 对应",
31:"YouTube 视频含 Pt.1 & 2",
35:"Discogs 普通版（matrix 32517/32518）；THT 20001 promo 为 release 1175804；视频含 Part I & II",
36:"Rudi Johnson Trio 版本：Discogs release 14825056",
39:"Discogs 年份 2011",
40:"Discogs 署名 The Identities，年份 1970",
43:"Discogs 厂牌 Dandit Production Co.，年份 1976",
44:"Discogs：A=Sapphire，B=Shoes",
46:"Discogs 署名 The Infinity Featuring Billy Butler；A=That Ain't Water…，B=Soulation；仅有该面盘面图",
6:"YouTube 只找到 Part 1 片段（另一面）",
11:"YouTube 只找到 A 面 Pushin' to the top",
34:"YouTube 只找到 Part II（另一面）",
45:"盘面图为 A 面（Discogs 仅一张）",
42:"盘面图为 A 面（Discogs 仅一张）",
}
def b64img(path,w=320):
    im=Image.open(path).convert("RGB"); im.thumbnail((w,w),Image.LANCZOS)
    buf=io.BytesIO(); im.save(buf,"JPEG",quality=82,optimize=True)
    return "data:image/jpeg;base64,"+base64.b64encode(buf.getvalue()).decode()
# videos that are age-restricted / not embeddable (checked with yt-dlp -J: age_limit, playable_in_embed); none as of 2026-10-05
NOEMBED=set()
def yt(v):
    if not v: return None
    t=oe.get(v,[0,["",""]])[1]
    d={"id":v,"title":t[0],"channel":t[1]}
    if v in NOEMBED: d["noEmbed"]=True
    return d
out=[]
for r in ROWS:
    id_,artist,a,b,year,label,cat,tune,rating,ref,notes=r
    f=YT[id_]
    k=ch.get(str(id_)); d=rel[k] if k else None
    rec={"page":1,"n":id_,"artist":artist,"a":a,"b":b,"year":year,"label":label,"cat":cat,"tune":tune,"rating":rating,"ref":ref,"notes":notes,
         "match":MATCHNOTE.get(id_,""),
         "discogs":None,"discogsSearch":"https://www.discogs.com/search/?type=release&q="+__import__("urllib.parse").parse.quote(f"{artist} {a if not a.startswith('.') else b}")}
    fside="A" if tune=="A1" else "B"
    for side in ("A","B"):
        v=f[0] if side==fside else f[2]
        y=yt(v)
        if y:
            so={"src":"yt",**y}
            if side==fside and f[1]=="?": so["uncertain"]=True
        elif (id_,side) in SP:
            t=SP[(id_,side)]; so={"src":"sp","id":t[0],"title":t[1],"channel":t[2]}
        else:
            so={"src":None}
        if (id_,side) in SIDE_NOTE: so["note"]=SIDE_NOTE[(id_,side)]
        rec[side]=so
    if d:
        i=IMG[id_]
        rec["discogs"]={"id":int(k),"url":f"https://www.discogs.com/release/{k}","title":f"{d['artists']} – {d['title']}","year":d["year"],"country":d["country"],
            "labels":"; ".join(f"{l} – {c}" for l,c in d["labels"]),"img":b64img(f"full/{id_}_{k}_{i}.jpg")}
    out.append(rec)
json.dump(out,open("records_p1.json","w"),ensure_ascii=False)
tpl=open("template.html",encoding="utf-8").read()
js=json.dumps(out,ensure_ascii=False).replace("</","<\\/")
open("funky45_p1.html","w",encoding="utf-8").write(tpl.replace("/*__DATA__*/[]",js))
import collections
c=collections.Counter(x[sd]["src"] for x in out for sd in "AB")
print("sides",dict(c),"discogs",sum(1 for x in out if x["discogs"]))
print("missing",[(x["n"],sd,x["a"] if sd=="A" else x["b"]) for x in out for sd in "AB" if not x[sd]["src"]])
