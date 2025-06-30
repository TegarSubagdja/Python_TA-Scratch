import math

def guidline(awal, akhir, posisi):
    x1, y1 = awal
    x2, y2 = akhir
    x0, y0 = posisi
    
    dx = x2 - x1
    dy = y2 - y1

    numerator = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1)
    denominator = math.hypot(dx, dy)

    return numerator / denominator if denominator != 0 else 0  # Hindari div by zero

def jarakGaris(awal, akhir, posisi):
    x1, y1 = awal
    x2, y2 = akhir
    x0, y0 = posisi

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return awal  # Garis tidak valid

    px = x0 - x1
    py = y0 - y1

    dot = px * dx + py * dy
    len_sq = dx * dx + dy * dy
    t = dot / len_sq

    proj_x = x1 + t * dx
    proj_y = y1 + t * dy

    return proj_x, proj_y  # Kembalikan float, int kalau perlu rounding nanti
