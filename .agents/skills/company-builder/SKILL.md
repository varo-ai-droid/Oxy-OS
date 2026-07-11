---
name: company-builder
description: Use when someone wants to build a complete company from scratch using multi-agent orchestration. Runs 9-phase autonomous process: pain hunt, tournament selection, business design, brand, product, launch video, founder video, red team, package recap.
disable-model-invocation: true
---

# Company Builder Skill

Builds a complete company from scratch using multi-agent orchestration (Fable 5 pattern). Runs 9 autonomous phases producing a launch-ready package.

## Prerequisites

- Codex CLI installed and authenticated (`codex --version` works)
- Python 3.10+ with pyyaml
- `whois` CLI for domain checks
- Optional API keys in `.env`:
  - `ELEVENLABS_API_KEY` - voiceover for videos
  - `HEYGEN_API_KEY` - avatar videos

## Usage

```
/company-builder
```

Runs all 9 phases sequentially with checkpointing. Can resume after failure.

## Output

All artifacts in `.agents/skills/company-builder/output/`:
- `recap/index.html` - Open this to see everything
- `pain-hunt/candidates.md` - 18 validated problems
- `tournament/winner.md` - Selected opportunity
- `business-design/business-plan.md` - Full plan with unit economics
- `brand/brand-guide.md` + `logo.svg` - Brand identity
- `product/index.html` - Landing page
- `videos/launch-script.md`, `founder-script.md` - Video scripts
- `red-team/verdict.md`, `fixes.md` - Adversarial review

## Configuration

Edit `config.yaml` to tune:
- `parallelism` (default 3 for laptop GPU)
- Phase agent counts
- Model preferences
- Attack vectors for red team

## Architecture

- `orchestrator.py` - Main entry, state machine
- `scripts/run_codex_agent.py` - Subprocess wrapper for Codex CLI
- `prompts/` - 15 prompt templates (Jinja2)
- `config.yaml` - All tunable parameters
- `state.json` - Checkpoint/resume state

## Phases

1. **Pain Hunt** - 10 researchers sweep 10 sources → 35 problems → 18 candidates
2. **Tournament** - 5 judges score on 6 criteria → top 4 → advocate/skeptic → 3 final judges vote
3. **Business Design** - 3 researchers: competitors, APIs, regulations, unit economics
4. **Brand** - Domain check, 6 logo iterations, voice guide
5. **Landing Page** - HTML/CSS/JS with offer, demo, pricing
6. **Launch Video** - Script for viral demo video
7. **Founder Video** - Personal message script
8. **Red Team** - 6 skeptics attack: TAM, pricing, tech, distribution, legal, retention
9. **Recap** - HTML package linking all artifacts

## Resume After Failure

```
/company-builder
```

Automatically resumes from last completed phase using `state.json`.