import math


# our space ship

class spaceship:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, draw):
        offset = (self.x, self.y)
        draw.paste(self.image, offset)