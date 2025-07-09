import math

def guidline(awal=0, akhir=0, posisi=0):
    x1, y1 = awal
    x2, y2 = akhir
    x0, y0 = posisi
    
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + (x2 * y1) - (y2 * x1))
    denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
    return numerator / denominator

def jarakGaris(awal, akhir, posisi):
    """
    Menghitung titik proyeksi dari `posisi` ke garis yang dibentuk oleh `awal` dan `akhir`.

    Parameters:
        awal: tuple (x1, y1)
        akhir: tuple (x2, y2)
        posisi: tuple (x0, y0)

    Returns:
        Tuple (x_proj, y_proj): Titik proyeksi (float)
    """
    x1, y1 = awal
    x2, y2 = akhir
    x0, y0 = posisi

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        # Garis tidak valid (awal == akhir)
        return awal

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

    return (int(round(proj_x)), int(round(proj_y)))
