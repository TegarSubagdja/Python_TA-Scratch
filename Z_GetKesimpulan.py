import pandas as pd
import os

# Nama-nama sheet
sheets = ['Waktu Pencarian', 'Panjang Jalur', 'Panjang Jalur Real',
          'Jumlah Open', 'Jumlah Close', 'Jumlah Belok']

# Baca semua sheet
df_all = pd.read_excel('Excel/Rekap/Keseluruhan_All.xlsx', sheet_name=None)

# DataFrame final
df_result = None

for sheet in sheets:
    df = df_all[sheet][['Kombinasi', 'avg']].copy()
    df = df.rename(columns={'avg': sheet})
    
    if df_result is None:
        df_result = df
    else:
        df_result = pd.merge(df_result, df, on='Kombinasi')

# Simpan ke Excel satu sheet
os.makedirs('Excel/Rekap', exist_ok=True)
df_result.to_excel('Excel/Rekap/Rekap_Avg_SemuaSheet.xlsx', index=False)

print("✅ File berhasil dibuat: Excel/Rekap/Rekap_Avg_SemuaSheet.xlsx")
print(df_result)
