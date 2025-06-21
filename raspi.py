import RPi.GPIO as GPIO
import time

# Define GPIO pins for IN1 to IN4
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# Setup GPIO mode
GPIO.setmode(GPIO.BCM) #mode
GPIO.setwarnings(False)

# Setup all pins as output
motor_pins = [IN1, IN2, IN3, IN4]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Define step sequence for 28BYJ-48 motor (half-step for smoother motion)
half_step_seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

# Function to move forward
def move_forward(steps=512, delay=0.001):
    for _ in range(steps):
        for step in half_step_seq:
            for pin, val in zip(motor_pins, step):
                GPIO.output(pin, val)
            time.sleep(delay)

# Main
try:
    print("Moving forward...")
    move_forward(512)  # 512 steps = ~1 full rotation
    print("Done.")
finally:
    GPIO.cleanup()
