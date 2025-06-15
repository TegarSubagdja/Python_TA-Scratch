from Utils import *

def Position(image):
    # Inisialisasi dictionary dan parameter
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()

    # Dictionary untuk menyimpan koordinat ID 1 dan 7
    koordinat = {'start': None, 'goal': None}

    if image is None:
        print("Gagal membaca gambar.")
        return koordinat

    # Konversi ke grayscale
    detector = aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(image)

    if ids is not None:
        aruco.drawDetectedMarkers(image, corners, ids)
        print("Marker terdeteksi dengan ID:", ids.flatten())

        for i, marker_id in enumerate(ids.flatten()):
            if marker_id in [1, 2]:
                marker_corners = corners[i][0]
                center_x = int(np.mean(marker_corners[:, 0]))
                center_y = int(np.mean(marker_corners[:, 1]))
                print(f"ID {marker_id}: posisi tengah = ({center_x}, {center_y})")

                # Simpan koordinat ke dict
                if marker_id == 1:
                    koordinat['start'] = (center_x, center_y)
                elif marker_id == 2:
                    koordinat['goal'] = (center_x, center_y)
    else:
        print("Tidak ada marker terdeteksi.")

    return koordinat
