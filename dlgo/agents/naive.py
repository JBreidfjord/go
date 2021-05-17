import random

from dlgo.agents.base import Agent
from dlgo.agents.helpers import is_point_an_eye
from dlgo.goboard import GameState, Move


class RandomBot(Agent):
    def select_move(self, game_state: GameState):
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
        return Move.play(random.choice(candidates))
