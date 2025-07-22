from Utils import *


def Pos(img, detector):

    corners, ids, _ = detector.detectMarkers(img)

    # Variabel untuk meyimpan start dan goal
    start = None
    goal = None

    # Jika ada marker ditemukan (adanya ids)
    if ids is not None:
        ids = ids.flatten()
        for i, marker_id in enumerate(ids):
            if marker_id == 3 or marker_id == 1:
                # Dapatkan corcer start
                pts = corners[i][0]
                # Dapatkan center start
                center = np.mean(pts, axis=0).astype(int)
                # Simpan posisi start
                start = (center, pts)
            elif marker_id == 9 or marker_id == 7:
                # Dapatkan corcer goal
                pts = corners[i][0]
                # Dapatkan center goal
                center = np.mean(pts, axis=0).astype(int)
                # Simpan posisi start
                goal = (center, pts)
                # Hitung Lebar Marker Goal
                mark_size = 0.5 * (np.linalg.norm(pts[0] - pts[1]) + np.linalg.norm(pts[2] - pts[3]))

        # Gambar informasi Marker
        aruco.drawDetectedMarkers(image=img, corners=corners)

        if not start or not goal:
            return None, None, None

        # Ubah ke dalam bentuk tupple
        startPts = [(int(x), int(y)) for x, y in start[1]]
        tStart = tuple(int(x) for x in start[0])
        start = (tStart, startPts)
        # Ubah kedalam bentuk tupple
        goalPts = [(int(x), int(y)) for x, y in goal[1]]
        tGoal = tuple(int(x) for x in goal[0])
        goal = (tGoal, goalPts)

        return (
            start,
            goal,
            mark_size
        )
    
    else:
        return 0,0,0
    

