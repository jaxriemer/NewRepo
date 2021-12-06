import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import sys
import paho.mqtt.client as mqtt
import uuid
import time
from pydub import AudioSegment
from pydub.playback import play

# control servo to complete the cloth deliver function
from adafruit_servokit import ServoKit

topic_hand_gesture = 'IDD/face_hand_gesture'
hand_gesture = 'not recieved'

def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic_hand_gesture)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')

# this is the callback that gets called each time a message is recieved
def on_message(cleint, userdata, msg):
	# you can filter by topics
    print('here')
    if msg.topic == topic_hand_gesture:
        global hand_gesture
        hand_gesture = msg.payload.decode('UTF-8')
        print(hand_gesture)

    # if msg.topic == topic_body:
    #     global body_pos
    #     body_pos = msg.payload.decode('UTF-8')

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))

# configure network encryption etc
client.tls_set()

# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

# this is blocking. to see other ways of dealing with the loop
#  https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#network-loop

def face_interaction(cue):
    if cue == "greet":
        greet_sound = AudioSegment.from_file("voice_package/greeting.m4a")
        play(greet_sound)

    elif cue == "moved":
        moving_reaction = AudioSegment.from_file("voice_package/moving.m4a")
        play(moving_reaction)


while True:

    print(hand_gesture)

    if hand_gesture == 'handwaving':
        face_interaction('greet')

    elif hand_gesture == 'secret':
        face_interaction('moved')




























