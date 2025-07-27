from Utils import *
from Pengujian.GetAverageMap import generate_keseluruhan_excel

def path_length(path):
    if len(path) < 2:
        return 0.0
    return sum(math.dist(path[i], path[i+1]) for i in range(len(path) - 1))

def runPengujianAvgLength(size = [16, 32, 64, 128]):

    def pivot_metric(df, metric_name):
        # Gunakan pivot_table dengan multiindex + agregasi rata-rata
        pivot = df.pivot_table(
            index=["Jumlah Kombinasi", "Kombinasi"],
            columns="Size Map",
            values=metric_name,
            aggfunc="mean"
        )
        # Pastikan semua kolom berupa string (32, 64, ...)
        pivot.columns = [f"{col}" for col in pivot.columns]
        pivot = pivot.reset_index()

        # Tambahkan kolom Rata-rata di paling kanan
        size_columns = [col for col in pivot.columns if col not in ["Jumlah Kombinasi", "Kombinasi"]]
        pivot["Rata-rata"] = pivot[size_columns].mean(axis=1)
        return pivot

    for i in range(5):
        mapChoice = i
        nameMap = "Map" if mapChoice < 1 else f"Map_{mapChoice}"

        # Load Grid
        map = Z_GetMap.load_grid(path=f"Map/JSON/{nameMap}.json", s=True)

        start = (0, 0)
        goal = (map.shape[0] - 1, map.shape[1] - 1)

        np.place(map, map == 1, 255)
        np.place(map, map == 2, 0)
        np.place(map, map == 3, 0)

        kombinasi_flags = list(itertools.product([False, True], repeat=6))
        print(f"Total kombinasi: {len(kombinasi_flags)}\n")
        # print(kombinasi_flags)

        # Kumpulan hasil per sheet
        rows_comb = []
        rows_method = []
        rows_time = []
        rows_path = []
        rows_open = []
        rows_close = []
        rows_turn = []
        rows_size = []
        rows_length = []

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
                tempPaths = []
                tempOpens = []
                tempCloses = []
                tempTurns = []
                tempLengths = []

                for _ in range(10):
                    (path, times), openlist, closelist = Algoritm(
                        map.copy(), start, goal, hchoice=2,
                        JPS=JPS, BDS=BDS, GLF=GLF,
                        BRC=BRC, TPF=TPF, PPO=PPO,
                        show=False, speed=200
                    )

                    tempTimes.append(times)
                    tempPaths.append(len(path))
                    tempLengths.append(path_length(path))
                    tempOpens.append(len(openlist))
                    tempCloses.append(len(closelist))
                    tempTurns.append(len(Turn(path)))

                print(f"{sz} {method_name} - mean_time: {np.mean(tempTimes):.4f}")

                rows_size.append(sz)
                rows_comb.append(len(aktif_flags))
                rows_method.append(method_name)
                rows_time.append(np.mean(tempTimes))
                rows_path.append(np.mean(tempPaths))
                rows_length.append(np.mean(tempLengths))
                rows_open.append(np.mean(tempOpens))
                rows_close.append(np.mean(tempCloses))
                rows_turn.append(np.mean(tempTurns))

        data = pd.DataFrame({
            "Jumlah Kombinasi": rows_comb,
            "Size Map": rows_size,
            "Kombinasi": rows_method,
            "waktu Pencarian": rows_time,
            "Panjang Jalur": rows_path,
            "Panjang Jalur Real": rows_length,
            "Jumlah Open Set": rows_open,
            "Jumlah Close Set": rows_close,
            "Jumlah Belokan": rows_turn,
        })

        # Buat pivot untuk setiap metrik dan tambahkan rata-rata
        pivot_waktu = pivot_metric(data, "waktu Pencarian")
        pivot_panjang = pivot_metric(data, "Panjang Jalur")
        pivot_length_real = pivot_metric(data, "Panjang Jalur Real")
        pivot_open = pivot_metric(data, "Jumlah Open Set")
        pivot_close = pivot_metric(data, "Jumlah Close Set")
        pivot_belok = pivot_metric(data, "Jumlah Belokan")

        # Simpan ke Excel multi-sheet
        with pd.ExcelWriter(f"Excel/Validasi/Hasil_Pengujian_{nameMap}_{size[-1]}_avg_length.xlsx") as writer:
            pivot_waktu.to_excel(writer, sheet_name="Waktu Pencarian", index=False)
            pivot_panjang.to_excel(writer, sheet_name="Panjang Jalur", index=False)
            pivot_length_real.to_excel(writer, sheet_name="Panjang Jalur Real", index=False)
            pivot_open.to_excel(writer, sheet_name="Jumlah Open", index=False)
            pivot_close.to_excel(writer, sheet_name="Jumlah Close", index=False)
            pivot_belok.to_excel(writer, sheet_name="Jumlah Belok", index=False)