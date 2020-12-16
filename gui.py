import pygame
import sys
import math
import os

from config import NAUGHT, CROSS

letterX = pygame.image.load(os.path.join('imgs', 'x.png'))
letterX = pygame.transform.scale(letterX, (112, 112))
letterO = pygame.image.load(os.path.join('imgs', 'o.png'))
letterO = pygame.transform.scale(letterO, (112, 112))


class Gui:
    def __init__(self):

        pygame.init()

        # colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREY = (150, 150, 150)
        self.GREEN = (100, 180, 100)

        # display
        self.BOARD_DIMENSION = 3
        self.SQUARE_SIZE = 128
        self.RADIUS = int(self.SQUARE_SIZE / 2 - 5)

        self.width = self.height = self.SQUARE_SIZE * self.BOARD_DIMENSION
        self.size = (self.width, self.height)

        self.screen = pygame.display.set_mode(self.size)

    def draw_menu_window(self, play_button, player1_slider, player2_slider):
        self.screen.fill(self.GREEN)
        play_button.draw(self.screen, (0, 0, 0))
        player1_slider.draw(self.screen, (0, 0, 0))
        player2_slider.draw(self.screen, (0, 0, 0))

    def start_menu(self):
        player_list = {0: 'Human', 1: 'Random', 2: 'Smart', 3: 'Minimax', 4: 'AlphaBeta'}
        player1_sel = 0
        player2_sel = 0

        play_button = Button(self.GREY, 96, 96, 192, 48, 'Play')
        player1_slider = Option(self.GREY, 96, 192, 192, 36, player_list, player1_sel)
        player2_slider = Option(self.GREY, 96, 246, 192, 36, player_list, player2_sel)

        while True:
            self.draw_menu_window(play_button, player1_slider, player2_slider)
            pygame.display.update()

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player1_slider.left_arrow.is_over(pos):
                        player1_slider.current_choice = (player1_slider.current_choice - 1) % len(player1_slider.choice_list)
                    elif player1_slider.right_arrow.is_over(pos):
                        player1_slider.current_choice = (player1_slider.current_choice + 1) % len(player1_slider.choice_list)
                    elif player2_slider.left_arrow.is_over(pos):
                        player2_slider.current_choice = (player2_slider.current_choice - 1) % len(player2_slider.choice_list)
                    elif player2_slider.right_arrow.is_over(pos):
                        player2_slider.current_choice = (player2_slider.current_choice + 1) % len(player2_slider.choice_list)

                    elif play_button.is_over(pos):
                        return player1_slider.current_choice, player2_slider.current_choice

    def get_mouse_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x_mouse, y_mouse = pygame.mouse.get_pos()
                    xpos = int(math.floor(x_mouse / self.SQUARE_SIZE))
                    ypos = int(math.floor(y_mouse / self.SQUARE_SIZE))
                    return xpos, ypos

    def draw_board(self, board):
        for x in range(self.BOARD_DIMENSION):
            for y in range(self.BOARD_DIMENSION):
                # Draw squares
                pygame.draw.rect(self.screen, self.GREEN,
                                 (x * self.SQUARE_SIZE, y * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
                pygame.draw.rect(self.screen, self.BLACK,
                                 (x * self.SQUARE_SIZE, y * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), 3)
        for x in range(self.BOARD_DIMENSION):
            for y in range(self.BOARD_DIMENSION):
                if board[y][x] == NAUGHT:
                    self.screen.blit(letterO, (x * self.SQUARE_SIZE + 8, y * self.SQUARE_SIZE + 8))
                elif board[y][x] == CROSS:
                    self.screen.blit(letterX, (x * self.SQUARE_SIZE + 8, y * self.SQUARE_SIZE + 8))
        pygame.display.update()


class Button:
    def __init__(self, colour, x, y, width, height, text=''):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def set_text(self, new_text):
        self.text = new_text
        return self

    def draw(self, wind, outline=None):
        if outline:
            pygame.draw.rect(wind, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(wind, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('Arial', 22)
            text = font.render(self.text, 1, (0, 0, 0))
            wind.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                             self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


class Triangle:
    def __init__(self, colour, x, y, size, direction):
        self.colour = colour
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction
        self.points = self.get_points()

    def get_points(self):
        if self.direction == 'right':
            point1 = [self.x, self.y]
            point2 = [self.x, self.y + self.size]
            point3 = [self.x + self.size, self.y + int(self.size / 2)]
        else:
            point1 = [self.x + self.size, self.y]
            point2 = [self.x + self.size, self.y + self.size]
            point3 = [self.x, self.y + int(self.size / 2)]
        return [point1, point2, point3]

    def draw(self, wind, outline=None):
        pygame.draw.polygon(wind, self.colour, self.points)
        if outline:
            pygame.draw.polygon(wind, outline, self.points, 2)

    def is_over(self, pos):
        if self.direction == 'right':
            if 2 * pos[1] - pos[0] >= 2 * self.y - self.x:
                if 2 * pos[1] + pos[0] <= 2 * self.y + 2 * self.size + self.x:
                    if pos[0] >= self.x:
                        return True
        else:
            if 2 * pos[1] + pos[0] >= 2 * self.y + self.size + self.x:
                if 2 * pos[1] - pos[0] <= 2 * self.y + self.size - self.x:
                    if pos[0] <= self.x + self.size:
                        return True
        return False


class Option:
    def __init__(self, colour, x, y, w, h, choice_list, current_choice):
        self.choice_list = choice_list
        self.current_choice = current_choice
        self.button = Button(colour, x, y, w, h, choice_list[current_choice])
        left_arrow_x = x - (3 * h / 2)
        self.left_arrow = Triangle(colour, left_arrow_x, y, h, 'left')
        right_arrow_x = x + w + (h / 2)
        self.right_arrow = Triangle(colour, right_arrow_x, y, h, 'right')

    def set_text(self, new_text):
        self.button.set_text(new_text)
        return self

    def draw(self, wind, outline=None):
        self.button.set_text(self.choice_list[self.current_choice])
        self.button.draw(wind, outline)
        self.left_arrow.draw(wind, outline)
        self.right_arrow.draw(wind, outline)
