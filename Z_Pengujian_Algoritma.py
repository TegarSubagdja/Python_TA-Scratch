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
    size = [32, 64, 128, 256, 512]
    
    map = Visualize.load_grid()
    for sz in size:
        map = Visualize.upscale(map, sz)
        arrSize.append(map)
        print(map.shape)

    kombinasi_flags = list(itertools.product([False, True], repeat=6))
    print(len(kombinasi_flags))  # Harus 64
    print(len(set(kombinasi_flags)))  # Harus juga 64, artinya tidak ada duplikat

    # Urutan: jps, bd, glm, brm, tpm, ppom

    hasil = []  # Simpan [flag, time]

    for arr in arrSize:

        start = (0, 0)
        goal = arr.shape[0] - 5, arr.shape[1] - 1

        for flags in kombinasi_flags:
            jps, bd, glm, brm, tpm, ppom = flags

            print(f"Testing: jps={jps}, bd={bd}, glm={glm}, brm={brm}, tpm={tpm}, ppom={ppom} di size {arr.shape}")

            avg = []

            for i in range(1, 2):
                (path, times) = Algoritm(
                arr, start, goal, hchoice=1, 
                jps=jps, 
                bd=bd, 
                glm=glm, 
                brm=brm, 
                tpm=tpm, 
                ppom=ppom, 
                show=True, 
                speed=200
                )
                avg.append(times)

            times = np.mean(avg)
            
            print(f"Time: {times:.6f} detik")
            hasil.append([jps, bd, glm, brm, tpm, ppom, times])

        # Sorting berdasarkan waktu tercepat
        hasil.sort(key=lambda x: x[-1])

        print("\n=== Hasil Kombinasi Tercepat ===")
        tercepat = min(hasil, key=lambda x: x[-1])
        print(f"Flags: {tercepat[:-1]} di size {arr.shape}  | Time: {tercepat[-1]:.6f} detik")

# Contoh pemanggilan:
if __name__ == "__main__":
    # run_experiment()
    # show_summary()
    run()
    
    # map = Visualize.load_grid()
    # map = Visualize.upscale(map, 32)
    # print(map.shape)

    # kombinasi_flags = list(itertools.product([False, True], repeat=6))
    # print(len(kombinasi_flags))  # Harus 64
    # print(len(set(kombinasi_flags)))  # Harus juga 64, artinya tidak ada duplikat

    # start = (0, 0)
    # goal = map.shape[0] - 5, map.shape[1] - 1

    # (path, times) = Algoritm(
    # map, start, goal, hchoice=1, 
    # jps=False, 
    # bd=False, 
    # glm=False, 
    # brm=False, 
    # tpm=False, 
    # ppom=False, 
    # show=False, 
    # speed=200)

    # print(f"Time: {times:.6f} detik")