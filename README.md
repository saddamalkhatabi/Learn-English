# Learn English · Pattern Universe

An Arabic-first, offline-friendly learning prototype that teaches English **through scenes, patterns, contrasts, and active recall**.

## Learning experience
- Three fully scripted seed lessons from the supplied source: **This is my house**, **I have a good job**, and **I've got a job**.
- Each seed lesson includes basic, intermediate and advanced usage, 12 contextual examples, a narrated explanation plan, scene illustrations and quiz/reconstruction.
- Browse and search all source entries with keyword categories, depth filters and relationship links. Automatic labels are provisional until linguistic review.
- English audio: browser TTS fallback; 15 confirmed Kokoro-82M MP3 files: 3 English lesson explanations plus 12 beginner scene recordings; full-scene generation is an optional GitHub Actions input.
- GitHub Actions site preview artifact, and GitHub Pages deployment when Pages is enabled for this repository/account.

## Run
Open `index.html` with a local static server or browse the GitHub Pages site after its first successful deployment. No backend, credentials or payment necessary.

## Audio and publishing
See `docs/TESTING-DEPLOYMENT.md`, `docs/ARCHITECTURE-AR.md`, `scripts/generate_audio.py`, and `.github/workflows/preview.yml` for details. The first workflow completed successfully and the 15 recorded MP3 assets are present on `main`. GitHub Pages still requires enabling in repository Settings → Pages; no live page URL has been verified yet.

The uploaded corpus is the source of truth, not necessarily a quality-assured grammar taxonomy. We retain source IDs and original rules and mark inferred labels as provisional.

## Verified first release

- [First successful Kokoro render & preview artifact](https://github.com/saddamalkhatabi/Learn-English/actions/runs/41244514987)
- [Original source corpus with keyword / category / depth labels](data/patterns.json) (provisional classifications)
- [Three authored lesson journeys](data/lessons.json) (36 scenes)
- [Recorded English audio folder](assets/audio)
- [Arabic system and pedagogy blueprint](docs/ARCHITECTURE-AR.md)
- [How to test and enable Pages](docs/TESTING-DEPLOYMENT.md)
