import time
import os
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
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
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 4
y = 10

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

cwd = os.getcwd()

hour_img = []
for h in range(24):
    hour_img.append((cwd + "/imgs/time_" + str(h) + ".jpg"))

day_img = []
for d in range(15):
    for i in range(2):
        day_img.append((cwd + "/imgs/day_" + str(d) + ".jpg"))

month_img = []
for m in range(12):
    month_img.append((cwd + "/imgs/month_" + str(m) + ".jpg"))

year_img = cwd + "/imgs/year.jpg"

max_page, min_page = 4, 1
curr_page = 1

mydate = 0
mymonth = 0
mytime = 0

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py

    # Parse date & time
    curr_time = strftime("%m/%d/%Y %H:%M:%S")
    date_str, time_str = curr_time.split(" ")
    hour, min, sec = time_str.split(":")
    month, day, year = date_str.split("/")

    # is_hour, is_day, is_month, is_year = False, False, False, False

    if buttonA.value and (not buttonB.value): # button B pressed
        if max_page > curr_page:
            curr_page += 1
    elif (not buttonA.value) and buttonB.value: # button A pressed
        if min_page < curr_page:
            curr_page -= 1
    # speed up for demonstration
    elif buttonA.value and buttonB.value:
        if curr_page == 1:
            hour = mytime
            mytime = mytime + 1
            if mytime > 23:
                mytime = 0
        elif curr_page == 2:
            day = str(mydate)
            mydate = mydate + 1
            if mydate > 30:
                mydate = 1
        elif curr_page == 3:
            month = mymonth
            mymonth = mymonth + 1
            if mymonth > 12:
                mymonth = 1
            
        

    if curr_page == 1:
        image = Image.open(hour_img[int(hour)])
        draw = ImageDraw.Draw(image)
        draw.text((70, 110), time_str, font=font, fill="#FFFFFF")
    elif curr_page == 2:
        image = Image.open(day_img[int(day)])
        draw = ImageDraw.Draw(image)
        draw.text((90, 110), ("DAY " + day), font=font, fill="#FFFFFF")
    elif curr_page == 3:
        month_list = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        image = Image.open(month_img[int(month)])
        draw = ImageDraw.Draw(image)
        draw.text((90, 110), month_list[int(month) - 1], font=font, fill="#FFFFFF")
    elif curr_page == 4:
        image = Image.open(year_img)
        draw = ImageDraw.Draw(image)
        draw.text((95, 110), year, font=font, fill="#FFFFFF")
                  

    # Display image.

    disp.image(image, rotation)
    time.sleep(1)
