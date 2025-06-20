import cv2
import numpy as np
from cv2 import aruco

# Inisialisasi webcam
cap = cv2.VideoCapture(2)  # Ganti 0 sesuai nomor kamera kamu

# Setup ArUco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

print("Tekan ESC untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame.")
        break

    # Deteksi ArUco
    corners, ids, _ = detector.detectMarkers(frame)

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        print("ID Marker Terdeteksi:", ids.flatten())
    else:
        print("Tidak ada marker terdeteksi.")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Tampilkan hasil
    cv2.imshow("Deteksi ArUco", binary)

    # Tekan ESC untuk keluar
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
