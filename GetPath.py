from Utils import *

def getPath(image, scale=20, idStart=1, idGoal=7):

    posa = Position(image, idStart, idGoal)

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

    return path

# cam = cv2.imread('1.jpg', 0)
# path = getPath(cam, 1, 0, 1)
# print(path)
# sys.exit()
