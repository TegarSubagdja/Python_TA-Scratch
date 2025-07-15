from Utils import *

running = True

# Array untuk path
path = []

# Setup kamera
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
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

    if (
        not path and
        start and
        goal
        ):
        # Cari error ke posisi goal
        errDist, errDegree = Error(img.copy(), start, goal)

        if errDist < (5 * marksize):
            break

        map = Prep(img.copy(), start, goal, markSize=marksize)

        s = start[0]
        g = goal[0]

        (path, times), *_ = JPS_Optimize.method(map, s, g, 2)
        print(f"ya")

    elif (
        start and goal
    ): 
        # Cari error ke posisi goal
        p = tuple(path[0])

        cv2.circle(img, p, 5, 255, -1)

        for i in range(len(path)-1):
            p1 = path[i]
            p2 = path[i+1]
            cv2.line(img, p1, p2, 255, 2)

        errDist, errDegree = Error(img.copy(), start, p)

        # print(f"Posisi path ke-0 : {p}")

        if errDist < (2 * marksize):
            print(f"len path : {len(path)}")
            path.pop(0)

        print(errDist)

    # Tampilkan frame
    cv2.imshow("Frame", img)
    if cv2.waitKey(1) & 0xFF == 27:
        running = False

cap.release()
cv2.destroyAllWindows()