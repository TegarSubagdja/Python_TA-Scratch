from Utils import *

def get(grid_size, jumlah_rintangan):
    grid = np.zeros((grid_size, grid_size), dtype=int)

    for _ in range(jumlah_rintangan):
        # Titik awal acak, pastikan aman untuk area 2x2
        row = random.randint(0, grid_size - 2)
        col = random.randint(0, grid_size - 2)

        # Isi 4 titik berdekatan (2x2 area)
        val = 1
        grid[row, col] = val
        grid[row + 1, col] = val
        grid[row, col + 1] = val
        grid[row + 1, col + 1] = val

    return grid

def run():
    map = Visualize.load_grid()
    map = Visualize.upscale(map, 128)
    print(map.shape)

    start = (0, 0)
    goal = map.shape[0] - 5, map.shape[1] - 1

    np.place(map, map == 1, 255)
    map[start] = 2
    map[goal] = 3

    kombinasi_flags = list(itertools.product([False, True], repeat=6))
    print(len(kombinasi_flags))  # Harus 64
    print(len(set(kombinasi_flags)))  # Harus juga 64, artinya tidak ada duplikat

    # Urutan: jps, bd, glm, brm, tpm, ppom

    hasil = []  # Simpan [flag, time]

    for flags in kombinasi_flags:
        jps, bd, glm, brm, tpm, ppom = flags

        print(f"Testing: jps={jps}, bd={bd}, glm={glm}, brm={brm}, tpm={tpm}, ppom={ppom}")

        avg = []

        for i in range(1, 10):
            (path, times) = Algoritm(
            map, start, goal, hchoice=1, 
            jps=False, 
            bd=bd, 
            glm=glm, 
            brm=brm, 
            tpm=tpm, 
            ppom=ppom, 
            show=False, 
            speed=200
            )
            avg.append(times)

        times = np.mean(avg)
        
        print(f"Time: {times:.6f} detik")
        hasil.append([jps, bd, glm, brm, tpm, ppom, times])

    # Sorting berdasarkan waktu tercepat
    hasil.sort(key=lambda x: x[-1])

    print("\n=== Hasil Kombinasi Tercepat ===")
    for row in hasil:
        print(f"Flags: {row[:-1]}  | Time: {row[-1]:.6f} detik")


# Contoh pemanggilan:
if __name__ == "__main__":
    # run_experiment()
    # show_summary()
    run()