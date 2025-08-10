from Utils import *
import cv2
import numpy as np
from cv2 import aruco

def nothing(x):
    pass

# Inisialisasi Aruco Marker
detector_params = aruco.DetectorParameters()
detector_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
detector = aruco.ArucoDetector(detector_dict, detector_params)

# Baca satu gambar statis
frame_original = cv2.imread("Map/Foto/WIN_20250806_03_22_35_Pro.jpg")
frame = frame_original.copy()

# Trackbar
cv2.namedWindow("Preview Gabungan")
cv2.createTrackbar("Threshold", "Preview Gabungan", 60, 255, nothing)
cv2.createTrackbar("Buffer Radius", "Preview Gabungan", 20, 100, nothing)
cv2.createTrackbar("Kernel Size", "Preview Gabungan", 16, 50, nothing)

# Simpan nilai sebelumnya
prev_thresh_val = -1
prev_buffer_radius = -1
prev_kernel_size = -1
prev_start = None
prev_goal = None

while True:
    # Ambil nilai trackbar
    thresh_val = cv2.getTrackbarPos("Threshold", "Preview Gabungan")
    buffer_radius = cv2.getTrackbarPos("Buffer Radius", "Preview Gabungan")
    kernel_size = cv2.getTrackbarPos("Kernel Size", "Preview Gabungan")
    kernel_size = max(1, kernel_size | 1)

    # Deteksi ArUco (bisa berubah saat lighting berubah)
    start, goal, marksize = Pos(frame, detector)

    # Cek jika parameter berubah
    parameter_changed = (
        thresh_val != prev_thresh_val or
        buffer_radius != prev_buffer_radius or
        kernel_size != prev_kernel_size or
        start != prev_start or
        goal != prev_goal
    )

    if not parameter_changed:
        key = cv2.waitKey(50)
        if key == 27:
            break
        continue

    # Update parameter sebelumnya
    prev_thresh_val = thresh_val
    prev_buffer_radius = buffer_radius
    prev_kernel_size = kernel_size
    prev_start = start
    prev_goal = goal

    if start is None or goal is None or start[0] is None or goal[0] is None:
        continue

    # Step 1: Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Step 2: Thresholding + Erosion
    _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    binary = cv2.erode(binary, kernel, iterations=3)

    # Step 3: Distance Transform → Buffer
    dist = cv2.distanceTransform(255 - binary, cv2.DIST_L2, 5)
    buffered_obstacle = np.uint8(dist < int(buffer_radius)) * 255
    binary_with_buffer = cv2.bitwise_or(binary, buffered_obstacle)

    # Step 4: Timpa posisi robot dan goal
    cv2.circle(binary_with_buffer, start[0], int(2 * marksize), 0, -1)
    cv2.circle(binary_with_buffer, goal[0], int(2 * marksize), 0, -1)

    # Resize untuk A*
    resize = cv2.resize(binary_with_buffer, (0, 0), fx=0.05, fy=0.05)

    # Konversi koordinat untuk A*
    x, y = start[0]
    start_grid = (y // 20, x // 20)
    x, y = goal[0]
    goal_grid = (y // 20, x // 20)

    try:
        (path, times), *_ = Astar_Optimize.methodBds(
            resize, start_grid, goal_grid, 2, PPO=True, BRC=True
        )
    except:
        path = []

    # Step 5: Overlay visualisasi buffer
    overlay = frame.copy()
    overlay[buffered_obstacle == 255] = [0, 0, 255]  # merah
    visual = cv2.addWeighted(frame, 1.0, overlay, 0.5, 0)

    # Tampilkan teks lokasi robot dan goal
    cv2.putText(visual, "Robot", start[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
    cv2.putText(visual, "Goal", goal[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)

    # Tampilkan jalur (opsional)
    if path:
        path_scaled = [(y * 20, x * 20) for (x, y) in path]
        for i in range(len(path_scaled) - 1):
            cv2.line(visual, path_scaled[i], path_scaled[i + 1], (255, 128, 255), 2)

    # Gabungkan tampilan
    gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    binary_3ch = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    withbuf_3ch = cv2.cvtColor(binary_with_buffer, cv2.COLOR_GRAY2BGR)

    row1 = np.hstack((visual, binary_3ch))
    row2 = np.hstack((withbuf_3ch, gray_3ch))
    combined = cv2.resize(np.vstack((row1, row2)), (1280, 720))

    cv2.imshow("Preview Gabungan", combined)

    key = cv2.waitKey(50)
    if key == 27:
        break
    elif key == ord('s'):
        cv2.imwrite('HasilBuffer.jpg', visual)
        print("Hasil disimpan.")

cv2.destroyAllWindows()
