import cv2
import numpy as np
from Utils import *

# Konfigurasi awal
target_point = (100, 100)

# Inisialisasi kamera (ubah ke 0 jika webcam utama)
cap = cv2.VideoCapture(2)
ret, cam = cap.read()

# Load parameter kalibrasi dari file .npz
data = np.load("Calibration/calibration.npz")
camMatrix = data['camMatrix']
distCoeff = data['distCoeff']

gray = cv2.cvtColor(cam, cv2.COLOR_BGR2GRAY)

# Koreksi distorsi sebelum diproses
cam = cv2.undistort(gray, camMatrix, distCoeff)

path = getPath(gray, 1, 0, 1)

# Cek apakah kamera berhasil dibuka
if not cap.isOpened():
    print("Tidak dapat membuka webcam.")
    exit()

while True:
    ret, cam = cap.read()
    if not ret:
        print("Gagal membaca frame dari webcam.")
        break

    gray = cv2.cvtColor(cam, cv2.COLOR_BGR2GRAY)

    # Koreksi distorsi sebelum diproses
    cam = cv2.undistort(gray, camMatrix, distCoeff)

    # Jalankan orientasi menggunakan ArUco
    result = GetOrientation(cam, id=0, target_point=path[0], show_result=False)

    # Inisialisasi path (hanya sekali di awal)
    if path is None:
        path = getPath(cam, 10, 0, 1)  # Sesuaikan parameter jika per lu

    # Jika orientasi valid
    if result and result['error_orientasi_derajat'] is not None:
        frame = result['image']
        center = result['koordinat']
        error = f"{int(result['error_orientasi_derajat'])}"
        distance = f"{int(result['distance'])}"

        # Visualisasi
        cv2.circle(cam, path[0], 10, (255, 128, 255), -1)
        cv2.putText(cam, f"Error: {error} deg", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(cam, f"Dist: {distance}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    # Tampilkan frame
    cv2.imshow('Realtime ArUco Tracking', cam)

    # Tekan ESC untuk keluar
    if cv2.waitKey(1) & 0xFF == 27:
        print("Tombol ESC ditekan, keluar dari program.")
        break

# Tutup kamera dan jendela
cap.release()
cv2.destroyAllWindows()
