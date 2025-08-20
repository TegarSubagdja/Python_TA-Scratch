from Utils import *
import pandas as pd
import os

df = pd.read_excel(r'D:\SEMHAS\TA_Python_Server\Excel\Vertical\hasil_gabungan_semua_sheet.xlsx')

print(df.head())

df = df[
    (df['Kombinasi'] == 'A*') 
    # (df['Ukuran'] == 16)
][['Kombinasi', 'Map', 'Ukuran', 'Waktu Pencarian', 'Jumlah Simpul', 'Jumlah Belok']]

df['Map'] = df['Map'].mask(df['Map'].duplicated(), '')
df['Kombinasi'] = df['Kombinasi'].mask(df['Kombinasi'].duplicated(), '')

# Tambahkan kolom baru untuk standar deviasi
df['std_waktu'] = df['Waktu Pencarian'].std()
df['std_simpul'] = df['Jumlah Simpul'].std()
df['std_belok'] = df['Jumlah Belok'].std()

# Simpan ke Excel
df.to_excel(r"D:\SEMHAS\Data\Part.xlsx", index=False)

os.startfile(r"D:\SEMHAS\Data\Part.xlsx")

print(df)
