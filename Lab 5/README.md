This lab is done collaboratively with Liqin He (lh553) and Xinning Fang (xf49)

# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms needs to be aware of.

## Prep

1.  Pull the new Github Repo.
2.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2021/Lab%202/prep.md), we offered the instruction at the bottom.
3.  Read about [OpenCV](https://opencv.org/about/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:

1. Raspberry Pi
1. Webcam 
1. Microphone (if you want to have speech or sound input for your design)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### OpenCV
A more traditional method to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python. We included 4 standard OpenCV examples: contour(blob) detection, face detection with the ``Haarcascade``, flow detection (a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (e.g. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example. 

Following is a nicer way you can run and see the flow of the `openCV-examples` we have included in your Pi. Instead of `ls`, the command we will be using here is `tree`. [Tree](http://mama.indstate.edu/users/ice/tree/) is a recursive directory colored listing command that produces a depth indented listing of files. Install `tree` first and `cd` to the `openCV-examples` folder and run the command:

```shell
pi@ixe00:~ $ sudo apt install tree
...
pi@ixe00:~ $ cd openCV-examples
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```

The flow detection might seem random, but consider [this recent research](https://cseweb.ucsd.edu/~lriek/papers/taylor-icra-2021.pdf) that uses optical flow to determine busy-ness in hospital settings to facilitate robot navigation. Note the velocity parameter on page 3 and the mentions of optical flow.

Now, connect your webcam to your Pi and use **VNC to access to your Pi** and open the terminal. Use the following command lines to try each of the examples we provided:
(***it will not work if you use ssh from your laptop***)

```
pi@ixe00:~$ cd ~/openCV-examples/contours-detection
pi@ixe00:~/openCV-examples/contours-detection $ python contours.py
...
pi@ixe00:~$ cd ~/openCV-examples/face-detection
pi@ixe00:~/openCV-examples/face-detection $ python face-detection.py
...
pi@ixe00:~$ cd ~/openCV-examples/flow-detection
pi@ixe00:~/openCV-examples/flow-detection $ python optical_flow.py 0 window
...
pi@ixe00:~$ cd ~/openCV-examples/object-detection
pi@ixe00:~/openCV-examples/object-detection $ python detect.py
```

**\*\*\*Try each of the following four examples in the `openCV-examples`, include screenshots of your use and write about one design for each example that might work based on the individual benefits to each algorithm.\*\*\***

**Contours detection**

  Contour detections can be used for photo filters. For example, sparkling stars or other special effects can be placed on all the detected edges. It could also turn the image into a stylish painting by distinguishing the edges between dark and light and painting areas with different shades of color. 
  
<img width="400" alt="contour_detection" src="https://user-images.githubusercontent.com/39501842/140844184-5b2f188c-56d0-4ac7-a81f-3e7a9621cfb5.png">

**Face detection**

  Face detection can be used on security cameras by alerting the owner or taking photos when suspicious faces are detected. It does not work well when faces are partially covered, and could be used for detecting whether subjects are wearing masks properly.
  
<img width="400" alt="face_detection" src="https://user-images.githubusercontent.com/39501842/140844478-79ba2ed3-b4a0-44ce-a576-ae39c1eaf85f.png">


**Flow detection**

  The flow detection could be used to detect the movements of feature points on people, and can be used as an extension of our red light green light game in Lab 4, where player movements could be detected by this flow detection algorithm and the win/lose state could be determined based on that.
  
<img width="400" alt="flow_detection" src="https://user-images.githubusercontent.com/39501842/140844198-717d0500-e41b-43ca-a4d7-8cf332a5878b.png">

**Object detection**

  Object detection can be used to alert the messiness of one place. For example, in an emergency exit hallway, when the number of objects exceeds a certain threshold, staff should be alerted to be aware and take action.

<img src="https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%205/imgs/object-detection.png"  width="400"/>


#### MediaPipe

A more recent open source and efficient method of extracting information from video streams comes out of Google's [MediaPipe](https://mediapipe.dev/), which offers state of the art face, face mesh, hand pose, and body pose detection.

![Alt Text](mp.gif)

To get started, create a new virtual environment with special indication this time:

```
pi@ixe00:~ $ virtualenv mpipe --system-site-packages
pi@ixe00:~ $ source mpipe/bin/activate
(mpipe) pi@ixe00:~ $ 
```

and install the following.

```
...
(mpipe) pi@ixe00:~ $ sudo apt install ffmpeg python3-opencv
(mpipe) pi@ixe00:~ $ sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23
(mpipe) pi@ixe00:~ $ pip3 install mediapipe-rpi4 pyalsaaudio
```

Each of the installs will take a while, please be patient. After successfully installing mediapipe, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the hand pose detection script we provide:
(***it will not work if you use ssh from your laptop***)


```
(mpipe) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(mpipe) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control, and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting. Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py` lines 48-53. 

**\*\*\*Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.\*\*\***

(You might also consider how this notion of percentage control with hand tracking might be used in some of the physical UI you may have experimented with in the last lab, for instance in controlling a servo or rotary encoder.)


<img src="https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%205/imgs/hand-pose1.png"  width="400"/>

<img src="https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%205/imgs/hand-pose2.png"  width="400"/>

  The hand pose detection could be used as an input system for the Raspberry Pi. The pinch gesture could be detected and used for selecting a virtual menu, pressing a virtual button, or pushing a virtual joystick. This works best when the user is standing away from the Pi and cannot reach the physical buttons, for instance: the user tells the device that is on a tripod far away from him/her to take a photo. The gesture is also suitable when the user’s hands are covered by mud when sculpturing, covered by sauces when cooking, or just sanitized when doing medical operations. In the above scenarios, a physical button would not work and hand pose could replace it. 

#### Teachable Machines
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple. However, its simplicity is very useful for experimenting with the capabilities of this technology.

![Alt Text](tm.gif)

To get started, create and activate a new virtual environment for this exercise with special indication:

```
pi@ixe00:~ $ virtualenv tmachine --system-site-packages
pi@ixe00:~ $ source tmachine/bin/activate
(tmachine) pi@ixe00:~ $ 
```

After activating the virtual environment, install the requisite TensorFlow libraries by running the following lines:
```
(tmachine) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ sudo chmod +x ./teachable_machines.sh
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ ./teachable_machines.sh
``` 

This might take a while to get fully installed. After installation, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the example script:
(***it will not work if you use ssh from your laptop***)

```
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python tm_ppe_detection.py
```


(**Optionally**: You can train your own model, too. First, visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. Second, use the webcam on your computer to train a model. For each class try to have over 50 samples, and consider adding a background class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate, or export your model as a 'Tensorflow' model, and select 'Keras'. You will find an '.h5' file and a 'labels.txt' file. These are included in this labs 'teachable_machines' folder, to make the PPE model you used earlier. You can make your own folder or replace these to make your own classifier.)

**\*\*\*Whether you make your own model or not, include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.\*\*\***
<img width="812" alt="Screen Shot 2021-11-08 at 8 22 17 PM" src="https://user-images.githubusercontent.com/39501842/140844395-271916fa-eae7-4404-869c-776234d31d27.png">
<img width="1082" alt="Screen Shot 2021-11-08 at 8 27 37 PM" src="https://user-images.githubusercontent.com/39501842/140844988-3a1497c9-67cc-4fb2-ae00-36258743495c.png">

We can train a model to detect packages or food delivery. When packages or foods are delivered at our door, our model will automatically notify us. Compared to OpenCV or MediaPipe, Teachable Machine can distinguish and identify different objects. 



*Don't forget to run ```deactivate``` to end the Teachable Machines demo, and to reactivate with ```source tmachine/bin/activate``` when you want to use it again.*

Future use: We can train a model to detect packages or food delivery. When packages or foods are delivered at our door, our model will automatically notify us.


#### Filtering, FFTs, and Time Series data. (optional)
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the accelerometer, try the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

**2. Set up averaging** Can you average your signal in N-sample blocks? N-sample running average?

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

**\*\*\*Include links to your code here, and put the code for these in your repo--they will come in handy later.\*\*\***


### Part B
### Construct a simple interaction.

Pick one of the models you have tried, pick a class of objects, and experiment with prototyping an interaction.
This can be as simple as the boat detector earlier.
Try out different interaction outputs and inputs.

**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***

**Clothes recommendation according to weather**

Our smart closet obtains weather data online and uses computer vision to detect the cloth the user is wearing. Then, the closet will alert the user if the cloth worn is not appropriate for the current weather, such as temperature or rain. For example, if the temperature is too cold and the user is only wearing a t-shirt, the closet will alert the user about the temperature and recommend the user to wear a jacket. 

Our users do not need to interact with the closet every time they put on clothes because we think that is onerous and unnecessary. The closet will only alert the user when our closet detects that the user’s cloth is not appropriate for the weather. This function is useful during days of sudden temperature change. 

Besides the digital components in this closet, we will also construct a physical mechanism that automatically brings the suggested outfit to the user right after the alert is given. This mechanism will work together with the computer vision to further help the user stay comfortable when outside.

<img src="https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%205/imgs/closet_sketch.jpg"/>

In our initial design of the smart closet, we created two conveyor belts to transform the cloths slowly to the left in the closet and quickly to the right when the cloth reaches the very left side. Between the belts a mechanism is designed to pass the cloths from one belt to the other. The cloths rotate 90 degrees on the fast speed belt to reduce the depth needed to install this smart closet. 

<img src="https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%205/imgs/ClosetDesign2.jpg"/>

### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it what it is supposed to do?
1. When does it fail?
1. When it fails, why does it fail?
1. Based on the behavior you have seen, what other scenarios could cause problems?

1. The closet will only detect the outermost layer of your clothes. 
1. If the misclassification of clothes leads to wrong recommendations of clothes, the user will be too cold or too hot throughout the day. And hate the closet...
1. When alerting and giving recommendations to the users, the closet can indicate the confidence of their recommendation. For example, if it is snowing but the user is only wearing a t-shirt, the closet can say, “the current snowing weather is too cold for only wearing a t-shirt, I think a coat is more appropriate.” However, if the cloth is only slight appropriate, the closet can say, “I think your clothes is not warm enough for today’s weather, you might want to consider wearing a little bit more”


**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system?
1. How bad would they be impacted by a miss classification?
1. How could change your interactive system to address this?
1. Are there optimizations you can try to do on your sense-making algorithm.



### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
* What is a good environment for X?
* What is a bad environment for X?
* When will X break?
* When it breaks how will X break?
* What are other properties/behaviors of X?
* How does X feel?

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***

[![Acting Out Video](https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%205/imgs/DemoVideoCover.jpg)](https://drive.google.com/file/d/12TELZ26dpRTNzY9gsF-hU6i5cUXe7gln/view?usp=sharing)

### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**\*\*\*Include a short video demonstrating the finished result.\*\*\***

<img src="https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%205/imgs/InitialPrototype.jpg"/>

<img src="https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%205/imgs/ClosetDesign.jpg"/>

<img src="https://github.com/AdamYuzhenZhang/Interactive-Lab-Hub/blob/Fall2021/Lab%205/imgs/PrototypePhotos.jpg"/>
