from Utils import *


def Pos(img):
    """
    Mendeteksi marker ID 0 (start) dan ID 1 (goal) dari citra ArUco.

    Parameters:
        img (np.ndarray): Gambar grayscale yang akan dianalisis.

    Returns:
        tuple:
            - start (tuple): (center, pts).
            - goal (tuple): (center, pts).
            - mark_size (float): Estimasi ukuran marker berdasarkan jarak antar sudut.

    Notes:
        - Jika tidak ada marker ditemukan, maka `start` dan `goal` bisa `None`.
    """
    
    # Inisialisasi ArUco
    detector_params = aruco.DetectorParameters()
    detector_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    detector = aruco.ArucoDetector(detector_dict, detector_params)
    corners, ids, _ = detector.detectMarkers(img)

    # Variabel untuk start dan goal
    start = None
    goal = None

    if ids is not None:
        # Menghitung Lebar Marker
        pts = corners[0][0] 
        mark_size = 0.5 * (np.linalg.norm(pts[0] - pts[1]) + np.linalg.norm(pts[2] - pts[3]))

        # Mencari Corner
        ids = ids.flatten()
        for i, marker_id in enumerate(ids):
            if marker_id == 1:
                pts = corners[i][0]
                center = np.mean(pts, axis=0).astype(int)
                start = (center, pts)
            elif marker_id == 7:
                pts = corners[i][0]
                center = np.mean(pts, axis=0).astype(int)
                goal = (center, pts)
        aruco.drawDetectedMarkers(img, corners, ids, (255,0,255))
    else:
        return 0,0,0

    return (
        start,
        goal,
        mark_size
    )
