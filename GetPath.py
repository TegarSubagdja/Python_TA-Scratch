from Utils import *

def getPath(image, scale=20, idStart=1, idGoal=7):

    cv2.imwrite('2-Position.jpg', image)
    posa, corners = Position(image, idStart, idGoal)

    if not posa:
        return 0, 0

    cv2.imwrite('3-Preprocessing.jpg', image)
    map, pos, mark_size = Preprocessing(image, posa, scale, corners)

    cv2.imwrite('8-Map.jpg', map)

    (path, time)= jps.method(map, pos['start'], pos['goal'], 2)

    if not path:
        return 0, 0

    path = [(y * scale, x * scale) for y, x in path]
    path[0] = posa['start'][::-1]
    path[-1] = posa['goal'][::-1]

    image = cv2.imread('Output/Overlay.jpg')

    for i in range(len(path) - 1):
        (y1, x1) = tuple(path[i])       
        (y2, x2) = tuple(path[i + 1])   
        cv2.line(image, (x1, y1), (x2, y2), (255, 64, 64), 4)

    for (y,x) in path:
        cv2.circle(image, (x,y), 8, (255,0,255), -1)

    return path, mark_size


# # cap = cv2.VideoCapture(2)

# # ret, frame = cap.read()

# frame = cv2.imread("Image/1.jpg")

# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# path, bo = getPath(frame, 10, 1, 7)