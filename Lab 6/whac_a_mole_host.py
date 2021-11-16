import pygame
import random
import time
import sys
import os
import paho.mqtt.client as mqtt
import uuid

import pygame
import whac_a_mole

import board
import busio
import adafruit_mpr121

topic = 'IDD/WacAMole'

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)

def on_message(cleint, userdata, msg):
    # if a message is recieved on the colors topic, parse it and set the color
    if msg.topic == topic:
        # TODO
        st = 0

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
#signal.signal(signal.SIGINT, handler)

# setup touch sensor
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# setup pygame
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
the_game = whac_a_mole.whac_a_mole(screen, img_background, img_Mole, img_Hole, screenX, screenY, holeX, holeY)

# our main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # mole 0
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


    the_game.draw_game()

    pygame.display.update()