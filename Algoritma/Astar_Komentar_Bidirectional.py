# Mengimpor modul yang diperlukan
# math: untuk operasi matematika
# heapq: untuk implementasi antrian prioritas
# time: untuk mengukur waktu eksekusi
import math, heapq, time


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


# Fungsi untuk merekonstruksi jalur dari dua arah
def reconstruct_path(came_from_forward, came_from_backward, intersection_node):
    # Rekonstruksi jalur dari start ke intersection_node
    path_forward = []
    current = intersection_node
    while current in came_from_forward:
        path_forward.append(current)
        current = came_from_forward[current]
    path_forward.append(current)  # Tambahkan node start
    path_forward = path_forward[::-1]  # Balik urutan untuk mendapatkan jalur dari start
    
    # Rekonstruksi jalur dari intersection_node ke goal
    path_backward = []
    current = intersection_node
    while current in came_from_backward:
        current = came_from_backward[current]
        path_backward.append(current)
    
    # Gabungkan kedua jalur
    return path_forward + path_backward


# Fungsi bidirectional search
def bidirectional_search(matrix, start, goal, hchoice):
    # Inisialisasi struktur data untuk pencarian maju (forward)
    open_set_forward = []
    close_set_forward = set()
    came_from_forward = {}
    gscore_forward = {start: 0}
    fscore_forward = {start: heuristic(start, goal, hchoice)}
    heapq.heappush(open_set_forward, (fscore_forward[start], start))
    
    # Inisialisasi struktur data untuk pencarian mundur (backward)
    open_set_backward = []
    close_set_backward = set()
    came_from_backward = {}
    gscore_backward = {goal: 0}
    fscore_backward = {goal: heuristic(goal, start, hchoice)}
    heapq.heappush(open_set_backward, (fscore_backward[goal], goal))
    
    # Mulai menghitung waktu eksekusi
    starttime = time.time()
    
    # Menyimpan node yang telah dikunjungi oleh kedua pencarian
    intersection = None
    best_path_length = float('inf')
    
    # Loop utama algoritma bidirectional search
    while open_set_forward and open_set_backward:
        # Proses pencarian maju (forward)
        current_forward = heapq.heappop(open_set_forward)[1]
        
        # Cek apakah node saat ini telah dikunjungi oleh pencarian mundur
        if current_forward in close_set_backward:
            # Temukan jalur terpendek melalui node ini
            path_length = gscore_forward[current_forward] + gscore_backward[current_forward]
            if path_length < best_path_length:
                best_path_length = path_length
                intersection = current_forward
        
        # Tambahkan node saat ini ke set tertutup pencarian maju
        close_set_forward.add(current_forward)
        
        # Eksplorasi tetangga dalam pencarian maju
        for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0), 
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            
            # Lewati jika pergerakan terhalang
            if blocked(current_forward[0], current_forward[1], dX, dY, matrix):
                continue
                
            # Hitung posisi tetangga
            neighbour = current_forward[0] + dX, current_forward[1] + dY
            
            # Hitung biaya pergerakan berdasarkan pilihan heuristik
            if hchoice == 1:
                # Biaya untuk metrik octile
                if dX != 0 and dY != 0:
                    tentative_g_score = gscore_forward[current_forward] + 14  # Gerakan diagonal
                else:
                    tentative_g_score = gscore_forward[current_forward] + 10  # Gerakan orthogonal
            elif hchoice == 2:
                # Biaya untuk metrik Euclidean
                if dX != 0 and dY != 0:
                    tentative_g_score = gscore_forward[current_forward] + math.sqrt(2)  # Diagonal
                else:
                    tentative_g_score = gscore_forward[current_forward] + 1  # Orthogonal
            
            # Lewati jika tetangga sudah dievaluasi
            if neighbour in close_set_forward:
                continue
                
            # Update nilai node jika ditemukan jalur yang lebih baik
            if tentative_g_score < gscore_forward.get(neighbour, float('inf')) or neighbour not in [i[1] for i in open_set_forward]:
                came_from_forward[neighbour] = current_forward
                gscore_forward[neighbour] = tentative_g_score
                fscore_forward[neighbour] = tentative_g_score + heuristic(neighbour, goal, hchoice)
                heapq.heappush(open_set_forward, (fscore_forward[neighbour], neighbour))
        
        # Proses pencarian mundur (backward)
        current_backward = heapq.heappop(open_set_backward)[1]
        
        # Cek apakah node saat ini telah dikunjungi oleh pencarian maju
        if current_backward in close_set_forward:
            # Temukan jalur terpendek melalui node ini
            path_length = gscore_forward[current_backward] + gscore_backward[current_backward]
            if path_length < best_path_length:
                best_path_length = path_length
                intersection = current_backward
        
        # Tambahkan node saat ini ke set tertutup pencarian mundur
        close_set_backward.add(current_backward)
        
        # Eksplorasi tetangga dalam pencarian mundur
        for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0), 
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            
            # Lewati jika pergerakan terhalang
            if blocked(current_backward[0], current_backward[1], dX, dY, matrix):
                continue
                
            # Hitung posisi tetangga
            neighbour = current_backward[0] + dX, current_backward[1] + dY
            
            # Hitung biaya pergerakan berdasarkan pilihan heuristik
            if hchoice == 1:
                # Biaya untuk metrik octile
                if dX != 0 and dY != 0:
                    tentative_g_score = gscore_backward[current_backward] + 14  # Gerakan diagonal
                else:
                    tentative_g_score = gscore_backward[current_backward] + 10  # Gerakan orthogonal
            elif hchoice == 2:
                # Biaya untuk metrik Euclidean
                if dX != 0 and dY != 0:
                    tentative_g_score = gscore_backward[current_backward] + math.sqrt(2)  # Diagonal
                else:
                    tentative_g_score = gscore_backward[current_backward] + 1  # Orthogonal
            
            # Lewati jika tetangga sudah dievaluasi
            if neighbour in close_set_backward:
                continue
                
            # Update nilai node jika ditemukan jalur yang lebih baik
            if tentative_g_score < gscore_backward.get(neighbour, float('inf')) or neighbour not in [i[1] for i in open_set_backward]:
                came_from_backward[neighbour] = current_backward
                gscore_backward[neighbour] = tentative_g_score
                fscore_backward[neighbour] = tentative_g_score + heuristic(neighbour, start, hchoice)
                heapq.heappush(open_set_backward, (fscore_backward[neighbour], neighbour))
        
    # Jika kedua pencarian bertemu
    endtime = time.time()
    if intersection:
        # Rekonstruksi jalur
        path = reconstruct_path(came_from_forward, came_from_backward, intersection)
        return (path, round(endtime - starttime, 6)), open_list, close_list
    else:
        # Tidak ditemukan jalur
        return (0, round(endtime - starttime, 6))


# Fungsi utama sebagai pengganti method() lama
def method(matrix, start, goal, hchoice):
    return bidirectional_search(matrix, start, goal, hchoice)