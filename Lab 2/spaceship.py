import math
from PIL import Image, ImageDraw, ImageFont

# our space ship

class spaceship:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.velocity = 0.01

    def draw(self, img):
        offset = (self.x-7, self.y-7, self.x+8, self.y+8)
        img.paste(Image.open(self.image), offset)

    def move(self, dx, dy):
        self.x += int(dx * self.velocity)
        self.y += int(dy * self.velocity)
