from pydub import AudioSegment
from pydub.playback import play


# def playAudio(text):
#     print('Play Audio')
#     print(text)
#     tts = gtts.gTTS(text, lang='en')
#     mp3 = BytesIO()
#     tts.write_to_fp(mp3)
#     mp3.seek(0)
#     audio = AudioSegment.from_file(mp3, format='mp3')
#     play(audio)


if __name__ == "__main__":

    for i in range(10):

        simida_sound = AudioSegment.from_wav("Simida.wav")
        theme_song = AudioSegment.from_wav("ThemeSong.wav")
        gun_sound = AudioSegment.from_wav("gun_sound.wav")
        play(simida_sound)
        play(theme_song)
        play(gun_sound)






