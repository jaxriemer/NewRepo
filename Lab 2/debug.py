from signal import pause
import RPi.GPIO as GPIO
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import
import time
from datetime import datetime

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
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

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

# creating new Image object
img = Image.new('RGB', (135, 240), (125, 125, 125))
draw = ImageDraw.Draw(img)

draw.rectangle(
   (0,240,240,200),
   fill = (0,0,255),
   outline=(0, 0, 0))


draw = ImageDraw.Draw(img)

draw.rectangle(
   (4,236,132,204),
   fill=(255, 0, 0),
   outline=(0, 0, 0))

button_count = 0
disp.image(img)


# BUTTON PIN-SETUP
START_BUTTON_PIN = 16
BREAK_BUTTON_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(START_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BREAK_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#CREATE COUNTDOWN
rotation = 90
def countdown(t):
   print('Start of countdown loop')
   # print(continue_countdown)
   while (t and GPIO.input(BREAK_BUTTON_PIN) != GPIO.LOW):
      mins, secs = divmod(t, 60)
      timer = '{:02d}:{:02d}'.format(mins, secs)
      print(timer, end="\r")
      time.sleep(1)
      t -= 1  
      if GPIO.input(BREAK_BUTTON_PIN) == GPIO.LOW:
         # continue_countdown = False
         print('Stop countdown')
         return

   # if continue_countdown == False:
   #    print('Exit function')
   #    # print(continue_countdown)
   #    return
# input time in seconds
# t = 2 
# function call
# countdown(int(t))



try:
   while True:
      if GPIO.input(START_BUTTON_PIN) == GPIO.LOW: #Check if user has started countdown
        image = Image.new("RGB", (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)

        # creating new Image object
        img = Image.new('RGB', (135, 240), (125, 125, 125))
        draw = ImageDraw.Draw(img)

        draw.rectangle(
        (0,240,240,200),
        fill = (0,0,255),
        outline=(0, 0, 0))


        draw = ImageDraw.Draw(img)

        draw.rectangle(
        (4,236,132,204),
        fill=(255, 0, 0),
        outline=(0, 0, 0))

        button_count = 0
        disp.image(img)
        if GPIO.input(BREAK_BUTTON_PIN) == GPIO.HIGH:
            draw.rectangle(
            (4,236,132,204),
            fill=(255, 0, 0),
            outline=(0, 0, 0))
            disp.image(img)

            image = Image.open("smiley2.jpg")
            disp.image(img)
            
            print('Button is pressed')
            countdown(int(5))
            if GPIO.input(BREAK_BUTTON_PIN) == GPIO.HIGH:
                draw = ImageDraw.Draw(img)
                draw.rectangle(
                (4,236,25,204),
                fill = (125, 125, 125),
                outline = (0, 0, 0))
                disp.image(img)

            countdown(int(5))
            if GPIO.input(BREAK_BUTTON_PIN) == GPIO.HIGH:
                draw = ImageDraw.Draw(img)
                draw.rectangle(
                (4,236,50,204),
                fill = (125, 125, 125),
                outline = (0, 0, 0))
                disp.image(img)

            countdown(int(5))
            if GPIO.input(BREAK_BUTTON_PIN) == GPIO.HIGH:  
                draw = ImageDraw.Draw(img)
                draw.rectangle(
                (4,236,75,204),
                fill = (125, 125, 125),
                outline = (0, 0, 0))
                disp.image(img)
        
            countdown(int(5))
            if GPIO.input(BREAK_BUTTON_PIN) == GPIO.HIGH:
                draw = ImageDraw.Draw(img)
                draw.rectangle(
                (4,236,100,204),
                fill = (125, 125, 125),
                outline = (0, 0, 0))
                disp.image(img)

            countdown(int(5))
            if GPIO.input(BREAK_BUTTON_PIN) == GPIO.HIGH:
                draw = ImageDraw.Draw(img)
                draw.rectangle(
                (4,236,125,204),
                fill = (125, 125, 125),
                outline = (0, 0, 0))
                disp.image(img)

            countdown(int(5))
            if GPIO.input(BREAK_BUTTON_PIN) == GPIO.HIGH:
                draw = ImageDraw.Draw(img)
                draw.rectangle(
                (4,236,150,204),
                fill = (125, 125, 125),
                outline = (0, 0, 0))
                disp.image(img)
            if GPIO.input(BREAK_BUTTON_PIN) == GPIO.HIGH:
                print('STOP')
                # Draw a black filled box to clear the image.
                draw.rectangle((0, 0, width, height), outline=0, fill=0)
                disp.image(img)

                # Load a TTF Font
                font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
                # Draw Some Text
                text = "Take a Break!"
                (font_width, font_height) = font.getsize(text)
                draw.text((width//2 - font_width//2, height//2 - font_height//2),
                text, font=font, fill=(255, 255, 0))
                img_rotate = img.rotate(90)
                disp.image(img_rotate)
        else:
            break
   else:
      print('Button is not pressed')

except KeyboardInterrupt:
   GPIO.cleanup()
