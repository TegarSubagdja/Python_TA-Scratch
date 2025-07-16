from Utils import *

def Prep(img, start, goal, markSize):
    # Step 1: Grayscale
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 2: Thresholding
    _, binary = cv2.threshold(img, 52, 255, cv2.THRESH_BINARY_INV)

    # Step 3: Distance Transform
    dist = cv2.distanceTransform(255 - binary, cv2.DIST_L2, 5)
    buffer_radius = int(markSize)
    buffered_obstacle = np.uint8(dist < buffer_radius) * 255

    # Step 4: Tambahkan buffer ke binary → hasil baru
    binary_with_buffer = cv2.bitwise_or(binary, buffered_obstacle)

    # Step 5: Timpa robot dengan warna hitam
    if start is not None and goal is not None:
        cv2.circle(binary_with_buffer, goal[0], int(2*markSize), 0, -1)
        cv2.circle(binary_with_buffer, start[0], int(2*markSize), 0, -1)

    _, resize = cv2.threshold(binary_with_buffer, 52, 255, cv2.THRESH_BINARY)

    resize = cv2.resize(binary_with_buffer, (0,0), fx=0.2, fy=0.2)

    return resize 

def PrepCoord(start, goal, path=None):
    if path is None:
        # Hanya ubah start dan goal (misal kalikan 5)
        x, y = start[0]
        pStart = (y // 5, x // 5)
        x, y = goal[0]
        pGoal = (y // 5, x // 5)
        return pStart, pGoal
    else:
        # Ubah start, goal, dan path (misal dibagi 5)
        x, y = start
        pStart = (y * 5, x * 5)
        x, y = goal
        pGoal = (y * 5, x * 5)
        newPath = [(y * 5, x * 5) for (x, y) in path]
        return pStart, pGoal, newPath
