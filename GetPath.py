from Utils import *

def getPath(image, scale=20, pos=False, corners=False):

    if not pos:
        return 0, 0

    map, pos = Preprocessing(image, pos, scale, corners)

    cv2.imwrite("cam.jpg", map)
    print(map.shape)
    print(pos)

    (path, time), *_ = astar_full.method(map, pos[0], pos[1], 2)

    if not path:
        return 0, 0

    # Mengubah setiap koordinat ke ukuran semula
    path = [(y * scale, x * scale) for y, x in path]

    path[0] = np.flip(pos[0])
    path[-1] = np.flip(pos[1])

    return path