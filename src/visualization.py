"""CSC111 Project 2: Result visualization.

This module uses Plotly to visualize the results of Blokus experiments.

Copyright (c) 2026 Arian Mahlooji, Ishaan Kelkar, Hoang Gia Bach
"""
from __future__ import annotations

import doctest
import python_ta
import plotly.graph_objects as go


def plot_win_rates(summary: dict, title: str) -> None:
    """Display a bar chart of win rates."""
    fig = go.Figure(data=[go.Bar(
        x=['Red wins', 'Blue wins', 'Ties'],
        y=[summary['red_win_rate'], summary['blue_win_rate'], summary['tie_rate']]
    )])
    fig.update_layout(title=title, yaxis_title='Rate')
    fig.show()


def plot_average_scores(summary: dict, title: str) -> None:
    """Display a bar chart of average final scores."""
    fig = go.Figure(data=[go.Bar(
        x=['Red average score', 'Blue average score'],
        y=[summary['average_red_score'], summary['average_blue_score']]
    )])
    fig.update_layout(title=title, yaxis_title='Squares controlled')
    fig.show()


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['__future__', 'doctest', 'python_ta', 'plotly.graph_objects'],
        'allowed-io': [],
        'max-line-length': 100
    })
