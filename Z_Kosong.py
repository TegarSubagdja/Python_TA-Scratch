import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Baca file Excel
df = pd.read_excel("Hasil_Pengujian_Map_1_128.xlsx")

# Ukuran map dan algoritma
map_labels = ['16', '32', '64', '128']
algoritmas = df['Kombinasi'].tolist()
jumlah_algo = len(algoritmas)
x = np.arange(len(map_labels))  # [0, 1, 2, 3]

# Lebar tiap batang
bar_width = 0.1

# Setup plot
plt.figure(figsize=(12, 6))

# Buat satu bar untuk setiap algoritma dengan offset
for i in range(7):
    waktu = df.loc[i, map_labels].values
    plt.bar(x + i * bar_width, waktu, width=bar_width, label=algoritmas[i])

# Atur sumbu X
plt.xticks(x + (jumlah_algo - 1) * bar_width / 2, map_labels)
plt.xlabel('Ukuran Map')
plt.ylabel('Waktu Eksekusi (detik)')
plt.title('Perbandingan Waktu Eksekusi Setiap Algoritma dalam Diagram Batang')
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
