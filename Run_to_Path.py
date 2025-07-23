from Utils import *
import cv2
import time
import serial
from collections import deque

# Konfigurasi
PORT = "COM9"
CAM_ID = 1
FRAME_SIZE = (1280, 720)
BASE_SPEED = 40
MAX_SPEED = 40
MIN_PWM = 0
MARKER_LOST_TIMEOUT = 2

# Inisialisasi Serial
try:
    ser = serial.Serial(PORT, 9600, timeout=1)
    print(f"Tersambung ke {PORT}")
except Exception as e:
    ser = None
    print(f"Gagal membuka port {PORT}: {e}")
    # exit()

# Inisialisasi Kamera
cap = cv2.VideoCapture(CAM_ID, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_SIZE[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_SIZE[1])

# Inisialisasi Aruco Marker
detector_params = aruco.DetectorParameters()
detector_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
detector = aruco.ArucoDetector(detector_dict, detector_params)

# Inisialisasi Variabel
path = None
pid = PID(Kp=0.5, Ki=0.1, Kd=0.13, dt=0.1, output_limit=MAX_SPEED, integral_limit=MAX_SPEED)
degree_buffer = deque(maxlen=3)
last_time = marker_lost_time = time.time()

# Loop Utama
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Ubah frame ke grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Cari titik start (robot) dan goal
    start, goal, marksize = Pos(gray, detector)

    # Tangani kehilangan marker
    if start is None or goal is None:
        if time.time() - marker_lost_time >= MARKER_LOST_TIMEOUT:
            path = None
        cv2.imshow("Frame", gray)
        if cv2.waitKey(1) & 0xFF == 27:
            if ser: pwm(ser, 0, 0)
            break
        continue
    marker_lost_time = time.time()

    # Jika path, robot dan tujuan tersedia
    if path and start and goal:
        target = tuple(path[0])
        errDist, errDegree = Error(gray, start, target)

        # Jika hanya 1 titik path tersisa dan sudah dekat → hapus path
        if len(path) == 1 and errDist < 3 * marksize:
            pid.reset()
            path = None

        # Jika belum sampai titik saat ini → navigasi
        elif errDist < 2 * marksize:
            pid.reset()
            path.pop(0)

        else:
            # Navigasi PID
            degree_buffer.append(errDegree)
            avg_degree = sum(degree_buffer) / len(degree_buffer)

            current_time = time.time()
            pid.dt = current_time - last_time
            last_time = current_time

            correction = pid.calc(avg_degree)
            left = max(MIN_PWM, min(MAX_SPEED, int(BASE_SPEED + correction + 5)))
            right = max(MIN_PWM, min(MAX_SPEED, int(BASE_SPEED - correction)))
            if ser: pwm(ser, left, right)

            # Gambar path
            for i in range(len(path) - 1):
                p1, p2 = path[i], path[i + 1]
                cv2.line(gray, p1, p2, 255, 2)
                cv2.circle(gray, p1, 4, 255, -1)
                cv2.putText(gray, str(p1), (p1[0] + 10, p1[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1)

            # Tampilkan info
            cv2.putText(gray, f"Dist   : {int(errDist)}", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, 255, 2)
            cv2.putText(gray, f"Degree : {int(avg_degree)}", (10, 100), cv2.FONT_HERSHEY_COMPLEX, 1, 255, 2)
            cv2.putText(gray, f"Left Speed  : {left}", (10, 150), cv2.FONT_HERSHEY_COMPLEX, 1, 255, 2)
            cv2.putText(gray, f"Right Speed : {right}", (10, 200), cv2.FONT_HERSHEY_COMPLEX, 1, 255, 2)

        # Tampilkan frame
        cv2.imshow("Frame", gray)
        if cv2.waitKey(1) & 0xFF == 27:
            if ser: pwm(ser, 0, 0)
            break
        continue

    # Jika tidak ada path dan robot terlihat
    elif start and goal:
        # Jarak ke goal untuk menentukan perlu hitung path atau tidak
        errDist, _ = Error(gray, start, goal)

        if errDist < 3 * marksize:
            # Cukup tampilkan frame, jangan hitung path baru
            cv2.imshow("Frame", gray)
            if cv2.waitKey(1) & 0xFF == 27:
                if ser: pwm(ser, 0, 0)
                break
            continue

        # Reset PWM dulu
        if ser: pwm(ser, 0, 0)

        # Hitung path baru
        map = Prep(gray.copy(), start, goal, markSize=marksize)
        pStart, pGoal = PrepCoord(start, goal)
        (path, _), *_ = JPS_Optimize.methodBds(map, pStart, pGoal, 2, BRC=True, GLF=True, PPO=True)

        if path:
            pStart, pGoal, path = PrepCoord(pStart, pGoal, path)
            path.pop(0)

        # Tampilkan frame
        cv2.imshow("Frame", gray)
        if cv2.waitKey(1) & 0xFF == 27:
            if ser: pwm(ser, 0, 0)
            break
        continue

    # Default tampilkan frame saja
    cv2.imshow("Frame", gray)
    if cv2.waitKey(1) & 0xFF == 27:
        if ser: pwm(ser, 0, 0)
        break

# Bersihkan
cap.release()
cv2.destroyAllWindows()
