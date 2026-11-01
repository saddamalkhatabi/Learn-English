"""Verify authored Group Six content and actual audio where available."""
import hashlib
import json
import pathlib
import sys

root=pathlib.Path(__file__).resolve().parents[1]
pack=json.loads((root/"data/group-six.json").read_text(encoding="utf-8"))
assert pack["schema"]==1 and len(pack["items"])==18
assert [p["id"] for p in pack["items"]]==list(range(1,19))
assert len({p["key"] for p in pack["items"]})==18
known=json.loads((root/"data/patterns.json").read_text(encoding="utf-8"))["patterns"]
ids={p["id"] for p in known}
expected={}
for p in pack["items"]:
    assert p["formula"] and p["meaning"] and p["explanation"] and p["explanationEn"] and p["contrast"]
    assert p["sourceIds"] and set(p["sourceIds"])<=ids
    assert len(p["scenes"])==4 and len(p["story"])==3 and len(p["dialogue"])==2
    assert len({s["en"] for s in p["scenes"]})==4
    assert all(s["photo"] is None and s["icon"] and s["context"] for s in p["scenes"])
    assert all(d["speaker"] in ("A","B") for d in p["dialogue"])
    stem=f"p{p['id']:02d}"
    expected[f"{stem}/intro"]=p["explanationEn"]
    for kind,rows in (("scene",p["scenes"]),("story",p["story"]),("dialogue",p["dialogue"])):
        for item in rows:
            assert item["en"] and item["ar"]
            assert not any("\u0600"<=c<="\u06ff" for c in item["en"])
            expected[f"{stem}/{kind}-{item['id']}"]=item["en"]
chapters=pack["chapters"]
assert len(chapters)==3 and [c["key"] for c in chapters]==["the-weekend-plan","the-school-project","the-journey-home"]
for chapter in chapters:
    assert len(chapter["lines"])==6
    for line in chapter["lines"]:
        assert line["en"] and line["ar"]
        expected[f"chapters/c{chapter['id']:02d}/line-{line['id']}"]=line["en"]
assert len(expected)==198
# Narration must contain pronounceable words; a standalone + or / cannot get a real WordBoundary.
for clip_id, spoken in expected.items():
    assert all(any(c.isalnum() for c in token) for token in spoken.split()), (clip_id, spoken)
index=json.loads((root/"data/group-six-audio-index.json").read_text(encoding="utf-8"))
assert index["schema"]==1 and index.get("verified_count")==len(index["items"])
sources=[]
for name in ("data/audio-word-cues.json","data/pattern-audio-index.json"):
    rows=json.loads((root/name).read_text(encoding="utf-8"))["items"]
    sources.extend((k if k.endswith(".mp3") else v.get("path"),v) for k,v in rows.items())
missing=[]
reused=0
for key,sentence in expected.items():
    row=index["items"].get(key)
    path=row.get("path") if row else None
    if not row:
        matches=[(p,r) for p,r in sources if r.get("text")==sentence and p]
        if matches:
            path,row=matches[0]
            reused+=1
        else:
            missing.append(key)
            continue
    assert row.get("text")==sentence,key
    file=root/path
    assert file.is_file(),str(file)
    assert hashlib.sha256(file.read_bytes()).hexdigest()==row["audio_sha256"],path
    cues=row["cues"]
    assert len(cues)==len(sentence.split()),key
    assert all(c[0]==i and 0<=c[1]<c[2]<=row["duration_ms"]+45 for i,c in enumerate(cues)),key
    assert all(cues[i-1][2]<=cues[i][1] for i in range(1,len(cues))),key
assert not(set(index["items"])-set(expected))
html=(root/"index.html").read_text(encoding="utf-8")
app=(root/"app.js").read_text(encoding="utf-8")
for token in ('id="view-group-six"','id="g6PatternList"','id="g6QuizOptions"','id="g6BankWords"','id="g6ChapterTabs"','src="group-six.js"','data-view="group-four"','data-view="group-three"'):
    assert token in html,token
assert "GROUP_SIX?.open" in app and "GROUP_SIX?.stop" in app
if "--require-audio" in sys.argv:
    assert not missing,f"Missing verified audio for {len(missing)} clips: {missing[:12]}"
print(f"OK: 18 patterns, 72 scenes, 54 pattern-story lines, 36 dialogues, 18 chapter lines; audio {198-len(missing)}/198 verified ({len(index['items'])} dedicated + {reused} reused), {len(missing)} pending")
