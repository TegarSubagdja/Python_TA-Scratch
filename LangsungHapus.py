import cv2
import numpy as np
import os

def nothing(x):
    pass

# Baca gambar dari file atau webcam
frame = cv2.imread('Image/IMG20250531140928.jpg')
frame = cv2.resize(frame, (1920, 1080))
if frame is None:
    raise ValueError("Gambar tidak ditemukan. Pastikan 'input.jpg' ada.")

# Buat jendela dan trackbars
cv2.namedWindow('Preprocessing UI')
cv2.createTrackbar('Kernel Size', 'Preprocessing UI', 1, 15, nothing)
cv2.createTrackbar('Iterations', 'Preprocessing UI', 1, 15, nothing)
cv2.createTrackbar('Threshold', 'Preprocessing UI', 100, 255, nothing)

while True:
    # Ambil nilai dari trackbars
    k_size = cv2.getTrackbarPos('Kernel Size', 'Preprocessing UI')
    iteration = cv2.getTrackbarPos('Iterations', 'Preprocessing UI')
    thresh_val = cv2.getTrackbarPos('Threshold', 'Preprocessing UI')

    # Pastikan kernel minimal 1x1
    k_size = max(1, k_size)
    kernel = np.ones((k_size, k_size), np.uint8)

    # Grayscale dan threshold
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)

    # Operasi morfologi
    closing = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=iteration)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations=iteration)

    # Tampilkan hasil
    cv2.imshow('Preprocessing UI', opening)

    # Tombol 's' untuk simpan hasil
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        filename = f'Preprocessing/k{k_size}_i{iteration}_t{thresh_val}.jpg'
        os.makedirs('Preprocessing', exist_ok=True)
        cv2.imwrite(filename, opening)
        print(f"Disimpan: {filename}")
    elif key == 27:  # Tombol ESC untuk keluar
        break

cv2.destroyAllWindows()
