from Utils import *

def Prep(img, start, goal):
    """
    Melakukan Preprocessing Pada Citra untuk Memastikan Pencarian Jalur Berjalan dengan Baik.

    Parameters:
        img (np.ndarray): Gambar akan dipreprocessing.
        start (tuple): Tuple berisi koordinat pusat dan bounding box start point
        goal (tuple): Tuple berisi koordinat pusat dan bounding box goal point

    Returns:
        np.ndarray: matrix peta biner 2D, berisi 0 dan 255
    """

    # Konversi ke grayscale jika belum
    if len(img.shape) != 2:
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            print("Format img tidak valid")

    # Hapus area marker robot dari gambar
    if start is not None and goal is not None:
        pts1 = goal[0].astype(np.int32)
        pts2 = start[0].astype(np.int32)
        cv2.circle(img, pts1, 100, 255, -1)
        cv2.circle(img, pts2, 100, 255, -1)
        cv2.imwrite('Map_GetPath.jpg', img)
        print('dieksekusi')

    # Threshold -> binary inverse: rintangan jadi putih (255), background jadi hitam (0)
    _, binary = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)

    # Penghapusan noise kecil
    kernel = np.ones((32, 32), np.uint8)
    morp = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel=kernel, iterations=18)
    # morp = cv2.erode(binary, kernel, iterations=3)
    # morp = cv2.dilate(morp, kernel, iterations=3)

    # Salin hasil akhir ke matrix baru
    matrix = np.copy(morp)

    # Simpan untuk debugging
    cv2.imwrite('Map_GetPath.jpg', morp)

    return matrix
