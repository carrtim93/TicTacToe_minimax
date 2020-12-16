from config import NAUGHT, CROSS, EMPTY


class Evaluator:
    WIN_SCORE = 1000
# if the board is losing -inf
# if the board is wining +inf
# else 0

    # should be static, but I may add functionality to it later
    def eval(self, board, empty_space, player, other):
        if board.check_win(player):
            score = 100 * empty_space
        elif board.check_win(other):
            score = -100 * empty_space
        else:
            score = 0
        return score
