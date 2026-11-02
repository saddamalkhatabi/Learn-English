# Production provenance

Upstream owner-authorized source: saddamalkhatabi/Learn-English, commit 3915ab51e5fd6c0af85ad57539c64895d18c0dbf.
- scripts/render_dual_kokoro.py: two independently validated voice rows and preservation of original recordings.
- scripts/generate_audio.py: Kokoro waveform encoding to MP3; copied under scripts/upstream. ROOT is set by the new producer.
- scripts/acoustic_pattern_fallback.py: Wav2Vec2 CTC alignment on the exact encoded MP3; copied under scripts/upstream, augmented with the raw greedy ASR transcript as secondary validation evidence.
- scripts/align_recordings.py: reviewed as the primary acoustic alignment precedent.

Kokoro v1.0 model weights: hexgrad/Kokoro-82M, Apache-2.0 model card, revision f3ff3571791e39611d31c381e3a41a3af07b4987. Voices: am_adam and af_bella. Models are production dependencies and are not distributed in the website bundle. Torchaudio English acoustic alignment uses WAV2VEC2_ASR_BASE_960H.

Images were created using the built-in image-generation tool. Three separate prompts requested exactly a 3-column × 4-row atlas of modest Arab adults/families in distinct realistic situations, natural light, no captions, no text, no watermark. Prompt scene order corresponds exactly to `dist/pilot.json` scene descriptions and cells, top left to right, row by row. PNG originals remain in the generating session; production assets are converted WebP copies in dist/assets/scenes. No panel is deleted or replaced by an unrelated placeholder. Each atlas was visually inspected before its scene rows were marked reviewed.

Production scene files: dist/assets/scenes/want-atlas.webp, need-atlas.webp, have-atlas.webp. Audio metadata and exact per-file hashes: dist/pilot.json. No timing values were interpolated from word length or sentence duration.


## Full-media expansion, 2026-11-02
All 13 authored patterns now resolve to 156 scene cells across 13 WebP atlases. Ten additional atlases were generated for the expansion; prompts and source references are retained in scripts/generated-scene-sources.json. All 312 core recordings and 28 supplemental recordings retain separate voice-specific measured alignment. The 72 prior recordings remain byte-for-byte unchanged. GitHub Actions is prepared but has not been executed for this Sites source repository.
