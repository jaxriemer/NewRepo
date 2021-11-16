# this is a class for the wac_a_mole game
import pygame

class whac_a_mole:
    def __init__(self, background):
        self.background = background;
        self.board = [0,0,0,0,0]

    def draw_mole(self, i, img, screen, x, y):
        if i == 1:
            screen.blit(img, (0, 0))
        elif i == 2:
            screen.blit(img, (0, 0))
        elif i == 3:
            screen.blit(img, (0, 0))
        elif i == 4:
            screen.blit(img, (0, 0))
        elif i == 5:
            screen.blit(img, (0, 0))

