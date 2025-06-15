from Utils import *

# Baca gambar dalam grayscale
scale = 40
image = cv2.imread('Image/4.jpg', 0)

# Preprocessing
posa = Position(image)
print("Posisi Awal : ", posa)
map, pos, residu = Preprocessing(image, posa, scale)
print("Setelah di flip : ", pos)

print("Nilai:", pos["start"])
print("Nilai:", pos["goal"])
print("Residu:", residu['start'])
print("Residu:", residu['goal'])

# Pencarian Jalur
(path, time), open_list, close_list = jps.method(map, pos['start'], pos['goal'], 2)
# print(f"Open List adalah : {open_list}")
# print(f"Close List adalah : {close_list}")
print(f"Waktu Pencarian : {time}")
# path, time = astar.method(map, pos['start'], pos['goal'], 2)

# Optimasi
path = prunning(path, map)
print("Path Asli : ", path)
print("Path Hasil Prunning : ", path)

# Mengubah Koordinat Jalur ke Ukuran Asli
path = [(y * scale, x * scale) for y, x in path]
path[0] = posa['start'][::-1]
path[-1] = posa['goal'][::-1]
print("Path Hasil Scale : ", path)

#Menggambar Path di Image Ukuran Asli
# image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
image = cv2.imread("Output/Overlay.jpg")

for i in range(1, len(path)):
    y1, x1 = path[i - 1]
    y2, x2 = path[i]
    cv2.line(image, (x1, y1), (x2, y2), 100, 4) 

for y, x in path:
    cv2.circle(image, (x, y), 8, (255,0,255), -1) 
    cv2.putText(image, f"({y}, {x})", (x+30,y), 1, 2, (255,0,255), 3)

cv2.imwrite('Output/Output.jpg', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
