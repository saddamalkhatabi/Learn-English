# Story and dialogue audio — truthful status & QA

## First production batch (already recorded)
Kokoro-82M (Apache-2.0) MP3 assets on `main`:
- `assets/audio/{this,have,got}/intro.mp3`: three full spoken English lesson explanations
- `assets/audio/{this,have,got}/scene-1-{1,2,3,4}.mp3`: twelve first-level scene lines

These were rendered by the successful GitHub Actions run documented in the README.

## Story and dialogue narration (automated second batch)
`data/stories.json` contains 9 short chapters (5 lines each) and 3 dialogues (4 turns each).
`scripts/generate_audio.py --stories` reads that content and produces:
- `assets/audio/<lesson-id>/story-<chapter>-<line>.mp3` (45 clips)
- `assets/audio/<lesson-id>/dialogue-<turn>.mp3` (12 clips)

The workflow `.github/workflows/preview.yml` runs this batch if it is missing. Inspect the run's success and check for the actual files in the repository before declaring them available. Existing MP3s are reused without unnecessary re-rendering.

## Synchronization levels
1. Native browser TTS: listen for SpeechSynthesisUtterance `boundary` events. A word highlight appears where the specific browser reports them. This is not reliably supported by every browser and voice.
2. Pre-recorded MP3: the current player distributes timing by word length and total playback duration. This is an **approximation**, not measured word-level alignment. It is suitable only for visual testing of the feature.
3. Production implementation required: run a forced aligner on each **final** generated MP3, review questionable contractions and boundary timing, save word start/end timestamps, and drive highlights using audio.currentTime. Do not invent precise timestamps.
4. The first 3 narrative intros currently have audio but no verified word-level timestamps, so they are played without a claim of precise forced alignment.

## Review checklist
- Confirm the text exactly matches the audio, especially contractions (`I've got`, `haven't got`) and `have` vs `have to`.
- Listen to each MP3 on speakers and headphones and confirm no clipped syllables or unexpected pauses.
- Native English review for the story, dialogue, and explanations.
- Check mobile Safari, desktop Chrome, Android Chrome and low-powered devices.
- Keep separate English voice and Arabic text: never feed Arabic translation to the English Kokoro model.
- Distinguish `I've got a job` as present possession/news from `I got a job` as a past event; context may imply a recent result.

## Preview
Use the ZIP artifact from a successful GitHub Actions run. Enable GitHub Pages if your plan/repo settings allow it; no Pages URL is guaranteed for a private repository.


## 2026-11-01: Acoustic timing migration from Family School 360

The original app360 implementation was inspected, specifically:
- `apps/1-4/my-little-routine/tools/align_routine_words.py`: MMS_FA acoustic alignment of exact unchanged MP3s, source SHA-256, duration in milliseconds, explicit word indices.
- `assets/js/app360-read-along-v1.js`: audio clock and measured [index,start,end] cues, no highlights during silence.
- `apps/4-8/story-language-lab/tools/build_read_along.py`: alternatively, the boundary metadata of the SAME TTS synthesis, shifted after trimming and validated against text.

Learn English now includes `scripts/align_recordings.py`, `.github/workflows/align-english-words.yml`, and a player that consumes `data/audio-word-cues.json` only when exact transcript and measured cues validate. The waveform is the already-committed Kokoro recording. The renderer follows `audio.currentTime` with animation frames and suppresses highlights in pauses.

**Important:** Adding the script does not imply the alignment output exists or has passed QA. Until the GitHub Actions acoustic alignment run succeeds and publishes its JSON to both the private project and public preview, the MP3 continues to play without guessed word-by-word highlighting. Browser synthesis uses native boundary callbacks if available.

Photo-scene preview currently uses mapped real-life images from Pexels with the old SVG as fallback. The separately generated image atlas is a prototype concept asset, not yet self-hosted.
