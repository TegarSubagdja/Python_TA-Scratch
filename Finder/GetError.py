from Utils import *

def euclidean(pos, target):
    return np.linalg.norm(np.array(pos) - np.array(target))

def normalize_angle(angle):
    return np.arctan2(np.sin(angle), np.cos(angle))

def midpoint(p1, p2):
    return ((p1[0]+p2[0])//2, (p1[1]+p2[1])//2)

def center_top_bottom(corners):
    top = midpoint(corners[1], corners[2])
    bottom = midpoint(corners[0], corners[3])
    return top, bottom

def Error(img, start, goal):

        # Menghitung error arah robot
        x1, y1 = start[0] if isinstance(start[0], (list, tuple)) else start
        x2, y2 = goal[0] if isinstance(goal[0], (list, tuple)) else goal
        arah_ke_goal = np.arctan2(y1 - y2, x1 - x2)

        # Menghitung jarak start ke goal
        distance = euclidean((x1, y1), (x2, y2))

        # Gambar panah orientasi marker ke goal
        cv2.line(img, (x1, y1), (x2, y2), (128), 2)
        
        # Kemiringan robot saat ini
        top, bottom = center_top_bottom(start[1])
        start_pts = start[1]
        # vector = np.array(start_pts[1]) - np.array(start_pts[0])
        orientasi_robot = np.arctan2(top[1] - bottom[1], top[0] - bottom[0])
        error_orientasi = normalize_angle(arah_ke_goal - orientasi_robot)
        error_derajat = np.degrees(error_orientasi)

        cv2.arrowedLine(img, top, bottom, (255, 255, 255), 2, tipLength=0.2)

        return (distance, error_derajat)