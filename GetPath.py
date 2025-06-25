from Utils import *

def getPath(image, scale=20, idStart=1, idGoal=7):

    posa, corners = Position(image, idStart, idGoal)

    if not posa:
        return 0

    map, pos = Preprocessing(image, posa, scale, corners)

    path, time = jps.method(map, pos['start'], pos['goal'], 2)
    print(f"Path dihasilkan : {path}")

    path = prunning(path, map)
    print("Path Asli : ", path)
    print("Path Hasil Prunning : ", path)

    path = [(y * scale, x * scale) for y, x in path]
    path[0] = posa['start'][::-1]
    path[-1] = posa['goal'][::-1]
    print("Path Hasil Scale : ", path)

    image = cv2.imread('Output/Overlay.jpg')

    for i in range(len(path) - 1):
        (y1, x1) = tuple(path[i])       
        (y2, x2) = tuple(path[i + 1])   
        cv2.line(image, (x1, y1), (x2, y2), (255, 64, 64), 4)

    for (y,x) in path:
        cv2.circle(image, (x,y), 8, (255,0,255), -1)

    cv2.imwrite('Output/Output.jpg', image)

    return path

# # cam = cv2.imread('Output/image.jpg', 0)
# cam = cv2.imread('Output/normal.jpg', 0)

# path = getPath(cam, 5, 0, 7)
# sys.exit()
