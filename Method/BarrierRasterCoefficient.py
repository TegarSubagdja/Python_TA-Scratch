import numpy as np

def barrierRaster(awal, akhir, peta):
    x1, y1 = awal
    x2, y2 = akhir

    # Pastikan batas tidak keluar peta
    y2 = min(y2, peta.shape[0])
    x2 = min(x2, peta.shape[1])

    area = peta[y1:y2, x1:x2]  # Ambil potongan area

    jumlah = np.count_nonzero(area == 255)  # Hitung jumlah 255 lebih cepat
    lebar = x2 - x1
    tinggi = y2 - y1
    luas = lebar * tinggi if lebar * tinggi > 0 else 1

    return jumlah / luas