from Utils import *
import cv2
import time
import numpy as np
import threading
from cv2 import aruco

# Inisialisasi ArUco
detector_params = aruco.DetectorParameters()
detector_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
detector = aruco.ArucoDetector(detector_dict, detector_params)

# Konstanta
robot_id = 2
goal_marker_id = 7

# Webcam
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# Atur resolusi (misal: 640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
if not cap.isOpened():
    print("❌ Tidak dapat membuka webcam.")
    exit()

# Path sharing
shared_path = []
path_lock = threading.Lock()
path_thread_running = False

def calculate_path(image, pos, corners):
    global shared_path, path_thread_running

    # Jalankan fungsi getPath() di thread
    try:
        temp_path = getPath(image=image, scale=20, pos=pos, corners=corners)
        temp_path[0] = np.flip(pos[1])
        temp_path[-1] = np.flip(pos[0])

        # Setelah selesai, simpan hasil ke shared_path
        with path_lock:
            shared_path = temp_path
    except Exception as e:
        print(f"❌ Error dalam thread pencarian path: {e}")
    finally:
        path_thread_running = False  # Tandai bahwa thread selesai

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Gagal membaca frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    try:
        result = GetOrientation(
            gray, sId=robot_id, gId=goal_marker_id,
            show_result=False, detector=detector
        )

        if result is None:
            print("⚠️ Marker tidak lengkap. Melewatkan frame.")

        koordinat, corners, orientasi_robot, mark_size, distance, _, _, image = result

        # Jika tidak ada thread pencarian aktif, mulai pencarian baru
        if not path_thread_running:
            path_thread_running = True
            threading.Thread(
                target=calculate_path,
                args=(gray.copy(), koordinat, corners),
                daemon=True
            ).start()
        # Gambar path jika sudah tersedia
        with path_lock:
            if shared_path:
                points = np.array([[y, x] for x, y in shared_path], np.int32)
                cv2.polylines(frame, [points], False, (255, 0, 255), 2)
                for x, y in shared_path:
                    cv2.circle(frame, (y, x), 3, (255, 0, 255), -1)

    except Exception as e:
        print(f"❌ Error utama: {e}")

    cv2.imshow("Realtime Path Threaded", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        print("🔚 ESC ditekan. Keluar...")
        break

cap.release()
cv2.destroyAllWindows()
