import board
from adafruit_seesaw import seesaw, rotaryio, digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import digitalio as dio
import os

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

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

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
last_position = 0

toward_player = False


while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, top), "To start the game,", font=font, fill="#FFFFFF")
    draw.text((x, 15), "press the red button.", font=font, fill="#FFFFFF")
    disp.image(image, rotation)

    # negate the position to make clockwise rotation positive
    position = -encoder.position

    if int(position) > int(last_position+2) and not toward_player:
        toward_player = True
        last_position = position
        position = -encoder.position
        print("Position: {}".format(position))
        print("head rotated towards the player")

    if int(position) < int(last_position-2) and toward_player:
        toward_player = False
        last_position = position
        position = -encoder.position
        print("Position: {}".format(position))
        print("head rotated towards the controller")


