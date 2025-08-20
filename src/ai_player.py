from board import Board
from move import Move
from heuristic import evaluate_board
import constants
import time

class AIPlayer:
    def __init__(self, player_color, max_depth=10, time_limit=3.0):
        self.player_color = player_color
        self.max_depth = max_depth
        self.time_limit = time_limit

    def choose_move(self, board):
        start_time = time.perf_counter()

        legal_moves = board.generate_moves_for_player(self.player_color)
        for move in legal_moves:
            board.make_move(move)
            if board.get_winner() == self.player_color:
                board.undo_move()
                return move
            board.undo_move()
        
        best_move = None
        depth = 1

        while depth <= self.max_depth:
            try:
                move, _ = self.search_best_move(board, depth, start_time)
                best_move = move
            except TimeoutError:
                break
            depth += 1

        return best_move

    def search_best_move(self, board, depth, start_time):
        best_score = float('-inf')
        best_move = None
        moves = board.generate_moves_for_player(self.player_color)

        if not moves:
            return None, 0

        for move in moves:
            if time.perf_counter() - start_time > self.time_limit:
                raise TimeoutError()
            board.make_move(move)
            score = self.minimax(board, depth - 1, float('-inf'), float('inf'), False, start_time)
            board.undo_move()
            if score > best_score:
                best_score = score
                best_move = move

        return best_move, best_score

    def minimax(self, board: Board, depth, alpha, beta, maximizing_player, start_time):
        if depth == 0 or board.get_winner() is not None:
            return evaluate_board(board, self.player_color)
        if time.perf_counter() - start_time > self.time_limit:
            raise TimeoutError()

        current_player = self.player_color if maximizing_player else (constants.BLACK if self.player_color == constants.WHITE else constants.WHITE)
        moves = board.generate_moves_for_player(current_player)

        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                board.make_move(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False, start_time)
                board.undo_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                board.make_move(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True, start_time)
                board.undo_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
