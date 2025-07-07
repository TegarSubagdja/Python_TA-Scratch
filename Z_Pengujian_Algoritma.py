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

def run():
    
    arrSize = []
    size = [32, 64, 128]
    
    map_awal = Visualize.load_grid()
    for sz in size:
        map_ = Visualize.upscale(map_awal, sz)
        arrSize.append(map_)
        print(map_.shape)

    kombinasi_flags = list(itertools.product([False, True], repeat=6))
    print(f"Total kombinasi: {len(kombinasi_flags)}") 

    hasil_semua = [] 

    for arr in arrSize:
        
        hasil_per_size = []  # Reset setiap ganti ukuran map

        start = (0, 0)
        goal = arr.shape[0] - 1, arr.shape[1] - 1

        np.place(arr, arr == 1, 255)
        arr[start] = 2
        arr[goal] = 3

        for flags in kombinasi_flags:
            jps, bd, glm, brm, tpm, ppom = flags
            print(f"Testing: jps={jps}, bd={bd}, glm={glm}, brm={brm}, tpm={tpm}, ppom={ppom} di size {arr.shape}")

            avg = []
            path_len = 0
            open_len = 0
            close_len = 0

            for i in range(1, 11):
                (path, times), open_list, close_list = Algoritm(
                    arr, start, goal, hchoice=1,
                    jps=jps, bd=bd, glm=glm,
                    brm=brm, tpm=tpm, ppom=ppom,
                    show=False, speed=200
                )
                avg.append(times)
                if path:
                    path_len = len(path)
                    open_len = len(open_list)
                    close_len = len(close_list)

            times = np.mean(avg)
            print(f"Time: {times:.6f} detik | Path Length: {path_len}")

            # Simpan data ke list besar
            hasil_semua.append({
                "map_size": arr.shape[0],
                "jps": jps,
                "bd": bd,
                "glm": glm,
                "brm": brm,
                "tpm": tpm,
                "ppom": ppom,
                "len_path": path_len,
                "len_openSet": open_len,
                "len_closeSet": close_len,
                "run_1": avg[0],
                "run_2": avg[1],
                "run_3": avg[2],
                "run_4": avg[3],
                "run_5": avg[4],
                "run_6": avg[5],
                "run_7": avg[6],
                "run_8": avg[7],
                "run_9": avg[8],
                "run_10": avg[9],
                "time": times
            })

            # Untuk keperluan sorting tercepat per ukuran map
            hasil_per_size.append([jps, bd, glm, brm, tpm, ppom, times])

        # Sorting untuk melihat kombinasi tercepat
        hasil_per_size.sort(key=lambda x: x[-1])
        tercepat = hasil_per_size[0]
        print("\n=== Hasil Kombinasi Tercepat ===")
        print(f"Flags: {tercepat[:-1]} di size {arr.shape} | Time: {tercepat[-1]:.6f} detik\n")

    # Simpan ke Excel dengan pandas
    df = pd.DataFrame(hasil_semua)
    df.to_excel("hasil_uji.xlsx", index=False)
    print("Data berhasil disimpan ke hasil_uji.xlsx")

def runMethod(jps=False, bd=False, glm=False, brm=False, tpm=False, ppom=False,):
    
    arrSize = []
    size = [32, 64, 128, 512, 1024]

    # Buat nama file berdasarkan metode yang aktif
    aktif_flags = []
    if bd: aktif_flags.append("BD")
    if ppom: aktif_flags.append("PPO")
    if brm: aktif_flags.append("BRC")
    if glm: aktif_flags.append("GLM")
    if tpm: aktif_flags.append("TPF")
    if jps: aktif_flags.append("JPS")

    map_awal = Visualize.load_grid()

    for sz in size:
        map_ = Visualize.upscale(map_awal, sz)
        arrSize.append(map_)
        print(map_.shape)

    hasil_semua = []  # List besar untuk semua data

    for arr in arrSize:
        
        hasil_per_size = []  # Reset setiap ganti ukuran map

        start = (0, 0)
        goal = arr.shape[0] - 1, arr.shape[1] - 1

        np.place(arr, arr == 1, 255)
        arr[start] = 2
        arr[goal] = 3

        print(f"Testing: jps={jps}, bd={bd}, glm={glm}, brm={brm}, tpm={tpm}, ppom={ppom} di size {arr.shape}")

        avg = []
        path_len = 0
        open_len = 0
        close_len = 0

        for i in range(1, 11):
            (path, times), open_list, close_list = Algoritm(
                arr, start, goal, hchoice=1,
                jps=jps, bd=bd, glm=glm,
                brm=brm, tpm=tpm, ppom=ppom,
                show=False, speed=200
            )
            avg.append(times)
            if path:
                path_len = len(path)
                open_len = len(open_list)
                close_len = len(close_list)

        times = np.mean(avg)
        print(f"Time: {times:.6f} detik | Path Length: {path_len}")

        # Simpan data ke list besar
        hasil_semua.append({
            "map_size": arr.shape[0],
            "method": aktif_flags,
            "len_path": path_len,
            "len_openSet": open_len,
            "len_closeSet": close_len,
            "run_1": avg[0],
            "run_2": avg[1],
            "run_3": avg[2],
            "run_4": avg[3],
            "run_5": avg[4],
            "run_6": avg[5],
            "run_7": avg[6],
            "run_8": avg[7],
            "run_9": avg[8],
            "run_10": avg[9],
            "time": times
        })

        # Untuk keperluan sorting tercepat per ukuran map
        hasil_per_size.append([jps, bd, glm, brm, tpm, ppom, times])

        # Sorting untuk melihat kombinasi tercepat
        hasil_per_size.sort(key=lambda x: x[-1])
        tercepat = hasil_per_size[0]
        print("\n=== Hasil Kombinasi Tercepat ===")
        print(f"Flags: {tercepat[:-1]} di size {arr.shape} | Time: {tercepat[-1]:.6f} detik\n")

    # Simpan ke Excel dengan pandas
    df = pd.DataFrame(hasil_semua)
    df.to_excel(f"hasil_uji_{aktif_flags}.xlsx", index=False)
    print("Data berhasil disimpan ke hasil_uji.xlsx")

# Contoh pemanggilan:
if __name__ == "__main__":
    # run_experiment()
    # show_summary()
    # run()
    runMethod()