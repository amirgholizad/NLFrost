    ###############################
#  PiBot Line Following 
#  Davis MT
#  28.02.2020
###############################

# import libraries 
import RPi.GPIO as gpio
import time
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
    gpio.output(13,0)
    gpio.output(15,0)


# main program loop


if __name__=="__main__":
    stopAll()   # make sure all pin are set to off

    rightOn()
    leftOn()

    time.sleep(5)
    rightOff()
    leftOff()
    time.sleep(1)
    rightOn()
    leftOff()
    time.sleep(5)
    rightOff()
    leftOff()



    gpio.cleanup()
            




