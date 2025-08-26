from board import Board
from console_ui import ConsoleUI
from ai_player import AIPlayer
import constants

def main():
    board = Board()
    ui = ConsoleUI(board)
    ai_black = AIPlayer(constants.BLACK, max_depth=3, time_limit=3.0)

    while True:
        ui.display_board()
        winner = board.get_winner()
        if winner:
            if winner == constants.WHITE:
                print("Pobednik je: Beli")
            else:
                print("Pobednik je: Crni")
            break

        if board.side_to_move == constants.WHITE:
            moves = board.generate_moves_for_player(board.side_to_move)
            print("\nDostupni potezi:")
            ui.display_moves(moves)

            selected_move = ui.ask_player_move(moves)
            board.make_move(selected_move)
        else:
            print("-" * 30)
            print("AI bira potez...")
            ai_move = ai_black.choose_move(board)
            print("AI igra:", ai_move)
            board.make_move(ai_move)
            print("-" * 30)

if __name__ == "__main__":
    main()