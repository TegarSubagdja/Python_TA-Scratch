from Utils import *

def euclidean(pos, target):
    return np.linalg.norm(np.array(pos) - np.array(target))

def normalize_angle(angle):
    return np.arctan2(np.sin(angle), np.cos(angle))

def to_tuple(data):
    """Konversi numpy array atau data lainnya ke tuple biasa"""
    if isinstance(data, np.ndarray):
        return tuple(data.tolist())
    elif isinstance(data, (list, tuple)):
        return tuple(data)
    else:
        return data

def Error(img, start, goal):
    """
    Menghitung Error ID 0 (start) ke Goal.
    """

    print(f"Format goal : {tuple(goal[0])}")

    if isinstance(goal, tuple):
        # Konversi ke tuple biasa jika diperlukan
        start_pos = to_tuple(start[0])
        
        # Jika goal adalah tuple koordinat langsung (x, y)
        if len(goal) == 2 and isinstance(goal[0], (int, float)):
            goal_pos = goal
        # Jika goal adalah tuple dengan struktur ((x, y), pts)
        elif len(goal) == 2 and hasattr(goal[0], '__len__'):
            goal_pos = to_tuple(goal[0])
        else:
            # Fallback - anggap goal[0] dan goal[1] adalah x dan y
            goal_pos = (goal[0], goal[1])
        
        # Menghitung jarak start ke goal
        distance = euclidean(start_pos, goal_pos)
        
        # Menghitung error arah robot
        start_pts = [to_tuple(pt) for pt in start[1]]
        dx, dy = np.array(goal_pos) - np.array(start_pos)
        arah_ke_goal = np.arctan2(dy, dx)

        # Gambar panah orientasi marker (hijau)
        cv2.arrowedLine(img, tuple(start[1][1].astype(int)), tuple(start[1][0].astype(int)), (255, 255, 255), 10, tipLength=0.1)
        # # Gambar panah ke goal (merah)
        cv2.line(img, tuple(start[0].astype(int)), tuple(goal[0].astype(int)), (255, 255, 255), 10)
        cv2.imwrite('Map_arrow.jpg', img)
        
        # Kemiringan robot saat ini
        vector = np.array(start_pts[1]) - np.array(start_pts[0])
        orientasi_robot = np.arctan2(vector[1], vector[0])
        error_orientasi = normalize_angle(arah_ke_goal - orientasi_robot)
        error_derajat = np.degrees(error_orientasi)

        return (distance, error_derajat)