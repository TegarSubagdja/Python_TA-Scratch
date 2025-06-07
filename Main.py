import cv2
import numpy as np
import pandas as pd
from Algoritma import jps
from GetPosition import position
from GetErrorPosition import error

# Baca gambar dalam grayscale
image = cv2.imread('Image/2.jpg', 0)

pos = position(image)
errpos = error(image) 
print(errpos)

_, biner = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY_INV)
kernel3x3 = np.ones((3,3), np.uint8)
erosi = cv2.erode(biner, kernel3x3, iterations=6)
kernel = np.ones((3,3), np.uint8)
dilasi = cv2.dilate(erosi, kernel, iterations=30)
cv2.circle(dilasi, pos['start'], 128, 0, -1)
cv2.circle(dilasi, pos['goal'], 128, 0, -1)

dilasi = cv2.resize(dilasi, (dilasi.shape[1]//2, dilasi.shape[0]//2))
pos = {
    key: (x // 2, y // 2)
    for key, (x, y) in pos.items()
}

map = np.array(dilasi)

Ys, Xs = pos['start']
Yg, Xg = pos['goal']
cv2.line(map, (Ys, Xs), (Ys, Xs), 255, 10)
# path, _ = jps.method(map, (Xs,Ys), (Xg, Yg), 2)

cv2.imwrite('Inilah Hasilnya.jpg', map)
cv2.waitKey(0)
cv2.destroyAllWindows()
