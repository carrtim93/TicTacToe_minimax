INF = 10000
from config import CROSS, NAUGHT


class MiniMax:

    def __init__(self, heuristic_eval, player, other):
        self.init_player = player
        self.init_other = other
        self.heuristic_eval = heuristic_eval

    def minimax(self, board, depth, player, opponent):
        # Minimax function without alpha beta pruning
        if player == CROSS:         # if computer
            best = [-INF, -1, -1]
        else:                       # if human
            best = [INF, -1, -1]

        if depth == 0 or board.game_over():
            score = self.heuristic_eval(board, board.count_empty(), self.init_player, self.init_other)
            return [score, -1, -1]

        for move in board.get_valid_moves():
            xpos, ypos = move[0], move[1]
            next_board = board.next_state(xpos, ypos, player)
            score = self.minimax(next_board, depth - 1, opponent, player)
            score[1], score[2] = xpos, ypos

            if player == self.init_player:
                if score[0] > best[0]:
                    best = score        # max value
            else:
                if score[0] < best[0]:
                    best = score        # min value
        return best

    def minimax_alphabeta(self, board, depth, player, opponent, alpha=-INF, beta=INF):
        # Minimax function with alpha beta pruning
        best_pos = [-1, -1]

        if depth == 0 or board.game_over():
            score = self.heuristic_eval(board, board.count_empty(), self.init_player, self.init_other)
            return score, [-1, -1]

        for move in board.get_valid_moves():
            xpos, ypos = move[0], move[1]
            next_board = board.next_state(xpos, ypos, player)
            score, pos = self.minimax_alphabeta(next_board, depth - 1, opponent, player, alpha, beta)
            pos[0], pos[1] = xpos, ypos

            if player == self.init_player:
                if score > alpha:
                    alpha = score        # max value
                    best_pos = pos
            else:
                if score < beta:
                    beta = score        # min value
                    best_pos = pos
            if beta <= alpha:
                break
        if player == self.init_player:
            return alpha, best_pos
        else:
            return beta, best_pos


