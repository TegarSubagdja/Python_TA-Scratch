from Utils import *

running = True

# Array untuk path
path = []

# Setup kamera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while running:
    ret, frame = cap.read()
    if not ret:
        break

    # Rubah frama kedalam bentuk grayscale
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Cari posisi robot
    start, goal, marksize = Pos(img)

    # Cari lintasan jika belum ada
    if (
        not path 
        and start
        and goal
        and errDist > (2 * marksize)
        ): 

        # Flip koordinat dari (x, y) -> (y, x)
        start = np.flip(start[0])
        goal = np.flip(goal[0])

        path, times = jps.method(map, start, goal, 2)
        print(f"Path ditemukan dengan waktu : ", times)

    if path:
        
        # Preprocessing
        map = Prep(img, start, goal)
        
        # Cari error ke posisi goal
        errDist, errDegree = Error(start, goal)

        # Cari error ke posisi pertama path
        goal = np.flip(path[0])
        errDist, errDegree = Error(start, goal)
        
        # Keluarkan path jika telah dikunjungi
        if errDist <= (2 * marksize):
            path.pop(0)

        for i in range(len(path) - 1):
            start = path[i][::-1]
            goal = path[i+1][::-1]
            cv2.line(img, start, goal, 255, 2)

    # Tampilkan frame
    cv2.imshow("Frame", img)
    if cv2.waitKey(1) & 0xFF == 27:
        running = False

cap.release()
cv2.destroyAllWindows()