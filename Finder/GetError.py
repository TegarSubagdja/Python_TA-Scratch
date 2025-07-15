from Utils import *

def euclidean(pos, target):
    return np.linalg.norm(np.array(pos) - np.array(target))

def normalize_angle(angle):
    return np.arctan2(np.sin(angle), np.cos(angle))

def Error(img, start, goal):

        # Menghitung jarak start ke goal
        distance = euclidean(start[0], goal[0])
        
        # Menghitung error arah robot
        x1, y1 = start[0] if isinstance(start[0], (list, tuple)) else start
        x2, y2 = goal[0] if isinstance(goal[0], (list, tuple)) else goal
        arah_ke_goal = np.arctan2(y1 - y2, x1 - x2)

        # Gambar panah orientasi marker
        cv2.arrowedLine(img, start[1][1], start[1][0], (255, 255, 255), 2, tipLength=0.1)

        # Gambar panah orientasi marker ke goal
        cv2.line(img, (x1, y1), (x2, y2), (128), 2)
        
        # Kemiringan robot saat ini
        start_pts = start[1]
        vector = np.array(start_pts[1]) - np.array(start_pts[0])
        orientasi_robot = np.arctan2(vector[1], vector[0])
        error_orientasi = normalize_angle(arah_ke_goal - orientasi_robot)
        error_derajat = np.degrees(error_orientasi)

        return (distance, error_derajat)