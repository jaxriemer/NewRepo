# servo motion

# import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import sys
import paho.mqtt.client as mqtt
import uuid
import time

from adafruit_servokit import ServoKit
#
# topic = 'IDD/body_position'
# body_position = 'Not read'

# # Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)


# # Name and set up the servo according to the channel you are using.
# servo_upper_0 = kit.servo[0]
# servo_bottom_0 = kit.servo[1]
# servo_upper_1 = kit.servo[2]
# servo_bottom_1 = kit.servo[3]
# servo_upper_2 = kit.servo[4]
# servo_bottom_2 = kit.servo[5]

servo_test = kit.servo[0]
servo_test.set_pulse_width_range(500, 2500)

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
# servo_shadow.set_pulse_width_range(500, 2500)


# this is blocking. to see other ways of dealing with the loop
#  https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#network-loop
#
# body_position = ['left','middle','right']
#
# def push_shadow_tile(condition):
#     show_add = 1
#     no_show_add = -1
#
#     outside = 180
#     inisde = 0
#
#     sleep_time = 0.02
#
#     if condition == 'left':
#         while servo_upper_0.angle < outside:
#             servo_upper_0.angle += show_add
#             servo_bottom_0.angle += show_add
#
#             if servo_upper_1.angle > inisde:
#                 servo_upper_1.angle += no_show_add
#                 servo_bottom_1.angle += no_show_add
#
#             if servo_upper_2.angle > inisde:
#                 servo_upper_2.angle += no_show_add
#                 servo_bottom_2.angle += no_show_add
#
#             time.sleep(sleep_time)
#
#     elif condition == 'middle':
#         while servo_upper_1.angle < outside:
#             servo_upper_1.angle += show_add
#             servo_bottom_1.angle += show_add
#
#             if servo_upper_0.angle >= inisde:
#                 servo_upper_0.angle += no_show_add
#                 servo_bottom_0.angle += no_show_add
#
#             if servo_upper_2.angle >= inisde:
#                 servo_upper_2.angle += no_show_add
#                 servo_bottom_2.angle += no_show_add
#             time.sleep(sleep_time)
#
#     elif condition == 'right':
#         while servo_upper_2.angle < outside:
#             servo_upper_2.angle += no_show_add
#             servo_bottom_2.angle += no_show_add
#
#             if servo_upper_1.angle > inisde:
#                 servo_upper_1.angle += no_show_add
#                 servo_bottom_1.angle += no_show_add
#
#             if servo_upper_0.angle > inisde:
#                 servo_upper_0.angle += show_add
#                 servo_bottom_0.angle += show_add
#
#             time.sleep(sleep_time)
#
#     else:
#         while servo_upper_2.angle > inside:
#             servo_upper_2.angle += no_show_add
#             servo_bottom_2.angle += no_show_add
#
#             if servo_upper_1.angle > inisde:
#                 servo_upper_1.angle += no_show_add
#                 servo_bottom_1.angle += no_show_add
#
#             if servo_upper_0.angle > inisde:
#                 servo_upper_0.angle += show_add
#                 servo_bottom_0.angle += show_add
#
#             time.sleep(sleep_time)


while True:
    # for pos in body_position:
    #     push_shadow_tile(pos)

    outside = 180
    inside = 0


        # # Set the servo to degree position
        # while servo_upper_0.angle < outside:
        #     servo_upper_0.angle += 1
        #     time.sleep(0.05)
        #
        # while servo_upper_0.angle > inside:
        #     servo_upper_0.angle += -1
        #     time.sleep(0.05)

    servo_test.angle = 180
    print('degree to 180')
    print(servo_test.angle)
    time.sleep(3)
    servo_test.angle = 0
    print(servo_test.angle)
    print('degree to 0')





