# servo motion

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import sys
import paho.mqtt.client as mqtt
import uuid
import time

# control servo to complete the cloth deliver function
from adafruit_servokit import ServoKit

topic = 'IDD/user_face_motion'
eye_status = 'Not read'

# # Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo_eye = kit.servo[0]
servo_eye_horizontal = kit.servo[1]
servo_eye_vertical = kit.servo[2]

servo_shadow = kit.servo[11]
servo_shadow_loc = kit.servo[5]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo_shadow.set_pulse_width_range(500, 2500)

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)
    # you can subsribe to as many topics as you'd like
    # client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
    # you can filter by topics
    if msg.topic == topic:
        global eye_status
        eye_status = msg.payload.decode('UTF-8')
        # print(eye_status)

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


def shadow_movement():
    # TODO
    open_deg = 180
    close_deg = 0

    servo_eye.angle = open_deg
    time.sleep(0.03)

    servo_eye.angle = close_deg
    time.sleep(0.03)

client.loop_start()

shadow_loc_deg = 0
servo_shadow.angle = 150

while True:
    # show shadow
    print("showing shadow")
    servo_shadow.angle = 150
    time.sleep(3)

    # hide shadow
    print("hiding shadow")
    servo_shadow.angle = 180
    time.sleep(3)

    # move shadow loc
    # print("shadow loc moving")
    # servo_shadow_loc.angle = shadow_loc_deg
    # if shadow_loc_deg <= 170:
    #     shadow_loc_deg += 10
    # elif shadow_loc_deg >= 0:
    #     shadow_loc_deg -= 10
    # time.sleep(3)







