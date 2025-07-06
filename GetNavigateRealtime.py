from Utils import *
import cv2
import serial
from collections import deque

# Konfigurasi Serial
PORT = 'COM11 '
BAUDRATE = 9600
last_send_time = time.time()
send_interval = 0.1  # 100ms
current_time = None

# PID Controller
pid = PID(Kp=20, Ki=1, Kd=10, dt=0.1, output_limit=255, integral_limit=200)
base_speed = 255
error_buffer = deque(maxlen=10)

# Target Titik
target_point = (100, 100)

# Buka Webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("Tidak dapat membuka webcam.")
    exit()

# Buka Serial
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"Tersambung ke {PORT}")
except serial.SerialException as e:
    print(f"Gagal membuka port serial: {e}")
    exit()

# Loop Utama
try:
    while True:
        ret, cam = cap.read()
        if not ret:
            print("Gagal membaca frame dari webcam.")
            break

        result = GetOrientation(cam, sId=3, gId=9, show_result=False)

        if result and result['error_orientasi_derajat'] is not None:
            error_buffer.append(result['error_orientasi_derajat'])
            smooth_error = sum(error_buffer) / len(error_buffer)
            correction = pid.calc(int(smooth_error))

            left_speed = max(0, min(255, int(base_speed - correction)))
            right_speed = max(0, min(255, int(base_speed + correction)))

            error = int(smooth_error)
            distance = int(result['distance'])

            finishDistance = 2 * result['size']
            current_time = time.time()
            if distance >= finishDistance and (current_time - last_send_time) >= send_interval:
                pwm(ser, left_speed, right_speed)
                last_send_time = current_time
                print(f"pwn dikirim {left_speed}, {right_speed}")
            elif distance < finishDistance:
                print("Sampai")
                pwm(ser, 0, 0)

            # Visualisasi
            cv2.circle(cam, target_point, 10, (255, 128, 255), -1)
            cv2.putText(cam, f"Error: {error}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            cv2.putText(cam, f"Distance: {distance}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            cv2.putText(cam, f"L: {left_speed} R: {right_speed}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        else:
            current_time = time.time()
            if (current_time - last_send_time) >= send_interval:
                pwm(ser, 0, 0)
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
ser.close()
cv2.destroyAllWindows()
