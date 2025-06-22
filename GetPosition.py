from cv2 import aruco
import numpy as np
import cv2

def Position(image, idStart, idGoal, marker_length=0.05, camera_matrix=None, dist_coeffs=None):
    if image is None:
        print("Gagal membaca gambar.")
        return None

    # Setup ArUco
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, _ = detector.detectMarkers(image)

    if ids is None:
        print("Tidak ada marker terdeteksi.")
        return None

    ids = ids.flatten()
    koordinat = {'start': None, 'goal': None}
    rvec_goal = None
    tvec_goal = None

    # Estimasi pose jika kamera tersedia
    if camera_matrix is not None and dist_coeffs is not None:
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(
            corners, marker_length, camera_matrix, dist_coeffs)

    # Loop marker
    for i, marker_id in enumerate(ids):
        if marker_id == idStart or marker_id == idGoal:
            marker_corners = corners[i][0]
            center_x = int(np.mean(marker_corners[:, 0]))
            center_y = int(np.mean(marker_corners[:, 1]))

            if marker_id == idStart:
                koordinat['start'] = (center_x, center_y)
            elif marker_id == idGoal:
                koordinat['goal'] = (center_x, center_y)
                if camera_matrix is not None and dist_coeffs is not None:
                    rvec_goal = rvecs[i]
                    tvec_goal = tvecs[i]

    # Validasi akhir
    if koordinat['start'] is None or koordinat['goal'] is None or rvec_goal is None or tvec_goal is None:
        print("Salah satu marker tidak lengkap atau pose gagal.")
        return None

    return koordinat, rvec_goal, tvec_goal
