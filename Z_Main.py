from Utils import *
import itertools
import json
import os

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


# Contoh pemanggilan:
run_experiment()
show_summary()
