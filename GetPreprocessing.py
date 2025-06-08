import numpy as np
import cv2

def Preprocessing(image, pos):

    #Mengubah kedalam bentuk biner dan menghilangkan objek kecil dan noise
    _, biner = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY_INV)
    kernel3x3 = np.ones((3,3), np.uint8)
    erosi = cv2.erode(biner, kernel3x3, iterations=6)
    kernel = np.ones((3,3), np.uint8)
    dilasi = cv2.dilate(erosi, kernel, iterations=30)
    cv2.circle(dilasi, pos['start'], 128, 0, -1)
    cv2.circle(dilasi, pos['goal'], 128, 0, -1)
    dilasi = cv2.resize(dilasi, (dilasi.shape[1]//2, dilasi.shape[0]//2))

    #Pengubah posisi ke ukuran baru
    pos = {
        key: (x // 2, y // 2)
        for key, (x, y) in pos.items()
    }

    #Merubah Citra kedalam array numpy
    map = np.array(dilasi)

    # Asumsikan pos['start'] dan pos['goal'] dalam format (x, y)
    Xs, Ys = pos['start']
    Xg, Yg = pos['goal']

    # Membalik urutan jadi (y, x)
    pos['start'] = (Ys, Xs)
    pos['goal'] = (Yg, Xg)

    return map, pos