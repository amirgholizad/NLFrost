#import RPi.GPIO as GPIO
#import time

#servo_pin = 17  # BCM numbering
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(servo_pin, GPIO.OUT)

# Set PWM frequency to 50Hz (20ms period)
#pwm = GPIO.PWM(servo_pin, 50)
#pwm.start(0)

#def set_angle(angle):
#    duty = 2 + (angle / 18)
#    GPIO.output(servo_pin, True)
#    pwm.ChangeDutyCycle(duty)
#    time.sleep(0.03)
#    GPIO.output(servo_pin, False)
#    pwm.ChangeDutyCycle(0)

#try:
#    while True:
#        angle = int(input("Enter angle (0 to 180): "))
#        set_angle(angle)
#except KeyboardInterrupt:
#    pwm.stop()
#    GPIO.cleanup()


