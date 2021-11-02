from gtts import gTTS
import os

mytext = 'Test'
language = 'en'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("test.mp3")
