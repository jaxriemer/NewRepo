
#This example is directly copied from the Tensorflow examples provided from the Teachable Machine.

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import sys

# weather API: https://pypi.org/project/python-weather/
import python_weather
import asyncio

# play audio
import gtts
from gtts import gTTS
from io import BytesIO
from pydub.playback import play
from pydub import AudioSegment
import os

# control servo to complete the cloth deliver function
import time
from adafruit_servokit import ServoKit


# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo_slide_forward = kit.servo[0]
servo_slide_backward = kit.servo[0]
servo_grab = kit.servo[2]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo_slide_forward.set_pulse_width_range(500, 2500)
servo_slide_backward.set_pulse_width_range(500, 2500)
servo_grab.set_pulse_width_range(500, 2500)


def move_servo_slide(closet_distance):
    if closet_distance > 0:
        servo_slide = servo_slide_forward
        print('move forward')
    else:
        servo_slide = servo_slide_backward
        print('move backward')

    print('move %d position'%closet_distance)

    turn = abs(closet_distance * 34)
    print('move %d turns'%turn)

    # for i in range(turn):
    while True:
        try:
            # Set the servo to 180 degree position
            servo_slide.angle = 180
            time.sleep(0.27) # the best sleep time
            # Set the servo to 0 degree position
            servo_slide.angle = 0
            time.sleep(0.27)

        except KeyboardInterrupt:
            # Once interrupted, set the servo back to 0 degree position
            servo_slide.angle = 0
            time.sleep(0.5)

def grab_cloth():
    deg = 0
    print('Grabing cloth')
    while deg < 110:
        deg += 1
        try:
            # Set the servo to degree position
            servo_grab.angle = deg
            time.sleep(0.03)

        except KeyboardInterrupt:
            # Once interrupted, set the servo back to 0 degree position
            servo_grab.angle = 0
            time.sleep(0.5)
            break

def release_cloth():
    deg = 110
    print('Releasing cloth')

    while deg > 0:
        deg -= 1
        try:
            # Set the servo to degree position
            servo_grab.angle = deg
            time.sleep(0.03)

        except KeyboardInterrupt:
            # Once interrupted, set the servo back to 0 degree position
            servo_grab.angle = 0
            time.sleep(0.5)
            break

def retrieve_cloth(curr_pos,target_cloth):

    if target_cloth =='no need':
        return curr_pos

    closet_cloth = {'coat':0,'tshirt':1,'jacket':2}

    target_pos = closet_cloth[target_cloth]
    print('current position is %d, moving to position %d.'%(curr_pos,target_pos))

    move_distance = target_pos - curr_pos
    move_servo_slide(move_distance)

    grab_cloth()
    release_cloth()
    curr_pos = target_pos

    return curr_pos

# initialize the position of servo_slide
curr_pos = 0

move_servo_slide(2)

