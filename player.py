from config import HUMAN, COMPUTER, CROSS, NAUGHT
from evaluator import Evaluator
from minimax import MiniMax
import random
import time


class HumanPlayer:
    def __init__(self, shape, gui):
        self.shape = shape
        self.gui = gui
        self.type = HUMAN
        self.current_board = None

    def get_current_board(self, board):
        self.current_board = board

    def get_move(self):
        while True:
            move = self.gui.get_mouse_input()
            if self.current_board.is_valid_location(move[0], move[1]):
                break
        return move


class Computer:
    def __init__(self, shape):
        self.shape = shape
        self.type = COMPUTER
        self.current_board = None

    def get_current_board(self, board):
        self.current_board = board

    def other_shape(self):
        if self.shape == CROSS:
            return NAUGHT
        else:
            return CROSS


class RandomPlayer(Computer):
    def __init__(self, shape):
        Computer.__init__(self, shape)
        self.name_str = 'Random'

    def get_move(self):
        while True:
            xpos = random.randint(0, 2)
            ypos = random.randint(0, 2)
            if self.current_board.is_valid_location(xpos, ypos):
                break
        return xpos, ypos


class SmartPlayer(Computer):
    def __init__(self, shape):
        Computer.__init__(self, shape)
        self.name_str = 'Smart'

    def get_move(self):
        # get valid moves
        valid_moves = self.current_board.get_valid_moves()
        # if the board is empty (first move) play in the middle
        if self.current_board.count_pieces() == 0:
            return 1, 1
        # if the other player has gone first, try to play in the middle, else play in the corner
        if self.current_board.count_pieces() == 1:
            if (1, 1) in valid_moves:
                return 1, 1
            else:
                return 0, 0
        # check if making a move results in a win
        for move in valid_moves:
            next_board = self.current_board.next_state(move[0], move[1], self.shape)
            if next_board.check_win(self.shape):
                return move
        # check other player win - the need to block
        for move in valid_moves:
            next_board = self.current_board.next_state(move[0], move[1], self.other_shape())
            if next_board.check_win(self.other_shape()):
                return move
        rand_move = random.choice(valid_moves)
        return rand_move[0], rand_move[1]


class SmartestPlayer(Computer):

    def __init__(self, shape, depth_lim=9):
        Computer.__init__(self, shape)
        evaluator = Evaluator()
        self.mini_max_obj = MiniMax(evaluator.eval, self.shape, self.other_shape())
        self.depth_lim = depth_lim
        self.name_str = 'MiniMax'

    def get_move(self):
        if self.current_board.count_empty() == 9:
            pos = [random.choice([0, 1, 2]), random.choice([0, 1, 2])]
        else:
            start_time = time.time()
            move = self.mini_max_obj.minimax(self.current_board, self.depth_lim, self.shape, self.other_shape())
            end_time = time.time()
            print(f'Elapsed time (Alpha-Beta): {end_time - start_time}')
            pos = [move[1], move[2]]
        return pos


class PrunePlayer(Computer):
    def __init__(self, shape, depth_lim=9):
        Computer.__init__(self, shape)
        evaluator = Evaluator()
        self.mini_max_obj = MiniMax(evaluator.eval, self.shape, self.other_shape())
        self.depth_lim = depth_lim
        self.name_str = 'Prune'

    def get_move(self):
        if self.current_board.count_empty() == 9:
            pos = [random.choice([0, 1, 2]), random.choice([0, 1, 2])]
        else:
            start_time = time.time()
            score, pos = self.mini_max_obj.minimax_alphabeta(self.current_board, self.depth_lim, self.shape, self.other_shape())
            end_time = time.time()
            print(f'Elapsed time (Pruned): {end_time - start_time}')
        return pos
