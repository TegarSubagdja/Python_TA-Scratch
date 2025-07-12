from Utils import *

img = cv2.imread('Image/4.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

start, goal, marksize = Pos(img)
map = Prep(img, start, goal)

start = np.flip(start[0])
goal = np.flip(goal[0])

# path, times = jps.method(map, start, goal, 2)

# print(times)

# if path:
#     for i in range(len(path) - 1):
#         start = path[i][::-1]
#         goal = path[i+1][::-1]
#         cv2.line(img, start, goal, 255, 2)

# img = cv2.resize(img, (0, 0), fx=0.1, fy=0.1)

cv2.imwrite('BenerGa.jpg', img)