# Chatterboxes

This lab is done collaboratively with Liqin He (lh553) and Xinning Fang (xf49)

[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Additional Parts

As mentioned during the class, we ordered additional mini microphone for Lab 3. Also, a new part that has finally arrived is encoder! Please remember to pick them up from the TA.

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. As we discussed in the class, there are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2021
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.
### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using a USB microphone, and the speaker on your webcamera. (Originally we intended to use the microphone on the web camera, but it does not seem to work on Linux.) In the home directory of your Pi, there is a folder called `text2speech` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)

[![Text2SpeechVideo](https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%203/Lab3_Text2Speech_cover.jpg)](https://drive.google.com/file/d/16iMoJOi39CqeSEUKsWBcNcEgNHM3XvWg/view?usp=sharing)

Our text to speech shell file is [text2speech_test.sh](text2speech_test.sh). When runing from the folder of this repository, we call:

      sh text2speech_test.sh

Bonus: If this topic is very exciting to you, you can try out this new TTS system we recently learned about: https://github.com/rhasspy/larynx

### Speech to Text

Now examine the `speech2text` folder. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 

In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

One thing you might need to pay attention to is the audio input setting of Pi. Since you are plugging the USB cable of your webcam to your Pi at the same time to act as speaker, the default input might be set to the webcam microphone, which will not be working for recording.

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

[![Speech2TextVideo](https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%203/Lab3_Speech2Text_cover.jpg)](https://drive.google.com/file/d/1Sb6804PlM5Navicr85CAQDMEblU0BYmO/view?usp=sharing)


Our speech to text shell file is [speech2text_test.sh](speech2text_test.sh). We also pushed the corresponding python code [test_words.py](test_words.py). When runing from the folder of this repository, we call:

      sh speech2text_test.sh

Bonus Activity:

If you are really excited about Speech to Text, you can try out [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) and [voice2json](http://voice2json.org/install.html)
There is an included [dspeech](./dspeech) demo  on the Pi. If you're interested in trying it out, we suggest you create a seperarate virutal environment for it . Create a new Python virtual environment by typing the following commands.

```
pi@ixe00:~ $ virtualenv dspeechexercise
pi@ixe00:~ $ source dspeechexercise/bin/activate
(dspeechexercise) pi@ixe00:~ $ 
```

### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

\*\***Post your storyboard and diagram here.**\*\*

![plot](https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%203/Lab3_Story1.jpg)

![plot](https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%203/Lab3_Story2.jpg)

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

\*\***Please describe and document your process.**\*\*

Our device is an assistant that gives users reminders at their door when users are about to leave their home. It gives two main categories of reminders.

The first category is a home-device reminder. The assistant is connected to all the other smart home devices and automatically detects the conditions of those devices when users are about to leave their home. The assistant can remind users to turn off the light, shut off the stove, lock the garden’s door, etc. 

- One sample interaction of home devices reminder: 

Assistant: “Your air purifier and your stove are still on. Should I turn them off?”
User: “Turn off the stove, but leave the air purifier on. ”
Assistant: “No problem, the stove is off.”


The second category is a personal reminder. The user can tell the assistant what they want to be reminded when they are about to leave home. 

- One sample interaction of personal reminder:

User: “Remind me to take the trash out next time I leave home”
Assistant: “Okay. I will remind to take the trash out”

When users are about to leave,
Assistant: “Don’t forget to take the trash out”
User: “Cool. Thanks ”

There are two ways to activate the reminder. 1) A button can be placed near the door. When users are about to leave, they press the button, and the assistant starts the reminder. 2) Install proximity sensor at the door to detect the approaching users. The reminder can be automatically activated while users change their shoes.


### Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

[![Acting Out Video](https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%203/Lab3_ActOutInteraction_cover.jpg)](https://drive.google.com/file/d/1b0r1y6c9nH7dRVJZ6TsWFIV_4rgvH9ON/view?usp=sharing)

### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...

- During the act out in the previous section, we found that we are used to speak in a more natural way which can be relatively harder for the device to parse and receive accurate information. Therefore we decided to improve the wording of the prompts users give to avoid confusion
- We also got feedback mentioning that the content of what we planned in the previous part is too much and a bit messy, as we also thought about the device turning gas and light off when a user is leaving the house while having the reminder functionality. So we chose to keep only the reminder feature but adding the ability for users to remove and read the tasks in the list.  

2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?

- We added a touch sensor that simulates the action of opening a door. The sensor is supposed to be installed on the door handle that will be triggered once touched. When the sensor is triggered, the device will then remind the user the tasks to do before the user leaves the house.

3. Make a new storyboard, diagram and/or script based on these reflections.

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

**
![plot](https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%203/Lab3_Part2Diagram2.png)
![plot](https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%203/Lab3_Part2Diagram.jpg)
The system consists of two parts: When the user is inside the house and when the user is about to leave:
1. Inside the house: Prompts users can trigger the device are: "Add task", "Remove task", "Read Task" and "Bye". When "Add task" is said, the device will record the task that the user chooses to add and append to the list of tasks. When "Remove task" is triggered, the device will first read the list of the tasks, and each task will come with a number at the beginning. Users can delete a task by either indicating the number of the task or directly telling the device the name of the task. "Read task" command will have the device read out all the tasks in the list, and "Bye" is used to terminate the reminder functionality.

2. When the user is about to leave the house and puts his hand on the door handle (here we choose to use the touch sensor in the interaction), the device will be triggered to remind the user of the tasks in the list that he needs to do. 
    
 
**

*Include videos or screencaptures of both the system and the controller.*

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?
\*\*

- First, we need to look at what is printed on the terminal to figure out when is the best time for us to say the prompt. It happened several times when we start speaking before the device actually started to record and only part of the prompt was received by the device. After adding prompts to indicate whether the device gets what users say, it is easier to figure the failure out, but this is not the ultimate solution.
- The device sometimes hears totally different prompts from the ones we actually say. So we tried to speak slowly and to speak word by word. But this is not the natural way a user should talk.
- If the above problems can be solved, the functions we wrote to add/remove/read tasks work well and the whole process has a nice flow.

\*\*

### What worked well about the controller and what didn't?

\*\**your answer here*\*\*

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

\*\**your answer here*\*\*


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

\*\*

We can also make use of the screen and the joycon when it comes to the removal of tasks. Currently what when the prompt of removing a task is triggered, the device will read the tasks in the list out with a number for each task. Then the user needs to either tell the device the name of the task or the number of the task. 

If all the tasks are printed on the screen with an option to choose, users can also choose the task they want to delete with the joycon, and confirm the deletion by pressing on the joycon.

\*\*

