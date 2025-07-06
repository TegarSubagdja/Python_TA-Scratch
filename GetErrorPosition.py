from Utils import *

def euclidian(pos, target):
    p1, p2 = pos
    q1, q2 = target
    return math.sqrt((p1 - q1)**2 + (p2 - q2)**2)

def normalize_angle(angle):
    return (angle + np.pi) % (2 * np.pi) - np.pi

def GetOrientation(image, gId=None, sId=None, show_result=True, save_path=None):

    if image is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan di path: {image}")

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, _ = detector.detectMarkers(image)

    if corners:
        pts = corners[0][0] 
        mark_size = 0.5 * (np.linalg.norm(pts[0] - pts[1]) + np.linalg.norm(pts[2] - pts[3]))
    else:
        mark_size = 0

    koordinat = {'start': None, 'goal': None}
    orientasi_robot = None
    error_orientasi = None
    distance = None

    if ids is not None:
        for i, marker_id in enumerate(ids.flatten()):
            marker_corners = corners[i][0]
            center_x = int(np.mean(marker_corners[:, 0]))
            center_y = int(np.mean(marker_corners[:, 1]))
            if marker_id == sId:
                koordinat['start'] = (center_x, center_y)
                vector = marker_corners[1] - marker_corners[0]
                orientasi_robot = np.arctan2(vector[1], vector[0])
            elif marker_id == gId:
                 koordinat['goal'] = (center_x, center_y)

        # aruco.drawDetectedMarkers(image, corners, ids, (255,64,255))

    # Hitung orientasi dan error terhadap titik target
    if koordinat['start'] and koordinat["start"] is not None and orientasi_robot is not None:
        start = koordinat['start']

        if koordinat['goal']:
            if isinstance(gId, tuple):
                goal = gId
            else:
                goal = koordinat['goal']
        else:
            return 0

        #hitung jarak
        distance = euclidian(start, goal)

        dx = goal[0] - start[0]
        dy = goal[1] - start[1]
        arah_ke_goal = np.arctan2(dy, dx)
        error_orientasi = normalize_angle(arah_ke_goal - orientasi_robot)

        # Visualisasi
        panjang_panah = 100
        orientasi_x = int(start[0] + panjang_panah * np.cos(orientasi_robot))
        orientasi_y = int(start[1] + panjang_panah * np.sin(orientasi_robot))

        cv2.line(image, start, goal, (255, 0, 255), 4)
        cv2.arrowedLine(image, start, (orientasi_x, orientasi_y), (255,64,64), 4, tipLength=0.2)
    else:
        return 0

    if save_path:
        cv2.imwrite(save_path, image)

    if show_result:
        cv2.imshow("Hasil Deteksi dan Orientasi", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if ids is not None:
        return {
            "koordinat": koordinat,
            "orientasi_robot": orientasi_robot,
            "size": mark_size,
            "error_orientasi_radian": error_orientasi,
            "error_orientasi_derajat": np.degrees(error_orientasi) if error_orientasi is not None else None,
            "distance": distance,
            "image": image
        }
    else:
        return 0