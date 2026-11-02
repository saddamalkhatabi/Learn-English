# نَسَق / Nasaq English Lab

A browser-local Arabic RTL learning platform built around varied examples of reusable English patterns. Main runtime: buildless HTML/CSS/JavaScript in `dist/`, no API keys or server dependencies.

## Current authored scope
- All 13 patterns currently in the teaching catalog have 12 distinct examples each: **156 core sentences**, **312 independently recorded Kokoro MP3s**, **2042 exact-recording word cues**, and **156 contextual scenes in 13 WebP atlases**.
- The explicit be used to contrast is labelled as a different construction and is optional in the understanding step, so it is not confused with past-habit used to.

- The preserved café story and six local dialogue openings plus shared responses have **14 additional sentences, 28 paired recordings and 270 cues**, separate from the core counts.
- **104 original core exam-format questions** (eight per pattern), **26 optional advanced questions**, bilingual explanations, solved examples and **156 novel-production challenges**.
- **16 purpose routes**, shared keyword categories, ordered pattern selection, stage/CEFR filters, and continuous or interactive teaching.
- All 1034 original source entries remain searchable and unchanged. They are reference material, not 1034 completed lessons. Expansion covers the 13 currently authored patterns; no mass approval of the source archive is claimed.

## Learning flow
Discover the scene; inspect 12 thumbnail-backed examples and their shared structure; compare meanings; reconstruct a sentence with automatic checking; express a new idea; complete eight common exam-format exercises. Advanced grammar is optional and not a completion gate.

Choice answers are checked on selection. Typed closed answers are checked after a short debounce and before moving between questions; no manual Verify button is needed. Word reconstruction is checked as soon as all words are selected. Open production receives only a clearly labelled structural heuristic and self-assessment; it is not assigned an invented grammar, pronunciation or fluency score. Questions are original practice, not copied official exam questions. Exam pictures are explicitly labelled as references from the pattern, not asserted to illustrate every word of the question.

Completing a lesson may open the next pattern automatically; the learner can disable that option. The continuous teacher plays every selected sentence, alternates Adam/Bella between different sentences, displays a seven-second text comparison and advances to the next pattern and group by default. Explicit other-voice replay does not advance. Story characters have stable voice identities.

The player saves the exact sentence, voice, currentTime, rate, selected IDs, mode and route. A user gesture resumes playback after reopening. Existing complete 36-sentence pilot paths migrate to the expanded full course without losing the current recording position. All 72 recordings from the prior release remain byte-for-byte unchanged.

## Shared media and content
`pilot.json` is the sentence and media registry. `curriculum.json` contains explanations, closed questions, advanced sections, keywords and purpose routes. `supplement.json` contains story/dialogue recordings. All playback surfaces use the same independent voice timing rows. The coach uses media currentTime and the lesson/story/chat surfaces use the corresponding real MP3's times at the chosen playback rate; no word-length timing heuristics are used.

Scenes appear in the home, unit and pattern cards, discovery and understanding steps, reconstruction, reference pictures in exam practice, coach strips, visual catalog, Idea Lab, story, dialogue, reviews and progress rows. No fake documentary origin is claimed for generated imagery; context, tense, duration and negation also need the accompanying language.

## Production archive and GitHub status
`downloads/nasaq-media-library-20261102.zip` contains all media, manifests, hashes, timing rows, production scripts, tests and the prepared workflow. `generation-index.json` is the auditable per-recording index. File timestamps not captured during generation remain null instead of being invented.

The canonical source is still the **Sites Git repository**, not a repository in the user's GitHub account. GitHub Actions has **not run for this Nasaq release**. `.github/workflows/nasaq-audio.yml` is ready to render/verify the entire curriculum and supplement and upload a 90-day artifact when this source is hosted in GitHub. Do not describe the prepared workflow as an executed GitHub event. Learn-English was read at commit 3915ab51e5fd6c0af85ad57539c64895d18c0dbf and was not modified.

## Validation
```sh
node --check dist/app.js
node --check dist/pilot-ui.js
node --check dist/learning.js
node --check dist/enhancements.js
node --check dist/route-player.js
node --test tests/*.cjs
node verify.mjs
python scripts/audit_pilot.py --require-complete
python scripts/archive_production.py
```

The audit checks distinct sentences, resolved exercises, 12 examples per pattern, actual file existence and SHA-256, voice identity declarations, exact text, actual FFprobe durations, separate complete ordered cue rows, and visually reviewed atlas references. Raw CTC ASR transcripts are retained as supporting evidence; word splitting and spelling mismatches are listed for review. This is not a human listening sign-off or a validated CEFR assessment. See `qa-report.json` for real browser checks and remaining limits.

## Reproduce or expand
Use Python 3.11 and FFmpeg. Install CPU `torch==2.6.0` and `torchaudio==2.6.0`, then `scripts/audio-requirements.txt`. Kokoro/misaki obtain their weights, voices, phonemizer support and English language model on first run. The model revision is recorded in the registry. The browser bundle does not include model weights.
```sh
python scripts/produce_audio.py
python scripts/produce_audio.py --manifest dist/supplement.json
python scripts/audit_pilot.py --require-complete
python scripts/archive_production.py
```
Author/review new linguistic content first. Preserve stable IDs and valid media; generation reuses recordings only when text, file hash and cue metadata still match. The authored expansion tools and image prompt scene order are under `scripts/`. Preserve local environment activation when running generation in a virtual environment.

## Restore
Original Site version 1: source ae297ee5f0207126646b62d14377a713be19d36f.
Before this expansion, Site version 2: source 64a08a48d4dd624edcc5c0cbcf173c79ac5db6d9, local checkpoint-before-full-media-20261102 branch/tag. Restore as a new version rather than deleting subsequent work. See docs/RESTORE.md and docs/PROVENANCE.md.
