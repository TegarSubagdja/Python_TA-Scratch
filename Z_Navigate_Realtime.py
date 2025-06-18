from Utils import *

cap = cv2.VideoCapture(0)
target_point = (100, 100)

if not cap.isOpened():
    print("Tidak dapat membuka webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame dari webcam.")
        break

    # Proses deteksi tetap pada frame asli
    result = GetOrientation(frame, id=0, target_point=target_point, show_result=False)

    print(result)

    if result:
        frame = result['image']
        center = result['koordinat']
        flipped_frame = cv2.flip(frame, 1)
        frame = cv2.circle(frame, target_point, 10, (255,128,255), -1)
        error = f"{int(result['error_orientasi_derajat'])}"
        cv2.putText(frame, error, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 1)
        cv2.imshow('Realtime ArUco Tracking', flipped_frame)
    else:
        flipped_frame = cv2.flip(frame, 1)
        cv2.imshow('Realtime ArUco Tracking', flipped_frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
