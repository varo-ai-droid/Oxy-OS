# Chess Coach — Move Capture & Analysis

## What This Is
A Chrome extension + local server + Cline skill that captures every chess.com move you play and analyzes your games to help you improve faster.

## How It Works

### 1. Chrome Extension (`chess/extension/`)
- Modified fork of AI-Chess-Assistant (Stockfish removed)
- Runs on chess.com, captures every move as FEN notation
- Sends completed games to local server at `http://localhost:9876`

### 2. Local Server (`chess/server/server.py`)
- Python HTTP server that receives game data
- Saves games to `chess/games/` as JSON files
- Run with: `python chess/server/server.py`

### 3. Analysis Skill (`chess/coach/`)
- Run `/chess-coach` to analyze all captured games
- Produces improvement report at `chess/coach/output/latest-report.md`

## Setup

1. **Build the extension:**
   ```
   cd chess/extension && npm install && npm run build
   ```
2. **Load in Chrome:**
   - Go to `chrome://extensions/`
   - Enable Developer mode
   - Load unpacked → select `chess/extension/dist/`
3. **Start the server:**
   ```
   python chess/server/server.py
   ```
4. **Play on chess.com:**
   - Open a game, click "Start" on the Oxy Chess Coach panel
   - Select your color
   - Play normally — every move is captured
   - When game ends, it's saved to `chess/games/`

## Analysis

After playing some games, run:
```
/chess-coach
```
This reads all games in `chess/games/` and produces an improvement report.

## File Structure
```
chess/
├── extension/          # Chrome extension (forked)
├── server/
│   └── server.py       # Local receiver server
├── games/              # Captured games (gitignored)
├── coach/
│   ├── SKILL.md        # Skill definition
│   ├── analyze.py      # Analysis script
│   └── output/         # Reports (gitignored)
└── AGENTS.md           # This file