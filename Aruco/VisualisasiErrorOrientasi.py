# aruco_orientation.py

from Utils import *
import cv2
import cv2.aruco as aruco
import numpy as np

def normalize_angle(angle):
    return (angle + np.pi) % (2 * np.pi) - np.pi

def GetOrientation(image, target_point, show_result=True, save_path=None):

    if image is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan di path: {image}")

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, _ = detector.detectMarkers(image)

    koordinat = {'start': None}
    orientasi_robot = None
    error_orientasi = None

    if ids is not None:
        for i, marker_id in enumerate(ids.flatten()):
            marker_corners = corners[i][0]
            center_x = int(np.mean(marker_corners[:, 0]))
            center_y = int(np.mean(marker_corners[:, 1]))

            if marker_id == 1:
                koordinat['start'] = (center_x, center_y)
                vector = marker_corners[1] - marker_corners[0]
                orientasi_robot = np.arctan2(vector[1], vector[0])

        aruco.drawDetectedMarkers(image, corners, ids)

    # Hitung orientasi dan error terhadap titik target
    if koordinat['start'] and orientasi_robot is not None:
        start = koordinat['start']
        goal = target_point  # Gunakan target_point dari parameter

        dx = goal[0] - start[0]
        dy = goal[1] - start[1]
        arah_ke_goal = np.arctan2(dy, dx)
        error_orientasi = normalize_angle(arah_ke_goal - orientasi_robot)

        # Visualisasi
        panjang_panah = 100
        orientasi_x = int(start[0] + panjang_panah * np.cos(orientasi_robot))
        orientasi_y = int(start[1] + panjang_panah * np.sin(orientasi_robot))

        cv2.line(image, start, goal, (255, 0, 255), 8)
        cv2.arrowedLine(image, start, (orientasi_x, orientasi_y), (255,64,64), 10, tipLength=0.2)

        teks_error = f"Error: {np.degrees(error_orientasi):.2f} deg"
        cv2.putText(image, teks_error, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    if save_path:
        cv2.imwrite(save_path, image)

    if show_result:
        cv2.imshow("Hasil Deteksi dan Orientasi", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return {
        "koordinat": koordinat,
        "orientasi_robot": orientasi_robot,
        "target_point": target_point,
        "error_orientasi_radian": error_orientasi,
        "error_orientasi_derajat": np.degrees(error_orientasi) if error_orientasi is not None else None,
        "image": image
    }
