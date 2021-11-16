import pygame
import random
import time
import sys
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
signal.signal(signal.SIGINT, handler)

# setup pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
running = True

# our main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False