from Utils import *

running = True

# Array untuk path
path = []

# Max distance to repath

while running:

    img = cv2.imread('Image/4.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Cari posisi robot
    start, goal, marksize = Pos(img)

    # Flip koordinat dari (x, y) -> (y, x)
    start = np.flip(start[0])
    goal = np.flip(goal[0])

    # Preprocessing
    map = Prep(img, start, goal)

    if path:
        # Cari error ke posisi pertama path
        goal = np.flip(path[0])
        errDist, errDegree = Error(start, goal)
    else:
        # Cari error ke posisi goal
        errDist, errDegree = Error(start, goal)

    # Cari lintasan jika belum ada
    if (
        not path 
        and start
        and goal
        and errDist > (2 * marksize)
        ): 
        path, times = jps.method(map, start, goal, 2)
        print(f"Path ditemukan dengan waktu : ", times)

    if path:
        # Keluarkan path jika telah dikunjungi
        if errDist <= (2 * marksize):
            path.pop(0)

        for i in range(len(path) - 1):
            start = path[i][::-1]
            goal = path[i+1][::-1]
            cv2.line(img, start, goal, 255, 2)

    cv2.imshow('BenerGa.jpg', img)