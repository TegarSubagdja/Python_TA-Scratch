from Utils import *
import pandas as pd
import os

df = pd.read_excel(r'D:\SEMHAS\TA_Python_Server\Excel\Vertical\hasil_gabungan_semua_sheet.xlsx')

print(df.head())


df = df[
    (df['Kombinasi'].isin(['A*'])) 
    # (df['Ukuran'] == 16)
][['Kombinasi', 'Map', 'Ukuran', 'Waktu Pencarian', 'Jumlah Simpul', 'Jumlah Belok', 'Panjang Jalur Real',]]

df['Map'] = df['Map'].mask(df['Map'].duplicated(), '')
df['Kombinasi'] = df['Kombinasi'].mask(df['Kombinasi'].duplicated(), '')

# Tambahkan kolom baru untuk standar deviasi
df['std_waktu'] = df['Waktu Pencarian'].std()
df['std_simpul'] = df['Jumlah Simpul'].std()
df['std_belok'] = df['Jumlah Belok'].std()

# Simpan ke Excel
df.to_excel(r"D:\SEMHAS\Data\Part.xlsx", index=False)
# os.startfile(r"D:\SEMHAS\TA_Python_Server\Excel\Vertical\hasil_gabungan_semua_sheet.xlsx")
# os.startfile(r"D:\SEMHAS\Data\Part.xlsx")

# Asumsikan df sudah ada dan kolom sudah benar
df["Map"] = df["Map"].replace("", pd.NA).ffill()
avg = df.groupby("Map")["Waktu Pencarian"].apply(lambda x: x / x.shift(1)).mean()
persen = (avg-1)*100
print(f"{persen:.0f}")

# Hitung persentase reduksi untuk setiap baris
df = pd.read_excel(r'D:\SEMHAS\Grafik\hasil_gabungan_transpose_Jumlah Belok.xlsx')
df["PPO%"] = (df["A*"] - df["PPO"]) / df["A*"] * 100
df["JBP%"] = (df["A*"] - df["JBP"]) / df["A*"] * 100
df["JGBP%"] = (df["A*"] - df["JGBP"]) / df["A*"] * 100

print(f'Di total dan di rata - rata {df["JGBP%"].mean():.3f}')

print(f"Rata rata penurunan PPO {df['PPO%'].std(ddof=1):.3f}")
print(f"Rata rata penurunan JBP {df['JBP%'].std(ddof=1):.3f}")
print(f"Rata rata penurunan JGBP {df['JGBP%'].std(ddof=1):.3f}")

# print(f"Mean PPO {df["BRC_%"].mean():.0f}")
# print(f"Mean JPS {df["JPS_%"].mean():.0f}")