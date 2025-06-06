import math, time, heapq

# Menghitung jarak heuristik antara dua titik menggunakan metode berbeda
def heuristic(a, b, hchoice):
    if hchoice == 1:
        # Menghitung jarak diagonal menggunakan rumus jarak octile
        xdist = math.fabs(b[0] - a[0])
        ydist = math.fabs(b[1] - a[1])
        if xdist > ydist:
            return 14 * ydist + 10 * (xdist - ydist)  # Biaya: 14 untuk diagonal, 10 untuk lurus
        else:
            return 14 * xdist + 10 * (ydist - xdist)
    if hchoice == 2:
        # Menghitung jarak Euclidean antara dua titik
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

# Memeriksa apakah pergerakan ke posisi tertentu dihalangi oleh rintangan
def blocked(cX, cY, dX, dY, matrix):
    # Memeriksa apakah posisi berada di luar batas matriks
    if cX + dX < 0 or cX + dX >= matrix.shape[0]:
        return True
    if cY + dY < 0 or cY + dY >= matrix.shape[1]:
        return True
        
    # Menangani pergerakan diagonal
    if dX != 0 and dY != 0:
        # Memeriksa apakah kedua sel yang berdekatan terhalang (tidak bisa lewat)
        if matrix[cX + dX][cY] == 1 and matrix[cX][cY + dY] == 1:
            return True
        # Memeriksa apakah sel diagonal target terhalang
        if matrix[cX + dX][cY + dY] == 1:
            return True
    else:
        # Menangani pergerakan lurus (horizontal atau vertikal)
        if dX != 0:  # Pergerakan horizontal
            if matrix[cX + dX][cY] == 1:
                return True
        else:  # Pergerakan vertikal
            if matrix[cX][cY + dY] == 1:
                return True
    return False

# Memeriksa apakah pergerakan diagonal terhalang
def dblock(cX, cY, dX, dY, matrix):
    # Memeriksa apakah kedua sel yang berdekatan dengan gerakan diagonal terhalang
    if matrix[cX - dX][cY] == 1 and matrix[cX][cY - dY] == 1:
        return True
    return False

# Menentukan arah pergerakan antara node saat ini dan node induk
def direction(cX, cY, pX, pY):
    # Menghitung vektor arah (-1, 0, atau 1 untuk setiap komponen)
    dX = int(math.copysign(1, cX - pX))
    dY = int(math.copysign(1, cY - pY))
    # Jika tidak ada pergerakan dalam suatu arah, set komponen ke 0
    if cX - pX == 0:
        dX = 0
    if cY - pY == 0:
        dY = 0
    return (dX, dY)

# Mencari node tetangga yang valid dengan mempertimbangkan aturan pergerakan
def nodeNeighbours(cX, cY, parent, matrix):
    neighbours = []
    # Jika tidak ada induk (node awal), periksa 8 arah
    if type(parent) != tuple:
        for i, j in [(-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
            if not blocked(cX, cY, i, j, matrix):
                neighbours.append((cX + i, cY + j))
        return neighbours
    
    # Mendapatkan arah dari induk ke posisi saat ini
    dX, dY = direction(cX, cY, parent[0], parent[1])

    # Menangani pergerakan diagonal
    if dX != 0 and dY != 0:
        # Memeriksa tetangga alami
        if not blocked(cX, cY, 0, dY, matrix):
            neighbours.append((cX, cY + dY))
        if not blocked(cX, cY, dX, 0, matrix):
            neighbours.append((cX + dX, cY))
        if (not blocked(cX, cY, 0, dY, matrix) or not blocked(cX, cY, dX, 0, matrix)) and not blocked(cX, cY, dX, dY, matrix):
            neighbours.append((cX + dX, cY + dY))
        # Memeriksa tetangga paksa
        if blocked(cX, cY, -dX, 0, matrix) and not blocked(cX, cY, 0, dY, matrix):
            neighbours.append((cX - dX, cY + dY))
        if blocked(cX, cY, 0, -dY, matrix) and not blocked(cX, cY, dX, 0, matrix):
            neighbours.append((cX + dX, cY - dY))
    else:
        # Menangani pergerakan lurus
        if dX == 0:  # Pergerakan vertikal
            if not blocked(cX, cY, dX, 0, matrix):
                if not blocked(cX, cY, 0, dY, matrix):
                    neighbours.append((cX, cY + dY))
                if blocked(cX, cY, 1, 0, matrix):
                    neighbours.append((cX + 1, cY + dY))
                if blocked(cX, cY, -1, 0, matrix):
                    neighbours.append((cX - 1, cY + dY))
        else:  # Pergerakan horizontal
            if not blocked(cX, cY, dX, 0, matrix):
                if not blocked(cX, cY, dX, 0, matrix):
                    neighbours.append((cX + dX, cY))
                if blocked(cX, cY, 0, 1, matrix):
                    neighbours.append((cX + dX, cY + 1))
                if blocked(cX, cY, 0, -1, matrix):
                    neighbours.append((cX + dX, cY - 1))
    return neighbours

# Melakukan operasi "lompatan" untuk menemukan titik lompatan berikutnya
def jump(cX, cY, dX, dY, matrix, goal):
    # Menghitung posisi berikutnya
    nX = cX + dX
    nY = cY + dY
    
    # Memeriksa apakah posisi berikutnya terhalang atau adalah tujuan
    if blocked(nX, nY, 0, 0, matrix):
        return None
    if (nX, nY) == goal:
        return (nX, nY)

    oX = nX
    oY = nY

    # Menangani pergerakan diagonal
    if dX != 0 and dY != 0:
        while True:
            # Memeriksa tetangga paksa
            if (not blocked(oX, oY, -dX, dY, matrix) and blocked(oX, oY, -dX, 0, matrix)
                or not blocked(oX, oY, dX, -dY, matrix) and blocked(oX, oY, 0, -dY, matrix)):
                return (oX, oY)

            # Memeriksa arah horizontal dan vertikal secara rekursif
            if (jump(oX, oY, dX, 0, matrix, goal) != None
                or jump(oX, oY, 0, dY, matrix, goal) != None):
                return (oX, oY)

            # Bergerak diagonal
            oX += dX
            oY += dY

            # Memeriksa apakah posisi baru valid
            if blocked(oX, oY, 0, 0, matrix):
                return None
            if dblock(oX, oY, dX, dY, matrix):
                return None
            if (oX, oY) == goal:
                return (oX, oY)
    else:
        # Menangani pergerakan lurus
        if dX != 0:  # Horizontal
            while True:
                # Memeriksa tetangga paksa
                if (not blocked(oX, nY, dX, 1, matrix) and blocked(oX, nY, 0, 1, matrix)
                    or not blocked(oX, nY, dX, -1, matrix) and blocked(oX, nY, 0, -1, matrix)):
                    return (oX, nY)

                oX += dX

                if blocked(oX, nY, 0, 0, matrix):
                    return None
                if (oX, nY) == goal:
                    return (oX, nY)
        else:  # Vertikal
            while True:
                # Memeriksa tetangga paksa
                if (not blocked(nX, oY, 1, dY, matrix) and blocked(nX, oY, 1, 0, matrix)
                    or not blocked(nX, oY, -1, dY, matrix) and blocked(nX, oY, -1, 0, matrix)):
                    return (nX, oY)

                oY += dY

                if blocked(nX, oY, 0, 0, matrix):
                    return None
                if (nX, oY) == goal:
                    return (nX, oY)

    return jump(nX, nY, dX, dY, matrix, goal)

# Mengidentifikasi node penerus dengan mencari titik lompatan yang valid
def identifySuccessors(cX, cY, came_from, matrix, goal):
    successors = []
    # Mendapatkan node tetangga
    neighbours = nodeNeighbours(cX, cY, came_from.get((cX, cY), 0), matrix)

    # Mencari titik lompatan untuk setiap tetangga
    for cell in neighbours:
        dX = cell[0] - cX
        dY = cell[1] - cY

        jumpPoint = jump(cX, cY, dX, dY, matrix, goal)

        if jumpPoint != None:
            successors.append(jumpPoint)

    return successors

# Metode pencarian jalur utama menggunakan Jump Point Search
def method(matrix, start, goal, hchoice):
    # Inisialisasi struktur data
    came_from = {}  # Pointer induk
    close_set = set()  # Set tertutup
    gscore = {start: 0}  # Biaya dari start
    fscore = {start: heuristic(start, goal, hchoice)}  # Estimasi total biaya

    # Antrian prioritas untuk set terbuka
    pqueue = []
    heapq.heappush(pqueue, (fscore[start], start))

    starttime = time.time()

    while pqueue:
        # Mendapatkan node dengan f-score terendah
        current = heapq.heappop(pqueue)[1]
        
        # Memeriksa apakah tujuan tercapai
        if current == goal:
            # Merekonstruksi jalur
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            data = data[::-1]
            endtime = time.time()
            return (data, round(endtime - starttime, 6)), close_set, pqueue

        close_set.add(current)

        # Mendapatkan penerus dari node saat ini
        successors = identifySuccessors(current[0], current[1], came_from, matrix, goal)

        # Memproses setiap penerus
        for successor in successors:
            jumpPoint = successor

            if jumpPoint in close_set:
                continue

            # Menghitung g-score sementara
            tentative_g_score = gscore[current] + lenght(current, jumpPoint, hchoice)

            # Memperbarui node jika ditemukan jalur yang lebih baik
            if tentative_g_score < gscore.get(jumpPoint, 0) or jumpPoint not in [j[1] for j in pqueue]:
                came_from[jumpPoint] = current
                gscore[jumpPoint] = tentative_g_score
                fscore[jumpPoint] = tentative_g_score + heuristic(jumpPoint, goal, hchoice)
                heapq.heappush(pqueue, (fscore[jumpPoint], jumpPoint))
        endtime = time.time()
    return (0, round(endtime - starttime, 6))

# Menghitung panjang/biaya antara node saat ini dan titik lompatan
def lenght(current, jumppoint, hchoice):
    # Mendapatkan komponen arah dan jarak
    dX, dY = direction(current[0], current[1], jumppoint[0], jumppoint[1])
    dX = math.fabs(dX)
    dY = math.fabs(dY)
    lX = math.fabs(current[0] - jumppoint[0])
    lY = math.fabs(current[1] - jumppoint[1])
    
    if hchoice == 1:
        # Menghitung jarak octile
        if dX != 0 and dY != 0:
            lenght = lX * 14  # Biaya pergerakan diagonal
            return lenght
        else:
            lenght = (dX * lX + dY * lY) * 10  # Biaya pergerakan lurus
            return lenght
    if hchoice == 2:
        # Menghitung jarak Euclidean
        return math.sqrt((current[0] - jumppoint[0]) ** 2 + (current[1] - jumppoint[1]) ** 2)