import pandas as pd
import numpy as np
import os

sheets = ['Waktu Pencarian', 'Panjang Jalur', 'Panjang Jalur Real', 'Jumlah Open', 'Jumlah Close', 'Jumlah Belok']

# Pastikan folder tujuan ada
os.makedirs('Excel/Rekap', exist_ok=True)

# Buat satu file Excel dengan multi-sheet
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

        # Gabungkan semua DataFrame berdasarkan Kombinasi
        for df in dfs:
            if df_combined is None:
                df_combined = df
            else:
                df_combined = pd.merge(df_combined, df, on='Kombinasi')

        # Simpan ke sheet bernama sesuai variabel `sheet`
        df_combined.to_excel(writer, sheet_name=sheet[:31], index=False)  # max 31 chars for Excel sheet names

        print(f"\n✅ Sheet '{sheet}' berhasil disimpan:")
        print(df_combined)
