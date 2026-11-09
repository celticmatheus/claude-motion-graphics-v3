# The user's rules for MG V3 (they override everything else in this skill)

Add every note the user gives on a V3 edit here as a dated rule, with why. Read this file before every V3 build.

- 2026-10-26 (brief): "full motion graphic", real images "at once or multiple times", go online and grab real things,
  take screenshots, cut out the people "so we can see the person", change the colours. Learn it frame by frame.
- Standing preferences carried from his other styles: soft sound only (no harsh ticks/glitch noise, quieter bed);
  his accent is Warm Cream #D97757 (also Anthropic's clay) — use it as the one accent unless the subject's brand
  colour reads better; real UI/pages/logos over flat cards.

## 2026-10-26 — demo v1 feedback: "it does sound strange when you mention the word AI" + "a little bit mundane"
1. **Never spell acronyms with dots for Kokoro.** "A.I." is read as two sentences ("a" … "I") with a 0.5 s hole after
   it. Write them plain: `AI`, `OpenAI`, `GPT-2`, `GPT-3` — Kokoro's phonemizer already says ay-eye / jee-pee-tee.
   Respell only names it gets wrong (`Ahmo-day` for Amodei). Then ALWAYS re-transcribe the voice and listen-check the
   suspicious words' durations in work/words.json (an "AI" longer than ~0.4 s or followed by a > 0.3 s gap = wrong).
2. **Mundane = measurable.** Run `tools/motion_study.py` on the render and compare with the references
   (reference/REF-D_costco.md table). v1 had 49 % dead frames, 1.2 px/s median pan, 0.29 px local motion → mundane.
   v2 (approved direction): 20 % dead, 65 % of frames with a camera move, local motion 1.0 px (= REF-A Jobs).
   Targets for every V3 film: **dead frames ≤ 30 %, longest dead stretch ≤ 1.6 s, camera moving ≥ 50 %,
   median local motion ≥ 0.8 px.**
3. **People must move.** Use real footage of the person cut out as video (`tools/vcut.sh … --pingpong`), not stills,
   whenever a clip exists (interviews, keynotes, the company's own films). Stills only for archive people.
4. **Every scene needs one physical action by an object or the type** (REF-D): something flies in and parks in
   front of the words, a ribbon swoops, a phone slides in and the camera snap-zooms into its screen, a building rises,
   banknotes spin in, a chart line draws through the stat, a word is found in a word-search, letters assemble.
5. **Colour worlds change scene to scene** (clay, ivory, slate, sky photo, black, grey) — never two monochrome worlds
   in a row; heavy EXTRUDED type (`ext()`, Archivo Black / Anton) for headlines.
