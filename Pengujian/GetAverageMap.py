# generate_keseluruhan.py

import pandas as pd
import numpy as np
import os
from Pengujian.GetAverageAll import rekap_avg_semua_sheet

def generate_keseluruhan_excel():
    sheets = ['Waktu Pencarian', 'Panjang Jalur', 'Panjang Jalur Real',
              'Jumlah Open', 'Jumlah Close', 'Jumlah Belok']

    os.makedirs('Excel/Rekap', exist_ok=True)

    with pd.ExcelWriter('Excel/Rekap/Keseluruhan_All.xlsx', engine='xlsxwriter') as writer:
        for sheet in sheets:
            dfs = []
            df_combined = None

            for i in range(5):
                map_name = "Map" if i < 1 else f"Map_{i}"
                df = pd.read_excel(
                    f'Excel/Validasi/Hasil_Pengujian_{map_name}_128_avg_length.xlsx',
                    sheet_name=sheet
                )
                df = df[['Kombinasi', 'Rata-rata']].copy()
                df = df.rename(columns={'Rata-rata': f'Map {i+1}'})
                dfs.append(df)

            for df in dfs:
                if df_combined is None:
                    df_combined = df
                else:
                    df_combined = pd.merge(df_combined, df, on='Kombinasi')

            # ✅ Tambahkan kolom avg
            df_combined['avg'] = df_combined[[f'Map {i+1}' for i in range(5)]].mean(axis=1)

            # Simpan ke Excel
            df_combined.to_excel(writer, sheet_name=sheet[:31], index=False)
            print(f"\n✅ Sheet '{sheet}' berhasil disimpan:")
            print(df_combined)
