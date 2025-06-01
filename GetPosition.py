import cv2
import cv2.aruco as aruco
import numpy as np

def position(image):
    # Inisialisasi dictionary dan parameter
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()

    if image is None:
        print("Gagal membaca gambar.")
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, _ = detector.detectMarkers(gray)

        if ids is not None:
            aruco.drawDetectedMarkers(image, corners, ids)
            print("Marker terdeteksi dengan ID:", ids.flatten())

            # Loop dan cari posisi marker ID 1 dan 7
            for i, marker_id in enumerate(ids.flatten()):
                if marker_id in [1, 7]:
                    # Ambil koordinat sudut-sudut marker
                    marker_corners = corners[i][0]  # shape (4, 2) 
                    # Hitung titik tengah (x, y)
                    center_x = int(np.mean(marker_corners[:, 0]))
                    center_y = int(np.mean(marker_corners[:, 1]))
                    print(f"ID {marker_id}: posisi tengah = ({center_x}, {center_y})")

                    # Tambahkan titik di gambar
                    cv2.circle(image, (center_x, center_y), 10, (0, 255, 0), -1)
                    cv2.putText(image, f"ID {marker_id}", (center_x + 10, center_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            print("Tidak ada marker terdeteksi.")