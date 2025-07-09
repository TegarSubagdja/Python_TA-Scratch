from Utils import *

# cap = cv2.VideoCapture(1)
# if not cap.isOpened():
#     print("Tidak dapat membuka webcam.")
#     exit()
# ret, cam = cap.read()

# Inisialisasi Aruco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

# Pengambilan Gambar
cam = cv2.imread('Image/webcam.jpg')
cam = cv2.cvtColor(cam, cv2.COLOR_BGR2GRAY)

# Ambil Orientasi
(koordinat, 
 corners, 
 orientasi_robot, 
 mark_size, 
 distance, 
 error_orientasi, 
 error_orientasi_deg, 
 image) = GetOrientation(cam, 2, 7, show_result=False, detector=detector)

print(koordinat)

path = getPath(image=cam, scale=20, pos=koordinat, corners=corners)
print(f"path adalah : {path}")

if path:
    points = np.array([[y, x] for x, y in path], np.int32)
    cv2.polylines(cam, [points], isClosed=False, color=(255, 0, 255), thickness=2)
    for x, y in path:
        cv2.circle(cam, (y, x), 3, (255, 0, 255), -1)

cv2.imwrite('cam.jpg', cam)