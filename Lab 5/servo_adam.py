import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo_grab = kit.servo[2]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo_grab.set_pulse_width_range(500, 2500)



def grab_cloth():
    deg = 0
    while deg < 150:
        deg += 1
        try:
            # Set the servo to degree position
            servo_grab.angle = deg
            time.sleep(0.1)

        except KeyboardInterrupt:
            # Once interrupted, set the servo back to 0 degree position
            servo_grab.angle = 0
            time.sleep(0.5)
            break

def release_cloth():
    deg = 150
    while deg > 0:
        deg -= 1
        try:
            # Set the servo to degree position
            servo_grab.angle = deg
            time.sleep(0.1)

        except KeyboardInterrupt:
            # Once interrupted, set the servo back to 0 degree position
            servo_grab.angle = 0
            time.sleep(0.5)
            break

grab_cloth()
release_cloth()