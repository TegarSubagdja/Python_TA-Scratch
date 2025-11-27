from Utils import *
import pandas as pd
import os

# Simpan print asli
old_print = print

def print(*args, **kwargs):
    new_args = []
    for arg in args:
        if isinstance(arg, float):
            # Format angka float → ganti '.' dengan ','
            arg = str(arg).replace('.', ',')
        else:
            arg = str(arg).replace('.', ',') if isinstance(arg, str) else arg
        new_args.append(arg)
    old_print(*new_args, **kwargs)

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

namaFile = "Panjang Jalur Real"

file = f"D:\SEMHAS\Grafik\Rename\hasil_gabungan_transpose_{namaFile}_Rename.xlsx"

# Hitung persentase reduksi untuk setiap baris
df = pd.read_excel(file)
df["JBP%"] = (df["A*"] - df["JBP"]) / df["A*"] * 100
df["JGBP%"] = (df["A*"] - df["JGBP"]) / df["A*"] * 100
df["JGBP%"] = (df["A*"] - df["JGBP"]) / df["A*"] * 100
df["JGBP%"] = (df["A*"] - df["JGBP"]) / df["A*"] * 100
df["JGBP%"] = (df["A*"] - df["JGBP"]) / df["A*"] * 100
# df["JGBP%"] = (df["A*"] - df["JGBP"]) / df["A*"] * 100

print(df[["Map","JBP%", "JGBP%"]])

mean_row = pd.DataFrame({
    "Map": ["Rata-rata"],
    "JBP%": [df["JBP%"].mean()],
    "JGBP%": [df["JGBP%"].mean()]
})

std_row = pd.DataFrame({
    "Map": ["Std"],
    "JBP%": [df["JBP%"].std()],
    "JGBP%": [df["JGBP%"].std()]
})

print(df)

df_out = pd.concat([df[["Map","Ukuran","JBP%", "JGBP%"]], mean_row, std_row], ignore_index=True)

df_out[["Map","Ukuran","JBP%", "JGBP%"]].to_excel(f'Perbandingan_{namaFile}_Avg.xlsx')

# df[["Map","JBP%", "JGBP%"]].to_excel(f'Perbandingan_{namaFile}.xlsx')

print(df)

print(f"Mean JBP {df["JBP%"].mean():.3f}")
print(f"Mean JGBP {df["JGBP%"].mean():.3f}")
print(f"Std JBP {df["JBP%"].std(ddof=1):.3f}")
print(f"Std JGBP {df["JGBP%"].std(ddof=1):.3f}")