from dlgo.agents.helpers import capture_diff, current_score
from dlgo.agents.naive import AlphaBetaBot, RandomBot
from dlgo.goboard import GameState, Move
from dlgo.gotypes import Player
from dlgo.utils import point_from_coords, print_board, print_move


def main():
    board_size = 9
    game = GameState.new_game(board_size)
    bot = AlphaBetaBot(eval_fn=current_score)

    move = None
    while not game.is_over():
        print(chr(27) + "[2J")
        if move is not None:
            print_move(game.next_player.other, move)
        print_board(game.board)
        if game.next_player == Player.black:
            move_input = input("-- ")
            if move_input.upper().startswith("R"):
                move = Move.resign()
            elif move_input.upper().startswith("P"):
                move = Move.pass_turn()
            else:
                point = point_from_coords(move_input.strip())
                move: Move = Move.play(point)
        else:
            move = bot.select_move(game)

        game = game.apply_move(move)

    print(game.winner())


if __name__ == "__main__":
    main()
