import numpy as np

def barrierRaster(awal, akhir, peta):
    x1, y1 = awal
    x2, y2 = akhir

    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])

    area = peta[x1:x2+1, y1:y2+1]  # Ambil potongan area

    jumlah = np.count_nonzero(area == 255)  # Hitung jumlah 255 lebih cepat
    lebar = x2 - x1
    tinggi = y2 - y1
    luas = lebar * tinggi if lebar * tinggi > 0 else 1

    # print(f" >>>> current {awal} {akhir} Jumlahnya adalah : {jumlah} dan luas {luas}")
    # print(area)

    return jumlah / luas