import math

def guidline(awal=0, akhir=0, posisi=0):
    x1, y1 = awal
    x2, y2 = akhir
    x0, y0 = posisi
    
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + (x2 * y1) - (y2 * x1))
    denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
    return numerator / denominator