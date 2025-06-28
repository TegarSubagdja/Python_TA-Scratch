import cv2
import numpy as np

image = cv2.imread('Image/8.jpg')
image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
kernel = np.ones((3, 3), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
thresh = cv2.erode(thresh, kernel, iterations=3)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 3000:
        
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = box.astype(int)

        # Gambar kotak luar
        cv2.polylines(image, [box], True, (0, 255, 255), 2)

        # Gambar dua diagonal silang
        cv2.line(image, tuple(box[0]), tuple(box[2]), (255, 0, 255), 2)  # Diagonal 1
        cv2.line(image, tuple(box[1]), tuple(box[3]), (0, 255, 0), 2)    # Diagonal 2

        # Tandai sudut
        for pt in box:
            cv2.circle(image, tuple(pt), 4, (0, 0, 255), -1)

cv2.imshow('Diagonal Silang', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
