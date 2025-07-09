from Utils import *

def Preprocessing(image, pos, scale, corners):
    # Merubah Representasi Pos
    pos = tuple((y // scale, x // scale) for (x, y) in pos)

    # Mencari Kontur
    Expantion_Distance = Contour(image, corners)

    # Resize citra
    upscale_image = cv2.resize(
        Expantion_Distance,
        (Expantion_Distance.shape[1] // scale, Expantion_Distance.shape[0] // scale),
        interpolation=cv2.INTER_NEAREST
    )

    # Konversi ke array
    map = np.array(upscale_image)

    return map, pos
