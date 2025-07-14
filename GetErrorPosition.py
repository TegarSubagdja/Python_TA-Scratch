from Utils import *
import numpy as np
import cv2

def euclidean(pos, target):
    return np.linalg.norm(np.array(pos) - np.array(target))

def normalize_angle(angle):
    return np.arctan2(np.sin(angle), np.cos(angle))

def GetOrientation(image, gId=None, sId=None, show_result=True, save_path=None, detector=None):
    if image is None:
        raise FileNotFoundError("Gambar tidak ditemukan.")

    if detector is None:
        raise ValueError("Detector ArUco belum disediakan.")

    corners, ids, _ = detector.detectMarkers(image)
    ids = ids.flatten() if ids is not None else []

    koordinat = {'start': None, 'goal': None}
    orientasi_robot = None
    distance = None
    error_orientasi = None
    mark_size = 0

    # Hitung ukuran marker jika ada
    if corners:
        pts = corners[0][0] 
        mark_size = 0.5 * (np.linalg.norm(pts[0] - pts[1]) + np.linalg.norm(pts[2] - pts[3]))

    # Cari marker start dan goal
    for i, marker_id in enumerate(ids):
        marker_corners = corners[i][0]
        center = tuple(marker_corners.mean(axis=0).astype(int))

        if not isinstance(sId, tuple) and marker_id == sId and koordinat['start'] is None:
            koordinat['start'] = center
            vector = marker_corners[1] - marker_corners[0]
            orientasi_robot = np.arctan2(vector[1], vector[0])

        if not isinstance(gId, tuple) and marker_id == gId and koordinat['goal'] is None:
            koordinat['goal'] = center

    # Setelah loop: fallback ke tuple jika perlu
    if isinstance(sId, tuple):
        koordinat['start'] = sId
        orientasi_robot = 0  # Default arah jika tuple langsung, bisa diatur sesuai kebutuhan

    if isinstance(gId, tuple):
        koordinat['goal'] = gId

    # Jika goal berbentuk tuple, gunakan langsung
    if isinstance(gId, tuple):
        koordinat['goal'] = gId

    # Validasi posisi dan orientasi
    if koordinat['start'] is None or orientasi_robot is None or koordinat['goal'] is None:
        return None  # lebih eksplisit dari return 0

    # Hitung arah ke goal dan error orientasi
    start = koordinat['start']
    goal = koordinat['goal']

    distance = euclidean(start, goal)
    dx, dy = goal[0] - start[0], goal[1] - start[1]
    arah_ke_goal = np.arctan2(dy, dx)
    error_orientasi = normalize_angle(arah_ke_goal - orientasi_robot)

    # Hitung panah orientasi
    panjang_panah = 100
    orientasi_x = int(start[0] + panjang_panah * np.cos(orientasi_robot))
    orientasi_y = int(start[1] + panjang_panah * np.sin(orientasi_robot))

    # Simpan gambar jika diminta
    if save_path:
        cv2.imwrite(save_path, image)

    # Visualisasi
    if show_result:
        img_vis = image.copy()
        cv2.line(img_vis, start, goal, (255, 0, 255), 4)
        cv2.arrowedLine(img_vis, start, (orientasi_x, orientasi_y), (255, 64, 64), 4, tipLength=0.2)
        cv2.imshow("Hasil Deteksi dan Orientasi", img_vis)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return (
        (start, goal),             # 0
        corners,                   # 1
        orientasi_robot,           # 2
        mark_size,                 # 3
        distance,                  # 4
        error_orientasi,           # 5
        np.degrees(error_orientasi),  # 6
        image                      # 7
    )

