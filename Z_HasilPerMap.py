import pandas as pd

sheets = ['Waktu Pencarian', 'Panjang Jalur', 'Panjang Jalur Real',
          'Jumlah Open', 'Jumlah Close', 'Jumlah Belok', 'Jumlah Simpul']

# Ukuran kolom yang akan dijumlahkan
ukuran_kolom = ['16', '32', '64', '128']

# Loop untuk 5 file map
for i in range(1, 6):
    map_name = 'Map' if i == 1 else f'Map_{i-1}'
    file_path = f'Excel/Validasi/Hasil_Pengujian_{map_name}_128_avg_length.xlsx'

    # Baca sheet 'Jumlah Open' dan 'Jumlah Close'
    df_open = pd.read_excel(file_path, sheet_name='Jumlah Open')
    df_close = pd.read_excel(file_path, sheet_name='Jumlah Close')

    # Pastikan kedua DataFrame memiliki baris dan kolom yang cocok
    assert df_open.shape == df_close.shape, "Ukuran sheet tidak cocok"
    assert all(df_open['Kombinasi'] == df_close['Kombinasi']), "Kombinasi tidak cocok"

    # Salin kolom Kombinasi
    df_result = df_open[['Kombinasi']].copy()

    # Jumlahkan kolom ukuran
    for col in ukuran_kolom:
        df_result[col] = df_open[col] + df_close[col]

    # Tulis sheet baru ke file yang sama
    with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df_result.to_excel(writer, sheet_name='Jumlah Simpul', index=False)

    print(f"Selesai memproses: {file_path}")

for sheet in sheets:
    semua_hasil = []
    for i in range(1, 6):

        map_name = 'Map' if i <= 1 else f'Map_{i-1}'

        # Baca file
        df = pd.read_excel(f'Excel/Validasi/Hasil_Pengujian_{map_name}_128_avg_length.xlsx', sheet_name=sheet)

        # Filter kombinasi yang diinginkan
        baris = df[df['Kombinasi'].isin(['A*', 'JPS', 'GL', 'BRC', 'PPO'])]

        print(baris)

        # Kolom ukuran
        ukuran_kolom = ['16', '32', '64', '128']

        # Ubah dari wide ke long
        hasil = baris.melt(id_vars='Kombinasi', value_vars=ukuran_kolom,
                        var_name='Ukuran', value_name='Nilai')

        # Tambahkan informasi Map ke kolom baru
        hasil['Map'] = map_name

        # Konversi ukuran ke int untuk urutan numerik
        hasil['Ukuran'] = hasil['Ukuran'].astype(int)

        # Urutkan
        hasil = hasil.sort_values(by=['Map', 'Ukuran']).reset_index(drop=True)

        # Tambahkan ke list
        semua_hasil.append(hasil)

    # Gabungkan semua hasil
    gabungan = pd.concat(semua_hasil, ignore_index=True)
    gabungan.to_excel(f'Excel/Vertical/hasil_gabungan_vertikal_{sheet}.xlsx', index=False)
    print("Data berhasil disimpan ke 'hasil_gabungan_vertikal.xlsx'")


# Inisialisasi dictionary untuk menyimpan hasil per sheet
data_by_sheet = {}

# Loop untuk membaca dan proses tiap sheet
for sheet in sheets:
    semua_hasil = []
    for i in range(1, 6):
        map_name = 'Map' if i == 1 else f'Map_{i-1}'

        df = pd.read_excel(f'Excel/Validasi/Hasil_Pengujian_{map_name}_128_avg_length.xlsx', sheet_name=sheet)

        # Filter hanya kombinasi yang diinginkan
        baris = df[df['Kombinasi'].isin(['A*', 'JPS', 'GL', 'BRC', 'PPO'])]

        # Kolom ukuran
        ukuran_kolom = ['16', '32', '64', '128']

        # Ubah format ke long
        hasil = baris.melt(id_vars='Kombinasi', value_vars=ukuran_kolom,
                           var_name='Ukuran', value_name=sheet)

        hasil['Map'] = map_name
        hasil['Ukuran'] = hasil['Ukuran'].astype(int)

        semua_hasil.append(hasil)

    # Gabung semua hasil untuk satu sheet
    data_by_sheet[sheet] = pd.concat(semua_hasil, ignore_index=True)

# Gabungkan semua data berdasarkan Kombinasi, Map, Ukuran
from functools import reduce

# Ambil semua dataframe dalam list
merged_data = reduce(lambda left, right: pd.merge(left, right, on=['Kombinasi', 'Map', 'Ukuran']), data_by_sheet.values())

# Simpan ke Excel
merged_data.to_excel('Excel/Vertical/hasil_gabungan_semua_sheet.xlsx', index=False)
print("Data berhasil disimpan ke 'hasil_gabungan_semua_sheet.xlsx'")


import pandas as pd

sheets = ['Waktu Pencarian', 'Panjang Jalur', 'Panjang Jalur Real',
          'Jumlah Open', 'Jumlah Close', 'Jumlah Belok', 'Jumlah Simpul']

for sheet in sheets:
    semua_hasil = []

    for i in range(1, 6):
        map_name = 'Map' if i <= 1 else f'Map_{i-1}'
        df = pd.read_excel(f'Excel/Validasi/Hasil_Pengujian_{map_name}_128_avg_length.xlsx', sheet_name=sheet)
        baris = df[df['Kombinasi'].isin(['A*', 'JPS', 'GL', 'BRC', 'PPO'])]

        ukuran_kolom = ['16', '32', '64', '128']
        hasil = baris.melt(id_vars='Kombinasi', value_vars=ukuran_kolom,
                           var_name='Ukuran')

        hasil['Map'] = map_name
        hasil['Ukuran'] = hasil['Ukuran'].astype(int)
        hasil = hasil.sort_values(by=['Kombinasi', 'Ukuran']).reset_index(drop=True)

        semua_hasil.append(hasil)

    # Gabungkan semua hasil
    gabungan = pd.concat(semua_hasil, ignore_index=True)

    # Pisahkan data A* dan Optimized
    data_astar = gabungan[gabungan['Kombinasi'] == 'A*'].copy().reset_index(drop=True)
    data_opt = gabungan[gabungan['Kombinasi'] == 'A*', 'JPS', 'GL', 'BRC', 'PPO'].copy().reset_index(drop=True)

    # Hitung persentase perubahan
    df_perbandingan = data_astar.copy()
    df_perbandingan['Optimized'] = data_opt['Nilai']
    df_perbandingan['Persentase Perubahan (%)'] = (((data_astar['Nilai'] - data_opt['Nilai']) / data_astar['Nilai']))

    # Tambahkan label peningkatan atau penurunan
    df_perbandingan['Peningkatan'] = df_perbandingan['Persentase Perubahan (%)'].apply(
        lambda x: 'Naik' if x > 0 else 'Turun' if x < 0 else 'Tetap'
    )

    # Simpan ke Excel
    df_perbandingan.to_excel(f'Excel/Vertical/perbandingan_{sheet}.xlsx', index=False)
    print(f"Data perbandingan berhasil disimpan ke 'perbandingan_{sheet}.xlsx'")



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
hasil_akhir.to_excel('Excel/Vertical/hasil_open_close_total.xlsx', index=False)

print("✅ Data dari semua Map berhasil disimpan ke 'hasil_open_close_total.xlsx'")
