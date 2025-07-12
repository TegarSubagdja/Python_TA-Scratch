from Utils import *

def euclidean(pos, target):
    return np.linalg.norm(np.array(pos) - np.array(target))

def normalize_angle(angle):
    return np.arctan2(np.sin(angle), np.cos(angle))

def Error(pos):
    """
    Menghitung Error ID 0 (start) ke Goal.

    Parameters:
        pos = ((start, pts), (goal, pts)).

    Returns:
        tuple:
            - distance (tuple): Jarak antara marker ID 0 ke tujuan.
            - error_degree (tuple): Selisih sudut titik saat ke tujuan dan sudut robot.

    Notes:
        - Jika tidak ada marker ditemukan, maka `start` dan `goal` bisa `None`.
    """

    # Mengekstraksi Posisi
    start, cornerStart = pos[0]
    goal, cornerGoal = pos[1]

    # Menghitung jarak start ke goal
    distance = euclidean(start, goal)

    ## Menghitung error arah robot
    # Kemiringan garis robot saat ini ke goal
    dx, dy = goal[0] - start[0], goal[1] - start[1]
    arah_ke_goal = np.arctan2(dy, dx)
    # Kemiringan robot saat ini
    vector = cornerStart[1] - cornerStart[0]
    orientasi_robot = np.arctan2(vector[1], vector[0])
    error_orientasi = normalize_angle(arah_ke_goal - orientasi_robot)
    error_derajat = np.degrees(error_orientasi)

    return (
        distance, 
        error_derajat
    )
