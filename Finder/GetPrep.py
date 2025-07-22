from Utils import *

scale=20

def Prep(img, start, goal, markSize):
    # Grayscale
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding
    _, binary = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((9,9), np.uint8)
    binary = cv2.erode(binary, kernel=kernel, iterations=3)

    # Distance Transform
    dist = cv2.distanceTransform(255 - binary, cv2.DIST_L2, 5)
    buffer_radius = int(3 * markSize)
    buffered_obstacle = np.uint8(dist < buffer_radius) * 255

    # Tambahkan buffer ke binary → hasil baru
    binary_with_buffer = cv2.bitwise_or(binary, buffered_obstacle)

    # Timpa robot dengan warna hitam
    if start is not None and goal is not None:
        cv2.circle(binary_with_buffer, goal[0], int(2*markSize), 0, -1)
        cv2.circle(binary_with_buffer, start[0], int(2*markSize), 0, -1)

    # Downsampling
    x, y = (1/scale), (1/scale)
    resize = cv2.resize(binary_with_buffer, (0,0), fx=x, fy=y)
    _, resize = cv2.threshold(resize, 100, 255, cv2.THRESH_BINARY)
    # cv2.imwrite('Hasil Prep.jpg', resize)

    return resize

def PrepCoord(start, goal, path=None):

    if path is None:
        # Ubah skala start dan goal ke ukuran kecil
        x, y = start[0]
        sStart = (y // scale, x // scale)
        x, y = goal[0]
        sGoal = (y // scale, x // scale)
        return sStart, sGoal
    else:
        # Ubah Skala start, goal, dan path  ke ukuran semula
        x, y = path[0]
        sStart = (y * scale, x * scale)
        x, y = path[-1]
        sGoal = (y * scale, x * scale)
        sPath = [(y * scale, x * scale) for (x, y) in path]
        return sStart, sGoal, sPath
