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



# decrement energy level
# Main loop:

button_count = 0
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()
disp.image(img)

button_count = 2

if button_count == 1:
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        (4,236,25,204),
        fill = (125, 125, 125),
        outline = (0, 0, 0))

if button_count == 2:
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        (4,236,50,204),
        fill = (125, 125, 125),
        outline = (0, 0, 0))

if button_count == 3:
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        (4,236,75,204),
        fill = (125, 125, 125),
        outline = (0, 0, 0))

if button_count == 4:
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        (4,236,100,204),
        fill = (125, 125, 125),
        outline = (0, 0, 0))

if button_count == 5:
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        (4,236,125,204),
        fill = (125, 125, 125),
        outline = (0, 0, 0))

if button_count == 6:
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        (4,236,150,204),
        fill = (125, 125, 125),
        outline = (0, 0, 0))

disp.image(img)
