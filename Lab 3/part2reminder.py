import gtts
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

from deepspeech import Model
import pyaudio
import numpy as np
import wave
import speech_recognition as sr

import adafruit_mpr121
import busio
import board

# DeepSpeech Model
model = Model('deepspeech-0.9.3-models.tflite')
model.enableExternalScorer('deepspeech-0.9.3-models.scorer')

# Setup MPR121
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

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

class Reminder(object):
    tasks = []
    def __init__(self):
        self.tasks = []

    def addTask(self, task):
        self.tasks.append(task)

    def getAllTasks(self):
        return self.tasks

    def existTaskNumber(self, i):
        if i < 0 or i > len(self.tasks):
            return False
        else:
            return True

    def removeTaskNumber(self, i):
        del self.tasks[i]

    def existTask(self, task):
        return task in self.tasks

    def removeTask(self, task):
        self.tasks.remove(task)

# create a new reminder
reminder = Reminder()

def word2Number(text):
    numbers = ["zero", "one", "two", "three", "four", "five", "six",
             "seven", "eight", "nine", "ten", "eleven", "twelve",
             "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
             "eighteen", "nineteen"]
    tokens = text.split(" ")
    results = []
    for word in tokens:
        if word in numbers:
            i = numbers.index(word)
            results.append(i)
    return results

# add task
def add_task(input):
    # input = input.replace('add task','')
    reminder.addTask(input)

    # for test:
    playAudio('Okay! %s is added' % input)

# read tasks
def read_tasks():
    read_all_task = ""
    num = 0
    task = reminder.getAllTasks()
    for i in task:
        num = num + 1
        read_all_task = read_all_task + str(num) + " " + i + ". "
    playAudio(read_all_task)

# remove task by number
def remove_task_number(input):
    numbers = word2Number(input)
    for i in numbers:
        if reminder.existTaskNumber(i-1):
            reminder.removeTaskNumber(i-1)

    playAudio('Okay! %s is removed' % input)

# remove task xx
def remove_task(input):
    if reminder.existTask(input):
        reminder.removeTask(input)

    playAudio('Got it! %s removed' % (input))


def getInstruction():
    try:
        recordAudio()
        input = audio2text()
    except:
        input = "No response"

    if "task" in input:
        if "add" in input:
            playAudio("What task do you want to add?")
            recordAudio()
            task = audio2text()
            add_task(task)
        elif "read" in input:
            read_tasks()
        elif "remove" in input:
            playAudio("Which task do you want to remove? You have")
            read_tasks()
            recordAudio()
            task = audio2text()
            if "number" in task:
                remove_task_number(task)
            else:
                remove_task(task)
    elif "bye" in input:
        return False
    else:
        if not input:
            playAudio("I didn't hear anything. Please repeat.")
        else:
            playAudio("You said")
            playAudio(input)
            playAudio("But I have no idea")
    return True

def home_condition():
    # home condition: for demo
    oven = 1
    light = 1
    air_conditioner = 0
    device_on = 0

    playAudio('Before you head out, I can help you manage your home devices')
    if oven == 1:
        playAudio('Your oven is on')
        device_on += 1

    if light == 1:
        playAudio('Your light is on')
        device_on += 1

    if device_on > 0:
        playAudio('Do you need help to turn them off?')

    recordAudio()
    command = audio2text()

    if command == "yes":
        playAudio('Okay, they are all off now.')
    else:
        playAudio('Okay, no problem.')


if __name__ == "__main__":
    reminder = Reminder()
    playAudio('Hello! I am your amazing assistant')

    # default tasks for test purposes
    reminder.tasks = ['bring birthday present with you','take trash out']

    while True:
        playAudio('How can I help you?')
        res = getInstruction()
        if not res:
            playAudio('Bye')
            break

    touched = mpr121.touched_pins
    # wait until any is touched
    while True not in touched:
        touched = mpr121.touched_pins

    home_condition()
    playAudio("Also, do not forget the following tasks before you leave.")
    read_tasks()
    playAudio("Wear a mask and stay safe.Have a nice day. See you later.")
    mpr121.reset()


