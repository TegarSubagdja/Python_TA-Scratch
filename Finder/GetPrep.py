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
    _, binary = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)

    buffer_radius = 100  # contoh: ½ ukuran robot
    kernels = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*buffer_radius+1, 2*buffer_radius+1))

    # Penghapusan noise kecil
    kernel = np.ones((10, 10), np.uint8)
    morp = cv2.erode(binary, kernel, iterations=5)
    # morp = cv2.dilate(morp, kernel, iterations=20)
    starting = time.time()
    buffered_obstacle = cv2.dilate(morp, kernels, iterations=1)
    stoping = time.time()
    print(stoping-starting)

    # Salin hasil akhir ke matrix baru
    matrix = np.copy(buffered_obstacle)

    # Simpan untuk debugging
    cv2.imwrite('Map_GetPath.jpg', buffered_obstacle)

    return matrix
