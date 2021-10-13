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

# # Setup button
# button = qwiic_button.QwiicButton()
# button.begin()

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
    input = input.replace('add task','')
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

# remove task number xx
def remove_task_number(input):
    input = input.replace('remove task number','')
    input = input.strip()
    numbers = word2Number(input)
    for i in numbers:
        if reminder.existTaskNumber(i-1):
            reminder.removeTaskNumber(i-1)
        print(i)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    playAudio('Okay! %s is removed' % input)

# remove task xx
def remove_task(input):
    input = input.replace('remove task','')
    input = input.strip()
    if reminder.existTask(input):
        reminder.removeTask(input)

    playAudio('Got it! %s removed' % (input))
    print(input)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

def getInstruction(commands):
    # for test
    # recordAudio()
    # input = audio2text()

    input = commands

    #for test
    playAudio('You said')
    # playAudio(input)
    playAudio(input)

    if "task" in input:
        if "add" in input:
            add_task(input)
        elif "read" in input:
            read_tasks()
        elif "remove" in input:
            if "number" in input:
                remove_task_number(input)
            else:
                remove_task(input)

# while True:
#     if button.is_button_pressed():
#         getInstruction()

# playAudio('Hello! I am your amazing assistant.')
# recordAudio()
# text2 = audio2text()
# playAudio("your recording")
# playAudio(text2)

if __name__ == "__main__":
    reminder = Reminder()
    playAudio('Hello!')

    #for test
    reminder.tasks = ['wash dishes','take trash out']
    commands = ["remove task take trash out" ,'read tasks']
    index = 0
    while True:
        playAudio('How can I help you?')
        getInstruction(commands[index])
        index += 1


