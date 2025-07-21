import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


file = ["Map", "Map_1", "Map_2", "Map_3", "Map_4"]

for fl in file:

    # Baca file Excel
    df = pd.read_excel(f"Hasil_Pengujian_{fl}_128_avg_length.xlsx")

    print(df.head())