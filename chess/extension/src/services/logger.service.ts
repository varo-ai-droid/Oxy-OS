/**
 * Logger Service - Captures every move and sends to local server
 */

import { boardService } from './board.service';
import type { FENString, PlayerColor } from '@/types';

export interface MoveRecord {
  moveNumber: number;
  player: PlayerColor;
  fen: FENString;
  timestamp: string;
}

export interface CapturedGame {
  id: string;
  date: string;
  site: 'chess.com';
  players: {
    white: string;
    black: string;
  };
  result: string | null;
  moves: MoveRecord[];
}

/**
 * Game Logger - Tracks full game state and logs moves
 */
export class GameLogger {
  private game: CapturedGame | null = null;
  private moveCount = 0;
  private lastLoggedFen: FENString = '';
  private gameEnded = false;

  /**
   * Start tracking a new game
   */
  public startGame(): void {
    const now = new Date();
    this.game = {
      id: `${now.toISOString().split('.')[0].replace(/[:-]/g, '')}_${Math.random().toString(36).slice(2, 6)}`,
      date: now.toISOString(),
      site: 'chess.com',
      players: {
        white: this.extractPlayerName('white') || 'White',
        black: this.extractPlayerName('black') || 'Black',
      },
      result: null,
      moves: [],
    };
    this.moveCount = 0;
    this.lastLoggedFen = '';
    this.gameEnded = false;
  }

  /**
   * Log a move when board changes
   */
  public logMove(playerColor: PlayerColor): void {
    if (!this.game || this.gameEnded) return;

    const fen = boardService.generateFEN();
    if (!fen || fen === this.lastLoggedFen) return;
    this.lastLoggedFen = fen;

    this.moveCount++;
    const moveRecord: MoveRecord = {
      moveNumber: this.moveCount,
      player: playerColor,
      fen,
      timestamp: new Date().toISOString(),
    };

    this.game.moves.push(moveRecord);
  }

  /**
   * End the game and send to server
   */
  public endGame(result?: string): void {
    if (!this.game || this.gameEnded) return;
    this.gameEnded = true;

    this.game.result = result || this.detectResult();

    // Send to local server
    this.sendToServer(this.game);
  }

  /**
   * Check if game is over by looking for chess.com's game-over elements
   */
  public checkGameOver(): boolean {
    if (this.gameEnded) return true;

    // Chess.com shows game-over overlay with class "game-over" or "board-layout-game-over"
    const gameOverElements = document.querySelectorAll(
      '.game-over, [class*="game-over"], .board-layout-game-over, .modal-game-over'
    );
    if (gameOverElements.length > 0) {
      const resultText = document.querySelector('.game-over-header, .result-header, [class*="result"]')?.textContent || null;
      this.endGame(resultText || undefined);
      return true;
    }
    return false;
  }

  /**
   * Get current game (for testing)
   */
  public getGame(): CapturedGame | null {
    return this.game;
  }

  /**
   * Send captured game to local server
   */
  private async sendToServer(game: CapturedGame): Promise<void> {
    try {
      const response = await fetch('http://localhost:9876/api/game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(game),
      });
      if (!response.ok) {
        console.warn('[OxyChess] Server returned', response.status);
      }
    } catch (err) {
      // Server might not be running — that's okay, we also save locally
      console.warn('[OxyChess] Could not send to server:', err);
    }
  }

  /**
   * Extract player name from chess.com DOM
   */
  private extractPlayerName(color: string): string {
    const selector = color === 'white'
      ? '.player-top .user-username-component, .clock-top .username'
      : '.player-bottom .user-username-component, .clock-bottom .username';
    const el = document.querySelector(selector);
    return el?.textContent?.trim() || '';
  }

  /**
   * Detect result from DOM
   */
  private detectResult(): string {
    const resultEl = document.querySelector('.game-over-header, .result-header');
    return resultEl?.textContent?.trim() || 'unknown';
  }
}

/** Singleton instance */
export const gameLogger = new GameLogger();