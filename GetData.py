from Utils import *

def generate():
    # Load matrix dari file
    data = np.load("VarianMatrix.npz")

    # Titik awal dan tujuan
    start = (2, 3)
    goal = (14, 14)

    # Dictionary untuk menyimpan hasil
    results = {}

    for name in data.files:
        matrix = data[name]
        size = matrix.shape[0]

        # Skalakan titik start/goal agar proporsional dengan ukuran matrix
        scale = size // 16
        scaled_start = (start[0]*scale, start[1]*scale)
        scaled_goal = (goal[0]*scale, goal[1]*scale)

        # Tempat simpan hasil 10 kali percobaan
        times = []
        path_lengths = []
        open_lengths = []
        close_lengths = []
        openclose_lengths = []

        try:
            for _ in range(10):
                (path, time), open_list, close_list = jps.method(matrix, scaled_start, scaled_goal, 2)

                times.append(time if time else 0)
                path_lengths.append(len(path) if path else 0)
                open_lengths.append(len(open_list) if open_list else 0)
                close_lengths.append(len(close_list) if close_list else 0)
                openclose_lengths.append((len(open_list) + len(close_list)) if open_list and close_list else 0)

            # Simpan rata-ratanya
            results[f"{name}_size"] = size
            results[f"{name}_avg_time"] = np.mean(times)
            results[f"{name}_avg_path_len"] = np.mean(path_lengths)
            results[f"{name}_avg_open_len"] = np.mean(open_lengths)
            results[f"{name}_avg_close_len"] = np.mean(close_lengths)
            results[f"{name}_avg_openclose_len"] = np.mean(openclose_lengths)

        except Exception as e:
            print(f"Error pada matrix '{name}': {e}")
            results[f"{name}_error"] = str(e)

    # Simpan semua ke file baru
    np.savez(f"{fileName}.npz", **results)
    print(f"Hasil analisis pathfinding telah disimpan ke '{fileName}.npz'")


def show():
    # Tampilkan hasil
    hasils = np.load(f"{fileName}.npz")
    for key in hasils.files:
        print(f"{key}: {hasils[key]}")

fileName = './Data/Astar'
show()