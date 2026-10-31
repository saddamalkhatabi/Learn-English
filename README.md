# Learn English · Pattern Universe

An Arabic-first, offline-friendly learning prototype that teaches English **through scenes, patterns, contrasts, and active recall**.

## Learning experience
- Three fully scripted seed lessons from the supplied source: **This is my house**, **I have a good job**, and **I've got a job**.
- Each seed lesson includes basic, intermediate and advanced usage, 12 contextual examples, a narrated explanation plan, scene illustrations and quiz/reconstruction.
- Browse and search all source entries with keyword categories, depth filters and relationship links. Automatic labels are provisional until linguistic review.
- English audio: browser TTS fallback; GitHub Actions Kokoro generation pipeline for downloadable prerecorded MP3 files (see workflow run for generation status).
- GitHub Actions site preview artifact, and GitHub Pages deployment when Pages is enabled for this repository/account.

## Run
Open `index.html` with a local static server or browse the GitHub Pages site after its first successful deployment. No backend, credentials or payment necessary.

## Audio and publishing
See `docs/DEPLOY.md`, `scripts/generate_audio.py`, and the GitHub Actions workflows for details. **Do not assume voice recordings have been generated just because the scripts exist**; confirm the actual workflow and output files.

The uploaded corpus is the source of truth, not necessarily a quality-assured grammar taxonomy. We retain source IDs and original rules and mark inferred labels as provisional.
