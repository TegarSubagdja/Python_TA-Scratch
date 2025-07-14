from Utils import *

# Contoh pemanggilan:
if __name__ == "__main__":

    mapChoice = 1

    if mapChoice < 1:
        nameMap = "Map"
    else:
        nameMap = f"Map_{mapChoice}"

    map = Z_GetMap.load_grid(path=f"Map/JSON/{nameMap}.json", s=True)
    # Z_GetMap.show(map)
    map = Z_GetMap.upscale(map, 16)
    Z_GetMap.show(map, name=nameMap)
    print(map.shape)
    print(map.shape)

    start = (0, 0)
    goal = (map.shape[0] - 4, map.shape[1] - 1)

    np.place(map, map == 1, 255)
    np.place(map, map == 2, 0)
    np.place(map, map == 3, 0)

    (path, times), openlist, closelist = Algoritm(
                    map=map.copy(), 
                    start=start, 
                    goal=goal, 
                    hchoice=2,
                    BRC=False,
                    TPF=False,
                    GLF=False,
                    BDS=True,
                    PPO=False,
                    JPS=True,
                    show=True, speed=1
                )
    print(f"path : {path}")
    print(f"Panjang Path : {len(path)}")
    print(f"Jumlah Open Set : {len(openlist)}")
    print(f"Jumlah Close Set : {len(closelist)}")
    print(f"Jumlah Belokan : {Turn(path)}")
    print(f"Jumlah Belokan : {len(Turn(path))}")
    print(f"Waktu Pencarian : {times}")

    # Stop ke pengujian total
    sys.exit()

    size = [32, 64, 128, 256, 512]

    kombinasi_flags = list(itertools.product([False, True], repeat=6))
    print(f"Total kombinasi: {len(kombinasi_flags)}\n")
    print(kombinasi_flags)

    # Kumpulan hasil per sheet
    rows_comb = []
    rows_method = []
    rows_time = []
    rows_path = []
    rows_open = []
    rows_close = []
    rows_turn = []
    rows_size = []

    awal = time.time()

    for sz in size:

        map = Z_GetMap.upscale(map, sz)

        for flags in kombinasi_flags:
            JPS, BDS, GLF, BRC, TPF, PPO = flags

            aktif_flags = []
            if JPS: aktif_flags.append("JPS")
            if BDS: aktif_flags.append("BDS")
            if GLF: aktif_flags.append("GL")
            if BRC: aktif_flags.append("BRC")
            if TPF: aktif_flags.append("TPF")
            if PPO: aktif_flags.append("PPO")
            method_name = "-".join(aktif_flags) if aktif_flags else "A*"

            start = (0, 0)
            goal = (map.shape[0] - 1, map.shape[1] - 1)

            np.place(map, map == 1, 255)
            np.place(map, map == 2, 0)
            np.place(map, map == 3, 0)

            tempTimes = []
            tempOpen = []
            tempClose = []

            (path, times), openlist, closelist = Algoritm(
                map.copy(), start, goal, hchoice=2,
                JPS=JPS, BDS=BDS, GLF=GLF,
                BRC=BRC, TPF=TPF, PPO=PPO,
                show=False, speed=200
            )

            tempTimes.append(times)

            print(f"{sz} {method_name}")

            rows_size.append(sz)
            rows_comb.append(len(aktif_flags))
            rows_method.append(method_name)
            rows_time.append(np.mean(tempTimes))
            rows_path.append(len(path))
            rows_open.append(len(openlist))
            rows_close.append(len(closelist))
            rows_turn.append(len(Turn(path)))
            

    data = pd.DataFrame({
        "Jumlah Kombinasi" : rows_comb,
        "Size Map" : rows_size,
        "Kombinasi" : rows_method,
        "waktu Pencarian" : rows_time,
        "Panjang Jalur" : rows_path,
        "Jumlah Open Set" : rows_open,
        "Jumlah Close Set" : rows_close,
        "Jumlah Belokan" : rows_turn
    })

    data.to_excel("output.xlsx", index=False)

    def pivot_metric(df, metric_name):
        # Gunakan pivot_table dengan multiindex + agregasi rata-rata
        pivot = df.pivot_table(
            index=["Jumlah Kombinasi", "Kombinasi"],
            columns="Size Map",
            values=metric_name,
            aggfunc="mean"  # jika terjadi duplikat entry
        )
        # Pastikan semua kolom berupa string (32, 64, ...)
        pivot.columns = [f"{col}" for col in pivot.columns]
        return pivot.reset_index()

    # Pivot masing-masing metrik
    pivot_waktu = pivot_metric(data, "waktu Pencarian")
    pivot_panjang = pivot_metric(data, "Panjang Jalur")
    pivot_open = pivot_metric(data, "Jumlah Open Set")
    pivot_close = pivot_metric(data, "Jumlah Close Set")
    pivot_belok = pivot_metric(data, "Jumlah Belokan")

    akhir = time.time()
    waktu = akhir - awal
    
    # Simpan semua ke dalam satu file Excel (multi-sheet)
    with pd.ExcelWriter(f"Hasil_Pengujian_{size[-1]}_{waktu}.xlsx") as writer:
        pivot_waktu.to_excel(writer, sheet_name="Waktu Pencarian", index=False)
        pivot_panjang.to_excel(writer, sheet_name="Panjang Jalur", index=False)
        pivot_open.to_excel(writer, sheet_name="Jumlah Open", index=False)
        pivot_close.to_excel(writer, sheet_name="Jumlah Close", index=False)
        pivot_belok.to_excel(writer, sheet_name="Jumlah Belok", index=False)

    os.startfile(f"D:\SEMHAS\TA_Python_Server\Hasil_Pengujian_{size[-1]}_{waktu}.xlsx")




