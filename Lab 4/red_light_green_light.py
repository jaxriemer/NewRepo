import board
from adafruit_seesaw import seesaw, rotaryio, digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import digitalio as dio
import os
import qwiic
import busio
import adafruit_ssd1306
from adafruit_servokit import ServoKit
import qwiic_button
import adafruit_mpr121
import time
from pydub import AudioSegment
from pydub.playback import play
import gtts
from io import BytesIO
from adafruit_servokit import ServoKit

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = dio.DigitalInOut(board.CE0)
dc_pin = dio.DigitalInOut(board.D25)
reset_pin = None

BAUDRATE = 64000000
spi = board.SPI()
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
padding = -2
top = padding
bottom = height - padding
x = 0

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)

backlight = dio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# encoder
seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)
button_held = False

encoder = rotaryio.IncrementalEncoder(seesaw)

# distance
ToF = qwiic.QwiicVL53L1X()
print("Distance Sensor Test\n")
if (ToF.sensor_init() == None):					 # Begin returns 0 on a good init
    print("Sensor online!\n")

# oled
#i2c = busio.I2C(board.SCL, board.SDA)
#oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
serial = i2c(port=1, address=0x3C)
oled = ssd1306(serial,width=128, height=32, rotate=2) # rotate=2 is 180 degrees
#oled.fill(0)
#oled.show()
#image_oled = Image.new("1", (oled.width, oled.height))
#draw_oled = ImageDraw.Draw(image_oled)

# servo
kit = ServoKit(channels=16)
servo = kit.servo[0]
# TODO: check servo datasheet
servo.set_pulse_width_range(500, 2500)

def rotate_head(degree):
    try:
        # Set the servo to 180 degree position
        servo.angle = degree
    except KeyboardInterrupt:
        # Once interrupted, set the servo back to 0 degree position
        servo.angle = 0
        time.sleep(0.5)

# button
button = qwiic_button.QwiicButton()
button.begin()

# touch sensor (MPR121)
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

def eliminate_player():
    text = "You are eliminated!"
    tts = gtts.gTTS(text, lang='en')
    mp3 = BytesIO()
    tts.write_to_fp(mp3)
    mp3.seek(0)
    audio = AudioSegment.from_file(mp3, format='mp3')
    play(audio)
    gun_sound = AudioSegment.from_wav("gun_sound.wav")
    play(gun_sound)

new_game = False

while not button.is_button_pressed():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, top), "Press the red button", font=font, fill="#FFFFFF")
    draw.text((x, 15), "to start the game.", font=font, fill="#FFFFFF")
    disp.image(image, rotation)

    if button.is_button_pressed():
        new_game = True

while new_game:
    # initiate last position of the encoder
    rotate_head(0)
    last_position = -encoder.position

    new_game = False
    continue_game = True
    toward_player = False

    t = 60

    #draw_oled.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    #draw_oled.text((0, 0), "Game starts.", font=font, fill=255)
    #oled.image(image_oled)
    #oled.show()
    with canvas(oled) as draw:
        draw.text((0, 0), "Game starts.", fill="white", font=font)

    time.sleep(3)

    distanceCount = 0
    PlayerMoved = False
    CheckForFail = False
    rotate_head(180)
    sensitivity = 200

    while continue_game:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x, top), "Game starts.", font=font, fill="#FFFFFF")

        draw.text((x, 25), "Rotate the encoder", font=font, fill="#FFFFFF")
        draw.text((x, 43), "to control the head.", font=font, fill="#FFFFFF")

        draw.text((x, 70), "Press the red button", font=font, fill="#FFFFFF")
        draw.text((x, 88), "to restart the game.", font=font, fill="#FFFFFF")
        disp.image(image, rotation)

        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        t -= 1

        #draw_oled.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
        #draw_oled.text((0,0),timer,font=font,fill=255)
        #oled.image(image_oled)
        #oled.show()
        with canvas(oled) as draw:
            draw.text((0, 0), "timer", fill="white", font=font)

        if not CheckForFail:
            girlSound = AudioSegment.from_wav("Simida.wav")
            play(girlSound)

        # Player dead
        if timer == "00:00":
            continue_game = False
            while not button.is_button_pressed():
                draw.rectangle((0, 0, width, height), outline=0, fill=0)
                draw.text((x, top), "You win.", font=font, fill="#FFFFFF")
                draw.text((x, 25), "Press the red button", font=font, fill="#FFFFFF")
                draw.text((x, 43), "to restart the game.", font=font, fill="#FFFFFF")
                disp.image(image, rotation)
                if button.is_button_pressed():
                    new_game = True
                    break

        if button.is_button_pressed():
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((x, top), "Game is about to start.", font=font, fill="#FFFFFF")
            disp.image(image, rotation)

            new_game = True
            continue_game = False
            time.sleep(5)
            break

        # Distance Sensor
        try:
            # check distance
            ToF.start_ranging()						 # Write configuration bytes to initiate measurement
            time.sleep(.05)
            current_distance= ToF.get_distance()	 # Get the result of the measurement from the sensor
            time.sleep(.05)
            ToF.stop_ranging()
            #print("Distance(mm): %d" % (current_distance))
            if (distanceCount > 5) and (abs(current_distance - prev_distance) > sensitivity):
                   # eliminate_player()
                    #print("Movement Distance(mm): %d"%(abs(current_distance - prev_distance)))
                PlayerMoved = True
            else:
                PlayerMoved = False
            prev_distance = current_distance
            distanceCount += 1
        except Exception as e:
            print(e)

        # negate the position to make clockwise rotation positive
        position = -encoder.position

        # if the controller rotates the encoder so that the face is towards the player
        if (-50 <= position <= 50) and (0 <= last_position <= 50) and (position > last_position) and (not toward_player):
            toward_player = True
            last_position = position
            print("Position: {}".format(position))
            print("head rotated towards the player")
            rotate_head(0)
            CheckForFail = True

        if (-50 <= position <= 50) and (0 <= last_position <= 50) and (position < last_position) and toward_player:
            # TODO: face rotates back (servo)
            toward_player = False
            last_position = position
            print("Position: {}".format(position))
            print("head rotated towards the controller")
            rotate_head(180)
            CheckForFail = False

        # Player dead
        if (CheckForFail and PlayerMoved):
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((x, top), "You win.", font=font, fill="#FFFFFF")
            draw.text((x, 25), "Press the red button", font=font, fill="#FFFFFF")
            draw.text((x, 43), "to restart the game.", font=font, fill="#FFFFFF")
            disp.image(image, rotation)
            eliminate_player()
            break

        if True in mpr121.touched_pins:
            print("Touched!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            continue_game = False
            while not button.is_button_pressed():
                #draw_oled.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
                #draw_oled.text((0, 0), "You win.", font=font, fill=255)
                #oled.image(image_oled)
                #oled.show()
                with canvas(oled) as draw:
                    draw.text((0, 0), "You win!", fill="white", font=font)

                draw.rectangle((0, 0, width, height), outline=0, fill=0)
                draw.text((x, top), "The player wins.", font=font, fill="#FFFFFF")
                draw.text((x, 25), "Press the red button", font=font, fill="#FFFFFF")
                draw.text((x, 43), "to restart the game.", font=font, fill="#FFFFFF")
                disp.image(image, rotation)
                if button.is_button_pressed():
                    new_game = True
                    break