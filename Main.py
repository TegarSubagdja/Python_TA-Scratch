import cv2
import os
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from GetPosition import position
from GetPreprocessing import preprocessing

path = 'Image/IMG20250531140928.jpg'

# Baca gambar
# current_dir = os.getcwd()
# path = askopenfilename(title="Pilih Gambar", initialdir=current_dir, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])

image = cv2.imread(path)
image = cv2.resize(image, (1920, 1080))

koordinate = position(image)
map = preprocessing(image)

cv2.waitKey(0)  # Tunggu tombol ditekan
cv2.destroyAllWindows()
