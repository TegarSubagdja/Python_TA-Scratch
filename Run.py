from Utils import *

cam = cv2.imread('Image/webcam.jpg')
cam = cv2.cvtColor(cam, cv2.COLOR_BGR2GRAY)

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

path = getPath(cam, 20, 2, 7, detector=detector)

print(path)