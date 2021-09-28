import time
import os
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import datetime

import busio
import qwiic_joystick
import qwiic_button
import spaceship

import random

from time import strftime

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Setup joystick
joystick = qwiic_joystick.QwiicJoystick()
joystick.begin()
# Setup button
button = qwiic_button.QwiicButton()
button.begin()

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
image = Image.new("RGBA", (width, height))
rotation = 90

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0, 0))
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

# create spaceship
spaceship_img = (cwd + "/imgs/spaceship.png")
the_ship = spaceship.spaceship(120, 100, spaceship_img)
# create list of bullets
the_bullets = spaceship.bullets()
# bullet spacer
bullet_tick = 0
# create list of enemies
the_enemies = spaceship.enemies()
enemy_img = (cwd + "/imgs/enemy.png")
enemy_tick = 30
# hardness = enemy tick
hardness = 30
# explosion effect
explode_img = (cwd + "/imgs/explode.png")
# whether time to play game
timeToPlay, live, justSet = False, True, False
# used to show the fail page
fail_tick = 20
# art
game_background = (cwd + "/imgs/game_background.png")
# score
score = 0
alarm_str = "16:36:00"

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py

    # Parse date & time
    curr_time = time.strftime("%m/%d/%Y %H:%M:%S")
    date_str, time_str = curr_time.split(" ")
    hour, min, sec = time_str.split(":")
    month, day, year = date_str.split("/")

    if buttonA.value and (not buttonB.value): # button B pressed
        if max_page > curr_page:
            curr_page += 1
    elif (not buttonA.value) and buttonB.value: # button A pressed
        if min_page < curr_page:
            curr_page -= 1

    if (not buttonA.value) and (not buttonB.value): # both buttons pressed
        if justSet == False:
            if timeToPlay:
                timeToPlay = False
            else:
                timeToPlay = True
            justSet = True

    if buttonA.value and buttonB.value:
        justSet = False

    if time_str == alarm_str:
        timeToPlay = True

    if curr_page == 1:
        image = Image.open(hour_img[int(hour)])
        image = image.convert("RGBA")
        draw = ImageDraw.Draw(image)
        draw.text((70, 110), time_str, font=font, fill="#FFFFFF")
    elif curr_page == 2:
        image = Image.open(day_img[int(day)])
        draw = ImageDraw.Draw(image)
        draw.text((90, 110), ("DAY " + day), font=font, fill="#FFFFFF")
    elif curr_page == 3:
        month_list = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        image = Image.open(month_img[int(month) - 1])
        draw = ImageDraw.Draw(image)
        draw.text((90, 110), month_list[int(month) - 1], font=font, fill="#FFFFFF")
    elif curr_page == 4:
        image = Image.open(year_img)
        draw = ImageDraw.Draw(image)
        draw.text((95, 110), year, font=font, fill="#FFFFFF")

    # play game
    if timeToPlay:
        background = Image.open(game_background).convert("RGBA")
        image.paste(background, (0,0,240,135), background)
        if live:
            # draw spaceship
            the_ship.draw(image)
            draw = ImageDraw.Draw(image)

            # move spaceship
            the_ship.move(joystick.get_horizontal() - 520, joystick.get_vertical() - 508)

            # add enemies
            if enemy_tick == 0:
                the_enemies.addEnemy(random.randint(20, 220), 0, random.randint(-1, 1), random.randint(1, 2), enemy_img)
                enemy_tick = hardness
                if hardness > 8:
                    hardness -= 2
            else:
                enemy_tick -= 1
            # draw enemies
            the_enemies.updateEnemies(image)

            # shoot bullet
            if button.is_button_pressed():
                # add bullet to bullets
                if bullet_tick == 0:
                    the_bullets.addBullet(the_ship.x, the_ship.y - 10, 0, -1)
                    bullet_tick = 5
                else:
                    bullet_tick -= 1

            # process and draw bullets
            the_bullets.updateBullets(draw)

            # collide
            failed, t = spaceship.collideEnemies(the_enemies, the_ship, the_bullets, explode_img, image)
            score += t

            # print score
            draw.text((2, 2), str(score), font=font, fill="#FFFFFF")

        if failed and fail_tick > 0:
            the_enemies.removeAll()
            the_bullets.removeAll()
            live = False
            draw.text((90, 60), "FAILED", font=font, fill="#FF0000")
            draw.text((90, 40), "Score: " + str(score), font=font, fill="#FFFFFF")
            fail_tick -= 1
            hardness = 30

        else:
            fail_tick = 20
            live = True

        # Game will automatically stop when the score reaches 20
        if score == 20:
            the_enemies.removeAll()
            the_bullets.removeAll()
            draw.text((90, 60), "SUCCESS", font=font, fill="#00FF00")
            timeToPlay = False

    disp.image(image, rotation)
    time.sleep(0.05)
