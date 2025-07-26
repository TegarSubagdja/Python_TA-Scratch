import pandas as pd
import numpy as np 
import os

sheets = ['Waktu Pencarian', 'Panjang Jalur', 'Panjang Jalur Real', 'Jumlah Open', 'Jumlah Close', 'Jumlah Belok']

for sheet in sheets:
    dfs = []               # reset untuk setiap sheet
    df_combined = None     # reset juga

    for i in range(5):
        if i < 1:
            map_name = "Map"
        else:
            map_name = f"Map_{i}"

        df = pd.read_excel(f'Excel/Validasi/Hasil_Pengujian_{map_name}_128_avg_length.xlsx', sheet_name=sheet)
        df = df[['Kombinasi', 'Rata-rata']].copy()

        df = df.rename(columns={'Rata-rata': f'Rata-rata Map {i+1}'})

        dfs.append(df)

    # Gabungkan semua df berdasarkan Kombinasi
    for df in dfs:
        if df_combined is None:
            df_combined = df
        else:
            df_combined = pd.merge(df_combined, df, on='Kombinasi')

    # Simpan hasil
    os.makedirs('Excel/Rekap', exist_ok=True)
    df_combined.to_excel(f'Excel/Rekap/Keseluruhan_{sheet}.xlsx', index=False)
    df_combined.to_csv(f'Excel/Rekap/Keseluruhan_{sheet}.csv', index=False)

    print(f"\nSheet: {sheet}")
    print(df_combined)
