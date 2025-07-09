from Utils import *

def Distance(start, goal, pos):
    """
    Menghitung titik proyeksi dari `posisi` ke garis yang dibentuk oleh `awal` dan `akhir`.

    Parameters:
        awal: tuple (x1, y1)
        akhir: tuple (x2, y2)
        posisi: tuple (x0, y0)

    Returns:
        Tuple (x_proj, y_proj): Titik proyeksi (float)
    """
    x1, y1 = start
    x2, y2 = goal
    x0, y0 = pos

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        # Garis tidak valid (awal == akhir)
        return start

    # Vektor dari awal ke posisi
    px = x0 - x1
    py = y0 - y1

    # Proyeksi skalar
    dot = px * dx + py * dy
    len_sq = dx * dx + dy * dy
    t = dot / len_sq

    # Titik proyeksi
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy

    # Menghitung jarak dari pos ke titik proyeksi
    distance = math.sqrt((x0 - proj_x)**2 + (y0 - proj_y)**2)

    return (int(round(proj_x)), int(round(proj_y))), distance
