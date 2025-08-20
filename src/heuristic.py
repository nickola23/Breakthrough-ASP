import constants

def evaluate_board(board, player):
    opponent = constants.BLACK if player == constants.WHITE else constants.WHITE
    score = 0

    center_column = board.size // 2

    for row in range(board.size):
        for col in range(board.size):
            piece = board.board[row][col]
            if piece == player:
                # osnovni faktor: broj figura
                score += 10

                # napredak prema protivnickoj strani
                if player == constants.WHITE:
                    score += (board.size - row)
                else:
                    score += row + 1

                # bonus za centar table
                score += 3 - abs(col - center_column)

                # mobilnost: broj legalnih poteza za figuru
                moves = board.generate_moves_for_piece(row, col, player)
                score += len(moves)

                # bonus za mogucnost skoka protivnika
                for move in moves:
                    if move.move_type == constants.CAPTURE:
                        score += 5

                # kazemo minus ako je figura izlozena protivniku (diagonalno iza nje)
                exposed = False
                if player == constants.WHITE:
                    if row > 0:
                        for dc in (-1, 1):
                            r, c = row - 1, col + dc
                            if board.in_bounds(r, c) and board.get_piece(r, c) == opponent:
                                exposed = True
                    if exposed:
                        score -= 5
                else:
                    if row < board.size - 1:
                        for dc in (-1, 1):
                            r, c = row + 1, col + dc
                            if board.in_bounds(r, c) and board.get_piece(r, c) == opponent:
                                exposed = True
                    if exposed:
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