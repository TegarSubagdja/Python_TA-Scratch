from Utils import *

def getPath(image, scale=20, pos=False, corners=False):

    print(pos)
    if not pos:
        return 0, 0

    map, pos = Preprocessing(image, pos, scale, corners)

    cv2.imwrite("Data/Image/map_biner.jpg", map)

    (path, time) = jps.method(map, pos[0], pos[1], 2)

    if not path:
        return 0, 0
    
    # Mengubah setiap koordinat ke ukuran semula
    path = [(y * scale, x * scale) for y, x in path]

    return path