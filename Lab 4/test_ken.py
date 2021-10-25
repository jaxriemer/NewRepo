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
    check_movement(50)

    print("test end")
