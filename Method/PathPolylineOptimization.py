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

def bresenham_classic(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    i1 = 2 * dy
    i2 = 2 * (dy - dx)
    d = i1 - dx

    if dx < 0:
        x = x2
        y = y2
        x_end = x1
    else:
        x = x1
        y = y1
        x_end = x2

    points.append((x, y))

    while x < x_end:
        if d < 0:
            d += i1
        else:
            d += i2
            y += 1
        x += 1
        points.append((x, y))

    return points

def bresenham_line(x1, y1, x2, y2):

    points = []

    deltax = abs(x2 - x1)
    deltay = abs(y2 - y1)

    # inisialisasi variabel
    if deltax >= deltay:
        # x independen
        numpixels = deltax + 1
        d = (2 * deltay) - deltax
        dinc1 = deltay << 1
        dinc2 = (deltay - deltax) << 1
        xinc1, xinc2 = 1, 1
        yinc1, yinc2 = 0, 1
    else:
        # y independen
        numpixels = deltay + 1
        d = (2 * deltax) - deltay
        dinc1 = deltax << 1
        dinc2 = (deltax - deltay) << 1
        xinc1, xinc2 = 0, 1
        yinc1, yinc2 = 1, 1

    # cek arah pergerakan
    if x1 > x2:
        xinc1, xinc2 = -xinc1, -xinc2
    if y1 > y2:
        yinc1, yinc2 = -yinc1, -yinc2

    # mulai dari titik awal
    x, y = x1, y1
    for _ in range(numpixels):
        points.append((x, y))
        if d < 0:
            d += dinc1
            x += xinc1
            y += yinc1
        else:
            d += dinc2
            x += xinc2
            y += yinc2

    return points

def bresenham_pure(x0, y0, x1, y1):
    """Original Bresenham line drawing (only works for slope 0 <= m <= 1, x0 < x1)."""
    points = []
    dx = x1 - x0
    dy = y1 - y0
    d = 2*dy - dx  # decision parameter
    y = y0

    for x in range(x0, x1 + 1):
        points.append((x, y))
        if d > 0:
            y += 1
            d -= 2*dx
        d += 2*dy

    return points

def bresenham(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

    if dy <= dx:  # slope <= 1
        d = 2*dy - dx
        for _ in range(dx+1):
            points.append((x, y))
            if d >= 0:
                y += sy
                d -= 2*dx
            x += sx
            d += 2*dy
    else:  # slope > 1
        d = 2*dx - dy
        for _ in range(dy+1):
            points.append((x, y))
            if d >= 0:
                x += sx
                d -= 2*dy
            y += sy
            d += 2*dx
    return points

def Prunning(P, map):

    # print(f"Path Asli : {P}")
    O_path = [P[0]]  # Tambahkan titik awal
    front = P[0]
    # print(f"Pada tahap awal titik pertama pada jalur dijadikan sebagai titik awal {P[0]}, kemudian mulai lompatan ke titik selanjutnya yaitu {front}")

    for i in range(1, len(P)):
        jumpPoint = P[i]
        # print(f"\nTitik Lompatan : {jumpPoint}")
        # print(f"Titik yang dilalui oleh untuk melompat ke titik {jumpPoint} adalah:")
        line = bresenham_line(front[0], front[1], jumpPoint[0], jumpPoint[1])
        # [print((x, y), f"bernilai {map[x][y]} yang bukan merupakan rintangan." if map[x][y]== 0 else f"bernilai {map[x][y]} yang merupakan rintangan!") for x, y in line]
        # Cek apakah ada rintangan (255)
        block = any(
            map[x][y] == 255 for (x, y) in line
        )
        if block:
            # Tambahkan titik sebelumnya ke hasil
            O_path.append(P[i-1])
            # print(f"Karena pada loncatan ke titik {jumpPoint} memotong rintangan, maka titik sebelumnya yaitu {P[i-1]} ditambahkan ke lintasan optimal, sehingga jalur optimal saat ini adalah: {O_path}")
            front = P[i-1]  # Perbarui titik_depan
        # else:
            # print(f"Karena tidak ada titik rintangan yang terpotong maka melanjutkan lompatan ke titik selanjutnya yaitu {P[i+1] if i !=len(P)-1 else "sudah mencapai titik akhir."}")
    O_path.append(P[-1])  # Tambahkan titik akhir
    # print(f"Maka setelah penghapusan titik tidak penting ini jalur optimal yang dihasilkan adalah: {O_path}")
    return O_path