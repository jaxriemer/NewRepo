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

if __name__ == "__main__":


    simida_sound = AudioSegment.from_wav("Simida.wav")
    theme_song = AudioSegment.from_wav("ThemeSong.wav")
    gun_sound = AudioSegment.from_wav("gun_sound.wav")

    combined = gun_sound*10 + theme_song

    play(combined)
    # play(simida_sound)
    # play(theme_song)
    # play(gun_sound)

    # eliminate_player()








