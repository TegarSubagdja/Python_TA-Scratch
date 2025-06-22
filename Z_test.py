import cv2
import numpy as np

# ========== PARAMETER KAMERA
camera_matrix = np.array([[800, 0, 320],
                          [0, 800, 240],
                          [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((5, 1))  # Asumsikan no distortion

# ========== MARKER SETUP
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
marker_length = 0.05  # 5 cm marker

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
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, marker_length, camera_matrix, dist_coeffs)

        id_list = ids.flatten()
        if 0 in id_list and 1 in id_list:
            idx0 = np.where(id_list == 0)[0][0]
            idx1 = np.where(id_list == 1)[0][0]

            rvec0, tvec0 = rvecs[idx0], tvecs[idx0]
            rvec1, tvec1 = rvecs[idx1], tvecs[idx1]

            # Rotasi marker 0
            R0, _ = cv2.Rodrigues(rvec0)

            # Transformasi posisi ID 1 ke dalam kerangka marker ID 0
            goal = R0.T @ (tvec1[0] - tvec0[0])
            start = np.array([0, 0, 0])  # Pusat marker ID 0

            # ========== BUAT JALUR ZIGZAG
            num_steps = 5
            path_0 = []
            for i in range(num_steps + 1):
                alpha = i / num_steps
                point = (1 - alpha) * start + alpha * goal

                if 0 < i < num_steps:
                    offset = 0.02 * (-1)**i
                    lateral = np.cross(goal, [0, 0, 1])
                    lateral = lateral / (np.linalg.norm(lateral) + 1e-6)
                    point += offset * lateral

                path_0.append(point)
            path_0 = np.array(path_0)

            # ========== PROYEKSIKAN PATH KE IMAGE
            image_points = []
            for pt in path_0:
                pt_cam = R0 @ pt.reshape(3, 1) + tvec0.reshape(3, 1)
                imgpt, _ = cv2.projectPoints(
                    pt_cam, np.zeros((3, 1)), np.zeros((3, 1)), camera_matrix, dist_coeffs)
                image_points.append(tuple(int(v) for v in imgpt[0][0]))

            # ========== GAMBAR PATH
            for i in range(len(image_points) - 1):
                cv2.line(frame, image_points[i], image_points[i+1], (0, 255, 0), 2)

            # ========== GAMBAR TENGAH MARKER ID 0 DAN 1
            for tvec in [tvec0, tvec1]:
                center_cam = tvec.reshape(3, 1)
                center_2d, _ = cv2.projectPoints(
                    center_cam, np.zeros((3, 1)), np.zeros((3, 1)), camera_matrix, dist_coeffs)
                center_2d = tuple(int(v) for v in center_2d[0][0])
                cv2.circle(frame, center_2d, 5, (0, 0, 255), -1)

            # ========== GAMBAR FRAME MARKER
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec0, tvec0, 0.03)
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec1, tvec1, 0.03)

    # ========== TAMPILKAN HASIL
    cv2.imshow("Path Zigzag Locked to Marker", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
