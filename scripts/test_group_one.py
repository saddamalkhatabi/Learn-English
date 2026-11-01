"""Content and assets checks for Group One. Run with python scripts/test_group_one.py."""
import hashlib
import json
import pathlib
import re

root=pathlib.Path(__file__).resolve().parents[1]
pack=json.loads((root/"data/group-one.json").read_text(encoding="utf-8"))
assert pack["schema"]==1 and len(pack["items"])==18
assert [p["id"] for p in pack["items"]]==list(range(1,19))
assert len({p["key"] for p in pack["items"]})==18
assert all(p["formula"] and p["meaning"] and p["explanation"] and p["explanationEn"]
           and p["contrast"] and p["sourceIds"] for p in pack["items"])
assert all(len(p["scenes"])==4 and len(p["story"])==3
           and len(p["dialogue"])==2 for p in pack["items"])
for p in pack["items"]:
    assert len({x["en"] for x in p["scenes"]})==4, p["key"]
    for item in p["scenes"]+p["story"]+p["dialogue"]:
        assert item["en"].strip() and item["ar"].strip(), p["key"]
        assert not any(ord(c) in range(0x600,0x700) for c in item["en"]),p["key"]
    assert all(s["context"] and s["icon"] for s in p["scenes"])
    assert all(x["speaker"] in ("A","B") for x in p["dialogue"])
known=json.loads((root/"data/patterns.json").read_text(encoding="utf-8"))["patterns"]
ids={p["id"] for p in known}
assert all(set(p["sourceIds"])<=ids for p in pack["items"])
pictures=json.loads((root/"assets/real-scenes/manifest.json").read_text(encoding="utf-8"))["files"]
for p in pack["items"]:
    for scene in p["scenes"]:
        if scene.get("photo"):
            book,tile=scene["photo"]
            assert scene["en"]==pictures[book]["tiles"][tile]["english"],(p["key"],scene["en"])
recorded=json.loads((root/"data/group-one-audio-index.json").read_text(encoding="utf-8"))
assert recorded["schema"]==1
words={}
for p in pack["items"]:
    stem=f"p{p['id']:02d}"
    words[f"{stem}/intro"]=p["explanationEn"]
    for kind,rows in (("scene",p["scenes"]),("story",p["story"]),("dialogue",p["dialogue"])):
        for entry in rows:
            words[f"{stem}/{kind}-{entry['id']}"]=entry["en"]
assert len(words)==180
for key,v in recorded["items"].items():
    assert key in words and v["text"]==words[key]
    path=root/v["path"]
    assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==v["audio_sha256"]
    cues=v["cues"]
    assert len(cues)==len(v["text"].split())
    assert all(c[0]==i and 0<=c[1]<c[2]<=v["duration_ms"]+45 for i,c in enumerate(cues))
    assert all(cues[i-1][2]<=cues[i][1] for i in range(1,len(cues)))
for name in ("index.html","app.js","group-one.js"):
    assert (root/name).is_file()
html=(root/"index.html").read_text(encoding="utf-8")
for id_ in ("view-group-one","g1PatternList","g1QuizOptions","g1BankWords","g1StoryList"):
    assert f'id="{id_}"' in html
print(f"OK: {len(pack['items'])} patterns, {sum(len(x['scenes']) for x in pack['items'])} scenes, "+
      f"{sum(len(x['story']) for x in pack['items'])} story lines, "+
      f"{sum(len(x['dialogue']) for x in pack['items'])} dialogues, "+
      f"{len(recorded['items'])} verified group voice files")
