import qwiic
import time
from pydub import AudioSegment
from pydub.playback import play
import gtts
from io import BytesIO
from adafruit_servokit import ServoKit

def eliminate_player():
    text = "Bye"
    tts = gtts.gTTS(text, lang='en')
    mp3 = BytesIO()
    tts.write_to_fp(mp3)
    mp3.seek(0)
    audio = AudioSegment.from_file(mp3, format='mp3')
    play(audio)
    gun_sound = AudioSegment.from_wav("gun_sound.wav")
    play(gun_sound)

# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)
# Name and set up the servo according to the channel you are using.
servo = kit.servo[0]
# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo.set_pulse_width_range(500, 2500)

def rotate_head(degree):
    try:
        # Set the servo to 180 degree position
        servo.angle = degree

    except KeyboardInterrupt:
        # Once interrupted, set the servo back to 0 degree position
        servo.angle = 0
        time.sleep(0.5)

def check_movement(sensitivity = 2):

    ToF = qwiic.QwiicVL53L1X()

    #try:
        # check initial distance
        #ToF.start_ranging()						 # Write configuration bytes to initiate measurement
       # time.sleep(.005)
        #init_distance = ToF.get_distance()	 # Get the result of the measurement from the sensor
       # print("Initial Distance 1 (mm): %d" % (init_distance))
      #  time.sleep(.005)
      #  ToF.stop_ranging()

    #except Exception as e:
     #   print(e)

    count = 0
    while True:

        try:
            # check distance
            ToF.start_ranging()						 # Write configuration bytes to initiate measurement
            time.sleep(.05)
            current_distance= ToF.get_distance()	 # Get the result of the measurement from the sensor
            time.sleep(.05)
            ToF.stop_ranging()

            print("Distance(mm): %d" % (current_distance))


            if (count > 5) and (abs(current_distance - prev_distance) > sensitivity):
                   # eliminate_player()
                    print("Movement Distance(mm): %d"%(abs(current_distance - prev_distance)))
                    break

            prev_distance = current_distance
            count += 1

        except Exception as e:
            print(e)

if __name__ == "__main__":
    #check_movement(50)

    rotate_head(180)
    time.sleep(2)
    rotate_head(0)
    time.sleep(2)

    print("test end")
