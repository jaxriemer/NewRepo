import gtts
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

from deepspeech import Model
import pyaudio
import numpy as np
import time
import wave
from playsound import playsound
import speech_recognition as sr
import qwiic_button

# Setup button
button = qwiic_button.QwiicButton()
button.begin()

# DeepSpeech Model
model = Model('deepspeech-0.9.3-models.tflite')
model.enableExternalScorer('deepspeech-0.9.3-models.scorer')

def playAudio(text):
    print('Play Audio')
    print(text)
    tts = gtts.gTTS(text, lang='en')
    mp3 = BytesIO()
    tts.write_to_fp(mp3)
    mp3.seek(0)
    audio = AudioSegment.from_file(mp3, format='mp3')
    play(audio)

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "output.wav"

def recordAudio():
    port = pyaudio.PyAudio()
    print('Recording Audio')
    stream = port.open(format=sample_format,
                       channels=channels,
                       rate=fs,
                       frames_per_buffer=chunk,
                       input=True)
    frames=[]

    for i in range(0, int(fs/chunk*seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    port.terminate()
    print('Finished Recording Audio')
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(port.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def audio2Text():
    print("Audio to Text")
    #playsound(filename)
    fin = wave.open(filename, 'rb')
    frames = fin.readframes(fin.getnframes())
    audio = np.frombuffer(frames, np.int16)
    fin.close()
    text = model.stt(audio)
    print(text)
    return text

r = sr.Recognizer()
def audio2text():
    print("Audio to Text")
    sound = sr.AudioFile(filename)
    #playsound(filename)
    with sound as source:
        audio = r.record(source)
    text = ''
    try:
        s = r.recognize_google(audio)
        print("Text: " + s)
        text = s
    except Exception as e:
        print("Exception: " + str(e))

    return text

class reminder:
    tasks = []
    def __init__(self):
        self.tasks = []

    def addTask(self, task):
        self.tasks.append(task)

    def getAllTasks(self):
        return self.tasks

    def removeTask(self, i):
        del self.tasks[i]


reminder = reminder()
# push button
# add task

def add_task(input):
    input = input.strip('add')
    input = input.strip('task')
    input = input.strip()
    reminder.addTask(input)

# read tasks
def read_tasks():
    read_all_task = ""
    num = 1
    task = reminder.getAllTasks()
    for i in task:
        num = num + 1
        read_all_task = read_all_task + num + " " + i + ". "
    playAudio(read_all_task)

# remove task xx
def remove_task_number(input):
    input = input.strip('remove')
    input = input.strip('task')
    input = input.strip('number')

def getInstruction():
    recordAudio()
    input = audio2text()
    if "task" in input:
        if "add" in input:
            # add task
        elif "read" in input:
            # read tasks
        elif "remove" in input:
            if "number" in input:
                # remove task number
            else:
                # remove task

while True:
    if button.is_button_pressed():
        getInstruction()

playAudio('Hello!')
recordAudio()
#time.sleep(5)
#text = audio2Text()
#playAudio("your audio 1")
#playAudio(text)

text2 = audio2text()
playAudio("your recording")
playAudio(text2)