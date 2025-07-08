from Utils import *
import threading

# Konfigurasi Serial
PORT = 'COM7'
BAUDRATE = 9600
last_send_time = time.time()
send_interval = 1  # 100ms
current_time = None

# Setup Aruco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters) 

# PID Controller
pid = PID(Kp=20, Ki=1, Kd=10, dt=0.1, output_limit=255, integral_limit=200)
base_speed = 255
error_buffer = deque(maxlen=10)

# Target Titik
target_point = (100, 100)

# Buka Webcam
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("Tidak dapat membuka webcam.")
    exit()

# Buka Serial
# try:
#     ser = serial.Serial(PORT, BAUDRATE, timeout=1)
#     print(f"Tersambung ke {PORT}")
# except serial.SerialException as e:
#     print(f"Gagal membuka port serial: {e}")
#     exit()

# Loop Utama
try:
    while True:
        ret, cam = cap.read()
        if not ret:
            print("Gagal membaca frame dari webcam.")
            break

        result = GetOrientation(cam, sId=2, gId=7, show_result=False, save_path=None, detector=detector)

        if result and result['error_orientasi_derajat'] is not None:

            finishDistance = 2 * result['size']
            distance = int(result['distance'])
            current_time = time.time()

            if distance >= finishDistance and (current_time - last_send_time) >= send_interval:
                # pwm(ser, left_speed, right_speed)
                last_send_time = current_time
                print(f"pwn dikirim {left_speed}, {right_speed}")
            elif distance < finishDistance:
                print("Sampai")
                # threading.Thread(target=pwm, args=(ser, left_speed, right_speed)).start() # ganti dengan ini agar tidak saling tunggu
                # pwm(ser, 0, 0)

            error_buffer.append(result['error_orientasi_derajat'])
            smooth_error = sum(error_buffer) / len(error_buffer)
            correction = pid.calc(smooth_error)

            left_speed = max(0, min(255, base_speed - correction))
            right_speed = max(0, min(255, base_speed + correction))

            error = int(smooth_error)

            # Visualisasi
            cv2.circle(cam, target_point, 10, (255, 128, 255), -1)
            cv2.putText(cam, f"Error: {error}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            cv2.putText(cam, f"Distance: {distance}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            cv2.putText(cam, f"L: {left_speed} R: {right_speed}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        else:
            current_time = time.time()
            if (current_time - last_send_time) >= send_interval:
                # pwm(ser, 0, 0)
                print(f"pwn tidak dikirim")
                last_send_time = current_time

        cv2.imshow('Tracking', cam)

        if cv2.waitKey(1) & 0xFF == 27:
            print("Tombol ESC ditekan, keluar dari program.")
            break

except KeyboardInterrupt:
    print("\nDihentikan oleh user.")

# Cleanup
cap.release()
# ser.close()
cv2.destroyAllWindows()
