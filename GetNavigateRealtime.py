from Utils import *
import threading
import time

# =================== Konfigurasi ===================
PORT = 'COM7'
BAUDRATE = 9600
SEND_INTERVAL = 1  # detik
last_send_time = time.time()

# ArUco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

# PID
pid = PID(Kp=20, Ki=1, Kd=10, dt=0.1, output_limit=255, integral_limit=200)
base_speed = 255
error_buffer = deque(maxlen=10)

# Target dan Path
target_point = (100, 100)
path = []

# Webcam
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Tidak dapat membuka webcam.")
    exit()

# Serial Opsional
# try:
#     ser = serial.Serial(PORT, BAUDRATE, timeout=1)
#     print(f"Tersambung ke {PORT}")
# except serial.SerialException as e:
#     print(f"Gagal membuka port serial: {e}")
#     exit()

# =================== Fungsi ===================
def render_info(frame, error, distance, left_speed, right_speed):
    cv2.circle(frame, target_point, 10, (255, 128, 255), -1)
    cv2.putText(frame, f"Error: {error}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.putText(frame, f"Distance: {distance}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.putText(frame, f"L: {left_speed} R: {right_speed}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

# =================== Loop Utama ===================
try:
    while True:
        ret, cam = cap.read()
        cam = cv2.cvtColor(cam, cv2.COLOR_BGR2GRAY)
        
        if not ret:
            print("Gagal membaca frame dari webcam.")
            break

        if not path:
            # Ambil jalur jika belum ada
            path = getPath(image=cam, scale=20, idStart=2, idGoal=7, detector=detector)
            path.pop(0)
            continue

        if path:
            points = np.array([[y, x] for x, y in path], np.int32)
            cv2.polylines(cam, [points], isClosed=False, color=(255, 0, 255), thickness=2)
            for x, y in path:
                cv2.circle(cam, (y, x), 3, (255, 0, 255), -1)

        # Ambil orientasi dari titik pertama di path
        result = GetOrientation(cam, sId=2, gId=path[0], show_result=False, detector=detector)

        if result and result['error_orientasi_derajat'] is not None:
            distance = int(result['distance'])
            finishDistance = 2 * result['size']
            current_time = time.time()

            if distance < finishDistance:
                print("Sampai. PWM dihentikan.")
                render_info(cam, 0, distance, 0, 0)
            else:
                # PID & Speed Control
                error_buffer.append(result['error_orientasi_derajat'])
                smooth_error = sum(error_buffer) / len(error_buffer)
                correction = pid.calc(smooth_error)

                left_speed = max(0, min(255, int(base_speed - correction)))
                right_speed = max(0, min(255, int(base_speed + correction)))

                if (current_time - last_send_time) >= SEND_INTERVAL:
                    # threading.Thread(target=pwm, args=(ser, left_speed, right_speed)).start()
                    print(f"PWM dikirim: L={left_speed}, R={right_speed}")
                    last_send_time = current_time

                render_info(cam, int(smooth_error), distance, left_speed, right_speed)

        else:
            # ArUco tidak terdeteksi
            current_time = time.time()
            if (current_time - last_send_time) >= SEND_INTERVAL:
                # threading.Thread(target=pwm, args=(ser, 0, 0)).start()
                print("Marker tidak terdeteksi. PWM dihentikan.")
                last_send_time = current_time
            render_info(cam, 0, 0, 0, 0)

        # Tampilkan frame
        cv2.imshow('Tracking', cam)
        if cv2.waitKey(1) & 0xFF == 27:
            print("Tombol ESC ditekan, keluar.")
            break

except KeyboardInterrupt:
    print("\nDihentikan oleh user.")

# =================== Cleanup ===================
cap.release()
# ser.close()
cv2.destroyAllWindows()
