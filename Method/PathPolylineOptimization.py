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

def Prunning(P, map):

    # print(f"Path Asli : {P}")
    O_path = [P[0]]  # Tambahkan titik awal
    # print(f"Tambahkan titik pertama ke path optimal : {O_path}")
    front = P[0]
    # print(f"Tentukan nilai titik lompatan awal : {front}")

    for i in range(1, len(P)):
        jumpPoint = P[i]
        # print(f"\nTitik Lompatan : {jumpPoint}")
        # print(f"Titik yang dilewati  : ")
        line = bresenham(front[0], front[1], jumpPoint[0], jumpPoint[1])
        # [print((x, y), "Aman" if map[x][y]== 0 else "Rintangan") for x, y in line]
        # Cek apakah ada rintangan (255)
        block = any(
            map[x][y] == 255 for (x, y) in line
        )
        if block:
            # Tambahkan titik sebelumnya ke hasil
            # print(f"Lompatan memotong rintangan!")
            # print(f"Tambahkan titik sebelumnya ke path optimal")
            O_path.append(P[i-1])
            # print(f"Path optimal saat ini : {O_path}")
            front = P[i-1]  # Perbarui titik_depan
        # else:
            # print(f"Status : Aman")
    # print(f"Titik {jumpPoint} adalah titik akhir")
    # print(f"Selesai")
    O_path.append(P[-1])  # Tambahkan titik akhir
    return O_path