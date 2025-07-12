from Utils import *

def Prep(img):

    """
    Melakukan Preprocessing Pada Citra untuk Memastikan Pencarian Jalur Berjalan dengan Baik.

    Parameters:
        img (np.ndarray): Gambar akan dipreprocessing.

    Returns:
        tuple:
            - start (tuple): (center, pts).
            - goal (tuple): (center, pts).
            - mark_size (float): Estimasi ukuran marker berdasarkan jarak antar sudut.

    Notes:
        - Jika tidak ada marker ditemukan, maka `start` dan `goal` bisa `None`.
    """

    # Rubah kedalam bentuk grayscale
    if len(img.shape) != 2:
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            print(f"Format img tidak valid")

    # Rubah kedalam bentuk biner
    _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)

    # Penghapusan noise
    kernel = np.ones((3,3), np.uint8)
    img = cv2.erode(img, kernel, iterations=3)

    # Pendefinisian Map
    map = img
    cv2.imwrite('Map_GetPath.jpg', map)

    return map