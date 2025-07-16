from Utils import *

running = True

# Array untuk path
path = None

# Setup kamera
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

current = time.time()

while running:
    ret, frame = cap.read()
    if not ret:
        break

    # Rubah frama kedalam bentuk grayscale
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Cari posisi robot
    start, goal, marksize = Pos(img)

    if (not start and not goal):
        path = None

    if time.time() - current > 5:
        path = None
        current = time.time()

    if (not path and start and goal):

        # Cari error ke posisi goal
        errDist, errDegree = Error(img.copy(), start, goal)

        if errDist < (5 * marksize):
            cv2.imshow("Frame", img)
            if cv2.waitKey(1) & 0xFF == 27:
                running = False
                continue

        map = Prep(img.copy(), start, goal, markSize=marksize)
        cv2.imwrite('Hasil Prep.jpg', map)

        # cv2.imwrite('cek.jpg', map)

        pStart, pGoal = PrepCoord(start, goal)
        print(pStart, pGoal)

        (path, times), *_ = JPS_Optimize.methodBds(map, pStart, pGoal, 2)
        print(path, times)

        if path:
            pStart, pGoal, path = PrepCoord(pStart, pGoal, path)
            print(path)
            path.pop(0)

    elif (start and goal): 

        # Cari error ke posisi goal
        target = tuple(path[0])

        errDist, errDegree = Error(img, start, target)

        # Menampilkan errDegree di pojok kiri atas
        cv2.putText(img, f"Error Degree: {errDist:.2f}°", (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1, cv2.LINE_AA)
        
        # Gambar seluruh path dan beri teks nomor
        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i + 1]
            cv2.line(img, p1, p2, (255,128,255), 2)

            # Tambahkan teks koordinat path di titik p1
            cv2.circle(img, p1, 4, 255, -1)
            cv2.putText(img, str(p1), (p1[0] + 10, p1[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1, cv2.LINE_AA)
            cv2.putText(img, f"Robot", (start[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1, cv2.LINE_AA)

        # Tampilkan semua koordinat path di bagian bawah layar
        path_str = "Path: " + str(list(path))
        cv2.putText(img, path_str[:1200], (10, img.shape[0] - 10),
                    cv2.FONT_HERSHEY_PLAIN, 1, 200, 1, cv2.LINE_AA)

        # Jika jarak robot ke tujuan sudah dekat, keluarkan titik tujuan
        if errDist < (marksize):
            path.pop(0)

    cv2.imshow("Frame", img)
    if cv2.waitKey(1) & 0xFF == 27:
        running = False

cap.release()
cv2.destroyAllWindows()