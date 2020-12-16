import player
import board
from config import *
import gui

import pygame

import sys
import random


class TicTacToeGame:

    def __init__(self):
        self.gui = gui.Gui()
        self.board = board.Board(3)
        self.players = []
        self.current_player = None
        self.other_player = None
        self.game_over = False

        self.start()

    def start(self):

        player1, player2 = self.gui.start_menu()
        self.current_player = self.create_player(player1, NAUGHT)
        self.other_player = self.create_player(player2, CROSS)

    def next_turn(self):
        self.current_player, self.other_player = self.other_player, self.current_player
        return self

    def create_player(self, player_type, shape):
        if player_type == 0:
            return player.HumanPlayer(shape, self.gui)
        elif player_type == 1:
            return player.RandomPlayer(shape)
        elif player_type == 2:
            return player.SmartPlayer(shape)
        elif player_type == 3:
            return player.SmartestPlayer(shape)
        elif player_type == 4:
            return player.PrunePlayer(shape)

    def run(self):
        while not self.game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # pause if computer turn
            if self.current_player.type == HUMAN and self.other_player.type == COMPUTER:
                pygame.time.wait(1000)
            elif self.current_player.type == COMPUTER and self.other_player == COMPUTER:
                pygame.time.wait(200)
            self.gui.draw_board(self.board)
            self.board.print_board()

            self.current_player.get_current_board(self.board)
            xpos, ypos = self.current_player.get_move()

            self.board.place_piece(xpos, ypos, self.current_player.shape)

            # check win
            if self.board.check_win(self.current_player.shape):
                print(f'{self.current_player.shape} has won!')
                self.board.print_board()
                self.game_over = True

            # check draw
            if self.board.check_draw():
                print('Game is tied')
                self.board.print_board()
                self.game_over = True
            self.next_turn()


def run():
    game = TicTacToeGame()
    game.run()


if __name__ == '__main__':
    run()
