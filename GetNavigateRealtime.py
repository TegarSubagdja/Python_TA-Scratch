from Utils import *
import cv2

cap = cv2.VideoCapture(1)
target_point = (100, 100)

if not cap.isOpened():
    print("Tidak dapat membuka webcam.")
    exit()

pid = PID(Kp=20, Ki=1, Kd=10, dt=0.1, output_limit=255, integral_limit=200)
base_speed = 250

while True:
    ret, cam = cap.read()
    if not ret:
        print("Gagal membaca frame dari webcam.")
        break


    # Proses deteksi tetap pada frame asli
    result = GetOrientation(cam, id=9, target_point=target_point, show_result=False)

    if result and result['error_orientasi_derajat'] is not None:
        correction = pid.calc(result['error_orientasi_derajat'])
        left_speed = max(0, min(255, int(base_speed - correction)))
        right_speed = max(0, min(255, int(base_speed + correction)))
        frame = cv2.flip(result['image'], 1)
        center = result['koordinat']
        error = f"{int(result['error_orientasi_derajat'])}"
        distance = f"{int(result['distance'])}"
        cv2.circle(frame, target_point, 10, (255, 128, 255), -1)
        cv2.putText(frame, error, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(frame, distance, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(frame, f"{left_speed}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(frame, f"{right_speed}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.imshow('Realtime ArUco Tracking True', frame)
    else:
        cam = cv2.flip(cam, 1)
        cv2.imshow('Realtime ArUco Tracking True', cam)

    # Tekan tombol ESC (27) untuk keluar
    if cv2.waitKey(1) & 0xFF == 27:
        print("Tombol ESC ditekan, keluar dari program.")
        break

cap.release()
cv2.destroyAllWindows()
