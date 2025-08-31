import constants

def evaluate_board(board, player):
    if player == constants.WHITE:
        opponent = constants.BLACK
    else:
        opponent = constants.WHITE

    score = 0
    center_column = board.size // 2

    for row in range(board.size):
        for col in range(board.size):
            piece = board.board[row][col]
            if piece == player:
                # broj figura
                score += 10

                # napredak
                if player == constants.WHITE:
                    score += (board.size - row)
                else:
                    score += row + 1

                # bonus za centar table
                score += 3 - abs(col - center_column)

                # broj mogucih poteza
                moves = board.generate_moves_for_piece(row, col, player)
                score += len(moves)

                # mogucnost uzimanja protivnika
                for move in moves:
                    if move.move_type == constants.CAPTURE:
                        score += 5

                # minus ako je figura ugrozena
                is_exposed = False
                if player == constants.WHITE:
                    row_direction = -1
                else:
                    row_direction = 1
                next_row = row + row_direction

                if 0 <= next_row < board.size:
                    for col_offset in (-1, 1):
                        next_col = col + col_offset
                        if board.in_bounds(next_row, next_col) and board.get_piece(next_row, next_col) == opponent:
                            is_exposed = True
                            break

                if is_exposed:
                    score -= 5

            elif piece == opponent:
                # smanjujemo za protivnicke figure
                score -= 10
                # dodatni minus za njihov napredak
                if player == constants.WHITE:
                    score -= (row)
                else:
                    score -= (board.size - row - 1)

    return score