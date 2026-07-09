# memory.md — Running Memory Log

## 2026-07-09 — GitHub Actions scheduled automations CREATED

- Created `.github/workflows/daily-news.yml` - Scheduled for 6:30 AM Berlin time (4:30 AM UTC)
- Created `.github/workflows/youtube-notify.yml` - Scheduled for 4:30 PM Berlin time (14:30 UTC), with git persistence for state files
- Created `automations/youtube-notify/last_videos.json` - State tracking file for video deduplication
- State persistence via git: Both workflows will commit updated state back to repository after each run
- Required GitHub secrets: BOT_TOKEN, CHAT_ID, BOT_TOKEN_NOTIFY, CHAT_ID_NOTIFY (to be added manually in repo settings)

## 2026-07-09 — Git auto-push automation SETUP & TESTED
- Created `automations/git-push/push.py` - Auto-push script with conventional commits
- Initialized git repo and pushed to GitHub: https://github.com/varo-ai-droid/Oxy-OS
- Added Python/VS Code ignores to `.gitignore`
- Integrated into CLAUDE.md rules - will run after each task completion

## 2026-07-09 — Project lint completed
- Ran comprehensive project-lint audit
- Fixed `context/knowledge/interests.md` - Updated outdated YouTube subscription status
- Fixed `CLAUDE.md` - Removed `.env.example` from daily-news structure (root `.env.example` used)
- All Python syntax valid, all YAML valid, structure now matches documentation
- Project clean at 43% context usage

## 2026-07-09 — YouTube notify bot tested with separate token
- Script successfully sent 21 notifications to separate Telegram bot
- BOT_TOKEN_NOTIFY and CHAT_ID_NOTIFY working in root .env
- Bot is fully independent from daily-news automation
- Time filter added: only videos from yesterday 16:01 onwards

## 2026-07-09 — YouTube notify bot upgraded to separate bot
- Updated root `.env` - Added BOT_TOKEN_NOTIFY and CHAT_ID_NOTIFY placeholders
- Updated `check_uploads.py` - Uses separate notify credentials
```

## 2026-07-09 — YouTube notification automation BUILT & TESTED
- Created `automations/youtube-notify/check_uploads.py` - 88-channel RSS checker
- Created `automations/youtube-notify/.env.example` - Config template
- Created `automations/youtube-notify/requirements.txt` - Dependencies
- Tested successfully: 9 notifications sent to Telegram
- Channels: All 88 from Takeout export, topics: AI, Business, Bodybuilding, Football, Lifestyle
- Uses RSS feeds (no API key needed) - fast MVP approach
- Created `setup_task.bat` for Windows Task Scheduler (run as admin to enable)

> This is the accumulating memory of our work together. Unlike `me.md` (stable identity) and `context/` (organized knowledge), this is a chronological log of learnings, decisions, corrections, and preferences discovered over time. I append to it as we go. Newest entries at the top.

## 2026-07-08 — daily-news automation TESTED & WORKING
- Ran test execution: "News sent successfully!" to Telegram
- Fixed HTML `<p>` tag removal in story summaries
- Added bold formatting for topic and story headlines in Telegram output
- Automation is shippable and functional

## 2026-07-08 — SHIPPED daily-news automation
- Created `.claude/skills/daily-news/SKILL.md` - Skill for `/daily-news` command
- Created `automations/daily-news/send_news.py` - Python script using RSS feeds + Telegram
- Created `automations/daily-news/requirements.txt` - feedparser, python-dotenv, requests, googletrans
- Created `automations/daily-news/.env.example` - Telegram config template
- Created `context/knowledge/news-feeds.md` - RSS feed URLs per topic priority
- Topics configured: P1 (AI, Business, Technology - 3 stories each), P2 (World, Germany - 2 each), P3 (Science - 1)
- Non-English articles auto-translated via googletrans
- Windows Task Scheduler setup documented for 6:30 AM daily runs

## 2026-07-08 — Built CLAUDE.md tier system
- Created `.claude/CLAUDE.md` - Computer-level rules (plain English, pushback culture, communication style)
- Created `CLAUDE.md` - Project-level rules (30-day ship plan, automations, structure)
- Created `context/areas/CLAUDE.md` - Area-specific rules (business focus, learning visibility, fitness privacy)
- Sources: oliwoodman/claude-md-templates (plain English), alfredolancelote-crypto/claude-md-starter-pack (AI agent patterns), adapted for Oxy's non-technical background and shipping-first mindset

## 2026-07-08 — Onboarding interview started
- Created `me.md`, `memory.md`, and `context/` hub during a ~30-min voice-driven onboarding interview.
- User answers by dictating via Open Whisper (voice-to-text); they talk at length, so questions are asked one at a time and I wait for the full answer before proceeding.
- Goal: fill every field in `me.md` and seed the `context/` hub so future sessions have full context.

## 2026-07-08 — Key decision: 30-day "first ship" plan
- Oxy's core blocker is NOT effort/fear — it's lacking a project to commit to ("destination not defined").
- He committed to a combined plan to break the "never shipped outside school" pattern:
  1. Build ONE working Oxy OS automation (news summary) — ~1 day.
  2. Write a business plan AND execute on it (must ship, not just paper).
  3. Learn one skill to a shippable level (e.g., useful Python script).
- As his assistant, I should help him PICK a concrete direction and hold him to shipping — not let him slip back into research-only mode.

## 2026-07-08 — KEY PRINCIPLE: assistant must learn & evolve over time
- Oxy wants the assistant to be his **biggest critic** (not a yes-man) and to **develop over time**.
- When he corrects me or states a preference/boundary, I MUST log it to memory.md (and adjust me.md/context as needed) so it persists permanently.
- This continuous self-improvement is a core Oxy OS design principle, not a one-time config.
- Default communication: short/direct, formal, brutally honest. Casual only on personal topics. Max info, min words.

## 2026-07-08 — Partnership rules (from Q10/Q10b, locked in)
- **Disagree actively:** Always try to disagree and argue my own position, even after he decides. Only agree if genuinely flawless.
- **Research-mode callout:** Call out procrastination via "research mode" EVERY time, openly/directly, informal/"insult" tone allowed until he says "stop."
- **Proactive ideas:** Suggest idea → build TOGETHER → decide. Don't just hand ideas; don't build alone.
- **Hard-rule persistence:** If he declares any rule a "hard rule" in any chat, I MUST write it to the file system so ANY future LLM knows it.
- **Pushback protocol:** On ignored advice, push back once to verify; if still refused, drop it.

## 2026-07-08 — Onboarding interview COMPLETED
- All 10 me.md sections filled (Identity, Work, Technical, Projects, Goals, Workflow, Communication, Learning, Environment, AI Partnership) + follow-ups.
- context/ hub seeded: projects/oxy-os.md, knowledge/interests.md, plus abstract.md for each folder.

