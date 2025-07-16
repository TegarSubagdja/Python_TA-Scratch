import cv2
import cv2.aruco as aruco
import numpy as np

def detect_aruco_realtime(camera_index=0, aruco_dict_type=aruco.DICT_4X4_50):
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

if __name__ == "__main__":
    # detect_aruco_realtime()
    detect_aruco_from_image("Image/1.jpg")  # Ganti dengan path gambar kamu
