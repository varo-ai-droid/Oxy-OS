"""
Oxy Chess Coach - Local Receiver Server

Receives game data from the Chrome extension and saves it to disk.
Run this in the background while playing on chess.com.
"""

import json
import os
import sys
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Directory where games are saved
GAMES_DIR = Path(__file__).resolve().parent.parent / "games"
GAMES_DIR.mkdir(exist_ok=True)

PORT = 9876


class GameHandler(BaseHTTPRequestHandler):
    """Handles incoming game data from the Chrome extension."""

    def do_POST(self):
        if self.path == "/api/game":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                game_data = json.loads(body)
                self._save_game(game_data)
                self._send_response(200, {"status": "ok"})
            except json.JSONDecodeError as e:
                self._send_response(400, {"error": f"Invalid JSON: {e}"})
            except Exception as e:
                self._send_response(500, {"error": str(e)})
        else:
            self._send_response(404, {"error": "Not found"})

    def do_GET(self):
        if self.path == "/api/health":
            self._send_response(200, {"status": "alive", "games_dir": str(GAMES_DIR)})
        elif self.path == "/api/games":
            self._send_response(200, self._list_games())
        else:
            self._send_response(404, {"error": "Not found"})

    def _save_game(self, game_data: dict) -> None:
        """Save game data to a JSON file."""
        game_id = game_data.get("id", f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        filename = f"{game_id}.json"
        filepath = GAMES_DIR / filename

        with open(filepath, "w") as f:
            json.dump(game_data, f, indent=2)

        print(f"[OxyChess] Saved game: {filepath} ({len(game_data.get('moves', []))} moves)")

    def _list_games(self) -> list:
        """List all saved game files."""
        games = []
        for f in sorted(GAMES_DIR.glob("*.json"), reverse=True):
            try:
                with open(f) as fh:
                    data = json.load(fh)
                    games.append({
                        "id": data.get("id", f.stem),
                        "date": data.get("date", ""),
                        "players": data.get("players", {}),
                        "result": data.get("result"),
                        "moves": len(data.get("moves", [])),
                        "file": f.name,
                    })
            except (json.JSONDecodeError, OSError):
                continue
        return games

    def _send_response(self, status: int, data: dict) -> None:
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        """Suppress default logging; use our own."""
        if args[0] != "POST /api/game":
            print(f"[OxyChess] {args[0]}")


def main():
    server = HTTPServer(("0.0.0.0", PORT), GameHandler)
    print(f"[OxyChess] Server running on http://localhost:{PORT}")
    print(f"[OxyChess] Games saved to: {GAMES_DIR}")
    print("[OxyChess] Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[OxyChess] Shutting down...")
        server.server_close()


if __name__ == "__main__":
    main()