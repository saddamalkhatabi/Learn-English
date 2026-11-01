"""Generate source-faithful pattern speech and SAME-SYNTHESIS word cues.

Only a successfully synthesized MP3 + real WordBoundary metadata pair is written
to the audio index. Never estimate timings from sentence or word length.
"""
import argparse
import asyncio
import hashlib
import json
import pathlib
import re
import subprocess
import unicodedata
import edge_tts

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = json.loads((ROOT / "data/patterns.json").read_text(encoding="utf-8"))["patterns"]
OUT = ROOT / "assets/pattern-audio"
INDEX = ROOT / "data/pattern-audio-index.json"
VOICE = "en-US-JennyNeural"
RATE = "-10%"

def normalize(text):
    return "".join(c.lower() for c in unicodedata.normalize("NFKD", text)
                   if c.isalnum() and not unicodedata.combining(c))

def cue_words(text, boundaries, duration):
    parts = re.findall(r"\S+", text)
    normal_parts = [normalize(p) for p in parts]
    if not parts or any(not p for p in normal_parts):
        raise ValueError("Unalignable transcript: " + text)
    flat = "".join(normal_parts)
    cursor = 0
    spans = {}
    for item in boundaries:
        if item.get("type") != "WordBoundary":
            continue
        token = normalize(item.get("text", ""))
        if not token:
            continue
        if flat[cursor:cursor + len(token)] != token:
            raise ValueError("Word boundary mismatch between audio and text: "
                             + text + " <> " + item.get("text", ""))
        onset = max(0, round(item["offset"] / 10000))
        offset = max(onset + 1, round((item["offset"] + item["duration"]) / 10000))
        offset = min(duration, offset)
        begin = cursor
        end = cursor + len(token)
        pos = 0
        for index, word in enumerate(normal_parts):
            word_end = pos + len(word)
            if pos < end and word_end > begin:
                if index not in spans:
                    spans[index] = [onset, offset]
                else:
                    spans[index][1] = offset
            pos = word_end
        cursor = end
    if cursor != len(flat) or len(spans) != len(parts):
        raise ValueError("Incomplete real word boundary coverage: " + text)
    cues = [[i, int(spans[i][0]), int(spans[i][1])] for i in range(len(parts))]
    if any(not (0 <= v[1] < v[2] <= duration + 45) for v in cues):
        raise ValueError("Word boundary exceeds audio duration")
    if any(cues[i-1][2] > cues[i][1] for i in range(1, len(cues))):
        raise ValueError("Overlapping words from same source audio")
    return cues

def duration_ms(path):
    data = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                    "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
                                    str(path)], text=True)
    return round(float(data.strip()) * 1000)

async def build_one(item, semaphore, attempts):
    path = OUT / (str(item["id"]) + ".mp3")
    meta = OUT / (str(item["id"]) + ".jsonl")
    async with semaphore:
        for attempt in range(attempts):
            try:
                if not (path.is_file() and meta.is_file() and meta.stat().st_size):
                    client = edge_tts.Communicate(item["en"], VOICE, rate=RATE,
                                                  boundary="WordBoundary")
                    await asyncio.wait_for(client.save(str(path), str(meta)), 90)
                boundary = [json.loads(line) for line in meta.read_text().splitlines() if line.strip()]
                duration = duration_ms(path)
                cues = cue_words(item["en"], boundary, duration)
                row = {"id":item["id"], "text":item["en"],
                       "path":"assets/pattern-audio/" + str(item["id"]) + ".mp3",
                       "audio_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                       "duration_ms":duration, "language":"en", "voice":VOICE,
                       "timing_source":"WordBoundary from same Edge TTS MP3 synthesis",
                       "cues":cues}
                meta.unlink(missing_ok=True)
                return row
            except Exception as exc:
                path.unlink(missing_ok=True)
                meta.unlink(missing_ok=True)
                if attempt + 1 == attempts:
                    raise RuntimeError(f"Pattern {item['id']} {item['en']}: {exc}") from exc
                await asyncio.sleep(2 + 3 * attempt)

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument("--retry", type=int, default=4)
    args = parser.parse_args()
    if not (4 <= args.start <= args.end <= 1034):
        parser.error("start and end must be between 4 and 1034 inclusive")
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [x for x in SOURCE if args.start <= x["id"] <= args.end and not x.get("duplicateOf")]
    existing = {"schema":1,"items":{}}
    if INDEX.exists():
        existing = json.loads(INDEX.read_text(encoding="utf-8"))
    semaphore = asyncio.Semaphore(args.concurrency)
    for offset in range(0, len(rows), 12):
        chunk = rows[offset:offset + 12]
        results = await asyncio.gather(*(build_one(p, semaphore, args.retry) for p in chunk))
        for row in results:
            existing["items"][str(row["id"])] = row
        existing["schema"] = 1
        existing["source"] = "Only exact synthesized MP3 and same-synthesis WordBoundary cues"
        INDEX.write_text(json.dumps(existing,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
        print(f"VALIDATED {offset + len(results)}/{len(rows)} patterns with measured cues",flush=True)
    print("DONE:", len(rows), "source patterns; recorded index:",
          len(existing["items"]), flush=True)

if __name__ == "__main__":
    asyncio.run(main())
