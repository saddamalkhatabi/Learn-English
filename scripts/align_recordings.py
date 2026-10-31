"""Align ORIGINAL committed Kokoro MP3s to their exact scripted English text.

Ported from app360's my-little-routine MMS_FA acoustic forced aligner.
No duration-weighted estimates and no re-synthesis; source audio SHA-256 is recorded.
Run only after all voice files are committed; uncertain clips fail closed.
"""
import hashlib, json, pathlib, re, unicodedata
import numpy as np
import soundfile as sf
import torch, torchaudio
from uroman import Uroman

ROOT = pathlib.Path(__file__).resolve().parents[1]
LESSONS = json.loads((ROOT/"data/lessons.json").read_text(encoding="utf-8"))["lessons"]
STORIES = json.loads((ROOT/"data/stories.json").read_text(encoding="utf-8"))["lessons"]
DEST = ROOT/"data/audio-word-cues.json"
bundle = torchaudio.pipelines.MMS_FA
torch.set_num_threads(4)
model = bundle.get_model().eval()
tokenizer = bundle.get_tokenizer()
aligner = bundle.get_aligner()
roman = Uroman()

def corpus():
    rows = {}
    for lesson in LESSONS:
        lid = lesson["id"]
        base = "assets/audio/"+lid+"/"
        rows[base+"intro.mp3"] = lesson["explanationEn"]
        for level_idx, level in enumerate(lesson["levels"], 1):
            for scene_idx, scene in enumerate(level["scenes"], 1):
                rows[base+f"scene-{level_idx}-{scene_idx}.mp3"] = scene["en"]
        story = STORIES[lid]
        for chapter_idx, chapter in enumerate(story["levels"], 1):
            for line_idx, line in enumerate(chapter["lines"], 1):
                rows[base+f"story-{chapter_idx}-{line_idx}.mp3"] = line["en"]
        for i, turn in enumerate(story["dialogue"], 1):
            rows[base+f"dialogue-{i}.mp3"] = turn["en"]
    if len(rows) != 96:
        raise ValueError(f"Expected exactly 96 recorded clips, got {len(rows)}")
    return rows

def normalized(word):
    basic = "".join(c for c in unicodedata.normalize("NFKD",word)
                    if not unicodedata.combining(c))
    return re.sub("[^a-z]","",roman.romanize_string(basic).lower())

def align(path, text):
    audio = ROOT/path
    contents = audio.read_bytes()
    digest = hashlib.sha256(contents).hexdigest()
    words = text.split()
    norms = [normalized(w) for w in words]
    if not words or not all(norms):
        raise ValueError(f"Unalignable tokens in {path}: {text}")
    samples, sr = sf.read(audio, dtype="float32")
    if len(samples.shape) == 2:
        samples = np.mean(samples,axis=1)
    wave = torchaudio.functional.resample(
        torch.from_numpy(samples.copy()).unsqueeze(0),sr,bundle.sample_rate)
    with torch.inference_mode():
        emissions, _ = model(wave)
        spans = aligner(emissions[0], tokenizer(norms))
    if len(spans)!=len(norms) or any(not g for g in spans):
        raise ValueError(f"Incomplete forced alignment: {path}")
    ms_per_frame = wave.shape[1]/emissions.shape[1]/bundle.sample_rate*1000
    cues = []
    for i, group in enumerate(spans):
        start=round(group[0].start*ms_per_frame)
        end=round(group[-1].end*ms_per_frame)
        cues.append([i,start,end])
    duration=round(len(samples)/sr*1000)
    if any(not (0<=c[1]<c[2]<=duration+30) for c in cues):
        raise ValueError(f"Out-of-duration timestamps: {path}")
    if any(cues[i-1][2]>cues[i][1] for i in range(1,len(cues))):
        raise ValueError(f"Overlapping timestamps: {path}")
    return {"text":text,"language":"en","audio_sha256":digest,
            "duration_ms":duration,"cues":cues,
            "timing_source":"MMS_FA acoustic forced alignment of exact original Kokoro MP3"}

def main():
    rows=corpus()
    existing={}
    if DEST.exists():
        try: existing=json.loads(DEST.read_text(encoding="utf-8")).get("items",{})
        except Exception: existing={}
    results={}
    for i,(path,text) in enumerate(rows.items(),1):
        digest=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        old=existing.get(path)
        if old and old.get("audio_sha256")==digest and old.get("text")==text:
            results[path]=old
        else:
            results[path]=align(path,text)
        if i%8==0:print(f"Acoustic word alignment: {i}/{len(rows)}", flush=True)
    out={"schema":1,"generated_from":"original committed Kokoro MP3s",
         "items":results,"total_recordings":len(results)}
    DEST.write_text(json.dumps(out,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
    print("VERIFIED:",len(results),"recordings,",sum(len(x["cues"]) for x in results.values()),"words")

if __name__=="__main__":
    main()
