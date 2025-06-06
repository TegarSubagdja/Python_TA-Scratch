def barrierRaster(awal, akhir, peta):
    jumlah = 0
    x1, y1 = awal
    x2, y2 = akhir

    max_y = len(peta)
    max_x = len(peta[0]) if max_y > 0 else 0

    for i in range(y1, min(y2, max_y)):
        for j in range(x1, min(x2, max_x)):
            if peta[i][j] == 1:
                jumlah += 1

    lebar = x2 - x1
    tinggi = y2 - y1
    luas = lebar * tinggi if lebar * tinggi > 0 else 1
    koeficien = jumlah / luas

    return koeficien
