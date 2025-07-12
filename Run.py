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
        errDist, errDegree = Error(start, goal)

        if errDist < (2 * marksize):
            break

        map = Prep(img, start, goal)

        s = tuple(start[0].tolist())
        g = tuple(goal[0].tolist())

        (path, times), *_ = JPS_Optimize.method(map, s, g, 2)
        print(path)
        
    elif (
        start and goal
    ): 
        # Cari error ke posisi goal
        p = tuple(path[0][::-1])

        errDist, errDegree = Error(start, p)

    # Tampilkan frame
    cv2.imshow("Frame", img)
    if cv2.waitKey(1) & 0xFF == 27:
        running = False

cap.release()
cv2.destroyAllWindows()