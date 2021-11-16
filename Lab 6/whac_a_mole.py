# this is a class for the wac_a_mole game
import pygame

class whac_a_mole:
    def __init__(self, screen, background, hammer, mole, hole, hitmole, hithole, x, y, imgX, imgY):
        # 0 hole, 1 mole, 2 hit hole, 3 hit mole
        self.board = [1,1,1,1,1]
        self.screen = screen
        self.background = background
        self.hammer = hammer
        self.mole = mole
        self.hole = hole
        self.hitmole = hitmole
        self.hithole = hithole
        self.x = x
        self.y = y
        self.imgX = imgX
        self.imgY = imgY

    def set_hole(self, i):
        if self.board[i] == 1:
            self.board[i] = 0

    def set_mole(self, i):
        if self.board[i] == 0:
            self.board[i] = 1

    def hit_hole(self, i):
            self.board[i] = 2

    def hit_mole(self, i):
            self.board[i] = 3

    def hit(self, i):
        print('hit ' + str(i))
        if 2 not in self.board and 3 not in self.board:
            if self.board[i] == 0:
                self.hit_hole(i)
            if self.board[i] == 1:
                self.hit_mole(i)

    def reset_hit(self):
        i = 0
        for b in self.board:
            if b == 2 or b == 3:
                self.board[i] = 0
            i += 1

    def draw_mole(self, i, b):
        if b == 0:
            img = self.hole
        elif b == 1:
            img = self.mole
        elif b == 2:
            img = self.hithole
        elif b == 3:
            img = self.hitmole

        if i == 0:
            self.screen.blit(img, (self.x / 2 - self.imgX * 3 / 2, self.y / 2 - self.imgY / 2))
        elif i == 1:
            self.screen.blit(img, (self.x / 2 - self.imgX / 2, self.y / 2 - self.imgY / 2))
        elif i == 2:
            self.screen.blit(img, (self.x / 2 + self.imgX / 2, self.y / 2 - self.imgY / 2))
        elif i == 3:
            self.screen.blit(img, (self.x / 2 - self.imgX, self.y / 2))
        elif i == 4:
            self.screen.blit(img, (self.x / 2, self.y / 2))

    def draw_game(self):
        self.screen.blit(self.background, (0, 0))
        i = 0
        hit = False
        for b in self.board:
            self.draw_mole(i, b)
            if b == 2 or b == 3:
                hit = True
            i += 1
        if hit == False:
            self.screen.blit(self.hammer, (self.x / 2, self.y / 2))

    def game_to_str(self):
        return " ".join(str(b) for b in self.board)

    def str_to_game(self, str):
        game = str.split(" ")
        game = [int(s) for s in game]
        self.board = game
