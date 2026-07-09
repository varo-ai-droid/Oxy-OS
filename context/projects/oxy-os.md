# Oxy OS — Active Project

## What it is
Oxy's personal AI operating system: a local-first assistant that knows everything about him, gives business + personal advice, writes automations, and holds all his digital projects. Built in VS Code (Klein agent). This is the 8th attempt — the previous ~7 failed due to messy/unclean structure and copying repos he didn't understand.

## Why it matters
- Primary goal: make Oxy more effective/efficient in life and business.
- Secondary (only if it becomes excellent): possible product.
- Directly attacks his "execution gap" by giving him a structured system + persistent memory (me.md, memory.md, context/).

## Current status
- Scaffolded memory system on 2026-07-08: `me.md`, `memory.md`, `context/` hub (identity/areas/projects/knowledge/archive).
- **2026-07-08: SHIPPED daily-news automation** - Tested and working. Telegram messages sending successfully.
- Previous AIOS attempts are effectively in `archive/` (failed, unrecoverable).

## Built automations (shipped)
1. **daily-news** ✅ - Telegram news summary at 6:30 AM. P1/P2/P3 topic priority system. TESTED AND WORKING.

## Wanted automations (next)
2. Notify when favorite YouTubers post.
3. Deep research on a topic using specified sources.
4. Draft a business plan.

## Planned integrations (future)
email, calendar, to-do app, Google Drive, various APIs.

## Hosting / ops
- Local on this laptop; pushed to a Git repo (Oxy has Git experience).
- Open to a 24/7 private server for automations later, no current need.

## Input method
Both typing and voice (Open Wispr / Whisper dictation).

## Next steps
- Schedule via Windows Task Scheduler at 6:30 AM daily
- Monitor for a week, then refine topics/sources