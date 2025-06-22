    ###############################
#  PiBot Line Following 
#  Davis MT
#  28.02.2020
###############################

# import libraries 
import RPi.GPIO as gpio
from time import sleep


# Servo setup
SERVO_PIN = 11
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(SERVO_PIN, gpio.OUT)

# Set up PWM at 50Hz

def test_servo():
    sleepVal = float(input("SleepVal: "))
    stopVal = float(input("stopVal: "))
    duty = float(input("DutyVal: "))
    pwm.ChangeDutyCycle(duty)
    sleep(sleepVal)
    pwm.ChangeDutyCycle(stopVal)
# def move_servo_to(angle):
#     max_duty = 7.6
#     min_duty = 6.8
#     duty = max_duty - (angle / 180.0) * (max_duty - min_duty)
#     print(f"Moving to {angle}° → Duty = {round(duty, 2)}%")
#     pwm.ChangeDutyCycle(duty)
#     sleep(0.5)
#     pwm.ChangeDutyCycle(0)

def move_servo_to(direction):
    pwm = gpio.PWM(SERVO_PIN, 50)
    pwm.start(0)
    if direction == "open":
        print("Servo open!")
        pwm.ChangeDutyCycle(9)
        sleep(0.4)
        pwm.ChangeDutyCycle(7) # Stop
        pwm.stop()
        return
    
    print("Servo close!")
    pwm.ChangeDutyCycle(6)
    sleep(0.2)
    pwm.ChangeDutyCycle(7) # Stop
    pwm.stop()
    return 

def open_arm():
    # move_servo_to(0)    # Full anti-clockwise
    move_servo_to("open")

def close_arm():
    # move_servo_to(90)   # Center
    move_servo_to("close")

def full_close():
    # move_servo_to(180)  # Full clockwise
    pass
    
def cleanup():
    print("Cleaning up GPIO")
    pwm.stop()
    gpio.cleanup()

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

# gpio.setmode(gpio.BOARD)


# turn off channel warnings messages
# gpio.setwarnings(False)

# Set GPIO pins as output
gpio.setup(13,gpio.OUT)
gpio.setup(15,gpio.OUT)


# set GPIO pins as inputs
# leftSensor = 7
# rightSensor = 10
# gpio.setup(leftSensor,gpio.IN)
# gpio.setup(rightSensor,gpio.IN)

# turn on left motor
def _leftOn():
    gpio.output(15,1)

# turn off left motor
def _leftOff():
    gpio.output(15,0)
    
    
# turn on right motor
def _rightOn():
    gpio.output(13,1)


#turn off right motor
def _rightOff():
    gpio.output(13,0)


# turn off all motors
def stopAll():
    print("Stopping all motors")
    gpio.output(13,0)
    gpio.output(15,0)


def moveForward():
    # print("Moving forward")
    _rightOn()
    _leftOn()

def moveStop():
    print("Stopping")
    _rightOff()
    _leftOff()

def moveRight():
    # print("Moving right")
    _rightOn()
    _leftOff()

def moveLeft():
    # print("Moving left")
    _rightOff()
    _leftOn()




# if __name__=="__main__":
#     stopAll()   # make sure all pin are set to off

#     current_state=  State.STOP

#     if current_state == State.STOP:
#         current_state = State(current_state+1)
#     elif current_state== State.DETECTING_BALL : 
#         moveRight()



#     gpio.cleanup()
            




