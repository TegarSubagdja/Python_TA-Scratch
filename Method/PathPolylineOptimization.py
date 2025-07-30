import numpy as np
import pandas as pd
import math

def supercover_line(awal, akhir):
    x1, y1 = awal
    x2, y2 = akhir

    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    xstep = 1 if x2 > x1 else -1
    ystep = 1 if y2 > y1 else -1

    ddy = 2 * dy
    ddx = 2 * dx

    points.append((x, y))

    if ddx >= ddy:  # First octant (0 <= slope <= 1)
        errorprev = error = dx  
        for _ in range(dx):
            x += xstep
            error += ddy
            if error > ddx:
                y += ystep
                error -= ddx
                if error + errorprev < ddx:
                    points.append((x, y - ystep))
                elif error + errorprev > ddx:
                    points.append((x - xstep, y))
                else:
                    points.append((x, y - ystep))
                    points.append((x - xstep, y))
            points.append((x, y))
            errorprev = error
    else:  # Second octant (1 < slope)
        errorprev = error = dy
        for _ in range(dy):
            y += ystep
            error += ddx
            if error > ddy:
                x += xstep
                error -= ddy
                if error + errorprev < ddy:
                    points.append((x - xstep, y))
                elif error + errorprev > ddy:
                    points.append((x, y - ystep))
                else:
                    points.append((x - xstep, y))
                    points.append((x, y - ystep))
            points.append((x, y))
            errorprev = error

    return points

def bresenham_line(awal, akhir):
    x1, y1 = awal
    x2, y2 = akhir

    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1

    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

    if dx > dy:
        err = dx // 2
        while x != x2:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy // 2
        while y != y2:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy

    points.append((x2, y2))  # Tambahkan titik akhir
    return points


def lompatanAman(awal, akhir, map):
    """Check if any node in the path is an obstacle (1)."""
    nodes = supercover_line(awal, akhir)
    if(any(map[x][y] == 255 for x, y in nodes)):
        return False
    else:
        return True

def is_one_point_move(awal, akhir):
    x1, y1 = awal
    x2, y2 = akhir
    if (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) <= 1.5):
        return True
    else:
        return False
    
def is_45_degree(awal, akhir):
    x1, y1 = awal
    x2, y2 = akhir
    
    if x2 - x1 == 0:  # Menghindari pembagian dengan nol (garis vertikal)
        return False
    slope = (y2 - y1) / (x2 - x1)
    return slope == 1 or slope == -1

# def Prunning(path, map):
#     start = 0
#     goal = 1
#     start_t = start
#     goal_t = goal
#     path_prunning = [path[start]]
#     while True:
#         while goal <= len(path)-1:
#             if not (lompatanAman(path[start], path[goal], map)):
#                 # if (is_45_degree(path[start], path[goal])):
#                 #     goal += 1
#                 #     break
#                 # elif goal == len(path):
#                 #     path_prunning.append(path[goal])
#                 #     break
#                 # else:
#                     path_prunning.append(path[goal-1])
#                     start = goal - 1
#                     break
#             else:
#                 goal += 1
#         if (start_t == start and goal_t == goal):
#             break
#         start_t = start
#         goal_t = goal
#     path_prunning.append(path[len(path)-1])
#     return path_prunning

def bresenham(x0, y0, x1, y1):
    """Mengembalikan list titik antara (x0,y0) ke (x1,y1) dengan Bresenham"""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    points.append((x1, y1))
    return points

def Prunning(P, grid):
    """Optimasi jalur dengan memotong node yang tidak perlu"""
    O_path = [P[0]]  # Tambahkan titik awal
    titik_depan = P[0]

    for i in range(1, len(P)):
        titik_target = P[i]
        garis = bresenham(titik_depan[0], titik_depan[1], titik_target[0], titik_target[1])
        print(garis)
        
        # Cek apakah ada rintangan (255)
        ada_rintangan = any(
            grid[y][x] == 255 for (y, x) in garis
        )
        
        if ada_rintangan:
            # Tambahkan titik sebelumnya ke hasil
            O_path.append(P[i-1])
            titik_depan = P[i-1]  # Perbarui titik_depan

    O_path.append(P[-1])  # Tambahkan titik akhir
    return O_path