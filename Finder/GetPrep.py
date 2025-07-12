from Utils import *

def Prep(img, start, goal):
    """
    Melakukan Preprocessing Pada Citra untuk Memastikan Pencarian Jalur Berjalan dengan Baik.

    Parameters:
        img (np.ndarray): Gambar akan dipreprocessing.
        start (tuple): Tuple berisi koordinat pusat dan bounding box start point
        goal (tuple): Tuple berisi koordinat pusat dan bounding box goal point

    Returns:
        np.ndarray: map biner.

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

    # Hapus area robot - Convert float32 to int32 dan format untuk fillPoly
    pts1 = goal[1].astype(np.int32)
    pts2 = start[1].astype(np.int32)
    
    # Pastikan pts dalam format yang benar untuk fillPoly - gunakan list of arrays
    cv2.fillPoly(img, [pts1], (255, 255, 255))
    cv2.fillPoly(img, [pts2], (255, 255, 255))

    # Pendefinisian Map
    map = img
    cv2.imwrite('Map_GetPath.jpg', map)

    return map