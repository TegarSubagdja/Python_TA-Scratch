import cv2
import cv2.aruco as aruco
import numpy as np

# Load gambar dari file atau webcam
img = cv2.imread('Image/1.jpg')  # ganti dengan frame dari kamera jika perlu
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Inisialisasi dictionary ArUco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

# Deteksi marker
corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

if corners:
    for i, marker_corners in enumerate(corners):
        pts = marker_corners[0]

        # Hitung panjang sisi horizontal (lebar)
        top_width = np.linalg.norm(pts[0] - pts[1])
        bottom_width = np.linalg.norm(pts[2] - pts[3])
        avg_width = (top_width + bottom_width) / 2

        # Hitung panjang sisi vertikal (tinggi)
        left_height = np.linalg.norm(pts[0] - pts[3])
        right_height = np.linalg.norm(pts[1] - pts[2])
        avg_height = (left_height + right_height) / 2

        print(f"Marker {ids[i][0]}: Lebar = {avg_width:.2f} px, Tinggi = {avg_height:.2f} px")

        # Opsional: Gambar marker dan tampilkan
        cv2.polylines(img, [np.int32(pts)], True, (0, 255, 0), 2)
        cv2.putText(img, f"{int(avg_width)}x{int(avg_height)} px", 
                    (int(pts[0][0]), int(pts[0][1]) - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imwrite('Detected Marker.jpg', img)
else:
    print("Marker tidak ditemukan.")
