import pandas as pd
import numpy as np
import os
from Pengujian.GetAverageAll import rekap_avg_semua_sheet
from Utils import *

# def RataSetiapUkurandanSetiapMap():
#     sheets = ['Waktu Pencarian', 'Panjang Jalur', 'Panjang Jalur Real',
#               'Jumlah Open', 'Jumlah Close', 'Jumlah Belok']
    
#     size = [16, 32, 64, 128]

#     os.makedirs('Excel/Rekap', exist_ok=True)

#     for sz in size:
#         with pd.ExcelWriter(f'Excel/Avg/Rata-rata-{sz}.xlsx', engine='xlsxwriter') as writer:
#             for sheet in sheets:
#                 dfs = []
#                 df_combined = None

#                 for i in range(5):
#                     map_name = "Map" if i < 1 else f"Map_{i}"
#                     df = pd.read_excel(
#                         f'Excel/Validasi/Hasil_Pengujian_{map_name}_128_avg_length.xlsx',
#                         sheet_name=sheet
#                     )
#                     df = df[['Kombinasi', f'{sz}']].copy()
#                     df = df.rename(columns={f'{sz}': f'Map {i+1}'})
#                     dfs.append(df)

#                 for df in dfs:
#                     if df_combined is None:
#                         df_combined = df
#                     else:
#                         df_combined = pd.merge(df_combined, df, on='Kombinasi')

#                 # ✅ Tambahkan kolom avg
#                 df_combined['avg'] = df_combined[[f'Map {i+1}' for i in range(5)]].mean(axis=1)

#                 # Simpan ke Excel
#                 df_combined.to_excel(writer, sheet_name=sheet[:31], index=False)
#                 print(f"\n✅ Sheet '{sheet}' berhasil disimpan:")
#                 print(df_combined)

# def GabungHasilFungsiAtas():
#     sheets = ['Waktu Pencarian', 'Panjang Jalur', 'Panjang Jalur Real',
#               'Jumlah Open', 'Jumlah Close', 'Jumlah Belok']
    
#     size = [16, 32, 64, 128]

#     os.makedirs('Excel/Rekap', exist_ok=True)

#     with pd.ExcelWriter(f'Excel/Avg/Rata-rata-All-Map.xlsx', engine='xlsxwriter') as writer:
#         for sheet in sheets:
#             dfs = []
#             df_combined = None

#             for sz in size:
#                 df = pd.read_excel(
#                     f'Excel/Avg/Rata-rata-{sz}.xlsx',
#                     sheet_name=sheet
#                 )
#                 df = df[['Kombinasi', f'avg']].copy()
#                 df = df.rename(columns={f'avg': f'{sz}'})
#                 dfs.append(df)

#             for df in dfs:
#                 if df_combined is None:
#                     df_combined = df
#                 else:
#                     df_combined = pd.merge(df_combined, df, on='Kombinasi')

#             # ✅ Tambahkan kolom avg
#             df_combined['avg'] = df_combined[[f'{sz}' for sz in size]].mean(axis=1)

#             # Simpan ke Excel
#             df_combined.to_excel(writer, sheet_name=sheet[:31], index=False)
#             print(f"\n✅ Sheet '{sheet}' berhasil disimpan:")
#             print(df_combined)

# RataSetiapUkurandanSetiapMap()
# GabungHasilFungsiAtas()

# for i in range(1, 6):

#     map = 'Map' if i<=1 else f'Map_{i-1}'

#     # Baca file
#     df = pd.read_excel(f'Excel/Validasi/Hasil_Pengujian_{map}_128_avg_length.xlsx')

#     # Filter dulu
#     baris = df[df['Kombinasi'].isin(['A*', 'JPS-BDS-GL-BRC-PPO'])]

#     print(baris, '\n')

#     # Kolom ukuran
#     ukuran_kolom = ['16', '32', '64', '128']

#     # Ubah dari wide ke long
#     hasil = baris.melt(id_vars='Kombinasi', value_vars=ukuran_kolom,
#                     var_name='Ukuran', value_name='Nilai')

#     # Konversi kolom 'Ukuran' ke integer agar bisa disortir numerik
#     hasil['Ukuran'] = hasil['Ukuran'].astype(int)

#     # Urutkan berdasarkan ukuran terkecil → kombinasi
#     hasil = hasil.sort_values(by=['Ukuran', 'Kombinasi']).reset_index(drop=True)

#     print(hasil)



for i in range(10):
    if i == 5:
        continue
    print(i)