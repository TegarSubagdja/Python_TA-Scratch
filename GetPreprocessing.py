from Utils import *

def Preprocessing(image, pos, scale, corners):

    cv2.imwrite('Data/Image/Process/4-Contour.jpg', image)
    Expantion_Distance, mark_size = Contour(image, corners)

    # Merubah Ukuran Gambar
    upscale_image = cv2.resize(Expantion_Distance, (Expantion_Distance.shape[1]//scale, Expantion_Distance.shape[0]//scale), interpolation=cv2.INTER_NEAREST)
    
    # Pengubah posisi ke ukuran baru
    pos = {
        key: (x // scale, y // scale)
        for key, (x, y) in pos.items()
    }

    # Merubah Citra kedalam array numpy
    map = np.array(upscale_image)

    # Asumsikan pos['start'] dan pos['goal'] dalam format (x, y)
    Xs, Ys = pos['start']
    Xg, Yg = pos['goal']

    # Membalik urutan jadi (y, x)
    pos['start'] = (Ys, Xs)
    pos['goal'] = (Yg, Xg)

    return map, pos, mark_size