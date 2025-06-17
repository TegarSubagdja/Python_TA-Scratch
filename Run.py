from Utils import *

image = cv2.imread('Image/2.jpg', 0)

path = getPath(image, 40, 2, 1)

errorOrientasi = Error(image)

print(errorOrientasi)

