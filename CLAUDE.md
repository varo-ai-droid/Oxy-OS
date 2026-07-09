# Oxy OS — AI Operating System

## What This Project Is
Your personal AI assistant that knows everything about you, gives business + personal advice, writes automations, and holds all your digital projects. Built in VS Code using Cline agent extension. This is your 8th AIOS attempt — rebuilt from scratch to avoid the "copied repo you don't understand" failure pattern.

## Your Goals (From me.md)
- **Primary:** Make you more effective/efficient in life and business
- **Secondary:** Prove you can ship (break the "never shipped outside school" pattern)
- **Money milestone:** ~€100k/month (you tend to break past any goal)
- **Proof to self:** #1 driver — loves proving limits are fake

## 30-Day Ship Plan
Your committed path to first shipped product:
1. **Build ONE working automation** (daily news summary) — SHIPPED ✅
2. **Write business plan AND execute** — must ship, not just paper
3. **Learn one skill to shippable level** — e.g., useful Python script

## Automations Built
1. **daily-news** - `/daily-news` sends Telegram summary at 6:30 AM Berlin time. Output: `automations/daily-news/send_news.py`
2. **youtube-notify** - Checks 88 channels via RSS, notifies on new uploads at 4:30 PM Berlin time. Output: `automations/youtube-notify/check_uploads.py`
3. **git-push** - Auto-pushes changes to GitHub after each task. Output: `automations/git-push/push.py`

## Scheduled Automations (GitHub Actions)
All automations run on GitHub Actions free tier with git-based state persistence:
- `.github/workflows/daily-news.yml` - Runs 6:30 AM Berlin time
- `.github/workflows/youtube-notify.yml` - Runs 4:30 PM Berlin time

## Skills Available
1. **project-lint** - `/project-lint` audits project structure, validates config files, identifies junk files, auto-fixes minor issues, and provides continuation instructions at 50% context. Output: `context/logs/lint-report.md`
2. **roast** - `/roast` convenes a 6-persona council to pressure-test ideas, then delivers GO/RESHAPE/KILL verdict with cheapest 48-hour test to de-risk. Output: Terminal verdict with actionable recommendations.
3. **alex-hormozi-mode** - `/alex` activates full Alex Hormozi persona for blunt, framework-heavy business advice. Use `/alex-exit` to deactivate. Wiki knowledge base at `projects/Alex-Hormozi-Coach/Hormozi-LLM-Wiki/wiki/`.

## Automations To Build
1. Deep research on a topic using specified sources
2. Draft a business plan → execute (not just document)

## Project Structure
```
me.md                    # Stable identity (loaded every session)
memory.md                # Running memory log (chronological learnings)
context/                 # Knowledge hub
├── identity/           abstract.md
├── areas/              abstract.md
├── projects/oxy-os.md  # This project details
├── knowledge/
│   ├── interests.md     # Your interests & YouTube subs
│   └── news-feeds.md    # RSS feeds for daily-news
└── archive/             # Failed AIOS attempts (learning history)
automations/
├── daily-news/
│   ├── send_news.py     # Main script
│   └── requirements.txt # Python dependencies
├── youtube-notify/
│   ├── check_uploads.py  # Main script
│   ├── .env.example     # Telegram config template
│   └── requirements.txt # Dependencies
└── git-push/
    └── push.py         # Auto-push script
```

## Key Principles
- **Build it yourself.** No copying repos you don't fully understand.
- **Direction required.** "Every door open, no destination defined" = nothing gets built.
- **Discipline activates.** You have execution ability — but only with concrete goals.
- **Continuous learning.** I update memory.md/context after every session without asking.

## Rules For This Repo
- Keep changes minimal: nothing you didn't ask for, no "improvements" on the way past
- Never commit real secrets/API keys to files
- If I'm not sure something exists — a package, an API, a setting — I check or say so
- Raise errors explicitly — never swallow them or add fallbacks you didn't ask for
- **File reading policy:** Skip reading `a.md`, `AI_OS_Video_Summary.md`, and `errors.log` unless specifically requested

## Git Auto-Push Protocol
- After each task I complete, I will run `python automations/git-push/push.py` to push changes
- Uses conventional commit messages (feat, fix, docs, chore)
- Repo: https://github.com/varo-ai-droid/Oxy-OS

## Future Integrations (Planned)
email, calendar, Todoist, Google Drive, various APIs — but only after first ship

## Hosting / Ops
- Local on Dell G15 laptop (RTX 4060)
- Pushed to Git (auto-push enabled)
- Open to 24/7 private server later, but no current need

## Your Communication Preferences
- **Default:** Short, direct, no fluff
- **Formal tone** (casual only on personal topics: gym, family, feelings)
- **Always brutally honest** — especially on research-mode slips