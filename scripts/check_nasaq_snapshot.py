"""Verify the exact published Sites snapshot and both voices without model downloads."""
import hashlib,json,pathlib,zipfile
root=pathlib.Path(__file__).resolve().parents[1]/"nasaq"
snapshot=json.loads((root/"SITE-SNAPSHOT.json").read_text())
for entry in snapshot["files"]:
 data=(root/entry["path"]).read_bytes()
 actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 assert actual==entry["sha"],entry["path"]
count=0
for name in ["pilot.json","supplement.json"]:
 manifest=json.loads((root/"dist"/name).read_text())
 for sentence in manifest["sentences"]:
  assert set(sentence["recordings"])=={"male","female"}
  for recording in sentence["recordings"].values():
   data=(root/"dist"/recording["path"]).read_bytes()
   assert hashlib.sha256(data).hexdigest()==recording["sha256"]
   words=recording["words"]
   assert len(words)==len(sentence["en"].split())
   assert [word["text"] for word in words]==sentence["en"].split()
   assert all(0<=w["start_ms"]<w["end_ms"]<=recording["duration_ms"]+45 for w in words)
   count+=1
assert count==340,count
index=json.loads((root/"dist/generation-index.json").read_text())
with zipfile.ZipFile(root/"dist/downloads/nasaq-media-library-20261102.zip") as archive:
 for path,expected in index["files"].items():
  assert hashlib.sha256(archive.read("dist/"+path)).hexdigest()==expected,path
print(f"PASS: {len(snapshot['files'])} exact published source files; {count} MP3s and independent word timings; ZIP hashes")

