from Utils import *

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

def optimasi_jalur(P, grid):
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

map = Z_GetMap.load_grid(path=f"Map/JSON/{"Map_1"}.json", s=True)
np.place(map, map == 1, 255)
print(map)
# Misal P adalah jalur awal hasil A*
path = [(0, 0), (1, 1), (1, 2), (1, 3), (2, 4), (3, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (8, 12), (9, 12), (10, 12), (11, 12), (12, 13), (13, 13), (14, 14), (15, 15)]

# grid adalah peta seperti yang sudah kamu buat sebelumnya
optimized = optimasi_jalur(path, map)

optimized = [(x,y) for (x,y) in optimized]
Z_GetMap.show(map, window_size=512, path=optimized)
print(path)
print("Jalur hasil optimasi:")
print(optimized)
