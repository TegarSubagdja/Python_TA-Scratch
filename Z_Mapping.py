import cv2
import numpy as np

image = cv2.imread('Image/2.jpg', 0)
image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)

_, thresh = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)
kernel = np.ones((3, 3), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
thresh = cv2.erode(thresh, kernel, iterations=3)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 3000:
        epsilon = 0.2 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        
        cv2.drawContours(image, [approx], -1, (255, 255, 255), 2)
        for point in approx:
            x, y = point.ravel()
            cv2.circle(image, (int(x), int(y)), 5, (255, 255, 255), -1)

cv2.imshow('Hasil', image)
cv2.waitKey(0)
cv2.destroyAllWindows()