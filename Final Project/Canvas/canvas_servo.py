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

topic = 'IDD/oneteam/canvas_body_position'
body_position = 'Not read'

# # Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo_upper_0 = kit.servo[0]
servo_bottom_0 = kit.servo[1]
servo_upper_1 = kit.servo[2]
servo_bottom_1 = kit.servo[3]
servo_upper_2 = kit.servo[12]
servo_bottom_2 = kit.servo[13]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
# servo_shadow.set_pulse_width_range(500, 2500)

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)
    # you can subsribe to as many topics as you'd like
    # client.subscribe('some/other/topic')

# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
    # you can filter by topics
    if msg.topic == topic:
        global body_position
        body_position = msg.payload.decode('UTF-8')


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

def push_shadow_tile(condition):

    show_add = -3
    no_show_add = 3
    outside = 5
    inside = 175
    sleep_time = 0.2

    if condition == 'left':

        print('pushing left')
        # push postion 0 out, pull others in.
        while servo_upper_0.angle > outside or servo_upper_1.angle < inside \
                or servo_upper_2.angle < inside:
            if servo_upper_0.angle > outside:
                servo_upper_0.angle += show_add
                servo_bottom_0.angle += show_add

            if servo_upper_1.angle < inside:
                servo_upper_1.angle += no_show_add
                servo_bottom_1.angle += no_show_add

            if servo_upper_2.angle < inside:
                servo_upper_2.angle += no_show_add
                servo_bottom_2.angle += no_show_add

            #time.sleep(sleep_time)
        time.sleep(2)

    elif condition == 'middle':

        print('pushing middle')
        while servo_upper_1.angle > outside or servo_upper_0.angle < inside \
                or servo_upper_2.angle < inside:
            if servo_upper_1.angle > outside:
                servo_upper_1.angle += show_add
                servo_bottom_1.angle += show_add

            if servo_upper_0.angle < inside:
                servo_upper_0.angle += no_show_add
                servo_bottom_0.angle += no_show_add

            if servo_upper_2.angle < inside:
                servo_upper_2.angle += no_show_add
                servo_bottom_2.angle += no_show_add
            #time.sleep(sleep_time)
        time.sleep(2)

    elif condition == 'right':

        print('pushing right')
        while servo_upper_2.angle > outside or servo_upper_1.angle < inside\
                or servo_upper_0.angle < inside:
            if servo_upper_2.angle > outside:
                servo_upper_2.angle += show_add
                servo_bottom_2.angle += show_add

            if servo_upper_1.angle < inside:
                servo_upper_1.angle += no_show_add
                servo_bottom_1.angle += no_show_add

            if servo_upper_0.angle < inside:
                servo_upper_0.angle += no_show_add
                servo_bottom_0.angle += no_show_add

            #time.sleep(sleep_time)
        time.sleep(2)

    else:

        print('all going back')
        while servo_upper_0.angle < inside or servo_upper_1.angle < inside or servo_upper_2.angle < inside:
            if servo_upper_2.angle < inside:
                servo_upper_2.angle += no_show_add
                servo_bottom_2.angle += no_show_add

            if servo_upper_1.angle < inside:
                servo_upper_1.angle += no_show_add
                servo_bottom_1.angle += no_show_add

            if servo_upper_0.angle < inside:
                servo_upper_0.angle += no_show_add
                servo_bottom_0.angle += no_show_add

            #time.sleep(sleep_time)
        time.sleep(2)

client.loop_start()

servo_upper_0.angle = 165
servo_bottom_0.angle = 165
servo_upper_1.angle = 165
servo_bottom_1.angle = 165
servo_upper_2.angle = 165
servo_bottom_2.angle = 165


while True:

    try:


        # print(body_position)
        push_shadow_tile('middle')
        time.sleep(2)
        push_shadow_tile('left')
        time.sleep(2)
        push_shadow_tile('middle')
        time.sleep(2)
        push_shadow_tile('right')



        print(servo_upper_0.angle)
        print(servo_bottom_0.angle)
        print(servo_upper_1.angle)
        print(servo_bottom_1.angle)
        print(servo_upper_2.angle)
        print(servo_bottom_2.angle)

    except KeyboardInterrupt:
        # Once interrupted, set the servo back to 0 degree position
        servo_upper_0.angle = 180
        servo_bottom_0.angle = 180
        servo_upper_1.angle = 180
        servo_bottom_1.angle = 180
        servo_upper_2.angle = 180
        servo_bottom_2.angle = 180
        break







