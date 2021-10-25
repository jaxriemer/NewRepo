import qwiic
import time
from pydub import AudioSegment
from pydub.playback import play
import gtts
from io import BytesIO

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


def check_movement():

    # print("VL53L1X Qwiic Test\n")
    ToF = qwiic.QwiicVL53L1X()
    # if (ToF.sensor_init() == None):					 # Begin returns 0 on a good init
    #     print("Sensor online!\n")

    prev_distance = None
    sensivity = 2

    while True:
        try:
            ToF.start_ranging()						 # Write configuration bytes to initiate measurement
            time.sleep(.005)
            distance = ToF.get_distance()	 # Get the result of the measurement from the sensor
            time.sleep(.005)
            ToF.stop_ranging()

            # distance= distance / 25.4/2

            print("Distance(mm): %d" % (distance))

        except Exception as e:
            print(e)


if __name__ == "__main__":

    check_movement()
