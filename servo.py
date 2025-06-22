# #import RPi.GPIO as GPIO
# #import time

# #servo_pin = 17  # BCM numbering
# #GPIO.setmode(GPIO.BCM)
# #GPIO.setup(servo_pin, GPIO.OUT)

# # Set PWM frequency to 50Hz (20ms period)
# #pwm = GPIO.PWM(servo_pin, 50)
# #pwm.start(0)

# #def set_angle(angle):
# #    duty = 2 + (angle / 18)
# #    GPIO.output(servo_pin, True)
# #    pwm.ChangeDutyCycle(duty)
# #    time.sleep(0.03)
# #    GPIO.output(servo_pin, False)
# #    pwm.ChangeDutyCycle(0)

# #try:
# #    while True:
# #        angle = int(input("Enter angle (0 to 180): "))
# #        set_angle(angle)
# #except KeyboardInterrupt:
# #    pwm.stop()
# #    GPIO.cleanup()


from gpiozero import Motor, AngularServo
from time import sleep
import RPi.GPIO as gpio
gpio.setmode(gpio.BOARD)


# turn off channel warnings messages
gpio.setwarnings(False)

# Set GPIO pins as output
gpio.setup(13,gpio.OUT)
gpio.setup(15,gpio.OUT)
gpio.output(15,0)

gpio.output(15,1)

arm_servo = AngularServo(11, min_angle = 0, max_angle = 90)

# Close
def close():
    arm_servo.value = 0.6
    sleep(0.45)
    arm_servo.value = None

    sleep(3)

# Open
def open():
    arm_servo.value = -0.5
    sleep(0.2)
    arm_servo.value = None


# from action import *



# minn = float(input())
# maxx = float(input())

# test_servo()
# i=2
# while(i!=9):
#     i = int(input())
#     if i==0:
#         close_arm()
#     elif i==1:

#         open_arm()
#     elif i==3:
#         full_close()
#     sleep(1)

# close_arm()
# sleep(2)
# open_arm()

i = 8


while i !=9:
    i = int(input())
    if i==1:
        open()
    elif i==2:
        close()
