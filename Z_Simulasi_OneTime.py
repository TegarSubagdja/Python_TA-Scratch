from Utils import *

scale = 20
realScale = scale/100

frame = cv2.imread('Image/2.jpg')
img = cv2.resize(frame, (0,0), fx=realScale, fy=realScale)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

start, goal, marksize = Pos(img)

if start and goal:
    None
else:
    sys.exit()

map = Prep(img, start, goal, marksize)
errDist, errDegree = Error(img, start, goal)

s = np.flip(start[0])
g = np.flip(goal[0])

(path, times), *_ = JPS_Optimize.methodBds(map, s, g, 2, BRC=True, PPO=True)

if path:
    None
else:
    sys.exit()

path = [(int(x // realScale), int(y // realScale)) for x, y in path]

if path:
    for i in range(len(path) - 1):
        start = path[i][::-1]
        goal = path[i+1][::-1]
        cv2.line(frame, start, goal, (255, 64, 255), 20, 2)
        cv2.circle(frame, goal, 30, (255, 64, 255), -1)

cv2.imwrite('BenerGa.jpg', frame)