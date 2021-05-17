from __future__ import annotations

from collections import namedtuple

from dlgo.goboard import Board, GameState
from dlgo.gotypes import Player, Point


class Territory:
    def __init__(self, territory_map: dict[Point, Player | str]):
        self.num_black_territory = 0
        self.num_white_territory = 0
        self.num_black_stones = 0
        self.num_white_stones = 0
        self.num_neutral = 0
        self.neutral_points = []
        for point, status in territory_map.items():
            if status == Player.black:
                self.num_black_stones += 1
            elif status == Player.white:
                self.num_white_stones += 1
            elif status == "territory_b":
                self.num_black_territory += 1
            elif status == "territory_w":
                self.num_white_territory += 1
            elif status == "neutral":
                self.num_neutral += 1
                self.neutral_points.append(point)


class GameResult(namedtuple("GameResult", "b w komi")):
    @property
    def winner(self):
        if self.b > self.w + self.komi:
            return Player.black
        return Player.white

    @property
    def winning_margin(self):
        w = self.w + self.komi
        return abs(self.b - w)

    def __str__(self):
        w = self.w + self.komi
        if self.b > w:
            return f"B+{self.b - w}"
        return f"W+{w - self.b}"


def evaluate_territory(board: Board):
    status = {}
    for row in range(1, board.num_rows + 1):
        for col in range(1, board.num_cols + 1):
            point = Point(row=row, col=col)
            if point in status:
                continue
            stone = board.get(point)
            if stone is not None:
                status[point] = stone
            else:
                group, neighbors = _collect_region(point, board)
                if len(neighbors) == 1:
                    neighbor_stone = neighbors.pop()
                    stone_str = "b" if neighbor_stone == Player.black else "w"
                    fill_with = "territory_" + stone_str
                else:
                    fill_with = "neutral"
                for pos in group:
                    status[pos] = fill_with
    return Territory(status)


def _collect_region(start_pos: Point, board: Board, visited=None):
    if visited is None:
        visited = {}
    if start_pos in visited:
        return [], set()
    all_points = [start_pos]
    all_borders = set()
    visited[start_pos] = True
    here = board.get(start_pos)
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for row_delta, col_delta in deltas:
        next_point = Point(row=start_pos.row + row_delta, col=start_pos.col + col_delta)
        if not board.is_on_grid(next_point):
            continue
        neighbor = board.get(next_point)
        if neighbor == here:
            points, borders = _collect_region(next_point, board, visited)
            all_points += points
            all_borders |= borders
        else:
            all_borders.add(neighbor)
    return all_points, all_borders


def compute_game_result(game_state: GameState):
    territory = evaluate_territory(game_state.board)
    return GameResult(
        territory.num_black_territory + territory.num_black_stones,
        territory.num_white_territory + territory.num_white_stones,
        komi=7.5,
    )
