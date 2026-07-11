/**
 * Chess Assistant - Stripped down: captures moves, no Stockfish
 */

import { PanelComponent, clearHighlights } from '@/components';
import { boardService, gameLogger } from '@/services';
import type { PlayerColor } from '@/types';

const POLLING_INTERVAL = 500;

/**
 * Chess Assistant - Captures every move and logs it
 */
export class ChessAssistant {
  private panel: PanelComponent;

  private isActive = false;
  private playerColor: PlayerColor = 'w';
  private pollingInterval: ReturnType<typeof setInterval> | null = null;
  private waitingForOpponentMove = false;
  private gameStarted = false;

  constructor() {
    this.panel = new PanelComponent({
      onActivate: () => this.promptForColor(),
      onDeactivate: () => this.deactivate(),
      onColorSelect: (color) => this.activate(color),
      onAutoPlayToggle: () => {}, // no-op
    });
  }

  /**
   * Initialize the assistant
   */
  public initialize(): void {
    this.panel.create();
  }

  /**
   * Prompt user to select color
   */
  private promptForColor(): void {
    if (!boardService.findBoard()) {
      alert('Could not find the chessboard. Make sure you are on a game page.');
      return;
    }

    this.panel.showColorSelection();
  }

  /**
   * Activate the assistant with selected color
   */
  private activate(color: PlayerColor): void {
    this.playerColor = color;
    this.gameStarted = false;

    this.startBoardPolling();
    boardService.addBoardBorder();

    this.isActive = true;
    this.panel.showActiveState();
    this.panel.updateStatus(`Capturing moves for ${color === 'w' ? 'White' : 'Black'}...`);
  }

  /**
   * Deactivate the assistant
   */
  private deactivate(): void {
    this.stopBoardPolling();

    if (this.gameStarted) {
      gameLogger.endGame();
    }

    const board = boardService.getBoard();
    if (board) {
      clearHighlights(board);
    }

    this.isActive = false;
    this.gameStarted = false;
    this.panel.showInactiveState();
  }

  /**
   * Start board polling for changes
   */
  private startBoardPolling(): void {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
    }

    boardService.updateLastBoardState();
    this.waitingForOpponentMove = false;

    this.pollingInterval = setInterval(() => {
      if (!this.isActive) return;

      if (boardService.hasBoardChanged()) {
        this.handleBoardChange();
      }

      // Check if game ended
      if (this.gameStarted && gameLogger.checkGameOver()) {
        this.panel.updateStatus('Game over! Moves captured.');
        this.gameStarted = false;
      }
    }, POLLING_INTERVAL);
  }

  /**
   * Stop board polling
   */
  private stopBoardPolling(): void {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
      this.pollingInterval = null;
    }
  }

  /**
   * Handle board state change
   */
  private handleBoardChange(): void {
    if (!this.gameStarted) {
      gameLogger.startGame();
      this.gameStarted = true;
    }

    if (this.waitingForOpponentMove) {
      // Opponent has moved — log it
      const opponentColor: PlayerColor = this.playerColor === 'w' ? 'b' : 'w';
      gameLogger.logMove(opponentColor);
      this.waitingForOpponentMove = false;
      boardService.updateLastBoardState();
      this.panel.updateStatus('Your turn...');
    } else {
      // We made a move — log it
      gameLogger.logMove(this.playerColor);
      this.waitingForOpponentMove = true;
      boardService.updateLastBoardState();

      const board = boardService.getBoard();
      if (board) {
        clearHighlights(board);
      }

      this.panel.updateStatus("Opponent's turn - waiting...");
    }
  }
}