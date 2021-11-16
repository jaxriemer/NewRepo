# this is a class for the wac_a_mole game
import pygame

class whac_a_mole:
    def __init__(self, screen, background, mole, hole, x, y, imgX, imgY):
        self.board = [0,0,0,0,0]
        self.screen = screen
        self.background = background
        self.mole = mole
        self.hole = hole
        self.x = x
        self.y = y
        self.imgX = imgX
        self.imgY = imgY

    def mole(self, i):
        self.board[i] = 1

    def hole(self, i):
        self.board[i] = 0

    def draw_mole(self, i, b):
        if b == 0:
            img = self.hole
        else:
            img = self.mole

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
        self.screen.blit(img_background, (0, 0))
        i = 0
        for b in self.board:
            draw_mole(i, b)
            i += 1
