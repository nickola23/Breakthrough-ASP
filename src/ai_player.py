from board import Board
from move import Move
from heuristic import evaluate_board
import constants

def choose_best_move(board: Board, player):
    moves = board.generate_moves_for_player(player)
    best_score = float('-inf')
    best_move = moves[0] if moves else None

    for move in moves:
        board.make_move(move)
        score = evaluate_board(board, player)
        board.undo_move()
        if score > best_score:
            best_score = score
            best_move = move

    return best_move