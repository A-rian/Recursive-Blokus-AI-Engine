"""CSC111 Project 2: Main runner for simplified Blokus.

Run this file to simulate games and visualize the results.

Copyright (c) 2026 Arian Mahlooji, Ishaan Kelkar, Hoang Gia Bach
"""
from __future__ import annotations

from players import Player, RandomPlayer, GreedyPlayer, TreeAIPlayer
from simulation import run_game, run_many_games, summarize_results
from visualization import plot_win_rates, plot_average_scores


def get_ai_player(difficulty: str) -> Player:
    """Return an AI player for the given difficulty level.

    Preconditions:
        - difficulty in {'easy', 'medium', 'hard'}

    >>> isinstance(get_ai_player('easy'), RandomPlayer)
    True
    >>> isinstance(get_ai_player('medium'), GreedyPlayer)
    True
    >>> isinstance(get_ai_player('hard'), TreeAIPlayer)
    True
    """
    if difficulty == 'easy':
        return RandomPlayer()
    elif difficulty == 'medium':
        return GreedyPlayer()
    else:
        return TreeAIPlayer(3)


def sample_single_game(difficulty: str) -> None:
    """Run one sample game against the chosen difficulty.

    Preconditions:
        - difficulty in {'easy', 'medium', 'hard'}
    """
    ai_player = get_ai_player(difficulty)
    result = run_game(ai_player, RandomPlayer(), verbose=True)
    print(f'Single game result against {difficulty} difficulty:')
    print(result)


def run_difficulty_experiment(difficulty: str, num_games: int) -> None:
    """Run an experiment for one AI difficulty level.

    Preconditions:
        - difficulty in {'easy', 'medium', 'hard'}
        - num_games > 0
    """
    ai_player = get_ai_player(difficulty)
    results = run_many_games(ai_player, RandomPlayer(), num_games)
    summary = summarize_results(results)

    print(f'{difficulty.title()} difficulty vs Random summary:')
    print(summary)

    plot_win_rates(summary, f'{difficulty.title()} Difficulty vs Random')
    plot_average_scores(summary, f'{difficulty.title()} Difficulty: Average Scores')


def compare_all_difficulties(num_games: int) -> None:
    """Run experiments for all difficulty levels.

    Preconditions:
        - num_games > 0
    """
    run_difficulty_experiment('easy', num_games)
    run_difficulty_experiment('medium', num_games)
    run_difficulty_experiment('hard', num_games)


if __name__ == '__main__':
    compare_all_difficulties(20)
    # Uncomment one of these to inspect a single full game:
    # sample_single_game('easy')
    # sample_single_game('medium')
    # sample_single_game('hard')
