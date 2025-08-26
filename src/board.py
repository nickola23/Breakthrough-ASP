import constants
from move import Move

class Board:
    def __init__(self):
        self.size = constants.BOARD_SIZE
        self.side_to_move = constants.WHITE
        self.move_history = []
        self.last_move = None
        self.board = []

        for i in range(constants.BOARD_SIZE):
            row = []
            for j in range(constants.BOARD_SIZE):
                row.append(constants.EMPTY)
            self.board.append(row)

        self.setup_start_position()

    def setup_start_position(self):
        for row_index in range(0, 2):
            for col_index in range(self.size):
                self.board[row_index][col_index] = constants.BLACK
        for row_index in range(self.size - 2, self.size):
            for col_index in range(self.size):
                self.board[row_index][col_index] = constants.WHITE

    def in_bounds(self, row_index, col_index):
        return 0 <= row_index < self.size and 0 <= col_index < self.size

    def get_piece(self, row_index, col_index):
        if not self.in_bounds(row_index, col_index):
            return None
        return self.board[row_index][col_index]

    def set_piece(self, row_index, col_index, piece):
        self.board[row_index][col_index] = piece

    def make_move(self, move):
        captured_piece = self.get_piece(move.to_row, move.to_col)
        moving_piece = self.get_piece(move.from_row, move.from_col)
        self.set_piece(move.to_row, move.to_col, moving_piece)
        self.set_piece(move.from_row, move.from_col, constants.EMPTY)
        self.move_history.append((move, captured_piece, self.side_to_move))
        self.last_move = move
        if self.side_to_move == constants.WHITE:
            self.side_to_move = constants.BLACK
        else:
            self.side_to_move = constants.WHITE

    def undo_move(self):
        if not self.move_history:
            return
        move, captured_piece, previous_side = self.move_history.pop()
        moving_piece = self.get_piece(move.to_row, move.to_col)
        self.set_piece(move.from_row, move.from_col, moving_piece)
        self.set_piece(move.to_row, move.to_col, captured_piece if captured_piece is not None else constants.EMPTY)
        self.side_to_move = previous_side
        if self.move_history:
            self.last_move = self.move_history[-1][0]
        else:
            self.last_move = None

    def get_winner(self):
        for col_index in range(self.size):
            if self.board[0][col_index] == constants.WHITE:
                return constants.WHITE
            if self.board[self.size - 1][col_index] == constants.BLACK:
                return constants.BLACK
        return None

    def generate_moves_for_player(self, player):
        moves = []
        for row_index in range(self.size):
            for col_index in range(self.size):
                if self.board[row_index][col_index] == player:
                    moves.extend(self.generate_moves_for_piece(row_index, col_index, player))
        return moves

    def generate_moves_for_piece(self, row_index, col_index, player):
        moves = []
        if player == constants.WHITE:
            target_row = row_index - 1
            opponent = constants.BLACK
        else:
            target_row = row_index + 1
            opponent = constants.WHITE

        if self.in_bounds(target_row, col_index) and self.board[target_row][col_index] == constants.EMPTY:
            moves.append(Move(row_index, col_index, target_row, col_index, constants.MOVE))

        for target_col in (col_index - 1, col_index + 1):
            if not self.in_bounds(target_row, target_col):
                continue
            target_piece = self.board[target_row][target_col]
            if target_piece == constants.EMPTY:
                moves.append(Move(row_index, col_index, target_row, target_col, constants.MOVE))
            elif target_piece == opponent:
                moves.append(Move(row_index, col_index, target_row, target_col, constants.CAPTURE))

        return moves