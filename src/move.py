import constants

class Move:
    def __init__(self, from_row, from_col, to_row, to_col, move_type=constants.MOVE):
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_row
        self.to_col = to_col
        self.move_type = move_type

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (self.from_row == other.from_row and
                self.from_col == other.from_col and
                self.to_row == other.to_row and
                self.to_col == other.to_col and
                self.move_type == other.move_type)

    def __str__(self):
        type_str = "CAPTURE" if self.move_type == constants.CAPTURE else "MOVE"
        return f"{constants.COLUMNS[self.from_col]}{self.from_row+1} -> {constants.COLUMNS[self.to_col]}{self.to_row+1} {type_str}"
