import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# data = {}
# list = ['A','B','C','D','E']

# # Ambil data dari semua map
# for i in range(1, 6):
#     map = i - 1
#     if map < 1:
#         map = "Map"
#     else:
#         map = f"Map_{map}"
#     df = pd.read_excel(f'Excel/Validasi/Hasil_Pengujian_{map}_128_avg_length.xlsx')
#     # Bersihkan spasi di kolom Kombinasi
#     df['Kombinasi'] = df['Kombinasi'].str.strip()
#     baris = df[df['Kombinasi'].isin(['A*', 'GL', 'BRC', 'TPF', 'BDS', 'JPS', 'PPO'])]
#     data[f"Map {list[i-1]}"] = baris.set_index('Kombinasi')

# # Buat layout subplot 3x2
# fig, axs = plt.subplots(3, 2, figsize=(10, 12))
# plt.subplots_adjust(hspace=0.4, wspace=0.3)
# axs = axs.flatten()

# map_sizes = ['16', '32', '64', '128']

# colors = {
#     'A*': '#E84C22',   
#     'GL': '#FF8427',   
#     'BRC': '#B64926',  
#     'TPF': '#912B0F',  
#     'BDS': '#FFBD47',  
#     'JPS': '#CC9900',  
#     'PPO': '#B22600'   
# }

# markers = {
#     'A*': 'o', 'GL': 'o', 'BRC': 'o', 'TPF': 'o',
#     'BDS': '*', 'JPS': '*', 'PPO': 'o'
# }

# for i, (key, values) in enumerate(data.items()):
#     # Plot each algorithm
#     for algo in colors:
#         if algo in values.index:  # Check if algorithm exists in data
#             axs[i].plot(map_sizes, values.loc[algo, map_sizes], 
#                        marker=markers[algo], label=algo, color=colors[algo], 
#                        linewidth=1, markersize=6, linestyle=':')
    
#     axs[i].set_title(key, fontsize=12, fontweight='bold')
#     axs[i].grid(True, alpha=0.3)
#     axs[i].legend(loc='upper left', fontsize=8)
    
#     # Set individual y-axis limits for each subplot
#     # Get the maximum value for this map and add some padding
#     max_val = 0
#     for algo in colors:
#         if algo in values.index:
#             current_max = values.loc[algo, map_sizes].max()
#             if current_max > max_val:
#                 max_val = current_max
    
#     # Set y-axis limit with 10% padding above the maximum value
#     axs[i].set_ylim(0, max_val * 1.1)
    
#     # Set y-label only for leftmost plots
#     if i in [0, 2, 4]:
#         axs[i].set_ylabel('Waktu (s)', fontsize=10)
    
#     # Set x-label only for bottom plots
#     if i in [3, 4]:
#         axs[i].set_xlabel('Ukuran Map', fontsize=10)

# # Hapus subplot ke-6 jika tidak digunakan
# if len(data) < len(axs):
#     fig.delaxes(axs[-1])

# fig.suptitle('Waktu Pencarian', fontsize=16, fontweight='bold')
# plt.subplots_adjust(hspace=5)
# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.show()

data = {}
list = ['A','B','C','D','E']

# Ambil data dari semua map
for i in range(1, 6):
    map = i - 1
    if map < 1:
        map = "Map"
    else:
        map = f"Map_{map}"
    df = pd.read_excel(f'Excel/Validasi/Hasil_Pengujian_{map}_128_avg_length.xlsx')
    # Bersihkan spasi di kolom Kombinasi
    df['Kombinasi'] = df['Kombinasi'].str.strip()
    baris = df[df['Kombinasi'].isin(['A*', 'GL', 'BRC', 'TPF', 'BDS', 'JPS', 'PPO'])]
    data[f"Map {list[i-1]}"] = baris.set_index('Kombinasi')

# Buat layout subplot 3x2
fig, axs = plt.subplots(3, 2, figsize=(7, 8))
plt.subplots_adjust(hspace=0.4, wspace=0.3)
axs = axs.flatten()

map_sizes = ['16', '32', '64', '128']
algorithms = ['A*', 'GL', 'BRC', 'TPF', 'BDS', 'JPS', 'PPO']

colors = {
    'A*': '#E84C22',   
    'GL': '#FF8427',   
    'BRC': '#B64926',  
    'TPF': '#912B0F',  
    'BDS': '#FFBD47',  
    'JPS': '#CC9900',  
    'PPO': '#B22600'   
}

for i, (key, values) in enumerate(data.items()):
    # Persiapan data untuk bar chart
    x = np.arange(len(map_sizes))  # posisi x untuk setiap ukuran map
    width = 0.12  # lebar setiap bar
    
    # Plot bar untuk setiap algorithm
    for j, algo in enumerate(algorithms):
        if algo in values.index:
            # Offset posisi x untuk setiap algorithm
            offset = (j - len(algorithms)/2) * width + width/2
            bars = axs[i].bar(x + offset, values.loc[algo, map_sizes], 
                             width, label=algo, color=colors[algo], 
                             alpha=0.8, edgecolor='black', linewidth=0.5)
            
            # Tambahkan nilai di atas setiap bar (opsional)
            for k, bar in enumerate(bars):
                height = bar.get_height()
                if height > 0:  # hanya tampilkan jika nilai > 0
                    axs[i].text(bar.get_x() + bar.get_width()/2., height + 0.004,
                            #    f'{height}', 
                               f'{algo}',
                               ha='center', va='bottom', 
                               fontsize=5, rotation=90)
    
    axs[i].set_title(key, fontsize=12, fontweight='bold')
    axs[i].grid(True, alpha=0.3, axis='y')
    axs[i].legend(loc='upper left', fontsize=7, ncol=2)
    
    # Set x-axis
    axs[i].set_xticks(x)
    axs[i].set_xticklabels(map_sizes)
    
    # Set individual y-axis limits for each subplot
    max_val = 0
    for algo in algorithms:
        if algo in values.index:
            current_max = values.loc[algo, map_sizes].max()
            if current_max > max_val:
                max_val = current_max
    
    # Set y-axis limit with 15% padding above the maximum value (lebih besar untuk text)
    axs[i].set_ylim(0, max_val * 1.15)
    
    # Set y-label only for leftmost plots
    if i in [0, 2, 4]:
        axs[i].set_ylabel('Waktu (s)', fontsize=10)
    
    # Set x-label only for bottom plots
    if i in [3, 4]:
        axs[i].set_xlabel('Ukuran Map', fontsize=10)

# Hapus subplot ke-6 jika tidak digunakan
if len(data) < len(axs):
    fig.delaxes(axs[-1])

fig.suptitle('Waktu Pencarian', fontsize=16, fontweight='bold')
plt.subplots_adjust(hspace=10)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()