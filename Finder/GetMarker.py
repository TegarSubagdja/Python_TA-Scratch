from Utils import *


def Pos(img):
    
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
            if marker_id == 3:
                pts = corners[i][0]
                center = np.mean(pts, axis=0).astype(int)
                start = (center, pts)
            elif marker_id == 9:
                pts = corners[i][0]
                center = np.mean(pts, axis=0).astype(int)
                goal = (center, pts)

        aruco.drawDetectedMarkers(img, corners, ids)

        if not start or not goal:
            return 0,0,0

        startPts = [(int(x), int(y)) for x, y in start[1]]
        goalPts = [(int(x), int(y)) for x, y in goal[1]]

        s = tuple(int(x) for x in start[0])
        g = tuple(int(x) for x in goal[0])

        start = (s, startPts)
        goal = (g, goalPts)

        return (
            start,
            goal,
            mark_size
        )
    else:
        return 0,0,0
    

