# importing the required libraries
import pygame as pg
import sys
import time
from pygame.locals import *
import network


class Player:
    XO = None
    turn = "X"
    winner = None
    draw = None
    row_data = None
    col_data = None
    width = 400
    height = 400
    white = (255, 255, 255)
    line_color = (0, 0, 0)
    board = [[None] * 3, [None] * 3, [None] * 3]
    fps = 30
    CLOCK = pg.time.Clock()
    screen = pg.display.set_mode((width, height + 100), 0, 32)

    initiating_window = pg.image.load("modified_cover.jpg")
    x_img = pg.image.load("X_modified.png")
    y_img = pg.image.load("o_modified.png")

    initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
    x_img = pg.transform.scale(x_img, (80, 80))
    o_img = pg.transform.scale(y_img, (80, 80))

    def __init__(self):
        pg.init()
        self.screen.blit(self.initiating_window, (0, 0))
        pg.display.update()
        self.client = network.Network()
        data = self.client.connect()
        data = str(data).split(":")
        self.XO = data[0]
        print(self.XO)
        time.sleep(3)
        pg.display.set_caption("Tic Tac Toe " + self.XO)
        self.game_initiating_window()

    @staticmethod
    def read_data(message):
        message = message.split(":")
        return int(message[0]), int(message[1])

    @staticmethod
    def make_data(tup):
        return str(tup[0]) + ":" + str(tup[1])

    def start(self):
        while True:
            if self.turn == self.XO:
                for event in pg.event.get():
                    print(event.type)
                    if event.type == QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        self.user_click()
                        if self.row_data and self.col_data:
                            print(f"sending {self.make_data((self.row_data, self.col_data))}")
                            self.client.send(self.make_data((self.row_data, self.col_data)))
                        if self.winner or self.draw:
                            self.reset_game()
                pg.display.update()
                self.CLOCK.tick(self.fps)

            elif self.turn != self.XO:
                d = self.client.receive()
                cords = self.read_data(d)
                print(cords)
                pg.event.clear()
                if cords[0] is not None and cords[1] is not None:
                    self.drawXO(cords[0], cords[1])

            if self.winner or self.draw:
                self.reset_game()
            

    def game_initiating_window(self):

        self.screen.fill(self.white)

        pg.draw.line(self.screen, self.line_color, (self.width / 3, 0), (self.width / 3, self.height), 7)
        pg.draw.line(self.screen, self.line_color, (self.width / 3 * 2, 0), (self.width / 3 * 2, self.height), 7)

        pg.draw.line(self.screen, self.line_color, (0, self.height / 3), (self.width, self.height / 3), 7)
        pg.draw.line(self.screen, self.line_color, (0, self.height / 3 * 2), (self.width, self.height / 3 * 2), 7)
        self.draw_status()

    def draw_status(self):
        if self.winner is None:
            message = self.turn + "'s Turn"
        else:
            message = self.winner + " won !"
        if self.draw:
            message = "Game Draw !"

        font = pg.font.Font(None, 30)
        text = font.render(message, True, (255, 255, 255))
        self.screen.fill((0, 0, 0), (0, 400, 500, 100))
        text_rect = text.get_rect(center=(self.width / 2, 500 - 50))
        self.screen.blit(text, text_rect)
        pg.display.update()

    def check_win(self):
        self.winner_count()
        if self.winner is None and all([all(row) for row in self.board]):
            self.draw = True
        self.draw_status()

    def winner_count(self):
        for row in range(0, 3):
            if (self.board[row][0] == self.board[row][1] == self.board[row][2]) and (self.board[row][0] is not None):
                self.winner = self.board[row][0]
                pg.draw.line(self.screen, (250, 0, 0),
                             (0, (row + 1) * self.height / 3 - self.height / 6),
                             (self.width, (row + 1) * self.height / 3 - self.height / 6), 4)
                return

        for col in range(0, 3):
            if (self.board[0][col] == self.board[1][col] == self.board[2][col]) and (self.board[0][col] is not None):
                self.winner = self.board[0][col]
                pg.draw.line(self.screen, (250, 0, 0), ((col + 1) * self.width / 3 - self.width / 6, 0),
                             ((col + 1) * self.width / 3 - self.width / 6, self.height), 4)
                return

        if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] is not None):
            self.winner = self.board[0][0]
            pg.draw.line(self.screen, (250, 70, 70), (50, 50), (350, 350), 4)
            return

        elif (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] is not None):
            self.winner = self.board[0][2]
            pg.draw.line(self.screen, (250, 70, 70), (350, 50), (50, 350), 4)
            return

    def drawXO(self, row, col):
        self.row_data = row
        self.col_data = col

        if row == 1:
            posx = 30
        elif row == 2:
            posx = self.width / 3 + 30
        elif row == 3:
            posx = self.width / 3 * 2 + 30

        if col == 1:
            posy = 30
        elif col == 2:
            posy = self.height / 3 + 30
        elif col == 3:
            posy = self.height / 3 * 2 + 30

        self.board[row - 1][col - 1] = self.turn

        if self.turn == 'X':
            self.screen.blit(self.x_img, (posy, posx))
            self.turn = 'O'
        else:
            self.screen.blit(self.o_img, (posy, posx))
            self.turn = 'X'
        self.check_win()
        pg.display.update()

    def user_click(self):
        print("check cklick")
        x, y = pg.mouse.get_pos()

        if x < self.width / 3:
            col = 1
        elif x < self.width / 3 * 2:
            col = 2
        elif x < self.width:
            col = 3
        else:
            col = None

        if y < self.height / 3:
            row = 1
        elif y < self.height / 3 * 2:
            row = 2
        elif y < self.height:
            row = 3
        else:
            row = None

        if row and col and self.board[row - 1][col - 1] is None:
            self.drawXO(row, col)

    def reset_game(self):
        time.sleep(3)
        self.turn = "X"
        self.draw = False
        self.winner = None
        self.row_data = None
        self.col_data = None
        self.board = [[None] * 3, [None] * 3, [None] * 3]
        self.game_initiating_window()


player = Player()
player.start()
