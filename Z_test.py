from Utils import *

cap = cv2.VideoCapture(2)
target_point = (100, 100)

if not cap.isOpened():
    print("Tidak dapat membuka webcam.")
    exit()

while True:
    ret, image = cap.read()
    if not ret:
        print("Gagal membaca frame dari webcam.")
        break

    # Proses deteksi tetap pada frame asli
    result = GetOrientation(image, id=0, target_point=target_point, show_result=False)

    print(result)

    if result and result['error_orientasi_derajat'] is not None:
        frame = result['image']
        center = result['koordinat']
        flipped_frame = cv2.flip(frame, 1)
        cv2.circle(flipped_frame, target_point, 10, (255, 128, 255), -1)
        error = f"{int(result['error_orientasi_derajat'])}"
        distance = f"{int(result['distance'])}"
        cv2.putText(flipped_frame, error, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(flipped_frame, distance, (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.imshow('Realtime ArUco Tracking', flipped_frame)
    else:
        flipped_frame = cv2.flip(image, 1)
        cv2.imshow('Realtime ArUco Tracking', flipped_frame)

    # Tekan tombol ESC (27) untuk keluar
    if cv2.waitKey(1) & 0xFF == 27:
        print("Tombol ESC ditekan, keluar dari program.")
        break

cap.release()
cv2.destroyAllWindows()
