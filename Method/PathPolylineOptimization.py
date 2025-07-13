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
    nodes = bresenham_line(awal, akhir)
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

def Prunning(path, map):
    start = 0
    goal = 1
    start_t = start
    goal_t = goal
    path_prunning = [path[start]]
    while True:
        while goal <= len(path)-1:
            if not (lompatanAman(path[start], path[goal], map)):
                if (is_45_degree(path[start], path[goal])):
                    goal += 1
                    break
                elif goal == len(path):
                    path_prunning.append(path[goal])
                    break
                else:
                    path_prunning.append(path[goal-1])
                    start = goal - 1
                    break
            else:
                goal += 1
        if (start_t == start and goal_t == goal):
            break
        start_t = start
        goal_t = goal
    path_prunning.append(path[len(path)-1])
    return path_prunning