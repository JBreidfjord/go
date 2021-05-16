from dlgo.agents.naive import RandomBot
from dlgo.goboard import GameState, Move
from dlgo.gotypes import Player
from dlgo.utils import point_from_coords, print_board, print_move


def main():
    board_size = 9
    game = GameState.new_game(board_size)
    bot = RandomBot()

    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)
        if game.next_player == Player.black:
            human_move = input("-- ")
            point = point_from_coords(human_move.strip())
            move: Move = Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)


if __name__ == "__main__":
    main()
