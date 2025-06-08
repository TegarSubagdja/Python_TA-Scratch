import cv2
import cv2.aruco as aruco
import numpy as np

def normalize_angle(angle):
    """Normalisasi sudut ke rentang [-pi, pi]."""
    return (angle + np.pi) % (2 * np.pi) - np.pi

def Error(image):
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    koordinat = {'start': None, 'goal': None}
    orientasi_robot = None

    if image is None:
        print("Gagal membaca gambar.")
        return koordinat, None

    corners, ids, _ = detector.detectMarkers(image)

    if ids is not None:
        aruco.drawDetectedMarkers(image, corners, ids)
        print("Marker terdeteksi dengan ID:", ids.flatten())

        for i, marker_id in enumerate(ids.flatten()):
            if marker_id in [1, 7]:
                marker_corners = corners[i][0]
                center_x = int(np.mean(marker_corners[:, 0]))
                center_y = int(np.mean(marker_corners[:, 1]))
                print(f"ID {marker_id}: posisi tengah = ({center_x}, {center_y})")

                if marker_id == 1:
                    koordinat['start'] = (center_x, center_y)
                    vector = marker_corners[1] - marker_corners[0]
                    orientasi_robot = np.arctan2(vector[1], vector[0])
                    print(f"Orientasi robot (ID 1) dalam radian: {orientasi_robot:.3f}")

                elif marker_id == 7:
                    koordinat['goal'] = (center_x, center_y)
    else:
        print("Tidak ada marker terdeteksi.")

    # Jika kedua marker ditemukan, hitung error orientasi
    if koordinat['start'] is not None and koordinat['goal'] is not None and orientasi_robot is not None:
        dx = koordinat['goal'][0] - koordinat['start'][0]
        dy = koordinat['goal'][1] - koordinat['start'][1]
        arah_ke_goal = np.arctan2(dy, dx)

        error_orientasi = normalize_angle(arah_ke_goal - orientasi_robot)

        print(f"Arah ke goal (ID 7) dalam radian: {arah_ke_goal:.3f}")
        print(f"Error orientasi (radian): {error_orientasi:.3f}")
        print(f"Error orientasi (derajat): {np.degrees(error_orientasi):.2f}")

        return koordinat, error_orientasi
    else:
        return koordinat, None
