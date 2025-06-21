import cv2
import numpy as np

def detect_tennis_balls(image_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Mask tennis ball color (yellow-green)
    lower_yellow = np.array([25, 100, 100])
    upper_yellow = np.array([45, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Remove court color (example for green court)
    lower_court = np.array([35, 40, 40])
    upper_court = np.array([85, 255, 255])
    court_mask = cv2.inRange(hsv, lower_court, upper_court)
    mask = cv2.bitwise_and(mask, cv2.bitwise_not(court_mask))

    # Morphological cleanup
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Edge detection
    edges = cv2.Canny(mask, 50, 150)

    # Find contours on edges
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area < 100 or area > 3000:
            continue

        # Contour solidity
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        if hull_area == 0:
            continue
        solidity = float(area) / hull_area
        if solidity < 0.8:
            continue

        # Circularity
        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        if circularity < 0.7 or circularity > 1.2:
            continue

        # Fit circle
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        if radius < 10 or radius > 50:
            continue

        # Distance fit check (fixed here)
        center = np.array([int(x), int(y)])
        distances = [cv2.norm(center, pt[0]) for pt in cnt]
        mean_dist = np.mean(distances)
        if abs(mean_dist - radius) / radius > 0.2:
            continue

        # Mean HSV inside contour check
        mask_contour = np.zeros(mask.shape, dtype=np.uint8)
        cv2.drawContours(mask_contour, [cnt], -1, 255, -1)
        mean_hsv = cv2.mean(hsv, mask=mask_contour)[:3]
        if not (lower_yellow[0] <= mean_hsv[0] <= upper_yellow[0]):
            continue

        # Passed all checks — draw bounding box and circle
        x_, y_, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x_, y_), (x_ + w, y_ + h), (0, 255, 0), 2)
        cv2.circle(image, (int(x), int(y)), int(radius), (255, 0, 0), 2)

    cv2.imshow('Better Tennis Ball Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
detect_tennis_balls('tennis_court.jpg')
