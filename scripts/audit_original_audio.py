#!/usr/bin/env python3
"""Read-only integrity check for all previously recorded English learning audio.

This audit NEVER generates, edits, converts or deletes media. Its only purpose
is to ensure that visual-only updates cannot silently break the original audio.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("one", "two", "three", "four", "five",
         "six", "seven", "eight", "nine", "ten")
EXPECTED = (154, 194, 195, 197, 197, 198, 198, 197, 198, 198)
checked = set()


def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate_recording(relative, row, label):
    path = (ROOT / relative).resolve()
    assert path.is_relative_to((ROOT / "assets").resolve()), (label, relative)
    assert path.suffix.lower() == ".mp3" and path.is_file(), (label, relative, "missing MP3")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == row.get("audio_sha256"), (label, relative, "MP3 checksum changed")
    text = row.get("text", "")
    cues = row.get("cues")
    assert text and isinstance(cues, list), (label, relative, "missing transcript or cues")
    assert len(cues) == len(text.split()), (label, relative, "word count differs")
    duration = row.get("duration_ms", 0)
    assert duration > 0, (label, relative, "missing duration")
    for i, cue in enumerate(cues):
        assert len(cue) == 3 and cue[0] == i, (label, relative, "cue index")
        assert 0 <= cue[1] < cue[2] <= duration + 45, (label, relative, "cue bounds")
        if i:
            assert cues[i - 1][2] <= cue[1], (label, relative, "cue overlap")
    checked.add(relative)


def main():
    originals = read_json("data/audio-word-cues.json")
    assert originals["total_recordings"] == 96
    assert len(originals["items"]) == 96
    for path, row in originals["items"].items():
        validate_recording(path, row, "original Kokoro")
    print("PASS: 96 original Kokoro MP3 recordings and measured word cues")

    sum_group = 0
    for name, count in zip(NAMES, EXPECTED):
        data = read_json(f"data/group-{name}-audio-index.json")
        assert len(data["items"]) == data["verified_count"] == count, name
        for key, row in data["items"].items():
            assert row.get("language") == "en", (name, key)
            validate_recording(row["path"], row, f"group-{name}:{key}")
        sum_group += count
        print(f"PASS: group-{name} = {count} recorded MP3 entries")
    assert sum_group == 1926

    source = read_json("data/pattern-audio-index.json")
    assert source["verified_count"] == len(source["items"]) == 997
    for key, row in source["items"].items():
        assert row.get("language") == "en", ("source", key)
        validate_recording(row["path"], row, f"source:{key}")
    print("PASS: 997 recorded source pattern MP3 entries")

    for name in NAMES:
        group = read_json(f"data/group-{name}.json")
        assert len(group["items"]) == 18
        assert all(len(item["scenes"]) == 4 for item in group["items"])
    print("PASS: original 10-group teaching data = 180 patterns and 720 scenes")
    print(f"ORIGINAL AUDIO PROTECTED: {len(checked)} distinct recorded files verified; no files changed.")


if __name__ == "__main__":
    main()
