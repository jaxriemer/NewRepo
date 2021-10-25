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

def check_movement(sensitivity = 2):

    try:
        ToF = qwiic.QwiicVL53L1X()
        # check initial distance
        ToF.start_ranging()						 # Write configuration bytes to initiate measurement
        time.sleep(.005)
        init_distance = ToF.get_distance()	 # Get the result of the measurement from the sensor
        time.sleep(.005)
        ToF.stop_ranging()
        prev_distance = init_distance
        print("Initial Distance(mm): %d" % (init_distance))

    except Exception as e:
        print(e)

    while True:

        try:
            # check distance
            ToF.start_ranging()						 # Write configuration bytes to initiate measurement
            time.sleep(.05)
            current_distance= ToF.get_distance()	 # Get the result of the measurement from the sensor
            time.sleep(.05)
            ToF.stop_ranging()
            print("current Distance(mm): %d"%(current_distance))

            if abs(current_distance - prev_distance) > sensitivity:
                # eliminate_player()
                # print("Distance(mm): %d" % (current_distance))
                # print("Movement Distance(mm): %d"%(abs(current_distance - prev_distance)))
                # break

            prev_distance = current_distance

        except Exception as e:
            print(e)

if __name__ == "__main__":
    check_movement(50)
