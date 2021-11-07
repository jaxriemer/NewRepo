# # control servo to complete the cloth deliver function
# import time
# from adafruit_servokit import ServoKit
#
# # Set channels to the number of servo channels on your kit.
# # There are 16 channels on the PCA9685 chip.
# kit = ServoKit(channels=16)
#
# # Name and set up the servo according to the channel you are using.
# servo_move = kit.servo[0]
# servo_pick = kit.servo[1]
#
# # Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# # Each servo might be different, you can normally find this information in the servo datasheet
# servo_move.set_pulse_width_range(500, 2500)
# servo_pick.set_pulse_width_range(500, 2500)
#
# degree_pick = 360
#
#
# def rotate_servo(servo,degree):
#     try:
#         # Set the servo to 180 degree position
#         servo.angle = degree
#     except KeyboardInterrupt:
#         # Once interrupted, set the servo back to 0 degree position
#         servo.angle = 0
#         time.sleep(0.5)
#
# def choose_clothes(clothes, curr_pos):
#     target_pos = clothes[clothes]
#
#
#
# def grab_clothes():
#     rotate_servo(servo_pick,degree_pick)
#     time.sleep(0.5)
#     rotate_servo(servo_pick,0)
#
#
# clothes = {'coat':0,'tshirt':1}
# servo_degree = {0:0, 1:180}
# curr_pos = 0



import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo = kit.servo[0]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo.set_pulse_width_range(500, 2500)

while True:
    try:
        # Set the servo to 180 degree position
        servo.angle = 180
        time.sleep(0.35)
        # Set the servo to 0 degree position
        servo.angle = 0
        time.sleep(0.35)

    except KeyboardInterrupt:
        # Once interrupted, set the servo back to 0 degree position
        servo.angle = 0
        time.sleep(0.5)
        break

















