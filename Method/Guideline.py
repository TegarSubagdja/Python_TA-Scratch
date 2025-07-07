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

def jarak_titik_ke_segmenn(awal, akhir, posisi):
    x1, y1 = awal
    x2, y2 = akhir
    x0, y0 = posisi

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        # Segmen adalah titik tunggal
        return math.hypot(x0 - x1, y0 - y1)

    # Hitung proyeksi titik ke garis (dalam bentuk skalar t)
    t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx**2 + dy**2)

    if t < 0:
        # Titik lebih dekat ke awal
        closest_x, closest_y = x1, y1
    elif t > 1:
        # Titik lebih dekat ke akhir
        closest_x, closest_y = x2, y2
    else:
        # Titik proyeksi jatuh di antara segmen
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

    # Hitung jarak Euclidean ke titik terdekat
    return math.hypot(x0 - closest_x, y0 - closest_y)


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
