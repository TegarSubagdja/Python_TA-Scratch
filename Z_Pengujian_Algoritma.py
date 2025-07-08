from Utils import *

def get(grid_size, jumlah_rintangan):
    grid = np.zeros((grid_size, grid_size), dtype=int)

    for _ in range(jumlah_rintangan):
        # Titik awal acak, pastikan aman untuk area 2x2
        row = random.randint(0, grid_size - 2)
        col = random.randint(0, grid_size - 2)

        # Isi 4 titik berdekatan (2x2 area)
        val = 255
        grid[row, col] = val
        grid[row + 1, col] = val
        grid[row, col + 1] = val
        grid[row + 1, col + 1] = val

    return grid

def run(map=None, show=False, size=[32, 64, 128]):

    if map is not None:
        map_awal = Visualize.load_grid()
    else:
        map_awal = map

    kombinasi_flags = list(itertools.product([False, True], repeat=6))
    print(f"Total kombinasi: {len(kombinasi_flags)}\n")

    # Dictionary besar untuk simpan semua metrik
    hasil_time = []
    hasil_path = []
    hasil_open = []
    hasil_close = []

    for flags in kombinasi_flags:
        JPS, BDS, GLF, BRC, TPF, PPO = flags

        aktif_flags = []
        if BDS: aktif_flags.append("BDS")
        if PPO: aktif_flags.append("PPO")
        if BRC: aktif_flags.append("BRC")
        if GLF: aktif_flags.append("GLM")
        if TPF: aktif_flags.append("TPF")
        if JPS: aktif_flags.append("JPS")
        method_name = "-".join(aktif_flags) if aktif_flags else "DEFAULT"

        aktif_count = len(aktif_flags)  # Hitung jumlah flag aktif

        row_time = {"count": aktif_count, "method": method_name}
        row_path = {"count": aktif_count, "method": method_name}
        row_open = {"count": aktif_count, "method": method_name}
        row_close = {"count": aktif_count, "method": method_name}


        for sz in size:
            map_ = Visualize.upscale(map_awal, sz)
            start = (0, 0)
            goal = map_.shape[0] - 1, map_.shape[1] - 1

            np.place(map_, map_ == 1, 255)
            map_[start] = 2
            map_[goal] = 3

            times_list = []
            path_lens = []
            open_lens = []
            close_lens = []

            for _ in range(10):
                (path, times), openlist, closelist = Algoritm(
                    map_.copy(), start, goal, hchoice=2,
                    JPS=JPS, BDS=BDS, GLF=GLF,
                    BRC=BRC, TPF=TPF, PPO=PPO,
                    show=show, speed=200
                )
                times_list.append(times)
                if path:
                    path_lens.append(len(path))
                    open_lens.append(len(openlist))
                    close_lens.append(len(closelist))

            row_time[str(sz)] = np.mean(times_list)
            row_path[str(sz)] = np.mean(path_lens) if path_lens else 0
            row_open[str(sz)] = np.mean(open_lens) if open_lens else 0
            row_close[str(sz)] = np.mean(close_lens) if close_lens else 0

            print(f"{method_name:20} | {sz} | Time: {row_time[str(sz)]:.6f} | Path: {row_path[str(sz)]:.1f}")

        hasil_time.append(row_time)
        hasil_path.append(row_path)
        hasil_open.append(row_open)
        hasil_close.append(row_close)

    # Simpan ke satu file dengan sheet berbeda
    with pd.ExcelWriter("Data/Pengujian/hasil_pengujian_512_Avg10_AllComb.xlsx") as writer:
        pd.DataFrame(hasil_time).to_excel(writer, sheet_name="Time", index=False)
        pd.DataFrame(hasil_path).to_excel(writer, sheet_name="Path Length", index=False)
        pd.DataFrame(hasil_open).to_excel(writer, sheet_name="Open Set", index=False)
        pd.DataFrame(hasil_close).to_excel(writer, sheet_name="Close Set", index=False)
    print("\n✅ Semua file berhasil disimpan secara terpisah dan rapi.")

def runMethod(JPS=False, BDS=False, GLF=False, BRC=False, TPF=False, PPO=False, show=False, size=[32, 64, 128]):
    sizes = [32, 64, 128, 256]

    # Buat nama metode dari flag aktif
    aktif_flags = []
    if BDS: aktif_flags.append("BDS")
    if PPO: aktif_flags.append("PPO")
    if BRC: aktif_flags.append("BRC")
    if GLF: aktif_flags.append("GLM")
    if TPF: aktif_flags.append("TPF")
    if JPS: aktif_flags.append("JPS")
    method_name = "-".join(aktif_flags) if aktif_flags else "DEFAULT"

    map_awal = Visualize.load_grid()

    waktu_per_map = {"method": method_name}

    for sz in sizes:
        map_ = Visualize.upscale(map_awal, sz)
        start = (0, 0)
        goal = map_.shape[0] - 1, map_.shape[1] - 1

        # Siapkan map
        np.place(map_, map_ == 1, 255)
        map_[start] = 2
        map_[goal] = 3

        print(f"Testing method={method_name} di map size {sz}x{sz}")

        times_list = []

        for _ in range(10):
            (path, times), _, _ = Algoritm(
                map_.copy(), start, goal, hchoice=2,
                JPS=JPS, BDS=BDS, GLF=GLF,
                BRC=BRC, TPF=TPF, PPO=PPO,
                show=show, speed=200
            )
            times_list.append(times)

        avg_time = np.mean(times_list)
        waktu_per_map[str(sz)] = avg_time
        print(f"  → rata-rata waktu: {avg_time:.6f} detik")

    # Simpan ke Excel
    df = pd.DataFrame([waktu_per_map])
    nama_file = f"hasil_rerata_{method_name}.xlsx"
    df.to_excel(nama_file, index=False)
    print(f"\n✅ Data berhasil disimpan ke {nama_file}")

# Contoh pemanggilan:
if __name__ == "__main__":
    # run(show=False, size=[32, 64, 128, 256, 512])
    # runMethod(jps=False, BDS=False, GLF=False, BRC=False, TPF=False, PPO=False, show=False)

    scale = 256
    
    map_awal = Visualize.load_grid(path="Map/JSON/Map_1.json")
    map_awal = Visualize.upscale(map_awal, scale)
    run(map=map_awal, show=False, size=[32, 64, 128])
    Z_GetMap.save(map_awal, f"Data/Image/Sample_2_{scale}.jpg")

    # start = (0, 0)
    # goal = map_awal.shape[0] - 1, map_awal.shape[1] - 1

    # np.place(map_awal, map_awal == 1, 255)
    # map_awal[start] = 2
    # map_awal[goal] = 3

    # avg = []
    # path_len = 0
    # open_len = 0
    # close_len = 0

    # (path, times), open_list, close_list = Algoritm(
    #     map_awal, start, goal, hchoice=2,
    #     JPS=False, BDS=False, GLF=False,
    #     BRC=False, TPF=False, PPO=True,
    #     show=True, speed=10
    # )
    # avg.append(times)
    # if path:
    #     path_len = len(path)
    #     open_len = len(open_list)
    #     close_len = len(close_list)

    # print(f"Panjang Path : {path_len}")
    # print(f"Panjang Path : {open_len}")
    # print(f"Panjang Path : {close_len}")
    # print(np.mean(avg))

    # times = np.mean(avg)
    # print(f"Time: {times:.6f} detik | Path Length: {path_len}")
