from Utils import *

def getPath(image, scale=20, idStart=1, idGoal=7, camera_matrix=None, dist_coeffs=None):

    posa, rvec, tvec = Position(image, idStart, idGoal, 0.05, camera_matrix, dist_coeffs)

    if not posa:
        return 0

    map, pos = Preprocessing(image, posa, scale)

    cv2.imwrite('Output.jpg', map)

    path, time = jps.method(map, pos['start'], pos['goal'], 2)
    print(f"Path dihasilkan : {path}")

    path = prunning(path, map)
    print("Path Asli : ", path)
    print("Path Hasil Prunning : ", path)

    path = [(y * scale, x * scale) for y, x in path]
    path[0] = posa['start'][::-1]
    path[-1] = posa['goal'][::-1]
    print("Path Hasil Scale : ", path)

    return path, rvec, tvec

camera_matrix = np.array([
    [800, 0, 320],
    [0, 800, 240],
    [0,   0,   1]
], dtype=np.float32)
dist_coeffs = np.zeros((5, 1))

cam = cv2.imread('Image/1.jpg', 0)
path, rvec, tvec = getPath(cam, 40, 1, 7, camera_matrix, dist_coeffs)
path3d = to3D(path, rvec, tvec, camera_matrix, dist_coeffs, 0)
print(path3d)
sys.exit()
