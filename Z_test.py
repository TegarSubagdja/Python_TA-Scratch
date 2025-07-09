import cv2
import numpy as np

# ========== PARAMETER KAMERA
camera_matrix = np.array([[800, 0, 320],
                          [0, 800, 240],
                          [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((5, 1))

# ========== SETUP ARUCO
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
marker_length = 0.05  # 5 cm marker

# ========== PATH DALAM KOORDINAT MARKER (X, Y, Z)
# Path ini tertanam pada bidang datar marker ID 0, dalam satuan meter
locked_path_marker_frame = np.array([
    [0.02, 0.02, 0.0],  # 2 cm kanan, 2 cm bawah dari tengah marker
    [0.15, 0.10, 0.0],
    [0.05, 0.05, 0.0],
    [0.07, 0.07, 0.0]
])

# ========== BUKA KAMERA
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None and 0 in ids:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, marker_length, camera_matrix, dist_coeffs)

        # Ambil pose marker ID 0
        idx0 = np.where(ids.flatten() == 0)[0][0]
        rvec0 = rvecs[idx0]
        tvec0 = tvecs[idx0]
        R0, _ = cv2.Rodrigues(rvec0)

        # PROYEKSIKAN PATH KE GAMBAR (setiap frame)
        image_points = []
        for pt in locked_path_marker_frame:
            pt_cam = R0 @ pt.reshape(3, 1) + tvec0.reshape(3, 1)
            imgpt, _ = cv2.projectPoints(
                pt_cam, np.zeros((3, 1)), np.zeros((3, 1)), camera_matrix, dist_coeffs)
            image_points.append(tuple(int(v) for v in imgpt[0][0]))

        # GAMBAR PATH
        for i in range(len(image_points) - 1):
            cv2.line(frame, image_points[i], image_points[i + 1], (0, 255, 0), 2)
            cv2.circle(frame, image_points[i], 4, (255, 0, 0), -1)

        # GAMBAR FRAME MARKER
        cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec0, tvec0, 0.03)

    # TAMPILKAN
    cv2.imshow("Path Flat on Marker", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Esc untuk keluar
        break

cap.release()
cv2.destroyAllWindows()