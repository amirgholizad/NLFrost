    ###############################
#  PiBot Line Following 
#  Davis MT
#  28.02.2020
###############################

# import libraries 
import RPi.GPIO as gpio
from gpiozero import Motor, AngularServo
from time import sleep


# from enum import IntEnum

# class State(IntEnum):
#     STOP = 0
#     DETECTING_BALL = 1
#     BALL_DETECTED = 2
#     BALL_REACHED = 3
#     DETECTING_FLAG = 4
#     FLAG_REACHED = 5
#     FLAG_DETECTED = 6
#     LOOP_BACK_DETECTING_BALL = 7  # same as DETECTING_BALL logically

# # Define transition logic
# def next_state(current_state):
#     if current_state == State.STOP:
#         return State.DETECTING_BALL
#     elif current_state == State.FLAG_DETECTED:
#         return State.LOOP_BACK_DETECTING_BALL
#     elif current_state == State.LOOP_BACK_DETECTING_BALL:
#         return State.BALL_DETECTED  # Optional: Define if needed
#     else:
#         return State(current_state + 1)

# set pin mapping to BOARD

gpio.setmode(gpio.BOARD)


# turn off channel warnings messages
gpio.setwarnings(False)

# Set GPIO pins as output
gpio.setup(13,gpio.OUT)
gpio.setup(15,gpio.OUT)


# set GPIO pins as inputs
# leftSensor = 7
# rightSensor = 10
# gpio.setup(leftSensor,gpio.IN)
# gpio.setup(rightSensor,gpio.IN)

# turn on left motor
def leftOn():
    gpio.output(15,1)

# turn off left motor
def leftOff():
    gpio.output(15,0)
    
    
# turn on right motor
def rightOn():
    gpio.output(13,1)


#turn off right motor
def rightOff():
    gpio.output(13,0)


# turn off all motors
def stopAll():
    print("Stopping all motors")
    gpio.output(13,0)
    gpio.output(15,0)


def moveForward():
    print("Moving forward")
    rightOn()
    leftOn()

def moveStop():
    print("Stopping")
    rightOff()
    leftOff()

def moveRight():
    print("Moving right")
    rightOn()
    rightOff()

def moveLeft():
    print("Moving left")
    rightOff()
    leftOn()


arm_servo = AngularServo(17, min_angle = 0, max_angle = 90)

def close():
# Close

    print("closing arm")

    arm_servo.value = 0.6
    sleep(0.45)
    arm_servo.value = None

    sleep(3)

# Open
def open():
    print("opening arm")
    arm_servo.value = -0.5
    sleep(0.2)
    arm_servo.value = None

# if __name__=="__main__":
#     stopAll()   # make sure all pin are set to off

#     current_state=  State.STOP

#     if current_state == State.STOP:
#         current_state = State(current_state+1)
#     elif current_state== State.DETECTING_BALL : 
#         moveRight()



#     gpio.cleanup()
            




