import cv2
import cv2.aruco as aruco
import numpy as np

def normalize_angle(angle):
    """Normalisasi sudut ke rentang [-pi, pi]."""
    return (angle + np.pi) % (2 * np.pi) - np.pi

# --- Baca gambar ---
image_path = "Image/1.jpg"  # Ganti sesuai path gambar
image = cv2.imread(image_path)

if image is None:
    print("Gagal membaca gambar.")
    exit()

# --- ArUco setup ---
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

# --- Deteksi Marker ---
corners, ids, _ = detector.detectMarkers(image)

koordinat = {'start': None, 'goal': None}
orientasi_robot = None

if ids is not None:
    aruco.drawDetectedMarkers(image, corners, ids)
    print("Marker terdeteksi dengan ID:", ids.flatten())

    for i, marker_id in enumerate(ids.flatten()):
        marker_corners = corners[i][0]
        center_x = int(np.mean(marker_corners[:, 0]))
        center_y = int(np.mean(marker_corners[:, 1]))
        cv2.circle(image, (center_x, center_y), 5, (0, 255, 255), -1)

        if marker_id == 1:
            koordinat['start'] = (center_x, center_y)
            vector = marker_corners[1] - marker_corners[0]
            orientasi_robot = np.arctan2(vector[1], vector[0])
            print(f"Start (ID 1) center: ({center_x}, {center_y})")
            print(f"Orientasi robot (radian): {orientasi_robot:.3f}")

        elif marker_id == 7:
            koordinat['goal'] = (center_x, center_y)
            print(f"Goal (ID 7) center: ({center_x}, {center_y})")

else:
    print("Tidak ada marker terdeteksi.")

# --- Perhitungan Error dan Visualisasi ---
if koordinat['start'] and koordinat['goal'] and orientasi_robot is not None:
    start = koordinat['start']
    goal = koordinat['goal']

    # Garis dari start ke goal
    cv2.line(image, start, goal, (0, 0, 255), 2)

    # Arah orientasi robot
    panjang_panah = 100
    orientasi_x = int(start[0] + panjang_panah * np.cos(orientasi_robot))
    orientasi_y = int(start[1] + panjang_panah * np.sin(orientasi_robot))
    cv2.arrowedLine(image, start, (orientasi_x, orientasi_y), (255, 0, 0), 2, tipLength=0.2)

    # Hitung error orientasi
    dx = goal[0] - start[0]
    dy = goal[1] - start[1]
    arah_ke_goal = np.arctan2(dy, dx)
    error_orientasi = normalize_angle(arah_ke_goal - orientasi_robot)

    print(f"Arah ke goal (radian): {arah_ke_goal:.3f}")
    print(f"Error orientasi (radian): {error_orientasi:.3f}")
    print(f"Error orientasi (derajat): {np.degrees(error_orientasi):.2f}°")

    # Tampilkan teks error di gambar
    teks_error = f"Error: {np.degrees(error_orientasi):.2f} deg"
    cv2.putText(image, teks_error, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

else:
    print("Tidak cukup marker untuk menghitung error orientasi.")

# --- Tampilkan dan Simpan Hasil ---
cv2.imshow("Hasil Deteksi dan Orientasi", image)
cv2.imwrite("output_orientasi.jpg", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
