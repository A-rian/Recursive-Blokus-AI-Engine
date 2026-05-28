"""CSC111 Project 2: Game tree for simplified Blokus.

This module contains a recursive game tree used by AI players to evaluate future
states of the simplified Blokus game.

Copyright (c) 2026 Arian Mahlooji, Ishaan Kelkar, Hoang Gia Bach
"""
from __future__ import annotations

from dataclasses import dataclass, field
import doctest
import python_ta
from blokus_state import GameState, Move, RED, BLUE


@dataclass
class GameTree:
    """A game tree node for simplified Blokus."""
    state: GameState
    move: Move | None = None
    children: list[GameTree] = field(default_factory=list)
    evaluation: float = 0.0

    def generate_tree(self, depth: int) -> None:
        """Generate the game tree up to the given depth.

        >>> tree = GameTree(GameState())
        >>> tree.generate_tree(1)
        >>> len(tree.children) > 0
        True
        """
        if depth == 0 or self.state.is_game_over():
            self.evaluation = evaluate_state(self.state)
            return

        legal_moves = self.state.get_legal_moves()
        if not legal_moves:
            child = GameTree(self.state.apply_move(None), None)
            child.generate_tree(depth - 1)
            self.children.append(child)
        else:
            for move in legal_moves:
                child_state = self.state.apply_move(move)
                child = GameTree(child_state, move)
                child.generate_tree(depth - 1)
                self.children.append(child)

        if self.state.current_player == RED:
            self.evaluation = max(subtree.evaluation for subtree in self.children)
        else:
            self.evaluation = min(subtree.evaluation for subtree in self.children)

    def best_move(self) -> Move | None:
        """Return the best move from this node.

        Preconditions:
            - len(self.children) > 0

        >>> tree = GameTree(GameState())
        >>> tree.generate_tree(1)
        >>> move = tree.best_move()
        >>> isinstance(move, Move) or move is None
        True
        """
        if not self.children:
            return None

        best_child = self.children[0]

        for i in range(1, len(self.children)):
            child = self.children[i]

            if self.state.current_player == RED:
                if child.evaluation > best_child.evaluation:
                    best_child = child
            else:
                if child.evaluation < best_child.evaluation:
                    best_child = child

        return best_child.move


def evaluate_state(state: GameState) -> float:
    """Return a heuristic evaluation for the given state.

    Positive values favour Red, and negative values favour Blue.

    >>> state = GameState()
    >>> isinstance(evaluate_state(state), float)
    True
    """
    red_score = state.score(RED)
    blue_score = state.score(BLUE)
    red_mobility = state.mobility(RED)
    blue_mobility = state.mobility(BLUE)

    return 2.0 * (red_score - blue_score) + 0.5 * (red_mobility - blue_mobility)


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['__future__', 'dataclasses', 'doctest', 'python_ta', 'blokus_state'],
        'allowed-io': [],
        'max-line-length': 100
    })
