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
    # Load map
    # np.set_printoptions(threshold=np.inf)  # Tampilkan semua elemen
    map = Visualize.load_grid()
    print(map)

    # Memperbesar Map Jika Diperlukan
    map = Visualize.upscale(map, 64)
    # print(map)
    print(map.shape)

    # Z_GetMap.show(map, 2048)

    start = (0,0)
    goal = map.shape[0]-5, map.shape[1]-1

    # Memastikan Format Map Benar
    np.place(map, map == 1, 255)
    map[start] = 2
    map[goal] = 3

    arr = []

    for i in range(1, 10):
        (path, times), *_ = jps_full.method(map, start, goal, 2, glm=False, brm=False , tpm=False, ppom=True, show=True, speed=100)
        print(times)   
        arr.append(times)

    print(np.mean(arr))

# Contoh pemanggilan:
if __name__ == "__main__":
    # run_experiment()
    # show_summary()
    run()
    # image = cv2.imread('Image/1.jpg', 0)
    # path = getPath(image, 20, 1, 7)
