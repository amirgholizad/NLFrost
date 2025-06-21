import cv2
import numpy as np

def detect_tennis_balls_from_webcam():
    # Open the webcam
    cap = cv2.VideoCapture(2)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize (optional)
        frame = cv2.resize(frame, (640, 480))

        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define yellow color range for tennis ball
        lower_yellow = np.array([25, 100, 100])
        upper_yellow = np.array([45, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Morphological cleaning
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        maxArea = -10000

        for cnt in contours:
            area = cv2.contourArea(cnt)

            if(area <= maxArea):
                continue

            maxArea = area

            if area < 100 or area > 5000:
                continue

            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            if circularity < 0.75:
                continue

            # Bounding box
            x, y, w, h = cv2.boundingRect(cnt)
            (cx, cy), radius = cv2.minEnclosingCircle(cnt)

            # Draw detection
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (int(cx), int(cy)), int(radius), (255, 0, 0), 2)

        # Show result
        cv2.imshow("Tennis Ball Detection (Classic CV)", frame)

        # Exit on ESC or 'q'
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run it
detect_tennis_balls_from_webcam()
