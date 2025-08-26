import constants
from board import Board

class ConsoleUI:
    def __init__(self, board):
        self.board = board

    def display_board(self):
        print("   ", end="")
        for col in range(self.board.size):
            print(f"{constants.COLUMNS[col]} ", end="")
        print()
        print("  +" + "--"*self.board.size + "+")

        for row in range(self.board.size):
            print(f"{row+1} |", end="")
            for col in range(self.board.size):
                piece = self.board.board[row][col]
                char = "."
                if piece == constants.WHITE:
                    char = "W"
                elif piece == constants.BLACK:
                    char = "B"

                if self.board.last_move and ((row == self.board.last_move.from_row and col == self.board.last_move.from_col) or
                                            (row == self.board.last_move.to_row and col == self.board.last_move.to_col)):
                    char = f"\033[91m{char}\033[0m" # Boji poslednji potez u crveno

                print(f"{char} ", end="")
            print(f"| {row+1}")
        print("  +" + "--"*self.board.size + "+")

        print("   ", end="")
        for col in range(self.board.size):
            print(f"{constants.COLUMNS[col]} ", end="")
        print()

    def display_moves(self, moves):
        for index, move in enumerate(moves):
            print(f"{index+1:>2}: {move}")

    def ask_player_move(self, moves):
        while True:
            try:
                choice = int(input("Izaberite broj poteza: "))
                if 1 <= choice <= len(moves):
                    return moves[choice-1]
                else:
                    print("Pogresan unos, probajte ponovo.")
            except ValueError:
                print("Unesite broj poteza.")