from Utils import *

scale = 0.3

image = cv2.imread('Image/7.jpg')
image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

orientation = GetOrientation(image, (1000, 250), 2, show_result=True)

print(orientation)