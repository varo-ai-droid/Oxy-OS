# Chess Coach Skill

Analyzes captured chess.com games and produces personalized improvement reports.

## Usage

```
/chess-coach
```

## What it does

1. Reads all game files from `chess/games/`
2. Analyzes each game for:
   - Opening choices and accuracy
   - Tactical mistakes (blunders, missed captures)
   - Positional patterns
   - Endgame performance
   - Time management patterns (if available)
3. Produces a structured improvement report with:
   - Top 3 weaknesses to work on
   - Specific openings to study
   - Recommended puzzles/tactics by theme
   - Accuracy trends over time

## Input

Game files in `chess/games/*.json` — each contains:
- Game metadata (date, players, result)
- Every move with FEN notation and timestamp

## Output

Summary in terminal + saves report to `chess/coach/output/latest-report.md`

## Dependencies

- Python 3
- No external packages (uses only stdlib)

## Files

- `analyze.py` — Main analysis script
- `output/latest-report.md` — Latest improvement report