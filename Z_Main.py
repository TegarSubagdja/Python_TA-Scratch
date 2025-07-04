from Utils import *
import itertools
from Algoritma import bds
from Algoritma import jbds

flag_names = ["tpm", "brm", "glm", "ppom"]
jumlah_flag = len(flag_names)
sizes = [16, 32, 64, 128, 256, 512]
json_path = "Data/Pengujian/Data.json"


def run_experiment():
    """Melakukan percobaan semua kombinasi flag dan simpan hasil ke JSON"""
    map = Visualize.load_grid()
    data_json = []

    for size in sizes:
        Upscale_map = Visualize.upscale(map, size)
        goal = (size - 1, size - 1)
        start = (1, 1)

        for flags in itertools.product([True, False], repeat=jumlah_flag):
            aktif = [flag_names[j] for j in range(jumlah_flag) if flags[j]]

            (path, times), open_list, close_list = astar_full.method(
                Upscale_map, start, goal, 2, *flags
            )

            print(f"Size: {size}, Aktif: {', '.join(aktif) if aktif else 'Tidak ada'}, Waktu: {times}")

            data_json.append({
                "size": size,
                "aktif": aktif if aktif else ["Tidak ada"],
                "waktu": times
            })

    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w") as f:
        json.dump(data_json, f, indent=4)

    print(f"\nData disimpan ke {json_path}")


def show_summary():
    """Menampilkan kombinasi tercepat & terlambat untuk setiap ukuran map"""
    if not os.path.exists(json_path):
        print(f"File {json_path} tidak ditemukan. Jalankan run_experiment() dulu.")
        return

    with open(json_path, "r") as f:
        data_json = json.load(f)

    print("\nRingkasan Waktu Terbaik & Terburuk per Ukuran Map:")

    for size in sizes:
        data_per_size = [d for d in data_json if d["size"] == size]
        if not data_per_size:
            continue

        tercepat = min(data_per_size, key=lambda d: d["waktu"])
        terlambat = max(data_per_size, key=lambda d: d["waktu"])

        print(f"\nUkuran Map: {size}x{size}")
        print(f"  ⚡ Tercepat : {tercepat['waktu']} detik, Aktif: {', '.join(tercepat['aktif'])}")
        print(f"  🐢 Terlambat: {terlambat['waktu']} detik, Aktif: {', '.join(terlambat['aktif'])}")

import random

def get(grid_size, jumlah_rintangan):
    grid = np.zeros((grid_size, grid_size), dtype=int)

    for _ in range(jumlah_rintangan):
        # Titik awal acak, pastikan aman untuk area 2x2
        row = random.randint(0, grid_size - 2)
        col = random.randint(0, grid_size - 2)

        # Isi 4 titik berdekatan (2x2 area)
        grid[row, col] = 255
        grid[row + 1, col] = 255
        grid[row, col + 1] = 255
        grid[row + 1, col + 1] = 255

    return grid


def run():
    size = 128

    # Load map
    map = Visualize.load_grid()

    # Memperbesar Map Jika Diperlukan
    # map = Visualize.upscale(map, size)
    print(map)
    print(map.shape)

    # Membuat map acak
    # map = get(128, 64)

    start = (0,0)
    goal = map.shape[0]-5, map.shape[1]-1

    # Memastikan Format Map Benar
    map[map == 1] = 255
    map[start] = 2
    map[goal] = 3

    arr = []

    for i in range(1, 100):
        _, times = jps_full.method(map, start, goal, 2, glm=False, brm=False , tpm=False, ppom=False, show=True, speed=10)
        print(times)   
        arr.append(times)

    print(np.mean(arr))

# Contoh pemanggilan:
if __name__ == "__main__":
    # run_experiment()
    # show_summary()
    # run()
    image = cv2.imread('Image/1.jpg', 0)
    path = getPath(image, 20, 1, 7)
