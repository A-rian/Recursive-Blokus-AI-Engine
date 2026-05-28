"""CSC111 Project 2: Game simulation functions.

This module contains functions for running one or many games between different
player strategies and collecting experiment results.

Copyright (c) 2026 Arian Mahlooji, Ishaan Kelkar, Hoang Gia Bach
"""
from __future__ import annotations

import doctest
import python_ta
from blokus_state import GameState, RED, BLUE
from players import Player, RandomPlayer


def run_game(red_player: Player, blue_player: Player, verbose: bool = False) -> dict:
    """Run one game and return summary statistics.

    >>> result = run_game(RandomPlayer(), RandomPlayer())
    >>> isinstance(result, dict)
    True
    >>> 'winner' in result and 'turns' in result
    True
    """
    state = GameState()
    turn_count = 0

    while not state.is_game_over():
        if state.current_player == RED:
            current_strategy = red_player
        else:
            current_strategy = blue_player

        move = current_strategy.choose_move(state)
        state = state.apply_move(move)
        turn_count += 1

        if verbose:
            print(f'Turn {turn_count}')
            print(state)
            print()

    return {
        'winner': state.winner(),
        'red_score': state.score(RED),
        'blue_score': state.score(BLUE),
        'turns': turn_count
    }


def run_many_games(red_player: Player, blue_player: Player, num_games: int) -> list[dict]:
    """Run many games and return the results.

    >>> results = run_many_games(RandomPlayer(), RandomPlayer(), 2)
    >>> len(results)
    2
    """
    return [run_game(red_player, blue_player) for _ in range(num_games)]


def summarize_results(results: list[dict]) -> dict:
    """Return a summary of experiment results.

    >>> results = [{'winner': RED, 'red_score': 5, 'blue_score': 3, 'turns': 8}]
    >>> summary = summarize_results(results)
    >>> summary['games']
    1
    >>> summary['red_win_rate']
    1.0
    """
    total_games = len(results)
    red_wins = sum(result['winner'] == RED for result in results)
    blue_wins = sum(result['winner'] == BLUE for result in results)
    ties = sum(result['winner'] is None for result in results)
    avg_turns = sum(result['turns'] for result in results) / total_games
    avg_red_score = sum(result['red_score'] for result in results) / total_games
    avg_blue_score = sum(result['blue_score'] for result in results) / total_games

    return {
        'games': total_games,
        'red_win_rate': red_wins / total_games,
        'blue_win_rate': blue_wins / total_games,
        'tie_rate': ties / total_games,
        'average_turns': avg_turns,
        'average_red_score': avg_red_score,
        'average_blue_score': avg_blue_score
    }


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['__future__', 'doctest', 'python_ta', 'blokus_state', 'players'],
        'allowed-io': ['run_game'],
        'max-line-length': 100
    })
