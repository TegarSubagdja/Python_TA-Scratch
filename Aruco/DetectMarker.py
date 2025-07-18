import cv2
import cv2.aruco as aruco
import numpy as np

def detect_aruco_realtime(camera_index=1, aruco_dict_type=aruco.DICT_4X4_50):
    """
    Deteksi ArUco marker secara realtime menggunakan webcam.

    Args:
        camera_index (int): Index kamera (default 0 untuk kamera utama).
        aruco_dict_type (int): Tipe dictionary ArUco (default DICT_4X4_50).
    """

    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Tidak dapat membuka kamera.")
        return

    # Inisialisasi dictionary dan parameter deteksi
    aruco_dict = aruco.getPredefinedDictionary(aruco_dict_type)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    print("Tekan 'q' untuk keluar.\nMulai deteksi ArUco Marker...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame dari kamera.")
            break

        # Deteksi marker
        corners, ids, _ = detector.detectMarkers(frame)

        if ids is not None:
            # Gambar kotak di sekitar marker dan tampilkan ID
            aruco.drawDetectedMarkers(frame, corners, ids, (255,0,255))
            
        cv2.imshow("Deteksi ArUco Realtime", frame)

        # Tekan 'q' untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

import cv2
import cv2.aruco as aruco
import numpy as np

def detect_aruco_from_image(image_path, aruco_dict_type=aruco.DICT_4X4_50):
    """
    Deteksi ArUco marker dari file gambar.

    Args:
        image_path (str): Path ke gambar.
        aruco_dict_type (int): Tipe dictionary ArUco.
    """

    # Load gambar
    frame = cv2.imread(image_path)
    if frame is None:
        print("Gagal membaca gambar:", image_path)
        return

    # Inisialisasi dictionary dan parameter deteksi
    aruco_dict = aruco.getPredefinedDictionary(aruco_dict_type)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    # Deteksi marker
    corners, ids, _ = detector.detectMarkers(frame)

    if ids is not None:
        print(f"Terdeteksi {len(ids)} marker: {ids.flatten()}")
        aruco.drawDetectedMarkers(frame, corners, ids)
    else:
        print("Tidak ada marker terdeteksi.")

    # Tampilkan hasil
    cv2.imshow("Deteksi ArUco dari Gambar", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

import cv2
import cv2.aruco as aruco
import numpy as np
import time

def detect_aruco_realtime_filer(camera_index=1, aruco_dict_type=aruco.DICT_4X4_50, min_valid_frames=3, timeout=2):
    """
    Deteksi ArUco marker secara realtime menggunakan webcam dengan validasi multi-frame.

    Args:
        camera_index (int): Index kamera.
        aruco_dict_type (int): Tipe dictionary ArUco.
        min_valid_frames (int): Jumlah frame minimal untuk menganggap marker valid.
        timeout (int): Timeout dalam detik untuk menghapus marker yang tidak terlihat lagi.
    """

    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    desired_width = 1280
    desired_height = 720

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

    if not cap.isOpened():
        print("Tidak dapat membuka kamera.")
        return

    # Inisialisasi dictionary dan parameter deteksi
    aruco_dict = aruco.getPredefinedDictionary(aruco_dict_type)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    # Penyimpanan histori marker
    marker_history = {}  # {id: {'count': int, 'last_seen': float}}

    print("Tekan 'q' untuk keluar.\nMulai deteksi ArUco Marker...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame dari kamera.")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        current_time = time.time()

        # Deteksi marker
        corners, ids, _ = detector.detectMarkers(frame)

        if ids is not None:
            for id_array in ids:
                marker_id = int(id_array[0])
                if marker_id in marker_history:
                    marker_history[marker_id]['count'] += 1
                    marker_history[marker_id]['last_seen'] = current_time
                else:
                    marker_history[marker_id] = {'count': 1, 'last_seen': current_time}

        # Hapus marker yang timeout
        to_delete = []
        for marker_id, info in marker_history.items():
            if current_time - info['last_seen'] > timeout:
                to_delete.append(marker_id)
        for marker_id in to_delete:
            del marker_history[marker_id]

        # Gambar marker valid
        if ids is not None:
            valid_ids = []
            valid_corners = []

            for i, id_array in enumerate(ids):
                marker_id = int(id_array[0])
                if marker_id in marker_history and marker_history[marker_id]['count'] >= min_valid_frames:
                    valid_ids.append(id_array)
                    valid_corners.append(corners[i])
                    # Tampilkan label marker valid
                    cv2.putText(frame, f"VALID ID: {marker_id}",
                                (int(corners[i][0][0][0]), int(corners[i][0][0][1]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Gambar hanya marker valid
            if valid_ids:
                aruco.drawDetectedMarkers(frame, valid_corners, np.array(valid_ids))

        cv2.imshow("Deteksi ArUco Realtime (Multi-frame Validasi)", frame)

        # Tekan 'q' untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # detect_aruco_realtime()
    # detect_aruco_from_image("Image/1.jpg")  # Ganti dengan path gambar kamu
    detect_aruco_realtime_filer(camera_index=1, min_valid_frames=3)
