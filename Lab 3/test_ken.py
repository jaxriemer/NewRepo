# import deepspeech
import numpy as np
import queue, os, os.path
import pyaudio
import board
import adafruit_apds9960.apds9960
import adafruit_mpr121
import busio
import random

from sys import byteorder
from array import array
import time
import gtts
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
from pydub.utils import which, mediainfo


# Make DeepSpeech Model
model = deepspeech.Model('deepspeech-0.9.3-models.tflite')
model.enableExternalScorer('deepspeech-0.9.3-models.scorer')

# i2c = busio.I2C(board.SCL, board.SDA)
# mpr121 = adafruit_mpr121.MPR121(i2c)
#
# sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
# sensor.enable_gesture = True
# sensor.enable_proximity = True
# # sensor.rotation = 270 # 270 for CLUE

THRESHOLD = 850

def playAudio(text):
    tts = gtts.gTTS(text, lang='en')
    mp3 = BytesIO()
    tts.write_to_fp(mp3)
    mp3.seek(0)
    audio = AudioSegment.from_file(mp3, format='mp3')
    play(audio)

if __name__ == "__main__":
    playAudio("Hello, finally working now.")

