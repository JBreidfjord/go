from __future__ import annotations

import math
import random

from dlgo.agents.base import Agent
from dlgo.agents.naive import RandomBot
from dlgo.goboard import GameState, Move
from dlgo.gotypes import Player


class MCTSNode(object):
    def __init__(
        self, game_state: GameState, parent: MCTSNode = None, move: Move = None
    ):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_counts = {Player.black: 0, Player.white: 0}
        self.num_rollouts = 0
        self.children: list[MCTSNode] = []
        self.unvisited_moves = game_state.legal_moves()

    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node

    def record_win(self, winner: Player):
        self.win_counts[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def is_terminal(self):
        return self.game_state.is_over()

    def winning_pct(self, player: Player):
        return float(self.win_counts[player]) / float(self.num_rollouts)


class MonteBot(Agent):
    def __init__(self, temperature: float = 1.5, max_search_rounds: int = 100):
        self.temperature = temperature
        self.num_rounds = max_search_rounds

    def select_move(self, game_state: GameState):
        root = MCTSNode(game_state)

        for _ in range(self.num_rounds):
            node = root
            while (not node.can_add_child()) and (not node.is_terminal()):
                node: MCTSNode = self.select_child(node)

            if node.can_add_child():
                node = node.add_random_child()

            winner = self.simulate_random_game(node.game_state)

            while node is not None:
                node.record_win(winner)
                node = node.parent

        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_pct(game_state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        return best_move

    def select_child(self, node: MCTSNode):
        total_rollouts = sum(child.num_rollouts for child in node.children)

        best_score = -1
        best_child = None
        for child in node.children:
            score = uct_score(
                total_rollouts,
                child.num_rollouts,
                child.winning_pct(node.game_state.next_player),
                self.temperature,
            )
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def simulate_random_game(self, game_state: GameState) -> Player:
        random_bot = RandomBot()
        while not game_state.is_over():
            move = random_bot.select_move(game_state)
            game_state = game_state.apply_move(move)
        return game_state.winner()


def uct_score(
    parent_rollouts: int, child_rollouts: int, win_pct: float, temperature: float
):
    exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
    return win_pct + (temperature * exploration)
