# Learn English · Pattern Universe

An Arabic-first, offline-friendly learning prototype that teaches English **through scenes, patterns, contrasts, and active recall**.

## المجموعة الأولى — المسار التفاعلي
- [المجموعة الأولى: 18 نمطًا و72 موقفًا و54 سطر قصة و36 جملة حوارية](docs/GROUP-ONE-AR.md). افتح تبويب «🌱 المجموعة الأولى».
- اختبار الفهم وبناء الجملة وحفظ التقدم، وأولوية للأصول الصوتية الموثقة.
- يوضح [تقرير الحالة](docs/GROUP-ONE-AR.md) ما يحتاج استكمالًا من الصور والتسجيلات قبل اعتماد الوسائط.

## المجموعة الثانية — الحياة اليومية والعادات
- [المجموعة الثانية: 18 نمطًا و72 موقفًا وثلاث قصص مترابطة](docs/GROUP-TWO-AR.md). افتح «🌤️ المجموعة الثانية».
- مشاهد توضيحية مؤقتة حتى تصميم الصور، مع 198 مادة صوتية مغطاة بأصول MP3 محققة وتوقيتات كلمات حقيقية، وتلوين الكلمات متزامن عند التشغيل.

## Learning experience
- Three fully scripted seed lessons from the supplied source: **This is my house**, **I have a good job**, and **I've got a job**.
- Each seed lesson includes three levels, 12 contextual scene examples, a recorded Kokoro explanation, clickable story chapters (5 lines per level), a 4-turn dialogue, active vocabulary highlighting and quiz/reconstruction.
- Browse and search all source entries with keyword categories, depth filters and relationship links. Automatic labels are provisional until linguistic review.
- English audio: 15 verified Kokoro-82M MP3 files committed (3 explanations + 12 beginner scenes); GitHub Actions now generates 45 narrated story lines and 12 dialogue clips as additional MP3 assets. Browser TTS is the fallback for pending or missing recordings. Audio generation needs a successful workflow before a new file can be considered present.
- GitHub Actions site preview artifact, and GitHub Pages deployment when Pages is enabled for this repository/account.

## Stories and synchronisation
- `data/stories.json` contains **3 original stories**, **9 chapters**, **45 story lines** and **12 dialogue turns** with Arabic translations and contextual illustrations.
- While using browser speech synthesis, word highlighting uses speech engine boundary events when supported.
- For MP3 recordings, the interim time-based word highlight is **approximate**, not verified forced alignment. Production-grade forced alignment is still to be implemented. See `docs/STORY-AUDIO.md`.

## Run
Open `index.html` with a local static server or browse the GitHub Pages site after its first successful deployment. No backend, credentials or payment necessary.

## Audio and publishing
See `docs/TESTING-DEPLOYMENT.md`, `docs/ARCHITECTURE-AR.md`, `scripts/generate_audio.py`, and `.github/workflows/preview.yml` for details. The first workflow completed successfully and the 15 recorded MP3 assets are present on `main`. Extra story and dialogue voice recordings are produced by later workflow runs. GitHub Pages still requires enabling in repository Settings → Pages; no live page URL has been verified yet.

The uploaded corpus is the source of truth, not necessarily a quality-assured grammar taxonomy. We retain source IDs and original rules and mark inferred labels as provisional.

## Verified first release

- [First successful Kokoro render & preview artifact](https://github.com/saddamalkhatabi/Learn-English/actions/runs/41244514987)
- [Original source corpus with keyword / category / depth labels](data/patterns.json) (provisional classifications)
- [Three authored lesson journeys](data/lessons.json) (36 scenes)
- [Recorded English audio folder](assets/audio)
- [Arabic system and pedagogy blueprint](docs/ARCHITECTURE-AR.md)
- [How to test and enable Pages](docs/TESTING-DEPLOYMENT.md)
