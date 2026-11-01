"""Generate measured English word cues from each ORIGINAL committed Kokoro MP3.

Faster English-only Wav2Vec2 CTC forced alignment, following app360's rule:
use timings measured from the SAME recording, never sentence-length heuristics.
Run with --lesson this|have|got to create separate validated artifacts.
"""
import argparse
import hashlib
import json
import pathlib
import re

import numpy as np
import soundfile as sf
import torch
import torchaudio

ROOT = pathlib.Path(__file__).resolve().parents[1]
LESSONS = json.loads((ROOT / "data/lessons.json").read_text(encoding="utf-8"))["lessons"]
STORIES = json.loads((ROOT / "data/stories.json").read_text(encoding="utf-8"))["lessons"]
torch.set_num_threads(2)
BUNDLE = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
VOCAB = {letter: i for i, letter in enumerate(BUNDLE.get_labels())}
MODEL = None


def corpus(lesson_filter=None):
    rows = {}
    for lesson in LESSONS:
        lid = lesson["id"]
        if lesson_filter and lid != lesson_filter:
            continue
        base = "assets/audio/" + lid + "/"
        rows[base + "intro.mp3"] = lesson["explanationEn"]
        for level_idx, level in enumerate(lesson["levels"], 1):
            for scene_idx, scene in enumerate(level["scenes"], 1):
                rows[base + f"scene-{level_idx}-{scene_idx}.mp3"] = scene["en"]
        story = STORIES[lid]
        for chapter_idx, chapter in enumerate(story["levels"], 1):
            for line_idx, line in enumerate(chapter["lines"], 1):
                rows[base + f"story-{chapter_idx}-{line_idx}.mp3"] = line["en"]
        for i, turn in enumerate(story["dialogue"], 1):
            rows[base + f"dialogue-{i}.mp3"] = turn["en"]
    expected = 32 if lesson_filter else 96
    if len(rows) != expected:
        raise ValueError(f"Expected {expected} recordings, found {len(rows)}")
    return rows


def token_sequence(text):
    tokens, owners = [], []
    words = text.strip().split()
    for i, word in enumerate(words):
        # The English CTC model supports A-Z and apostrophes; ignore punctuation.
        normalized = "".join(c for c in word.upper() if c in VOCAB and c != "|")
        if not normalized:
            raise ValueError(f"No CTC symbols for word {i} in {text!r}")
        for letter in normalized:
            tokens.append(VOCAB[letter])
            owners.append(i)
        if i < len(words) - 1:
            tokens.append(VOCAB["|"])
            owners.append(-1)
    return words, tokens, owners


def measure(mp3_path, text, model):
    file = ROOT / mp3_path
    digest = hashlib.sha256(file.read_bytes()).hexdigest()
    words, token_ids, owners = token_sequence(text)
    samples, source_sr = sf.read(file, dtype="float32")
    if samples.ndim > 1:
        samples = np.mean(samples, axis=1)
    samples = np.ascontiguousarray(samples)
    sample_count = len(samples)
    if not sample_count:
        raise ValueError("Empty audio: " + mp3_path)
    wave = torch.from_numpy(samples).unsqueeze(0)
    if source_sr != BUNDLE.sample_rate:
        wave = torchaudio.functional.resample(wave, source_sr, BUNDLE.sample_rate)
    with torch.inference_mode():
        emission, _ = model(wave)
        emission = emission.log_softmax(dim=-1)
        labels = torch.tensor([token_ids], dtype=torch.int32)
        alignments, token_scores = torchaudio.functional.forced_align(
            emission, labels, blank=VOCAB["-"])
        spans = torchaudio.functional.merge_tokens(
            alignments[0], token_scores[0], blank=VOCAB["-"])
    if len(spans) != len(token_ids):
        raise ValueError(f"Token span mismatch: {mp3_path} {len(spans)} != {len(token_ids)}")
    milliseconds_per_frame = (wave.shape[-1] / emission.shape[1]) / BUNDLE.sample_rate * 1000
    duration_ms = round(sample_count / source_sr * 1000)
    bounds = [[None, None] for _ in words]
    for span, owner in zip(spans, owners):
        if owner < 0:
            continue
        start = round(span.start * milliseconds_per_frame)
        end = round(span.end * milliseconds_per_frame)
        if bounds[owner][0] is None:
            bounds[owner][0] = start
        bounds[owner][1] = end
    cues = [[i, starts, ends] for i, (starts, ends) in enumerate(bounds)]
    if any(
        s is None or e is None or s < 0 or e <= s or e > duration_ms + 40
        for _, s, e in cues
    ):
        raise ValueError("Incomplete or out-of-range word boundaries: " + mp3_path)
    if any(cues[i-1][2] > cues[i][1] for i in range(1, len(cues))):
        raise ValueError("Overlapping word boundaries: " + mp3_path)
    return {
        "text": text, "language": "en", "audio_sha256": digest,
        "duration_ms": duration_ms, "cues": cues,
        "timing_source": "English Wav2Vec2 CTC forced alignment of original committed Kokoro MP3",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lesson", choices=["this", "have", "got"], default=None)
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "data/audio-word-cues.json")
    args = parser.parse_args()
    rows = corpus(args.lesson)
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    old = {}
    if output.exists():
        try:
            old = json.loads(output.read_text(encoding="utf-8")).get("items", {})
        except (ValueError, OSError):
            pass
    global MODEL
    result = {}
    for idx, (path, text) in enumerate(rows.items(), 1):
        digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        cached = old.get(path)
        if cached and cached.get("audio_sha256") == digest and cached.get("text") == text:
            result[path] = cached
        else:
            if MODEL is None:
                print("Loading English Wav2Vec2 acoustic model", flush=True)
                MODEL = BUNDLE.get_model().eval()
            result[path] = measure(path, text, MODEL)
        if idx % 4 == 0 or idx == len(rows):
            output.write_text(json.dumps({
                "schema": 1, "items": result, "total_recordings": len(result)
            }, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
            print(f"Validated {idx}/{len(rows)} original recordings", flush=True)
    assert len(result) == len(rows)
    print("PASS:", len(result), "recordings and",
          sum(len(v["cues"]) for v in result.values()), "word cues", flush=True)


if __name__ == "__main__":
    main()
