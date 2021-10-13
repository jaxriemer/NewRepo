import deepspeech
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
AudioSegment.converter = which("ffmpeg")

def add_task(user: UserInstance):
    playsound("Adding a new task! What do you want to add?")
    task = get_audio_from_client()
    playsound("Adding {}".format(task))
    user.add_task(task)