import time

from dlgo.agents.helpers import capture_diff, current_score
from dlgo.agents.naive import AlphaBetaBot, RandomBot
from dlgo.goboard import GameState
from dlgo.gotypes import Player
from dlgo.utils import print_board, print_move


def main():
    board_size = 9
    game = GameState.new_game(board_size)
    bots = {
        Player.black: AlphaBetaBot(eval_fn=capture_diff, depth=3),
        Player.white: AlphaBetaBot(eval_fn=current_score, depth=3),
    }

    move = None
    while not game.is_over():
        # Short sleep to make the game watchable
        time.sleep(0.3)

        print(chr(27) + "[2J")
        if move is not None:
            print_move(game.next_player.other, move)
        print_board(game.board)

        move = bots[game.next_player].select_move(game)

        game = game.apply_move(move)

    print(game.winner())


if __name__ == "__main__":
    main()
