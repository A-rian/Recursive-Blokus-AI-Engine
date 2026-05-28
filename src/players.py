"""CSC111 Project 2: Player strategies for simplified Blokus.

This module contains random, greedy, and tree-based AI players.

Copyright (c) 2026 Arian Mahlooji, Ishaan Kelkar, Hoang Gia Bach
"""
from __future__ import annotations

import random
import doctest
import python_ta
from blokus_state import GameState, Move
from blokus_tree import GameTree, evaluate_state


class Player:
    """An abstract player strategy."""

    def choose_move(self, state: GameState) -> Move | None:
        """Return a move for the given state."""
        raise NotImplementedError


class RandomPlayer(Player):
    """A player that chooses uniformly from all legal moves."""

    def choose_move(self, state: GameState) -> Move | None:
        """Return a random legal move.

        >>> player = RandomPlayer()
        >>> move = player.choose_move(GameState())
        >>> isinstance(move, Move) or move is None
        True
        """
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return None
        return random.choice(legal_moves)


class GreedyPlayer(Player):
    """Return best immediate move.

    >>> player = GreedyPlayer()
    >>> move = player.choose_move(GameState())
    >>> isinstance(move, Move) or move is None
    True
    """

    def choose_move(self, state: GameState) -> Move | None:
        """Return the best immediate move.

        >>> player = GreedyPlayer()
        >>> move = player.choose_move(GameState())
        >>> isinstance(move, Move) or move is None
        True
        """
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return None

        best_move = legal_moves[0]
        best_value = evaluate_state(state.apply_move(best_move))

        for i in range(1, len(legal_moves)):
            move = legal_moves[i]
            next_state = state.apply_move(move)
            value = evaluate_state(next_state)

            if state.current_player == 'R' and value > best_value:
                best_move = move
                best_value = value
            elif state.current_player == 'B' and value < best_value:
                best_move = move
                best_value = value

        return best_move


class TreeAIPlayer(Player):
    """A player that searches a game tree to choose a move."""
    depth: int

    def __init__(self, depth: int) -> None:
        """Initialize this player with a search depth.

        >>> player = TreeAIPlayer(2)
        >>> player.depth
        2
        """
        self.depth = depth

    def choose_move(self, state: GameState) -> Move | None:
        """Return a move chosen by this player.

        >>> player = TreeAIPlayer(1)
        >>> move = player.choose_move(GameState())
        >>> isinstance(move, Move) or move is None
        True
        """
        tree = GameTree(state.copy())
        tree.generate_tree(self.depth)
        return tree.best_move()


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['__future__', 'random', 'doctest', 'python_ta',
                          'blokus_state', 'blokus_tree'],
        'allowed-io': [],
        'max-line-length': 100
    })
