from Utils import *
import cv2

cap = cv2.VideoCapture(2)
target_point = (100, 100)
path = None

if not cap.isOpened():
    print("Tidak dapat membuka webcam.")
    exit()

while True:
    ret, cam = cap.read()
    if not ret:
        print("Gagal membaca frame dari webcam.")
        break

    # Proses deteksi tetap pada frame asli
    result = GetOrientation(cam, id=0, target_point=target_point, show_result=False)

    if not path:
        path = getPath(cam, 10, 0, 1)

    if result and result['error_orientasi_derajat'] is not None:
        frame = result['image']
        center = result['koordinat']
        error = f"{int(result['error_orientasi_derajat'])}"
        distance = f"{int(result['distance'])}"
        cv2.circle(cam, target_point, 10, (255, 128, 255), -1)
        cv2.putText(cam, error, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(cam, distance, (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.imshow('Realtime ArUco Tracking', cam)
    else:
        cv2.imshow('Realtime ArUco Tracking', cam)

    # Tekan tombol ESC (27) untuk keluar
    if cv2.waitKey(1) & 0xFF == 27:
        print("Tombol ESC ditekan, keluar dari program.")
        break

cap.release()
cv2.destroyAllWindows()
