import cv2
import numpy as np
import pandas as pd
from Algoritma import jps
from GetPosition import position

# Baca gambar dalam grayscale
image = cv2.imread('Image/2.jpg', 0)

pos = position(image)
_, biner = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY_INV)
kernel3x3 = np.ones((3,3), np.uint8)
erosi = cv2.erode(biner, kernel3x3, iterations=6)
kernel = np.ones((3,3), np.uint8)
dilasi = cv2.dilate(erosi, kernel, iterations=30)
cv2.circle(dilasi, pos['start'], 128, 0, -1)
cv2.circle(dilasi, pos['goal'], 128, 0, -1)

dilasi = cv2.resize(dilasi, (dilasi.shape[1]//2, dilasi.shape[0]//2))
posn = {
    key: (x // 2, y // 2)
    for key, (x, y) in pos.items()
}

map = np.array(dilasi)

Ys, Xs = posn['start']
Yg, Xg = posn['goal']
path = jps.method(map, (Xs,Ys), (Xg, Yg), 2)
print("Jalur:", path)

if path[0] != 0 and path[0] is not None:
    for i in range(len(path[0]) - 1):
        pt1 = (path[0][i][1], path[0][i][0])   
        pt2 = (path[0][i+1][1], path[0][i+1][0])
        cv2.line(map, pt1, pt2, 255, 10)

cv2.imwrite('Hasil.jpg', map)
cv2.waitKey(0)
cv2.destroyAllWindows()
