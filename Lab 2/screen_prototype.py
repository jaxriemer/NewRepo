# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import digitalio
import board
from PIL import Image, ImageDraw
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

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
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
# pylint: enable=line-too-long

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

# Get current time
#current_datetime = datetime.strftime("%m/%d/%Y %H:%M:%S")
current_datetime = datetime.today()
current_time = datetime.strftime(current_datetime, '%H')
current_datetime = current_datetime.replace(hour =22,minute=0,second=0) #To simulate prototype
s1 = current_datetime.replace(hour =7,minute=0,second=0)
s2 = current_datetime.replace(hour =8,minute=0,second=0)
s3 = current_datetime.replace(hour =9,minute=0,second=0)
s4 = current_datetime.replace(hour =11,minute=0,second=0)
s5 = current_datetime.replace(hour =13,minute=0,second=0)
s6 = current_datetime.replace(hour =17,minute=0,second=0)
s7 = current_datetime.replace(hour =22,minute=0,second=0)


# Display sleeping image when it is before 7am
if datetime.strftime(current_datetime, '%H') <= datetime.strftime(s1, '%H'):
    image = Image.open("sleep.jpg")

# Display coffee image when after 7 am and before 8am
if  datetime.strftime(s1, '%H') < datetime.strftime(current_datetime, '%H') <= datetime.strftime(s2, '%H'):
    image = Image.open("coffee.JPG")

# Display breakfast image when after 8 am and before 9am
if  datetime.strftime(s2, '%H') < datetime.strftime(current_datetime, '%H') <= datetime.strftime(s3, '%H'):
    image = Image.open("breakfast.jpg")

# Display snack image when after 9am and before 11am
if  datetime.strftime(s3, '%H') < datetime.strftime(current_datetime, '%H') <= datetime.strftime(s4, '%H'):
    image = Image.open("sandwich.jpg")

# Display lunch image when after 11 am and before 1pm
if  datetime.strftime(s4, '%H') < datetime.strftime(current_datetime, '%H') <= datetime.strftime(s5, '%H'):
    image = Image.open("sandwich.jpg")

# Display snack image when after 1pm and before 5pm
if  datetime.strftime(s5, '%H') < datetime.strftime(current_datetime, '%H') <= datetime.strftime(s6, '%H'):
    image = Image.open("trailmix.jpg")

# Display dinner image when after 5pm and before 10pm
if  datetime.strftime(s6, '%H') < datetime.strftime(current_datetime, '%H') <= datetime.strftime(s7, '%H'):
    image = Image.open("dinner.jpg")

# Display sleep image when after 10pm
if datetime.strftime(s7, '%H') <= datetime.strftime(current_datetime, '%H'):
    image = Image.open("sleep.jpg")

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


# Scale the image to the smaller screen dimension
image_ratio = (image.width / image.height)/2
screen_ratio = width / height
if screen_ratio < image_ratio:
    scaled_width = image.width * height // image.height
    scaled_height = height
else:
    scaled_width = width
    scaled_height = image.height * width // image.width
image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

# Crop and center the image
x = scaled_width // 2 - width // 2
y = scaled_height // 2 - height // 2
image = image.crop((x, y, x + width, y + height))

# Display image.
disp.image(image)

