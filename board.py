import numpy as np
from config import NAUGHT, CROSS, EMPTY
from copy import deepcopy


class Board:

    def __init__(self, dim):

        # set up initial board configuration
        self.dim = dim
        self.pieces = np.zeros((self.dim,self.dim))

    def __getitem__(self, ind):
        return self.pieces[ind]

    def is_valid_location(self, xpos, ypos):
        if self[ypos][xpos] == EMPTY:
            return True
        else:
            return False

    def place_piece(self, xpos, ypos, shape):
        self[ypos][xpos] = shape

    def check_win(self, shape):
        # check horizontals
        for y in range(self.dim):
            if self[y][0] == shape and self[y][1] == shape and self[y][2] == shape:
                return True
        # check vertical
        for x in range(self.dim):
            if self[0][x] == shape and self[1][x] == shape and self[2][x] == shape:
                return True
        # check diagonal
        if self[0][0] == shape and self[1][1] == shape and self[2][2] == shape:
            return True
        elif self[0][2] == shape and self[1][1] == shape and self[2][0] == shape:
            return True
        return False

    def check_draw(self):
        for x in range(self.dim):
            for y in range(self.dim):
                if self[y][x] == EMPTY:
                    return False
        return True

    def game_over(self):
        return self.check_win(NAUGHT) or self.check_win(CROSS) or self.check_draw()

    def count_pieces(self):
        return np.count_nonzero(self.pieces)

    def count_empty(self):
        return np.count_nonzero(self.pieces == 0)

    def get_valid_moves(self):
        valid_moves = []
        for x in range(self.dim):
            for y in range(self.dim):
                if self[y][x] == EMPTY:
                    valid_moves.append((x, y))
        return valid_moves

    def next_state(self, x, y, shape):
        new_board = deepcopy(self)
        new_board.place_piece(x, y, shape)
        return new_board

    def print_board(self):
        print(self.pieces)
