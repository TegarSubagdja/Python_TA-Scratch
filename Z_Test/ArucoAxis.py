import cv2
import numpy as np

# Baca gambar dari file
image_path = "Image/1.jpg"  # Ganti dengan path gambar kamu
frame = cv2.imread(image_path)

if frame is None:
    print("Gagal membaca gambar.")
    exit()

h, w = frame.shape[:2]

# Dummy intrinsics (asumsi)
fx = fy = 1000.0
cx = w / 2.0
cy = h / 2.0
camera_matrix = np.array([[fx, 0, cx],
                          [0, fy, cy],
                          [0,  0,  1]], dtype=np.float32)
dist_coeffs = np.zeros((5, 1), dtype=np.float32)

# ArUco setup
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# Panjang marker (meter)
marker_length = 0.04  # 4 cm

# Deteksi marker
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
corners, ids, _ = detector.detectMarkers(gray)

if ids is not None:
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
        corners, marker_length, camera_matrix, dist_coeffs)

    for rvec, tvec in zip(rvecs, tvecs):
        cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, marker_length * 0.5)

# Tampilkan hasil
cv2.imwrite("output_orientasi.jpg", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
