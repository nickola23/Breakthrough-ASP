from board import Board
from move import Move
from heuristic import evaluate_board
import constants
import time

class AIPlayer:
    def __init__(self, player, max_depth=3, time_limit=3.0):
        self.player = player
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.hashed_table = {}

    def choose_move(self, board):
        start_time = time.perf_counter()

        legal_moves = board.generate_moves_for_player(self.player)
        for move in legal_moves:
            board.make_move(move)
            if board.get_winner() == self.player:
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
        moves = board.generate_moves_for_player(self.player)

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
        board_key = (str(board.board), depth, maximizing_player)

        if board_key in self.hashed_table:
            saved_depth, saved_score = self.hashed_table[board_key]
            if saved_depth >= depth:
                return saved_score

        if depth == 0 or board.get_winner() is not None:
            score = evaluate_board(board, self.player)
            self.hashed_table[board_key] = (depth, score)
            return score
        if time.perf_counter() - start_time > self.time_limit:
            raise TimeoutError()

        if maximizing_player:
            current_player = self.player
        else:
            if self.player == constants.WHITE:
                current_player = constants.BLACK
            else:
                current_player = constants.WHITE

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
            self.hashed_table[board_key] = (depth, max_eval)
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
            self.hashed_table[board_key] = (depth, min_eval)
            return min_eval