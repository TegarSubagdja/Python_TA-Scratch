from Utils import *

def Preprocessing(image, pos, scale):

    safe = Contour(image)

    # Merubah Ukuran Gambar
    dilasi = cv2.resize(safe, (safe.shape[1]//scale, safe.shape[0]//scale), interpolation=cv2.INTER_NEAREST)
    
    # Pengubah posisi ke ukuran baru
    pos = {
        key: (x // scale, y // scale)
        for key, (x, y) in pos.items()
    }

    # Merubah Citra kedalam array numpy
    map = np.array(dilasi)

    # Asumsikan pos['start'] dan pos['goal'] dalam format (x, y)
    Xs, Ys = pos['start']
    Xg, Yg = pos['goal']

    # Membalik urutan jadi (y, x)
    pos['start'] = (Ys, Xs)
    pos['goal'] = (Yg, Xg)

    return map, pos