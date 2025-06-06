# Mengimpor modul yang diperlukan
# math: untuk operasi matematika
# heapq: untuk implementasi antrian prioritas
# time: untuk mengukur waktu eksekusi
import math, heapq, time
import sys
sys.path.append('../')
from MethodOptimasi.BarrierRasterCoefficient import barrierRaster
from MethodOptimasi.Guideline import guidline
from MethodOptimasi.PathPolylineOptimization import supercover_line




# Fungsi untuk memeriksa apakah suatu pergerakan terhalang atau tidak
def blocked(cX, cY, dX, dY, matrix):
    # Memeriksa apakah posisi berada di luar batas matriks pada sumbu X
    if cX + dX < 0 or cX + dX >= matrix.shape[0]:
        return True
    # Memeriksa apakah posisi berada di luar batas matriks pada sumbu Y
    if cY + dY < 0 or cY + dY >= matrix.shape[1]:
        return True
    
    # Penanganan untuk gerakan diagonal (ketika dX dan dY keduanya tidak nol)
    if dX != 0 and dY != 0:
        # Memeriksa apakah kedua sel yang berdekatan terhalang
        if matrix[cX + dX][cY] == 1 and matrix[cX][cY + dY] == 1:
            return True
        # Memeriksa apakah sel diagonal target terhalang
        if matrix[cX + dX][cY + dY] == 1:
            return True
    else:
        # Penanganan untuk gerakan horizontal
        if dX != 0:
            if matrix[cX + dX][cY] == 1:
                return True
        # Penanganan untuk gerakan vertikal
        else:
            if matrix[cX][cY + dY] == 1:
                return True
    return False


# Fungsi untuk menghitung nilai heuristik (perkiraan jarak) antara dua titik
def heuristic(a, b, hchoice):
    if hchoice == 1:
        # Menghitung jarak Manhattan pada sumbu X dan Y
        xdist = math.fabs(b[0] - a[0])
        ydist = math.fabs(b[1] - a[1])
        # Menggunakan metric octile (untuk grid 8-arah)
        if xdist > ydist:
            return 14 * ydist + 10 * (xdist - ydist)  # 14 untuk diagonal, 10 untuk orthogonal
        else:
            return 14 * xdist + 10 * (ydist - xdist)
    if hchoice == 2:
        # Menghitung jarak Euclidean
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


# Fungsi utama algoritma A* untuk pencarian jalur
def method(matrix, start, goal, hchoice):
    # Inisialisasi struktur data yang diperlukan
    close_set = set()  # Set untuk node yang sudah dievaluasi
    came_from = {}    # Dictionary untuk menyimpan jalur
    gscore = {start: 0}  # Biaya dari start ke node saat ini
    fscore = {start: heuristic(start, goal, hchoice)}  # Total estimasi biaya

    # Hitung Barier Raster
    p = barrierRaster(start, goal, matrix)
    print(f"Nilai Barier Raster adalah {p}")

    # Inisialisasi antrian prioritas
    pqueue = []
    heapq.heappush(pqueue, (fscore[start], start))

    # Mulai menghitung waktu eksekusi
    starttime = time.time()

    # Loop utama algoritma A*
    while pqueue:
        # Ambil node dengan nilai f terkecil
        current = heapq.heappop(pqueue)[1]
        
        # Jika node saat ini adalah tujuan, rekonstruksi jalur
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path = path[::-1]
            endtime = time.time()
            return (path, round(endtime - starttime, 6)), close_set, pqueue
        
        # Tambahkan node saat ini ke set tertutup
        close_set.add(current)
        
        # Periksa semua tetangga yang mungkin (8 arah)
        for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0), 
                       (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            
            # Lewati jika pergerakan terhalang
            if blocked(current[0], current[1], dX, dY, matrix):
                continue

            # Hitung posisi tetangga
            neighbour = current[0] + dX, current[1] + dY

            # Hitung biaya pergerakan berdasarkan pilihan heuristik
            if hchoice == 1:
                # Biaya untuk metrik octile
                if dX != 0 and dY != 0:
                    tentative_g_score = gscore[current] + 14  # Gerakan diagonal
                else:
                    tentative_g_score = gscore[current] + 10  # Gerakan orthogonal
            elif hchoice == 2:
                # Biaya untuk metrik Euclidean
                if dX != 0 and dY != 0:
                    tentative_g_score = gscore[current] + math.sqrt(2)  # Diagonal
                else:
                    tentative_g_score = gscore[current] + 1  # Orthogonal

            # Lewati jika tetangga sudah dievaluasi
            if neighbour in close_set:
                continue

            # Update nilai node jika ditemukan jalur yang lebih baik
            if tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1] for i in pqueue]:
                came_from[neighbour] = current
                gscore[neighbour] = tentative_g_score
                # fscore[neighbour] = tentative_g_score + heuristic(neighbour, goal, hchoice) # tanpa barier raster
                # fscore[neighbour] = tentative_g_score + (heuristic(neighbour, goal, hchoice) * (1-math.log(p))) # dengan barier raster
                fscore[neighbour] = tentative_g_score + heuristic(neighbour, goal, hchoice) + guidline(start, goal, current) # dengan guidline
                # fscore[neighbour] = tentative_g_score + (heuristic(neighbour, goal, hchoice) * (1-math.log(p))) + guidline(start, goal, current) # dengan barier raster dan guidline
                heapq.heappush(pqueue, (fscore[neighbour], neighbour))
        
        endtime = time.time()
    # Kembalikan 0 dan waktu eksekusi jika tidak ditemukan jalur
    return (0, round(endtime - starttime, 6))