from gtts import gTTS
import os

# define variables
s = "I think you are wearing a t shirt. "
s += "You should wear more clothes. Do not forget your jacket. "

s += "I think you are wearing a jacket. "
s += "Outfit matches the weather. Goodbye. "

s += "I think you are wearing a coat. "
s += "You should wear less clothes. Here is a t shirt. "

# initialize tts, create mp3 and play
tts = gTTS(s, lang='en')
tts.save("audio.mp3")
os.system("mpg123 " + file)

