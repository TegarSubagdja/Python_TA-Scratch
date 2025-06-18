from Utils import *

image = cv2.imread('Image/3.jpg', 0)

path = getPath(image, 40, 1, 7)
path.pop(0)

image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

while True:
    result = GetOrientation(image, target_point=(path[0][1], path[0][0]), show_result=False, save_path="Output/Output.jpg")
    resize = result['image']
    resize = cv2.resize(resize, (resize.shape[1]//4, resize.shape[0]//4))

    cv2.imshow('hasil deteksi', resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


