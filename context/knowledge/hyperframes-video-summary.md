# Video Summary: Claude as a Video Editing Team (HyperFrames)

**Video:** https://www.youtube.com/watch?v=ZNbgOhxhzXg
**Creator:** Nate Herk (AI Automation Society)
**Resources:** https://github.com/nateherkai/hyperframes-student-kit

---

## Core Thesis

Claude (via Claude Code + Claude Design) can now act as a **complete video editing team** — handling text overlays, subtitles, motion graphics, charts, and animated elements — all through natural language. No coding knowledge required. A 23-second clip that would take 2 hours to edit manually can be produced in minutes.

---

## Two Methods Covered

### Method 1: Claude Design (Web App)
- **What it is:** Anthropic's web app (launched the day before this video) for building websites, slide decks, and now **animated videos**.
- **How it works:**
  - Create a design system (logos, branding, colors, typography) so all outputs stay on-brand
  - Use "From Template → Animation" to create timeline-based motion design
  - Drop in a video file (MP4) and prompt it to animate with text/motion graphics
- **Key limitation:** Claude Design **cannot read/listen to the video** — you must paste the transcript with timestamps manually so it knows what's being said and when to sync graphics.
- **Export:** Can't export MP4 directly — either screen-record fullscreen, or hand off to Claude Code with a command to render as MP4 (via HyperFrames under the hood).
- **Verdict:** Very viable, fast (~2 min), impressive results. Best for quick, polished output.

### Method 2: HyperFrames (More Powerful)
- **What it is:** An open-source HTML-native motion-graphics video framework by HeyGen — described as "a better version of Remotion." Every composition is a regular HTML file with a paused GSAP timeline.
- **Setup:**
  1. Get the official HeyGen HyperFrames repo URL
  2. Paste into Claude Code: "Analyze this repo, build skills, help me install it"
  3. Claude Code sets it up in minutes
- **Workflow (the authoring loop):**
  - `edit → lint → preview (Studio, live) → draft render → verify frames → final render`
  - Commands: `npx hyperframes lint`, `npx hyperframes preview`, `npx hyperframes render`
- **Key features:**
  - Built-in catalog of animations (macOS notifications, Reddit cards, 3D UI reveals, app showcases, transitions)
  - Audio-reactive animations
  - Karaoke-style word-synced subtitles
  - Transcribe video locally (Whisper) or via OpenAI API for word-level timestamps
  - Custom skills (`.claude/skills/`) that encode framework patterns — `/make-a-video`, `/short-form-video`, `/hyperframes`, `/gsap`, etc.

---

## Live Demo Walkthrough (Golden Ratio Video)

1. **Drop video** into project (37s talking-head clip)
2. **Invoke skill:** "Use the make-a-video skill, help me create a video for golden-ratio-demo.mp4"
3. **Claude analyzes:** Samples frames, identifies content ("you at your desk in AAS quarter zip with mic")
4. **Asks questions:** Video style (face + motion graphics vs. course-style corner pip), trim or keep full, transcribe for word timestamps
5. **Creates plan** for each section — review and approve BEFORE rendering (saves tokens)
6. **Renders V1** → self-corrects to V2 → preview on localhost
7. **Feedback loop:** Give feedback like you would to a human editor ("at 4-5 seconds the blur is on top of the text, move it behind") → V3, V4, etc.

---

## Cost & Performance Notes

- **Token usage:** First run ~260k tokens, second run ~125k tokens
- **Session cost:** One project ≈ 10% of a 5-hour limit on the $200/month max plan
- **Best practice:** Clear session between iterations — ask for a summary/handoff message, clear, paste back to reorient
- **Rendering:** Multiple simultaneous renders will tax CPU/RAM (caused glitchy facecam in his previous video)

---

## What Works Well vs. What Doesn't

### Works well:
- Promo videos, sizzle reels, brand hype videos
- Educational/course-style videos (face-cam + motion graphics)
- Converting websites to animated promos (drop in standalone HTML)
- Iterating fast with natural-language feedback

### Doesn't work well yet:
- **Shorts (9:16 vertical):** "Not there yet" — wouldn't post them, but getting closer
- **SaaS product demos:** ClickUp demo was version 5 and still lost energy/taste mid-way
- **Raw unedited footage:** Can't reliably detect retakes/dead space — pre-cut mistakes yourself (or use Descript, which also messes up)
- **Localhost previews:** Hit-or-miss with HyperFrames (0s/0s bug) — sometimes need to just render full and give feedback

---

## Key Takeaways

1. **Taste still matters.** People with editing/creative intuition will 10x their productivity; people without taste get mediocre outputs.
2. **Iteration is everything.** Every video you make improves your whole video editing studio — build up skills and design docs as you go.
3. **Don't expect perfection from a clone.** You must put in work, but you can iterate extremely fast.
4. **Token management is critical.** Review plans before rendering, clear sessions between iterations, use handoff messages.

---

## The GitHub Repo (hyperframes-student-kit)

- **570 stars / 208 forks** — a teaching kit with **12 finished video projects** built on Hyperframes + GSAP
- **Structure:** `.claude/skills/` (slash commands), `assets/` (brand tokens), `video-projects/` (12 projects), `docs/`, `scripts/`
- **The 12 projects:**
  - Short-form vertical: `may-shorts-19`, `may-shorts-18`
  - Short-form landscape: `may-shorts-6`
  - Product promos: `clickup-demo`, `linear-promo-30s`, `hyperframes-sizzle`, `first-agent-promo`
  - Educational: `aisoc-lesson-5-1`, `golden-ratio-demo`, `claude-edit-intro`
  - Brand hype: `aisoc-hype`, `aisoc-app-release`
- **Customizing for your brand:** Swap `brand-tokens.css`, logo, background, and create your own `DESIGN.md` (copy the AIS example). Grep for hardcoded AIS hex values.
- **Prerequisites:** Node 20+, FFmpeg, Chrome, ~5GB disk, 16GB RAM recommended
- **License:** MIT (code/compositions) — but AIS brand assets are NOT licensed for reuse