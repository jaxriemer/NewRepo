import math
from PIL import Image, ImageDraw, ImageFont

# our space ship

class spaceship:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, img):
        offset = (self.x-7, self.y-7, self.x+8, self.y+8)
        img.paste(Image.open(self.image), offset)