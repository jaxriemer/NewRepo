# control servo to complete the cloth deliver function
import time
from adafruit_servokit import ServoKit


# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo_slide_forward = kit.servo[0]
servo_slide_backward = kit.servo[0]
servo_pick = kit.servo[0]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo_slide_forward.set_pulse_width_range(500, 2500)
servo_slide_backward.set_pulse_width_range(500, 2500)
servo_pick.set_pulse_width_range(500, 2500)



def move_servo_slide(closet_distance):
    if closet_distance > 0:
        servo_slide = servo_slide_forward
        print('move forward')
    else:
        servo_slide = servo_slide_backward
        print('move backward')

    print('move %d position'%closet_distance)

    turn = abs(closet_distance * 5) #TODO: need to alter 5 to correct number
    print('move %d turns'%turn)

    for i in range(turn):
        try:
            # Set the servo to 180 degree position
            servo_slide.angle = 180
            time.sleep(0.27) # the best sleep time
            # Set the servo to 0 degree position
            servo_slide.angle = 0
            time.sleep(0.27)

        except KeyboardInterrupt:
            # Once interrupted, set the servo back to 0 degree position
            servo_slide.angle = 0
            time.sleep(0.5)

def push_cloth():
    print('about to push cloth')
    try:
        # Set the servo to 180 degree position
        servo_pick.angle = 180
        print('cloth pushed')
        time.sleep(10)
        # Set the servo to 0 degree position
        servo_pick.angle = 0
    except KeyboardInterrupt:
    # Once interrupted, set the servo back to 0 degree position
        servo_pick.angle = 0
        time.sleep(0.5)


def retrieve_cloth(curr_pos,target_cloth):

    closet_cloth = {'coat':0,'tshirt':1,'jacket':2}
    target_pos = closet_cloth[target_cloth]
    print('current position is %d, moving to position %d.'%(curr_pos,target_pos))

    move_distance = target_pos - curr_pos
    move_servo_slide(move_distance)

    push_cloth()
    curr_pos = target_pos

    return curr_pos

def servo_distance_test(closet_distance):
    turn = abs(closet_distance * 14) #TODO: need to alter 5 to correct number
    while True:
        try:
            # Set the servo to 180 degree position
            servo.angle = 180
            time.sleep(0.27)
            # Set the servo to 0 degree position
            servo.angle = 0
            time.sleep(0.27)

        except KeyboardInterrupt:
            # Once interrupted, set the servo back to 0 degree position
            servo.angle = 0
            time.sleep(0.5)
            break



# test
# curr_pos = 5
# curr_pos = retrieve_cloth(curr_pos,'jacket')
servo_distance_test(1)



















