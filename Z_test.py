import cv2
import numpy as np

# ========== PARAMETER KAMERA (contoh, sesuaikan dengan kalibrasi kamera mu)
camera_matrix = np.array([[800, 0, 320],
                          [0, 800, 240],
                          [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((5, 1))  # Asumsikan no distortion untuk contoh ini

# ========== PARAMETER MARKER
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
marker_length = 0.05  # meter (5 cm)

# ========== BUKA KAMERA
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ========== DETEKSI MARKER
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None and len(ids) >= 2:
        # ========== DAPATKAN POSE
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, camera_matrix, dist_coeffs)

        # Cari marker ID 0 dan 1
        id_list = ids.flatten()
        if 0 in id_list and 1 in id_list:
            idx0 = np.where(id_list == 0)[0][0]
            idx1 = np.where(id_list == 1)[0][0]

            rvec0, tvec0 = rvecs[idx0], tvecs[idx0]
            rvec1, tvec1 = rvecs[idx1], tvecs[idx1]

            # Convert rvec ke rotasi (untuk ID 0)
            R0, _ = cv2.Rodrigues(rvec0)

            # ========== HITUNG POSISI MARKER 1 DALAM FRAME MARKER 0
            t_rel = tvec1[0] - tvec0[0]
            pos1_in_0 = R0.T @ t_rel

            # ========== BUAT JALUR ZIGZAG DALAM FRAME MARKER 0
            start = np.array([0, 0, 0])
            goal = pos1_in_0

            num_steps = 5
            path_0 = []
            for i in range(num_steps + 1):
                alpha = i / num_steps
                point = (1 - alpha) * start + alpha * goal

                # Tambahkan zigzag lateral di sumbu X (kanan-kiri)
                offset = 0.02 * (-1)**i  # zigzag kanan-kiri 2 cm
                lateral = np.cross(goal, [0, 0, 1])  # vector tegak lurus di plane
                lateral = lateral / (np.linalg.norm(lateral) + 1e-6)
                point += offset * lateral

                path_0.append(point)
                print(path_0)

            path_0 = np.array(path_0)


            # ========== PROYEKSIKAN PATH KE IMAGE
            image_points = []
            for pt in path_0:
                # transform ke kamera frame: R0 * pt + tvec0
                pt_cam = R0 @ pt.reshape(3, 1) + tvec0.reshape(3, 1)
                imgpt, _ = cv2.projectPoints(pt_cam, np.zeros((3,1)), np.zeros((3,1)), camera_matrix, dist_coeffs)
                image_points.append(tuple(int(v) for v in imgpt[0][0]))

            # ========== GAMBAR PATH
            for i in range(len(image_points) - 1):
                cv2.line(frame, image_points[i], image_points[i+1], (0, 255, 0), 2)

            # Gambar pose markers juga
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec0, tvec0, 0.03)
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec1, tvec1, 0.03)

    # ========== TAMPILKAN HASIL
    cv2.imshow("Path Tracking (Marker Locked)", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
