import time

from dlgo.agents.naive import RandomBot
from dlgo.goboard import GameState
from dlgo.gotypes import Player
from dlgo.utils import print_board, print_move


def main():
    board_size = 9
    game = GameState.new_game(board_size)
    bots = {
        Player.black: RandomBot(),
        Player.white: RandomBot(),
    }

    while not game.is_over():
        # Short sleep to make the game watchable
        time.sleep(0.3)

        bot_move = bots[game.next_player].select_move(game)
        print(chr(27) + "[2J")  # Clear the screen
        print_board(game.board)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)


if __name__ == "__main__":
    main()
