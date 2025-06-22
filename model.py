import cv2
import numpy as np
from time import sleep
from action import *
import signal, sys

def handle_sigint(signal_received, frame):
    print("\nCtrl+C detected. Cleaning up before exit...")
    # Add your custom stop logic here
    stopAll()
    cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_sigint)



# from gpiozero import Motor, AngularServo


# arm_servo = AngularServo(17, min_angle = 0, max_angle = 90)

# def close():
# # Close

#     print("closing arm")

#     arm_servo.value = 0.6
#     sleep(0.45)
#     arm_servo.value = 0


# # Open
# def open():
#     print("opening arm")
#     arm_servo.value = -0.5
#     sleep(0.2)
#     arm_servo.value = 0

def detect_color(frame, lower_color, upper_color, center_color):
    frame = cv2.resize(frame, (720, 480))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define yellow color range
    lower_color = np.array(lower_color)
    upper_color = np.array(upper_color)
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Morphological cleaning to reduce noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = (0, 0)
    area = 0
    if(contours):
        largest_contour = max(contours, key = cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        if area > 100:
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(frame, center, radius, (0, 255, 255), 2)
            cv2.circle(frame, center, 5, center_color, -1)
    return frame, center, area

def detect_tennis_balls_from_webcam():
    # Device Webcam 0
    arm_up = True


    cap = cv2.VideoCapture(0)

    desired_fps = 5
    cap.set(cv2.CAP_PROP_FPS, desired_fps)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, (x_y, y_y), area_y = detect_color(frame, [20, 80, 80], [55, 255, 255], (0, 255, 255))  #yellow
        frame, (x_o, y_o), area_o = detect_color(frame, [0, 100, 50], [10, 255, 150], (0, 255, 0))  #red

        # print("--------------------------------------------------")
        # print(f"Yellow Ball - Center: ({x_y}, {y_y}), Area: {area_y}")
        # print(f"Orange Ball - Center: ({x_o}, {y_o}), Area: {area_o}")
        # print("--------------------------------------------------")
        
        # cv2.imshow("Tennis Ball Detection (Classic CV)", frame)
        if arm_up:
            x = x_y
        else:
            x = x_o
        
        if x == 0:
            # print("No ball detected.")
            
            moveRight()
            
        elif 720/ 2 - 50 < x < 720 / 2 + 50:
            print(f"Area yellow: {area_y}")
            if area_y > 30000 and arm_up:
                arm_up = False
                stopAll()
                sleep(0.2)
                close_arm() # Close the arm
                sleep(0.1)  # Simulate arm movement delay
            elif area_o > 100000 and not arm_up:
                arm_up = True
                open_arm() # Open the arm
                sleep(0.1)  # Simulate arm movement delay
            moveForward()
        elif x <= 720 / 2 - 50:
            moveLeft()
        else:
            moveRight()


        # sleep(0.5)

        # Quitting program with 'q'
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            stopAll()
            cleanup()
            break


    cap.release()
    cv2.destroyAllWindows()



if __name__=="__main__":   
    detect_tennis_balls_from_webcam() 










        #################### Multi-ball handling ####################
        # for cnt in contours:
        #     area = cv2.contourArea(cnt)

        #     if area < 100:
        #         continue

        #     perimeter = cv2.arcLength(cnt, True)
        #     if perimeter == 0:
        #         continue
        #     circularity = 4 * np.pi * area / (perimeter * perimeter)
        #     if circularity < 0.75:
        #         continue

        #     # Bounding box
        #     x, y, w, h = cv2.boundingRect(cnt)
        #     (cx, cy), radius = cv2.minEnclosingCircle(cnt)

        #     # Draw detection
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #     cv2.circle(frame, (int(cx), int(cy)), int(radius), (255, 0, 0), 2)
        #############################################################
