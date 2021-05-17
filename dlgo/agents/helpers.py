from __future__ import annotations

import copy

import numpy as np
from dlgo.goboard import Board, GameState, Move
from dlgo.gotypes import Player, Point
from dlgo.scoring import GameResult, compute_game_result


def is_point_an_eye(board: Board, point: Point, color: Player):
    if board.get(point) is not None:
        return False
    # All adjacent points must contain friendly stones
    for neighbor in point.neighbors():
        if board.is_on_grid(neighbor):
            neighbor_color: Player = board.get(neighbor)
            if neighbor_color != color:
                return False

    friendly_corners = 0
    off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1),
    ]
    for corner in corners:
        if board.is_on_grid(corner):
            corner_color: Player = board.get(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4
    return friendly_corners >= 3


def capture_diff(game_state: GameState) -> int:
    black_stones = 0
    white_stones = 0
    for row in range(1, game_state.board.num_rows + 1):
        for col in range(1, game_state.board.num_cols + 1):
            point = Point(row=row, col=col)
            color = game_state.board.get(point)
            if color == Player.black:
                black_stones += 1
            elif color == Player.white:
                white_stones += 1
    diff = black_stones - white_stones
    if game_state.next_player == Player.black:
        return diff
    return -diff


def current_score(game_state: GameState) -> int:
    game_result: GameResult = compute_game_result(game_state)
    if game_result.winner == Player.black:
        return game_result.winning_margin
    return -game_result.winning_margin


def alpha_beta(
    game_state: GameState,
    depth: int,
    eval_fn,
    maximizing_player: bool,
    alpha: int = -np.inf,
    beta: int = np.inf,
    return_move: bool = False,
) -> Move | float | int | None:
    if game_state.is_over():
        game_result: GameResult = compute_game_result(game_state)
        if game_result.winner == Player.black:
            return np.inf
        return -np.inf

    elif depth == 0:
        return eval_fn(game_state)

    if maximizing_player:
        max_eval = -np.inf
        best_move = None
        moves = game_state.legal_moves()
        np.random.shuffle(moves)
        for move in moves:
            if (
                move.is_pass
                or move.is_resign
                or is_point_an_eye(game_state.board, move.point, game_state.next_player)
            ):
                continue
            game = copy.deepcopy(game_state)
            game.apply_move(move)
            eval = alpha_beta(game, depth - 1, eval_fn, False, alpha, beta)
            if eval > max_eval and return_move:
                best_move = move
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break

        return best_move if return_move else max_eval

    else:
        min_eval = np.inf
        best_move = None
        moves = game_state.legal_moves()
        np.random.shuffle(moves)
        for move in moves:
            if (
                move.is_pass
                or move.is_resign
                or is_point_an_eye(game_state.board, move.point, game_state.next_player)
            ):
                continue
            game = copy.deepcopy(game_state)
            game.apply_move(move)
            eval = alpha_beta(game, depth - 1, eval_fn, True, alpha, beta)
            if eval < min_eval and return_move:
                best_move = move
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break

        return best_move if return_move else min_eval
