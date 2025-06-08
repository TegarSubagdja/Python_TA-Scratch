import cv2
import numpy as np
import pandas as pd
from Algoritma import jps
# Awalan
from GetPosition import Position
from GetErrorPosition import Error
from GetPreprocessing import Preprocessing
# Optimasi
from MethodOptimasi.PathPolylineOptimization import prunning

# Baca gambar dalam grayscale
scale = 3
image = cv2.imread('Image/2.jpg', 0)

# Preprocessing
pos = Position(image)
print("Posisi Awal : ", pos)
map, pos = Preprocessing(image, pos, scale)
print("Setelah di flip : ", pos)

# Pencarian Jalur
path, _ = jps.method(map, pos['start'], pos['goal'], 2)
print("Path Asli : ", path)

# Optimasi
path = prunning(path, map)
print("Path Hasil Prunning : ", path)

# Mengubah Koordinat Jalur ke Ukuran Asli
path = [(y * scale, x * scale) for y, x in path]
print("Path Hasil Scale : ", path)

#Menggambar Path di Image Ukuran Asli
image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

for i in range(1, len(path)):
    y1, x1 = path[i - 1]
    y2, x2 = path[i]
    cv2.line(image, (x1, y1), (x2, y2), (0,255,0), 5)  # 255 = warna putih, 2 = ketebalan

for y, x in path:
    cv2.circle(image, (x, y), 2, (0,0,255), -1)  # Note: (x, y) karena OpenCV pakai (x, y) order

cv2.imwrite('Output/Output.jpg', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
