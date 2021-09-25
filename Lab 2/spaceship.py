import math
from PIL import Image, ImageDraw, ImageFont

# our space ship

class spaceship:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.velocity = 0.03

    def draw(self, img):
        offset = (self.x-7, self.y-7, self.x+8, self.y+8)
        img.paste(Image.open(self.image), offset)

    def move(self, dx, dy):
        self.x += int(dx * self.velocity)
        self.y += int(dy * self.velocity)

class bullet:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.velocity = 20

    def draw(self, draw):
        offset = (self.x-2, self.y-2, self.x+2, self.y+2)
        draw.rectangle(offset, outline="red", fill="red")

    def move(self):
        self.x += self.vx * self.velocity
        self.y += self.vy * self.velocity



class bullets:
    def __int__(self):
        self.bs = []

    def addBullet(self, x, y, vx, vy):
        self.bs.append(bullet(x,y,vx,vy))

    def moveBullets(self):
        for b in self.bs:
            b.move()

    def removeBullets(self):
        for b in self.bs:
            if b.x > 250 or b.x < -10 or b.y > 145 or b.y < -10:
                self.bs.remove(b)

    def drawBullets(self, draw):
        for b in self.bs:
            b.draw(draw)

    def updateBullets(self, draw):
        self.moveBullets()
        self.removeBullets()
        self.drawBullets()
