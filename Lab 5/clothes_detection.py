
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

what_to_wear = 0
rain = False
temp = -999999

async def getweather():
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client(format=python_weather.IMPERIAL)

    # fetch a weather forecast from a city
    weather = await client.find("New York City")

    # returns the current day's forecast temperature (int)
    print(weather.current.temperature)

    today = weather.forecasts[0]
    global temp
    temp = today.temperature
    if "rain" in today.sky_text:
        global rain
        rain = True

    if today.temperature > 70:
        global what_to_wear
        what_to_wear = 1
    elif 50 <= today.temperature <= 70:
        what_to_wear = 0
    elif today.temperature < 50:
        what_to_wear = 3

    # close the wrapper once done
    await client.close()

# def playAudio(text):
#     print('Play Audio')
#     print(text)
#     tts = gtts.gTTS(text, lang='en')
#     mp3 = BytesIO()
#     tts.write_to_fp(mp3)
#     mp3.seek(0)
#     audio = AudioSegment.from_file(mp3, format='mp3')
#     play(audio)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

img = None
webCam = False
if(len(sys.argv)>1 and not sys.argv[-1]== "noWindow"):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      print("Trying to open the Webcam.")
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True
   except:
      print("Unable to access webcam.")


# Load the model
model = tensorflow.keras.models.load_model('clothing_model.h5')

# Load Labels:
labels=[]
f = open("clothes_labels.txt", "r")
for line in f.readlines():
    if(len(line)<1):
        continue
    labels.append(line.split(' ')[1].strip())

# run the weather api
loop = asyncio.get_event_loop()
loop.run_until_complete(getweather())
loop.close()

# playAudio("Today's temperature is " + str(temp) + " degrees")

def detect_and_recommend_clothes(prediction):

    cloth_recommendation = "no need"

    # determine if umbrella is needed
    if rain:
        print("It is going to rain today. Do not forget your umbrella.")
        # playAudio("It is going to rain today. Do not forget your umbrella.")

    if np.argmax(prediction) == 2:
        print("Background detected")
        # playAudio("Background detected")
        return cloth_recommendation
    else:
        print("I think you are wearing a " + labels[np.argmax(prediction)])
        # playAudio("I think you are wearing " + labels[np.argmax(prediction)])
        print('It is currently %d degree in NYC.'%temp)

        if np.argmax(prediction) == what_to_wear:
            print("Outfit matches")
            return cloth_recommendation
            # playAudio("You are good to go. Goodbye.")

        # wearing jacket
        elif np.argmax(prediction) == 0:
            if what_to_wear == 1:
                print("You should wear less clothes. Here is a t-shirt.")
                # playAudio("You should wear more clothes. Do not forget your coat.")
                cloth_recommendation = "tshirt"
                return cloth_recommendation

            elif what_to_wear == 3:
                print("You should wear more clothes. Do not forget your jacket.")
                # playAudio("You should wear less clothes. Here is a t shirt.")
                cloth_recommendation = "jacket"
                return cloth_recommendation

        # wearing t-shirt
        elif np.argmax(prediction) == 1:
            if what_to_wear == 0:
                print("You should wear more clothes. Do not forget your jacket.")
                # playAudio("You should wear less clothes. Here is your jacket.")
                cloth_recommendation = "jacket"
                return cloth_recommendation

            elif what_to_wear == 3:
                print("You should wear more clothes. Do not forget your coat.")
                # playAudio("You should wear less clothes. Here is a t shirt.")
                cloth_recommendation = "coat"
                return cloth_recommendation

        # wearing coat
        elif np.argmax(prediction) == 3:
            if what_to_wear == 0:
                print("You should wear less clothes. Here is your jacket.")
                # playAudio("You should wear more clothes. Do not forget your jacket.")
                cloth_recommendation = "jacket"
                return cloth_recommendation

            elif what_to_wear == 1:
                print("You should wear less clothes. Here is your t shirt.")
                # playAudio("You should wear more clothes. Do not forget your coat.")
                cloth_recommendation = "tshirt"
                return cloth_recommendation


def move_servo_slide(closet_distance):
    if closet_distance > 0:
        servo_slide = servo_slide_forward
        # print('move forward')
    else:
        servo_slide = servo_slide_backward
        # print('move backward')

    # print('move %d position'%closet_distance)

    turn = abs(closet_distance * 34)
    # print('move %d turns'%turn)

    for i in range(turn):
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
    # print('Grabing cloth')
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
    # print('Releasing cloth')

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
    # print('current position is %d, moving to position %d.'%(curr_pos,target_pos))
    print('Please wait, I am moving to grab the %s for you'%target_cloth)

    move_distance = target_pos - curr_pos
    move_servo_slide(move_distance)

    print('Here is your %s. Have a great day!'%target_cloth)
    grab_cloth()
    release_cloth()
    curr_pos = target_pos

    return curr_pos

# initialize the position of servo_slide
curr_pos = 0

while(True):

    # read camera image
    if webCam:
        ret, img = cap.read()

    rows, cols, channels = img.shape
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    size = (224, 224)
    img =  cv2.resize(img, size, interpolation = cv2.INTER_AREA)
    #turn the image into a numpy array
    image_array = np.asarray(img)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    prediction = model.predict(data)

    if webCam:
        if sys.argv[-1] == "noWindow":
           cv2.imwrite('detected_out.jpg',img)
           continue
        cv2.imshow('detected (press q to quit)',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
    else:
        break

    target_cloth = detect_and_recommend_clothes(prediction)
    curr_pos = retrieve_cloth(curr_pos,target_cloth)

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()
