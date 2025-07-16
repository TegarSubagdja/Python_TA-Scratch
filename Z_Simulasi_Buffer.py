from Utils import *

def nothing(x):
    pass

# Buat jendela dan trackbar
cv2.namedWindow("Preview Gabungan")
cv2.createTrackbar("Threshold", "Preview Gabungan", 60, 255, nothing)
cv2.createTrackbar("Buffer Radius", "Preview Gabungan", 20, 100, nothing)
cv2.createTrackbar("Kernel Size", "Preview Gabungan", 16, 50, nothing)

# Kamera
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Ambil nilai dari trackbar
    thresh_val = cv2.getTrackbarPos("Threshold", "Preview Gabungan")
    buffer_radius = cv2.getTrackbarPos("Buffer Radius", "Preview Gabungan")
    kernel_size = cv2.getTrackbarPos("Kernel Size", "Preview Gabungan")
    kernel_size = max(1, kernel_size | 1)  # Pastikan ganjil

    # Step 1: Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Step 2: Thresholding
    _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)

    start, goal, marksize = Pos(frame)

    if not start and not goal:
        continue

    # Step 3: Distance Transform
    dist = cv2.distanceTransform(255 - binary, cv2.DIST_L2, 5)
    buffered_obstacle = np.uint8(dist < int(marksize)) * 255

    # Step 4: Tambahkan buffer ke binary → hasil baru
    binary_with_buffer = cv2.bitwise_or(binary, buffered_obstacle)

    # Step 5: Timpa robot dengan warna hitam
    cv2.circle(binary_with_buffer, start[0], int(2*marksize), (0), -1)
    cv2.circle(binary_with_buffer, goal[0], int(2*marksize), (0), -1)

    _, resize = cv2.threshold(binary_with_buffer, thresh_val, 255, cv2.THRESH_BINARY)

    resize = cv2.resize(binary_with_buffer, (0,0), fx=0.2, fy=0.2)

    x, y = start[0]
    start = (y // 5, x // 5)
    x, y = goal[0]
    goal = (y // 5, x // 5)

    (path, times), *_ = JPS_Optimize.method(resize, start, goal, 2, PPO=True)

    cv2.putText(frame, f"Robot", (start), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1, cv2.LINE_AA)
    cv2.putText(frame, f"Goal", (goal), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1, cv2.LINE_AA)
    
    if path:
        x, y = path[0]
        start = (y * 5, x * 5)
        x, y = path[-1]
        goal = (y * 5, x * 5)
        path = tuple((y * 5, x * 5) for (x, y) in path)
        for i in range(len(path)-1):
            cv2.line(frame, path[i], path[i+1], (255,128,255), 3)

    # Step 5: Overlay visualisasi
    overlay = frame.copy()
    overlay[buffered_obstacle == 255] = [0, 0, 255]  # Buffer area → merah
    visual = cv2.addWeighted(frame, 1.0, overlay, 0.5, 0)

    # Konversi ke 3 channel agar bisa ditampilkan berdampingan
    gray_3ch    = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    binary_3ch  = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    withbuf_3ch = cv2.cvtColor(binary_with_buffer, cv2.COLOR_GRAY2BGR)

# Gabungkan semua dalam dua baris
    row1 = np.hstack((visual, binary_3ch))
    row2 = np.hstack((withbuf_3ch, gray_3ch))
    combined = np.vstack((row1, row2))

    # Tampilkan hasil gabungan
    cv2.imshow("Preview Gabungan", combined)

    # Keluar jika ESC ditekan
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
