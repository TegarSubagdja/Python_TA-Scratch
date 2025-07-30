import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def grafik(sheet, label, algorithms):
    data = {}
    list = ['A','B','C','D','E']

    # Ambil data dari semua map
    for i in range(1, 6):
        map = i - 1
        if map < 1:
            map = "Map"
        else:
            map = f"Map_{map}"
        df = pd.read_excel(f'Excel/Validasi/Hasil_Pengujian_{map}_128_avg_length.xlsx', sheet_name=sheet)
        # Bersihkan spasi di kolom Kombinasi
        df['Kombinasi'] = df['Kombinasi'].str.strip()
        baris = df[df['Kombinasi'].isin(algorithms)]
        data[f"Map {list[i-1]}"] = baris.set_index('Kombinasi')

    # Buat layout subplot 3x2
    fig, axs = plt.subplots(3, 2, figsize=(10, 12))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    axs = axs.flatten()

    map_sizes = ['16', '32', '64', '128']

    # PERBAIKAN: Tambahkan JPS-BDS ke dalam colors dan markers
    colors = {
        'A*': '#E84C22',   
        'GL': '#FF8427',   
        'BRC': '#B64926',  
        'TPF': '#912B0F',  
        'BDS': '#FFBD47',  
        'JPS': '#CC9900',  
        'JPS-BDS': '#8B4513',  # Tambahkan warna untuk JPS-BDS
        'PPO': '#B22600'   
    }

    markers = {
        'A*': 'o', 'GL': 'o', 'BRC': 'o', 'TPF': 'o',
        'BDS': '*', 'JPS': '*', 'JPS-BDS': '*', 'PPO': 'o'  # Tambahkan marker untuk JPS-BDS
    }

    for i, (key, values) in enumerate(data.items()):
        # PERBAIKAN: Gunakan algorithms list yang sama untuk line chart
        for algo in algorithms:  # Ganti dari 'colors' ke 'algorithms'
            if algo in values.index:  # Check if algorithm exists in data
                axs[i].plot(map_sizes, values.loc[algo, map_sizes], 
                        marker=markers.get(algo, 'o'), label=algo, color=colors.get(algo, '#000000'), 
                        linewidth=1, markersize=6, linestyle='--')
        
        axs[i].set_title(key, fontsize=12, fontweight='bold')
        axs[i].grid(True, alpha=0.3)
        axs[i].legend(loc='upper left', fontsize=8)
        
        # Set individual y-axis limits for each subplot
        max_val = 0
        for algo in algorithms:  # Ganti dari 'colors' ke 'algorithms'
            if algo in values.index:
                current_max = values.loc[algo, map_sizes].max()
                if current_max > max_val:
                    max_val = current_max
        
        # Set y-axis limit with 10% padding above the maximum value
        axs[i].set_ylim(0, max_val * 1.1)
        
        # Set y-label only for leftmost plots
        if i in [0, 2, 4]:
            axs[i].set_ylabel(f'{label}', fontsize=10)
        
        # Set x-label only for bottom plots
        if i in [3, 4]:
            axs[i].set_xlabel('Ukuran Map', fontsize=10)

    # Hapus subplot ke-6 jika tidak digunakan
    if len(data) < len(axs):
        fig.delaxes(axs[-1])

    plt.subplots_adjust(hspace=5)
    plt.tight_layout(rect=[0, 0.02, 1, 0.98])
    plt.show()

    # Area Bar Chart
    fig, axs = plt.subplots(3, 2, figsize=(10, 12))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    axs = axs.flatten()

    # PERBAIKAN: Tambahkan JPS-BDS ke hatch_patterns
    hatch_patterns = {
        'A*': '', 'GL': '', 'BRC': '', 'TPF': '',
        'BDS': '', 'JPS': '', 'JPS-BDS': '///', 'PPO': ''  # Tambahkan pattern untuk JPS-BDS
    }

    for i, (key, values) in enumerate(data.items()):
        # Persiapan data untuk bar chart
        x = np.arange(len(map_sizes))
        width = 0.12
        
        # Plot bar untuk setiap algorithm
        for j, algo in enumerate(algorithms):
            if algo in values.index:
                offset = (j - len(algorithms)/2) * width + width/2
                bars = axs[i].bar(x + offset, values.loc[algo, map_sizes], 
                                width, label=algo, color=colors.get(algo, "#B22600"), 
                                alpha=0.8, edgecolor='black', linewidth=0.5,
                                hatch=hatch_patterns.get(algo, '')
                                )
                
                # Tambahkan nilai di atas setiap bar
                for k, bar in enumerate(bars):
                    height = bar.get_height()
                    if height > 0:
                        axs[i].text(bar.get_x() + bar.get_width()/2., height + 0.001,
                                f'{algo}',
                                ha='center', va='bottom', 
                                fontsize=7, rotation=90)
        
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
        
        axs[i].set_ylim(0, max_val * 1.15)
        
        # Set y-label only for leftmost plots
        if i in [0, 2, 4]:
            axs[i].set_ylabel(f'{label}', fontsize=10)
        
        # Set x-label only for bottom plots
        if i in [3, 4]:
            axs[i].set_xlabel('Ukuran Map', fontsize=10)

    # Hapus subplot ke-6 jika tidak digunakan
    if len(data) < len(axs):
        fig.delaxes(axs[-1])

    plt.tight_layout(rect=[0, 0.02, 1, 0.98])
    plt.show()

# Test dengan algoritma yang sama
algorithms = ['JPS','BDS','JPS-BDS']
label="Jumlah"
sheet="Waktu Pencarian"
grafik(sheet, label, algorithms)