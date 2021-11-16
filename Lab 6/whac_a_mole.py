# this is a class for the wac_a_mole game

class wac_a_mole:
    def __init__(self, background):
        self.background = background;
        self.board = [0,0,0,0,0,0,0,0,0]

    def draw_mole(self, i, img):
