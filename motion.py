import cv2
import numpy as np
from gpiozero import Motor, Servo
from time import sleep

# GPIO Setup
left_motor = Motor(forward=17, backward=18)
right_motor = Motor(forward=22, backward=23)
arm_servo = Servo(24)

# Camera
cap = cv2.VideoCapture(0)  # Adjust if needed

# Yellow Color Range (HSV)
lower_yellow = np.array([20, 80, 80])
upper_yellow = np.array([55, 255, 255])

def detect_yellow_object(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        if area > 100:
            (x, y), radius = cv2.minEnclosingCircle(largest)
            return int(x), int(y), int(radius), area
    return None

def rotate_in_place():
    left_motor.forward()
    right_motor.backward()

def move_towards(cx, frame_w):
    center = frame_w // 2
    tol = 40
    if cx < center - tol:
        left_motor.backward()
        right_motor.forward()
    elif cx > center + tol:
        left_motor.forward()
        right_motor.backward()
    else:
        left_motor.forward()
        right_motor.forward()

def stop_motors():
    left_motor.stop()
    right_motor.stop()

def trap_ball():
    print("Trapping ball...")
    arm_servo.max()
    sleep(1)
    arm_servo.mid()

def release_ball():
    print("Releasing ball...")
    arm_servo.min()
    sleep(1)
    arm_servo.mid()

# Main Control
try:
    stage = "find_ball"

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        h, w = frame.shape[:2]
        detection = detect_yellow_object(frame)

        if stage == "find_ball":
            if not detection:
                print("Rotating to find ball...")
                rotate_in_place()
            else:
                stop_motors()
                cx, cy, r, area = detection
                print(f"Ball detected: cx={cx}, radius={r}, y={cy}")
                if r < 40:
                    move_towards(cx, w)
                else:
                    stop_motors()
                    trap_ball()
                    stage = "find_flag"

        elif stage == "find_flag":
            if not detection:
                print("Rotating to find flag...")
                rotate_in_place()
            else:
                stop_motors()
                cx, cy, r, area = detection
                print(f"Flag detected: cx={cx}, radius={r}, y={cy}")
                if cy > 200:  # If object is low → probably ball again
                    print("Ignoring ball, looking for flag...")
                    rotate_in_place()
                elif r < 40:
                    move_towards(cx, w)
                else:
                    stop_motors()
                    release_ball()
                    print("Mission complete!")
                    break

        sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    stop_motors()
    cap.release()
    cv2.destroyAllWindows()
    print("Shutdown complete.")
