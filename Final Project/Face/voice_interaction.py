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

topic_hand_gesture = 'IDD/oneteam/face_hand_gesture'
hand_gesture = 'not received'

def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic_hand_gesture)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')

# this is the callback that gets called each time a message is recieved
def on_message(cleint, userdata, msg):
	# you can filter by topics
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

client.loop_start()

def face_interaction(hand_gesture):
    if hand_gesture == "handwaving":
        greet_sound = AudioSegment.from_file("voice_package/greeting.m4a")
        play(greet_sound)

    elif hand_gesture == "thumb_down":
        moving_reaction = AudioSegment.from_file("voice_package/thumb_down.m4a")
        play(moving_reaction)

    elif hand_gesture == "heart":
        moving_reaction = AudioSegment.from_file("voice_package/heart.m4a")
        play(moving_reaction)

    elif hand_gesture == "secret":
        moving_reaction = AudioSegment.from_file("voice_package/secret.m4a")
        play(moving_reaction)

said_hi = 0
said_heart = 0
said_thumb_down = 0
said_secret = 0

while True:
    # if said_hi == 0 and hand_gesture == 'handwaving':
    #     face_interaction('handwaving')
    #     said_hi += 1
    #
    # elif said_thumb_down == 0 and hand_gesture == 'thumb_down':
    #     face_interaction('thumb_down')
    #     said_thumb_down += 1
    #
    # elif said_secret == 0 and hand_gesture == 'secret':
    #     face_interaction('secret')
    #     said_secret += 1
    #
    # elif said_heart == 0 and hand_gesture == 'heart':
    #     face_interaction('heart')
    #     said_heart += 1

    face_interaction('handwaving')
    time.sleep(2)
    face_interaction('thumb_down')
    time.sleep(2)
    face_interaction('heart')













