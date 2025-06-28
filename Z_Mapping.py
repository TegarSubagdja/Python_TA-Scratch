from Utils import *
import cv2

image = cv2.imread('1-getPath.jpg', 0)

cv2.namedWindow('Threshold', cv2.WINDOW_NORMAL)

for i in range(1, 255):
    _, thresh = cv2.threshold(image, i, 255, cv2.THRESH_BINARY_INV)
    
    # Salin gambar biar aslinya tidak berubah
    display = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)  # Ubah ke BGR agar bisa diberi warna teks
    
    # Tambahkan teks di pojok kiri atas
    cv2.putText(display, f'Threshold: {i}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Threshold', display)
    cv2.waitKey(100)  # Atur delay

cv2.destroyAllWindows()