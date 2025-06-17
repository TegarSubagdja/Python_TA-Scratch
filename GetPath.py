from Utils import *

def getPath(image, scale=20, idStart=1, idGoal=7):

    # Preprocessing
    posa = Position(image, idStart, idGoal)

    if not posa:
        return 0

    print("Posisi Awal : ", posa)
    map, pos = Preprocessing(image, posa, scale)
    print("Setelah di flip : ", pos)

    print("Nilai:", pos["start"])
    print("Nilai:", pos["goal"])

    # Pencarian Jalur
    (path, time), open_list, close_list = jps.method(map, pos['start'], pos['goal'], 2)
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

    return path


# image = cv2.imread('Image/6.jpg', 0)
# getPath(image, 40, 2, 1)
