import pygame
import random
import time
import sys
import os
import paho.mqtt.client as mqtt
import uuid

import pygame

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

# setup pygame
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screenX, screenY = pygame.display.get_surface().get_size()
running = True

# load assets
cwd = os.getcwd()
img_background = pygame.image.load(cwd + "/imgs/Background.png")
img_background = pygame.transform.scale(img_background, (screenX, screenY))

# our main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = Flase

    screen.blit(img_background, (0, 0))
    pygame.display.update()