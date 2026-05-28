"""CSC111 Project 2: Simplified Blokus game state and move generation.

This module contains the data structures used to represent a simplified version
of Blokus on a 6x6 board. It supports move generation, move validation, game
state transitions, and game scoring.

Copyright (c) 2026 Arian Mahlooji, Ishaan Kelkar, Hoang Gia Bach
"""
from __future__ import annotations

from dataclasses import dataclass
import copy
import doctest
import python_ta

BOARD_SIZE = 6
EMPTY = '.'
RED = 'R'
BLUE = 'B'


@dataclass(frozen=True)
class Move:
    """A move in the simplified Blokus game.

    Instance Attributes:
        - piece_name: the name of the piece being placed
        - cells: the absolute board positions occupied by the piece after placement

    Representation Invariants:
        - len(self.cells) >= 1
        - all(0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE for row, col in self.cells)
    """
    piece_name: str
    cells: tuple[tuple[int, int], ...]


PIECE_SHAPES = {
    'single': [[(0, 0)]],
    'domino': [[(0, 0), (0, 1)], [(0, 0), (1, 0)]],
    'trio': [[(0, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (2, 0)]],
    'L3': [
        [(0, 0), (1, 0), (1, 1)],
        [(0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 1)]
    ]
}

CORNERS = {(0, 0), (0, BOARD_SIZE - 1), (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)}


class GameState:
    """A state of the simplified Blokus game.

    Instance Attributes:
        - board: a 2D list representing the game board
        - current_player: the player whose turn it is
        - remaining_pieces: a mapping from player to the pieces they have not used yet
        - passes_in_row: the number of consecutive turns with no legal placement

    Representation Invariants:
        - len(self.board) == BOARD_SIZE
        - all(len(row) == BOARD_SIZE for row in self.board)
        - self.current_player in {RED, BLUE}
        - set(self.remaining_pieces.keys()) == {RED, BLUE}
        - self.passes_in_row in {0, 1, 2}
    """
    board: list[list[str]]
    current_player: str
    remaining_pieces: dict[str, set[str]]
    passes_in_row: int

    def __init__(self) -> None:
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = RED
        self.remaining_pieces = {
            RED: {'single', 'domino', 'trio', 'L3'},
            BLUE: {'single', 'domino', 'trio', 'L3'}
        }
        self.passes_in_row = 0

    def copy(self) -> GameState:
        """Return a deep copy of this game state.

        >>> state = GameState()
        >>> new_state = state.copy()
        >>> new_state is state
        False
        >>> new_state.board == state.board
        True
        """
        new_state = GameState()
        new_state.board = copy.deepcopy(self.board)
        new_state.current_player = self.current_player
        new_state.remaining_pieces = {
            RED: set(self.remaining_pieces[RED]),
            BLUE: set(self.remaining_pieces[BLUE])
        }
        new_state.passes_in_row = self.passes_in_row
        return new_state

    def switch_player(self) -> None:
        """Switch the current player.
        >>> state = GameState()
        >>> state.current_player
        'R'
        >>> state.switch_player()
        >>> state.current_player
        'B'
        """
        self.current_player = BLUE if self.current_player == RED else RED

    def has_any_piece_on_board(self, player: str) -> bool:
        """Return whether the given player has any piece already placed."""
        return any(cell == player for row in self.board for cell in row)

    def get_legal_moves(self, player: str | None = None) -> list[Move]:
        """Return all legal moves for the given player.

        If player is None, use the current player.

        >>> state = GameState()
        >>> moves = state.get_legal_moves('R')
        >>> len(moves) > 0
        True
        >>> all(isinstance(move, Move) for move in moves)
        True
        """
        if player is None:
            player = self.current_player

        legal_moves = []
        for piece_name in self.remaining_pieces[player]:
            legal_moves.extend(self._get_legal_moves_for_piece(player, piece_name))

        return legal_moves

    def _get_legal_moves_for_piece(self, player: str, piece_name: str) -> list[Move]:
        """Return all legal moves for the given player using the given piece.

        >>> state = GameState()
        >>> moves = state._get_legal_moves_for_piece('R', 'single')
        >>> all(move.piece_name == 'single' for move in moves)
        True
        """
        legal_moves = []
        for orientation in PIECE_SHAPES[piece_name]:
            legal_moves.extend(
                self._get_moves_for_orientation(player, piece_name, orientation)
            )

        return legal_moves

    def _get_moves_for_orientation(
            self, player: str, piece_name: str, orientation: list[tuple[int, int]]
    ) -> list[Move]:
        """Return all legal moves for one orientation of a piece.

        >>> state = GameState()
        >>> moves = state._get_moves_for_orientation('R', 'single', [(0, 0)])
        >>> len(moves) > 0
        True
        """
        legal_moves = []
        placements = self._generate_placements_for_shape(orientation)

        for cells in placements:
            if self._is_legal_placement(player, cells):
                legal_moves.append(Move(piece_name, tuple(sorted(cells))))

        return legal_moves

    def _generate_placements_for_shape(self, shape: list[tuple[int, int]]) \
            -> list[list[tuple[int, int]]]:
        """Generate all board placements for the given normalized shape."""
        max_row = max(r for r, _ in shape)
        max_col = max(c for _, c in shape)
        placements = []

        for start_row in range(BOARD_SIZE - max_row):
            for start_col in range(BOARD_SIZE - max_col):
                cells = [(start_row + r, start_col + c) for r, c in shape]
                placements.append(cells)

        return placements

    def _is_legal_placement(self, player: str, cells: list[tuple[int, int]]) -> bool:
        """Return whether placing the given cells is legal for player."""
        for row, col in cells:
            if self.board[row][col] != EMPTY:
                return False

        if not self.has_any_piece_on_board(player):
            return any(cell in CORNERS for cell in cells)

        touches_corner = False
        for row, col in cells:
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and self.board[nr][nc] == player:
                    touches_corner = True

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and self.board[nr][nc] == player:
                    return False

        return touches_corner

    def apply_move(self, move: Move | None) -> GameState:
        """Return the new state after applying move.

        If move is None, the current player passes.

        >>> state = GameState()
        >>> move = Move('single', ((0, 0),))
        >>> next_state = state.apply_move(move)
        >>> next_state.board[0][0]
        'R'
        >>> next_state.current_player
        'B'
        """
        new_state = self.copy()

        if move is None:
            new_state.passes_in_row += 1
            new_state.switch_player()
            return new_state

        for row, col in move.cells:
            new_state.board[row][col] = self.current_player

        new_state.remaining_pieces[self.current_player].remove(move.piece_name)
        new_state.passes_in_row = 0
        new_state.switch_player()
        return new_state

    def is_game_over(self) -> bool:
        """Return whether this game is over.

        >>> state = GameState()
        >>> state.is_game_over()
        False
        >>> state.passes_in_row = 2
        >>> state.is_game_over()
        True
        """
        if self.passes_in_row >= 2:
            return True

        return len(self.get_legal_moves(RED)) == 0 and len(self.get_legal_moves(BLUE)) == 0

    def score(self, player: str) -> int:
        """Return the number of squares controlled by player.

        >>> state = GameState()
        >>> state.board[0][0] = 'R'
        >>> state.score('R')
        1
        >>> state.score('B')
        0
        """
        return sum(cell == player for row in self.board for cell in row)

    def mobility(self, player: str) -> int:
        """Return the number of legal moves for player."""
        return len(self.get_legal_moves(player))

    def winner(self) -> str | None:
        """Return the winner, or None for a tie or unfinished game."""
        if not self.is_game_over():
            return None

        red_score = self.score(RED)
        blue_score = self.score(BLUE)
        if red_score > blue_score:
            return RED
        elif blue_score > red_score:
            return BLUE
        else:
            return None

    def __str__(self) -> str:
        """Return a simple string representation of the board."""
        return '\n'.join(' '.join(row) for row in self.board)


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['__future__', 'dataclasses', 'copy', 'doctest', 'python_ta'],
        'allowed-io': [],
        'max-line-length': 100
    })
