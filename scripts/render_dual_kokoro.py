#!/usr/bin/env python3
"""Create Bella/Adam paired MP3s without modifying any existing group or seed recordings."""
import argparse
import hashlib
import json
import pathlib
import subprocess

from kokoro import KPipeline
from generate_audio import write_clip
from acoustic_pattern_fallback import ForcedAligner

ROOT = pathlib.Path(__file__).resolve().parents[1]
GROUPS = "one two three four five six seven eight nine ten".split()
VOICES = {"female": "af_bella", "male": "am_adam"}


def examples(group, lo, hi, include_chapters=False):
    dataset = json.loads((ROOT / f"data/group-{group}.json").read_text(encoding="utf-8"))
    result = {}
    for pattern in dataset["items"]:
        if not lo <= pattern["id"] <= hi:
            continue
        stem = f"p{pattern['id']:02d}"
        result[f"{stem}/intro"] = pattern["explanationEn"]
        for kind, rows in (("scene", pattern["scenes"]),
                           ("story", pattern["story"]),
                           ("dialogue", pattern["dialogue"])):
            for row in rows:
                result[f"{stem}/{kind}-{row['id']}"] = row["en"]
    if include_chapters:
        for ch in dataset.get("chapters", []):
            for row in ch["lines"]:
                result[f"chapters/c{ch['id']:02d}/line-{row['id']}"] = row["en"]
    return result


def duration(path):
    seconds = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)], text=True)
    return round(float(seconds.strip()) * 1000)


def valid(row, path, text):
    if not row or row.get("text") != text or not path.is_file():
        return False
    if hashlib.sha256(path.read_bytes()).hexdigest() != row.get("audio_sha256"):
        return False
    cues = row.get("cues", [])
    return len(cues) == len(text.split()) and all(
        len(c) == 3 and c[0] == i and 0 <= c[1] < c[2] <= row["duration_ms"] + 45
        and (i == 0 or cues[i - 1][2] <= c[1]) for i, c in enumerate(cues))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", required=True, choices=GROUPS)
    ap.add_argument("--first", type=int, default=1)
    ap.add_argument("--last", type=int, default=3)
    ap.add_argument("--chapters", action="store_true")
    args = ap.parse_args()
    if not 1 <= args.first <= args.last <= 18:
        ap.error("pattern numbers must be in range 1-18")
    targets = examples(args.group, args.first, args.last, args.chapters)
    assert len(targets) == 10 * (args.last - args.first + 1) + (18 if args.chapters and args.group != "one" else 0)

    index_path = ROOT / f"data/group-{args.group}-dual-audio-index.json"
    index = (json.loads(index_path.read_text(encoding="utf-8"))
             if index_path.exists() else
             {"schema": 1, "group": args.group, "engine": "Kokoro-82M",
              "voices": VOICES, "items": {}})
    assert index["schema"] == 1 and index["group"] == args.group
    pipeline = None
    aligner = None

    for i, (clip, spoken) in enumerate(targets.items(), start=1):
        paired = index["items"].setdefault(clip, {})
        for gender, voice in VOICES.items():
            relative = f"assets/group-dual-audio/{args.group}/{gender}/{clip}.mp3"
            path = ROOT / relative
            previous = paired.get(gender)
            if valid(previous, path, spoken):
                continue
            if not path.is_file():
                if pipeline is None:
                    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
                write_clip(pipeline, voice, spoken, path)
            if aligner is None:
                aligner = ForcedAligner()
            cues = aligner.align(path, spoken)
            row = {"text": spoken, "path": relative,
                   "audio_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                   "duration_ms": duration(path), "language": "en",
                   "voice": voice, "cues": cues,
                   "timing_source": "Measured from the same Kokoro MP3"}
            if not valid(row, path, spoken):
                raise ValueError(f"Invalid paired recording: {relative}")
            paired[gender] = row
            index_path.parent.mkdir(parents=True, exist_ok=True)
            index_path.write_text(json.dumps(index, ensure_ascii=False,
                             separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"VERIFIED {i}/{len(targets)} two voices: {clip}", flush=True)

    assert all(valid(index["items"][clip][gender],
                     ROOT / index["items"][clip][gender]["path"], spoken)
               for clip, spoken in targets.items() for gender in VOICES)
    print(f"PASS: {len(targets)} correctly aligned female/male pairs", flush=True)


if __name__ == "__main__":
    main()
