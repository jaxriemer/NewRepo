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
import random

# control servo to complete the cloth deliver function
from adafruit_servokit import ServoKit

topic_body = 'IDD/oneteam/face_body_position'

eye_status = 'not receiving'
body_pos = 'not receiving'

# # Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
eye_vertical_servo= kit.servo[4]
eye_horizontal_servo = kit.servo[1]
eyelid_upper_servo = kit.servo[2]
eyelid_lower_servo = kit.servo[0]
eyebrow_servo_servo = kit.servo[3]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
# servo_eye.set_pulse_width_range(500, 2500)

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic_body)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recieved
def on_message(cleint, userdata, msg):
	# you can filter by topics

    if msg.topic == topic_body:
        global body_pos
        body_pos = msg.payload.decode('UTF-8')

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

def eyelid_movement(movement):
    # lag1 = random.randint(2, 5)
    # lag2 = random.randint(2, 5)

    if eyelid_movement == "open" or eyelid_movement == "wink":
        print("eye open")
        eyelid_upper_servo.angle =30
        eyelid_lower_servo.angle = 25
        # print("ready to sleep for " + str(lag1) + " seconds")
        time.sleep(1)

    if eyelid_movement == "closed" or eyelid_movement == "wink":
        print("eye close")
        eyelid_upper_servo.angle = 10
        eyelid_lower_servo.angle = 3
        # print("ready to sleep for " + str(lag2) + " seconds")
        time.sleep(1)

def eyeball_movement(body_pos):
    #TODO: determine the correct angle
    if body_pos == 'left':
        eye_horizontal_servo.angle= 85
        time.sleep(1)
    elif body_pos == 'right':
        eye_horizontal_servo.angle = 0
        time.sleep(1)
    else:
        eye_horizontal_servo.angle = 40
        time.sleep(1)


# def face_talking(cue):
#
#     if cue == "greet":
#         greet_sound = AudioSegment.from_file("voice_package/greet.m4a")
#         play(greet_sound)
#
#     elif cue == "moved":
#         moving_reaction = AudioSegment.from_file("voice_package/moving.m4a")
#         play(moving_reaction)

client.loop_start()

time_counter = 0
eyelid_open = False

while True:

    try:
        # Set the servo to 180 degree position
        eye_horizontal_servo.angle = 85
        time.sleep(3)
        # Set the servo to 0 degree position
        eye_horizontal_servo.angle = 0
        time.sleep(3)

    except KeyboardInterrupt:

        # Once interrupted, set the servo back to 0 degree position
        eye_vertical_servo.angle = 22
        eye_horizontal_servo.angle = 40
        eyelid_upper_servo.angle = 10
        eyelid_lower_servo.angle = 3
        eyebrow_servo_servo.angle = 0

        time.sleep(0.5)

        break












