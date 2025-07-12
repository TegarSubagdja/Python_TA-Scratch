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

def Error(start, goal):
    """
    Menghitung Error ID 0 (start) ke Goal.
    """
    if isinstance(goal, tuple):
        # Konversi ke tuple biasa jika diperlukan
        start_pos = to_tuple(start[0])
        
        # Periksa struktur goal
        print(f"DEBUG - goal structure: {goal}")
        print(f"DEBUG - goal type: {type(goal)}")
        print(f"DEBUG - goal length: {len(goal)}")
        
        # Jika goal adalah tuple koordinat langsung (x, y)
        if len(goal) == 2 and isinstance(goal[0], (int, float)):
            goal_pos = goal
        # Jika goal adalah tuple dengan struktur ((x, y), pts)
        elif len(goal) == 2 and hasattr(goal[0], '__len__'):
            goal_pos = to_tuple(goal[0])
        else:
            # Fallback - anggap goal[0] dan goal[1] adalah x dan y
            goal_pos = (goal[0], goal[1])
        
        # DEBUG: Print nilai aktual
        print(f"DEBUG - start_pos: {start_pos}")
        print(f"DEBUG - goal_pos: {goal_pos}")
        
        # Menghitung jarak start ke goal
        distance = euclidean(start_pos, goal_pos)
        print(f"DEBUG - calculated distance: {distance}")
        
        # Manual calculation untuk verifikasi
        manual_dist = np.sqrt((start_pos[0] - goal_pos[0])**2 + (start_pos[1] - goal_pos[1])**2)
        print(f"DEBUG - manual distance: {manual_dist}")
        
        ## Menghitung error arah robot
        start_pts = [to_tuple(pt) for pt in start[1]]
        dx, dy = np.array(goal_pos) - np.array(start_pos)
        arah_ke_goal = np.arctan2(dy, dx)
        
        # Kemiringan robot saat ini
        vector = np.array(start_pts[1]) - np.array(start_pts[0])
        orientasi_robot = np.arctan2(vector[1], vector[0])
        error_orientasi = normalize_angle(arah_ke_goal - orientasi_robot)
        error_derajat = np.degrees(error_orientasi)

        return (distance, error_derajat)