from Utils import *

image = cv2.imread('Image/3.jpg', 0)

path = getPath(image, 40, 1, 7)
path.pop(0)

image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# for i in range(1, len(path)):
#         y1, x1 = path[i - 1]
#         y2, x2 = path[i]
#         cv2.line(image, (x1, y1), (x2, y2), 127, 8) 

# for y, x in path:
#     cv2.circle(image, (x, y), 16, (255,0,255), -1)
#     cv2.putText(image, f"({y}, {x})", (x+30,y+30), 1, 1.5, (255,255,255), 3)

while True:
    result = GetOrientation(image, target_point=(path[0][1], path[0][0]), show_result=False, save_path="Output/Output.jpg")
    resize = result['image']
    resize = cv2.resize(resize, (resize.shape[1]//4, resize.shape[0]//4))

    cv2.imshow('hasil deteksi', resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


