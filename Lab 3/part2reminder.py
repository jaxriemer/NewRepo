import gtts
import sys
import os
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

import deepspeech
import pyaudio
from sys import byteorder
import array
import numpy as np
import time

# DeepSpeech Model
model = deepspeech.Model('deepspeech-0.9.3-models.tflite')
model.enableExternalScorer('deepspeech-0.9.3-models.scorer')

def is_silent(data_chunk):
    """Returns 'True' if below the 'silent' threshold"""
    snd_data = array('h', data_chunk)
    if byteorder == 'big':
        snd_data.byteswap()
    return max(snd_data) <850

class AudioListener(object):

    def __init__(self):
        self.num_silent = 0
        self.snd_started = False
        self.end_recording = False
        self.buffer_queue = []

    def set_end_record(self, silent):
        if silent and self.snd_started:
            self.num_silent += 1
        elif silent and not self.snd_started:
            self.snd_started = True
        elif not silent and self.snd_started:
            self.snd_started = False
            self.num_silent = 0

        if self.snd_started and self.num_silent > 40:
            self.end_recording = True

    def get_frames(self):
        return self.buffer_queue

    def add_recording(self, data):
        self.buffer_queue.append(data)

    def get_end_record(self):
        return self.end_recording

def playAudio(text):
    tts = gtts.gTTS(text, lang='en')
    mp3 = BytesIO()
    tts.write_to_fp(mp3)
    mp3.seek(0)
    audio = AudioSegment.from_file(mp3, format='mp3')
    play(audio)

def getAudio():
    # Create a Streaming session
    context = model.createStream()
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK_SIZE = 320
    capture = AudioListener()
    # Encapsulate DeepSpeech audio feeding into a callback for PyAudio
    def process_audio(in_data, frame_count, time_info, status):
        data16 = np.frombuffer(in_data, dtype=np.int16)
        capture.add_recording(data16)
        silent = is_silent(data16)
        capture.set_end_record(silent)
        return (in_data, pyaudio.paContinue)

    # PyAudio parameters
    # Feed audio to deepspeech in a callback to PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
        stream_callback=process_audio
    )

    stream.start_stream()
    while stream.is_active() and not capture.get_end_record():
        time.sleep(0.1)

    for frame in capture.get_frames():
        context.feedAudioContent(frame)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    text = context.finishStream()
    return text


playAudio('Hello! @@@@@@@@@@@')
text = getAudio()
playAudio("your audio")
playAudio(text)