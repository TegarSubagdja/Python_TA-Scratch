#Tuning Image Preprocessing 
https://github.com/TegarSubagdja/Python_Cleaning-Image-Threshold-Morphology.git

#Gambar Ke Plot
# --- Plot semua tahap menggunakan matplotlib ---
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle("Tahapan Pengolahan Citra & Jalur", fontsize=16)

# Helper untuk menampilkan citra BGR → RGB
def show(ax, img, title):
    if len(img.shape) == 2:
        ax.imshow(img, cmap='gray')
    else:
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax.set_title(title)
    ax.axis('off')

show(axes[0, 0], output_image, "Input Image + Posisi")
show(axes[0, 1], gray, "Grayscale")
show(axes[0, 2], map, "Threshold (Map)")
show(axes[1, 0], closing, "Morph Closing")
show(axes[1, 1], opening, "Morph Opening")
show(axes[1, 2], result, "Jalur Hasil Akhir")

plt.tight_layout()
plt.subplots_adjust(top=0.90)
plt.show()

## Deteksi Aruco Market dan Axis
import cv2
import numpy as np

# Inisialisasi kamera
cap = cv2.VideoCapture(1)  # Ganti 0 jika kamera lain digunakan

# Ambil resolusi untuk dummy intrinsic
ret, frame = cap.read()
if not ret:
    print("Gagal membaca dari kamera")
    cap.release()
    exit()

h, w = frame.shape[:2]

# Dummy intrinsics (asumsi)
fx = fy = 1000.0
cx = w / 2.0
cy = h / 2.0
camera_matrix = np.array([[fx, 0, cx],
                          [0, fy, cy],
                          [0,  0,  1]], dtype=np.float32)
dist_coeffs = np.zeros((5, 1), dtype=np.float32)

# ArUco setup
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# Panjang marker (meter) – harus sesuai ukuran nyata marker di dunia
marker_length = 0.04  # 4 cm

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, marker_length, camera_matrix, dist_coeffs)

        for rvec, tvec in zip(rvecs, tvecs):
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, marker_length * 0.5)

    cv2.imshow("Deteksi ArUco tanpa Kalibrasi", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
