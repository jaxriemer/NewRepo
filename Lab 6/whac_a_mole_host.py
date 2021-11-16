import pygame
import random
import time
import sys
import os
import paho.mqtt.client as mqtt
import uuid
import signal

import pygame
import whac_a_mole

import board
import busio
import adafruit_mpr121

import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

topic = 'IDD/WacAMole'

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

BAUDRATE = 64000000

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

height =  disp.height
width = disp.width
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

#global current_board
cloud_board = "0 0 0 0 0"

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)

def on_message(cleint, userdata, msg):
    # if a message is recieved on the colors topic, parse it and set the color
    if msg.topic == topic:
        print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
        cloud_board = {msg.payload.decode('UTF-8')}
        #current_board = list(map(int, msg.payload.decode('UTF-8').split(',')))


client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')
client.on_connect = on_connect
client.on_message = on_message

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

client.loop_start()

# this lets us exit gracefully (close the connection to the broker)
def handler(signum, frame):
    print('exit gracefully')
    client.loop_stop()
    exit (0)

# hen sigint happens, do the handler callback function
# signal.signal(signal.SIGINT, handler)

# setup touch sensor
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# setup pygame
pygame.init()
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((800, 450))
screenX, screenY = pygame.display.get_surface().get_size()
running = True

# load assets
cwd = os.getcwd()
img_background = pygame.image.load(cwd + "/imgs/Background.png")
img_background = pygame.transform.scale(img_background, (screenX, screenY))
holeX = screenX/5.3
holeY = screenY/2.25
img_Mole = pygame.image.load(cwd + "/imgs/Mole.png")
img_Mole = pygame.transform.scale(img_Mole, (holeX, holeY))
img_Hole = pygame.image.load(cwd + "/imgs/Hole.png")
img_Hole = pygame.transform.scale(img_Hole, (holeX, holeY))
img_hammer = pygame.image.load(cwd + "/imgs/Hammer.png")
img_hammer = pygame.transform.scale(img_hammer, (screenX/2, screenY/2))
img_hitHole = pygame.image.load(cwd + "/imgs/HitHole.png")
img_hitHole = pygame.transform.scale(img_hitHole, (holeX, screenY/1.5))
img_hitMole = pygame.image.load(cwd + "/imgs/HitMole.png")
img_hitMole = pygame.transform.scale(img_hitMole, (holeX, screenY/1.5))

# init game
the_game = whac_a_mole.whac_a_mole(screen, img_background, img_hammer, img_Mole, img_Hole, img_hitMole, img_hitHole, screenX, screenY, holeX, holeY)

# ask the user to choose whether they want to set the mole or hit the mole
Player_set, Player_hit = False, False

while not Player_set and not Player_hit:
    player_choice = input(">> Enter 1 if you want to set the mole and 2 if you want to hit the mole: ")
    if player_choice == "2":
        Player_hit = True
        print("You have chosen to hit the mole.")
    if player_choice == "1":
        Player_set = True
        print("You have chosen to set the mole.")

# our main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    print(cloud_board)
    the_game.str_to_game(cloud_board)

    # player's side
    if Player_hit:
        #print("current board:")
        #print(current_board)
        hitting = [0,0,0,0,0]
        # mole 0
        if mpr121[5].value or mpr121[4].value:
            the_game.hit(0)
        else:
            hitting[0] = 1
        # mole 1
        if mpr121[3].value or mpr121[2].value:
            the_game.hit(1)
        else:
            hitting[1] = 1
        # mole 2
        if mpr121[1].value or mpr121[0].value:
            the_game.hit(2)
        else:
            hitting[2] = 1
        # mole 3
        if mpr121[6].value or mpr121[7].value or mpr121[8].value:
            the_game.hit(3)
        else:
            hitting[3] = 1
        # mole 4
        if mpr121[9].value or mpr121[10].value or mpr121[11].value:
            the_game.hit(4)
        else:
            hitting[4] = 1

        # reset if not touching
        if 0 not in hitting:
            the_game.reset_hit()


    else:
        # mole 0
        #print(current_board)
        if mpr121[5].value or mpr121[4].value:
            the_game.set_mole(0)
        else:
            the_game.set_hole(0)
        # mole 1
        if mpr121[3].value or mpr121[2].value:
            the_game.set_mole(1)
        else:
            the_game.set_hole(1)
        # mole 2
        if mpr121[1].value or mpr121[0].value:
            the_game.set_mole(2)
        else:
            the_game.set_hole(2)
        # mole 3
        if mpr121[6].value or mpr121[7].value or mpr121[8].value:
            the_game.set_mole(3)
        else:
            the_game.set_hole(3)
        # mole 4
        if mpr121[9].value or mpr121[10].value or mpr121[11].value:
            the_game.set_mole(4)
        else:
            the_game.set_hole(4)

    message = the_game.game_to_str()
    client.publish(topic, message)

    the_game.draw_game()
    pygame.display.update()