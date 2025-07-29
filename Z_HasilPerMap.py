import pandas as pd

# List penampung semua hasil
semua_hasil = []

sheets = ['Waktu Pencarian', 'Panjang Jalur', 'Panjang Jalur Real',
          'Jumlah Open', 'Jumlah Close', 'Jumlah Belok']

pilih = sheets[5]

# for i in range(1, 6):

#     map_name = 'Map' if i <= 1 else f'Map_{i-1}'

#     # Baca file
#     df = pd.read_excel(f'Excel/Validasi/Hasil_Pengujian_{map_name}_128_avg_length.xlsx', sheet_name=pilih)

#     # Filter kombinasi yang diinginkan
#     baris = df[df['Kombinasi'].isin(['A*', 'JPS-BDS-GL-BRC-PPO'])]

#     # Kolom ukuran
#     ukuran_kolom = ['16', '32', '64', '128']

#     # Ubah dari wide ke long
#     hasil = baris.melt(id_vars='Kombinasi', value_vars=ukuran_kolom,
#                        var_name='Ukuran', value_name='Nilai')

#     # Tambahkan informasi Map ke kolom baru
#     hasil['Map'] = map_name

#     # Konversi ukuran ke int untuk urutan numerik
#     hasil['Ukuran'] = hasil['Ukuran'].astype(int)

#     # Urutkan
#     hasil = hasil.sort_values(by=['Kombinasi', 'Ukuran']).reset_index(drop=True)

#     # Tambahkan ke list
#     semua_hasil.append(hasil)

# # Gabungkan semua hasil
# gabungan = pd.concat(semua_hasil, ignore_index=True)
# gabungan.to_excel(f'hasil_gabungan_vertikal_{pilih}.xlsx', index=False)
# print("Data berhasil disimpan ke 'hasil_gabungan_vertikal.xlsx'")


import pandas as pd

# List semua hasil dari setiap map
semua_gabungan = []

# Loop untuk 5 map
for i in range(1, 6):
    map_name = 'Map' if i == 1 else f'Map_{i-1}'

    file_path = f'Excel/Validasi/Hasil_Pengujian_{map_name}_128_avg_length.xlsx'
    sheet_open = 'Jumlah Open'
    sheet_close = 'Jumlah Close'
    ukuran_kolom = ['16', '32', '64', '128']

    try:
        # Baca sheet
        df_open = pd.read_excel(file_path, sheet_name=sheet_open)
        df_close = pd.read_excel(file_path, sheet_name=sheet_close)
    except Exception as e:
        print(f"❌ Gagal membaca file {file_path}: {e}")
        continue

    # Long format
    open_long = df_open.melt(id_vars='Kombinasi', 
                             value_vars=ukuran_kolom,
                             var_name='Ukuran', value_name='OpenList')

    close_long = df_close.melt(id_vars='Kombinasi', 
                               value_vars=ukuran_kolom,
                               var_name='Ukuran', value_name='CloseList')

    # Gabung
    gabung = pd.merge(open_long, close_long, on=['Kombinasi', 'Ukuran'])

    # Hitung total
    gabung['TotalList'] = gabung['OpenList'] + gabung['CloseList']

    # Filter kombinasi
    gabung = gabung[gabung['Kombinasi'].isin(['A*', 'JPS-BDS-GL-BRC-PPO'])]

    # Konversi dan urutkan
    gabung['Ukuran'] = gabung['Ukuran'].astype(int)
    gabung['Map'] = map_name
    gabung = gabung.sort_values(by=['Ukuran', 'Kombinasi']).reset_index(drop=True)

    # Tambahkan ke list semua hasil
    semua_gabungan.append(gabung)

# Gabungkan semua map
hasil_akhir = pd.concat(semua_gabungan, ignore_index=True)

# Simpan ke file Excel
hasil_akhir.to_excel('hasil_open_close_total.xlsx', index=False)

print("✅ Data dari semua Map berhasil disimpan ke 'hasil_open_close_total.xlsx'")
