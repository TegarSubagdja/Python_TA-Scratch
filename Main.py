import cv2
import numpy as np
import pandas as pd
from Algoritma import jps
from GetPosition import Position
from GetErrorPosition import Error
from GetPreprocessing import Preprocessing

# Baca gambar dalam grayscale
image = cv2.imread('Image/2.jpg', 0)

pos = Position(image)
print("Posisi Awal : ", pos)
map, pos = Preprocessing(image, pos)
print("Setelah di flip : ", pos)

path, _ = jps.method(map, pos['start'], pos['goal'], 2)
print(path)

cv2.imwrite('Inilah Hasilnya.jpg', map)
cv2.waitKey(0)
cv2.destroyAllWindows()
