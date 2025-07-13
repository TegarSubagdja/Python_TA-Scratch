from Utils import *

def euclidean(pos, target):
    return np.linalg.norm(np.array(pos) - np.array(target))

def normalize_angle(angle):
    return np.arctan2(np.sin(angle), np.cos(angle))

def Error(img, start, goal):

        # Menghitung jarak start ke goal
        distance = euclidean(start[0], goal[0])
        
        # Menghitung error arah robot
        start_pts = start[1]
        dx = start[0][0] - goal[0][0]
        dy = start[0][1] - goal[0][1]
        arah_ke_goal = np.arctan2(dy, dx)

        # Gambar panah orientasi marker (hijau)
        cv2.arrowedLine(img, start[1][1], start[1][0], (255, 255, 255), 1, tipLength=0.1)
        cv2.imwrite('Map_arrow.jpg', img)
        
        # Kemiringan robot saat ini
        vector = np.array(start_pts[1]) - np.array(start_pts[0])
        orientasi_robot = np.arctan2(vector[1], vector[0])
        error_orientasi = normalize_angle(arah_ke_goal - orientasi_robot)
        error_derajat = np.degrees(error_orientasi)

        return (distance, error_derajat)