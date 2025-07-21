from Utils import *

scale=20

def Prep(img, start, goal, markSize):
    # Step 1: Grayscale
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 2: Thresholding
    _, binary = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((9,9), np.uint8)
    binary = cv2.erode(binary, kernel=kernel, iterations=3)

    # Step 3: Distance Transform
    dist = cv2.distanceTransform(255 - binary, cv2.DIST_L2, 5)
    buffer_radius = int(3 * markSize)
    buffered_obstacle = np.uint8(dist < buffer_radius) * 255

    # Step 4: Tambahkan buffer ke binary → hasil baru
    binary_with_buffer = cv2.bitwise_or(binary, buffered_obstacle)

    # Step 5: Timpa robot dengan warna hitam
    if start is not None and goal is not None:
        cv2.circle(binary_with_buffer, goal[0], int(2*markSize), 0, -1)
        cv2.circle(binary_with_buffer, start[0], int(2*markSize), 0, -1)

    _, resize = cv2.threshold(binary_with_buffer, 100, 255, cv2.THRESH_BINARY)

    x, y = (1/scale), (1/scale)

    resize = cv2.resize(binary_with_buffer, (0,0), fx=x, fy=y)

    cv2.imwrite('Hasil Prep.jpg', resize)

    return resize

def PrepCoord(start, goal, path=None):

    if path is None:
        # Hanya ubah start dan goal (misal kalikan scale)
        x, y = start[0]
        pStart = (y // scale, x // scale)
        x, y = goal[0]
        pGoal = (y // scale, x // scale)
        return pStart, pGoal
    else:
        # Ubah start, goal, dan path (misal dibagi scale)
        x, y = path[0]
        pStart = (y * scale, x * scale)
        x, y = path[-1]
        pGoal = (y * scale, x * scale)
        newPath = [(y * scale, x * scale) for (x, y) in path]
        return pStart, pGoal, newPath
