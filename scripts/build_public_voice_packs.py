"""Pack source-verified MP3 recordings into small, lazily loaded public-preview JS bundles.

The public preview remains independent of the private repository. Only code-free
base64 MP3 bytes and their source ID keys are included; cue metadata stays in
the separate verified data/pattern-audio-index.json.
"""
import base64
import hashlib
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]
INDEX=ROOT/"data/pattern-audio-index.json"
DEST=ROOT/"assets/pattern-audio-bundles"
SIZE=32

def pack_start(id):
    return 4 + ((id-4)//SIZE)*SIZE

def main():
    index=json.loads(INDEX.read_text(encoding="utf-8"))
    rows=index.get("items",{})
    if not rows:raise RuntimeError("No verified voices")
    DEST.mkdir(parents=True,exist_ok=True)
    bundles={}
    for sid,entry in rows.items():
        id=int(sid)
        if id<4:continue
        file=ROOT/entry["path"]
        payload=file.read_bytes()
        if hashlib.sha256(payload).hexdigest()!=entry["audio_sha256"]:
            raise RuntimeError("MP3 source hash mismatch: "+sid)
        bundles.setdefault(pack_start(id),{})[sid]=base64.b64encode(payload).decode("ascii")
    for start,items in sorted(bundles.items()):
        # The assignment only contains user-supplied learning text IDs -> MP3 data,
        # not arbitrary code sourced from the language corpus.
        js="window.LE_PATTERN_AUDIO=Object.assign(window.LE_PATTERN_AUDIO||{}, "+json.dumps(items,separators=(",",":"))+");\n"
        (DEST/f"pack-{start:04d}.js").write_text(js,encoding="utf-8")
    manifest={"schema":1,"pack_span":SIZE,"packs":[{"start":n,"ids":list(v)} for n,v in sorted(bundles.items())],
              "recorded_unique_count":sum(len(v) for v in bundles.values())}
    (DEST/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
    print("Packed",manifest["recorded_unique_count"],"source-verified recordings into",len(bundles),"lazy bundles")

if __name__=="__main__":main()
