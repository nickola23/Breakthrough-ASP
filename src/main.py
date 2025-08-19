from board import Board
from console_ui import ConsoleUI
from ai_player import choose_best_move
import constants

def main():
    board = Board()
    ui = ConsoleUI(board)

    while True:
        ui.display_board()
        winner = board.get_winner()
        if winner:
            print("Pobednik je:", "Beli" if winner==constants.WHITE else "Crni")
            break

        moves = board.generate_moves_for_player(board.side_to_move)
        print("\nDostupni potezi:")
        ui.display_moves(moves)

        if board.side_to_move == constants.WHITE:
            selected_move = ui.ask_player_move(moves)
            board.make_move(selected_move)
        else:
            move = choose_best_move(board, constants.BLACK)
            board.make_move(move)

if __name__ == "__main__":
    main()