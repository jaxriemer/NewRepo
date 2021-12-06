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

topic_face = 'IDD/face_motion'
topic_body = 'IDD/body_position'

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
    client.subscribe(topic_face)
    client.subscribe(topic_body)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recieved
def on_message(cleint, userdata, msg):
	# you can filter by topics
    if msg.topic == topic_face:
        global eye_status
        eye_status = msg.payload.decode('UTF-8')

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

def eyelid_movement(status):
    print("eye open")
    eyelid_upper_servo.angle =30
    eyelid_lower_servo.angle = 3

    time.sleep(2)

    print("eye close")
    eyelid_upper_servo.angle = 3
    eyelid_lower_servo.angle = 90
    time.sleep(2)

def eyeball_movement(body_pos):
    #TODO: determine the correct angle
    if body_pos == 'left':
        eye_horizontal_servo.angle= 85

    elif body_pos == 'middle':
        eye_horizontal_servo.angle = 45

    elif body_pos == 'right':
        eye_horizontal_servo.angle = 0

    else:
        eye_horizontal_servo.angle = 90
#
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
eye_horizontal_degree = 0
eye_vertical_degree = 0

eye_horizontal_servo.angle = 90
eye_vertical_servo.angle = 90

greeted = False
commented_walking = False

while True:
    # if body_pos != 'background' and greeted == False:
    #     face_talking('greet')
    #     greeted = True

    # eyelid_movement(eye_status)
    eyeball_movement("left")
    time.sleep(2)
    eyeball_movement("right")
    time.sleep(2)
    eyeball_movement("middle")
    time.sleep(2)
    eyeball_movement("background")
    time.sleep(2)

    # if time_counter%50 == 0 and commented_walking == False:
    #     face_talking('moved')
    #     commented_walking = True
    # eye horizontal movement
    #
    # if (eye_movement_lag % 200) == 0:
    #     if eye_horizontal_degree == 0:
    #
    #         servo_eye_horizontal.angle = 180
    #         eye_horizontal_degree = 180
    #         time.sleep(0.03)
    #
    #     else:
    #         servo_eye_horizontal.angle = 0
    #         eye_horizontal_degree = 0
    #         time.sleep(0.03)
    #
    # # eye vertical movement
    # if (eye_movement_lag % 300) == 0:
    #     if eye_vertical_degree == 0:
    #         servo_eye_vertical.angle = 180
    #         eye_vertical_degree = 180
    #         time.sleep(0.03)
    #
    #     else:
    #         servo_eye_vertical.angle = 0
    #         eye_vertical_degree = 0
    #         time.sleep(0.03)

    time.sleep(0.03)

    time_counter += 1








