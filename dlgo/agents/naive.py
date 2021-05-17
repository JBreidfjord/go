import random

from dlgo.agents.base import Agent
from dlgo.agents.helpers import alpha_beta, capture_diff, is_point_an_eye
from dlgo.goboard import GameState, Move
from dlgo.gotypes import Player


class RandomBot(Agent):
    def select_move(self, game_state: GameState) -> Move:
        """Chooses a random valid move. Will avoid closing its own eyes."""
        candidates = []
        for move in game_state.legal_moves():
            if move.is_pass or move.is_resign:
                continue
            if not is_point_an_eye(
                game_state.board, move.point, game_state.next_player
            ):
                candidates.append(move)

        if not candidates:
            return Move.pass_turn()
        return random.choice(candidates)


class AlphaBetaBot(Agent):
    def __init__(self, depth: int = 3, eval_fn=capture_diff):
        """Optionally takes an evaluation function to override the default."""
        self.depth = depth
        self.eval_fn = eval_fn

    def select_move(self, game_state: GameState) -> Move:
        """Chooses a move from a minimax search w/ alpha-beta pruning."""
        maximizing_player = game_state.next_player == Player.black
        move = alpha_beta(
            game_state, self.depth, self.eval_fn, maximizing_player, return_move=True
        )
        if move is None:
            return Move.pass_turn()
        return move
