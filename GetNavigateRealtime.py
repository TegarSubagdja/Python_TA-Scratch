from Utils import *
import cv2
from collections import deque

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

target_point = (100, 100)

if not cap.isOpened():
    print("Tidak dapat membuka webcam.")
    exit()

pid = PID(Kp=20, Ki=1, Kd=10, dt=0.1, output_limit=255, integral_limit=200)
base_speed = 250

error_buffer = deque(maxlen=10)

while True:
    ret, cam = cap.read()
    if not ret:
        print("Gagal membaca frame dari webcam.")
        break

    cam = cv2.resize(cam, (0,0), fx=0.5, fy=0.5)
    # Proses deteksi tetap pada frame asli
    result = GetOrientation(cam, sId=9, gId=3, show_result=False)

    if result and result['error_orientasi_derajat'] is not None:
        #Perhitungan PID
        error_buffer.append(result['error_orientasi_derajat'])
        smooth_error = sum(error_buffer) / len(error_buffer)
        correction = pid.calc(int(smooth_error))
        left_speed = max(0, min(255, int(base_speed - correction)))
        right_speed = max(0, min(255, int(base_speed + correction)))

        # cam = cv2.flip(result['image'], 1)
        center = result['koordinat']
        error = f"{int(result['error_orientasi_derajat'])}"
        distance = int(result['distance'])

        finishDistance = 2 * result['size']
        if distance >= finishDistance:
            print("Sampai")

        cv2.circle(cam, target_point, 10, (255, 128, 255), -1)
        cv2.putText(cam, error, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(cam, f"{distance}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(cam, f"{left_speed}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(cam, f"{right_speed}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.imshow('Realtime ArUco Tracking True', cam)
    else:
        # cam = cv2.flip(cam, 1)
        cv2.imshow('Realtime ArUco Tracking True', cam)

    # Tekan tombol ESC (27) untuk keluar
    if cv2.waitKey(1) & 0xFF == 27:
        print("Tombol ESC ditekan, keluar dari program.")
        break

cap.release()
cv2.destroyAllWindows()
