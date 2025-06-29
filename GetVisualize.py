from Utils import *  # Sesuaikan jika perlu

def hex_to_rgb(hex_code):
    """Mengubah kode HEX menjadi tuple RGB."""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))

def Visualize(matrix, title="Matrix Visualization", path=None, algo_name="unknown", matrix_name="unknown", folder="Output/Data"):
  import pygame
import numpy as np
import os
from Utils import *  # Sesuaikan jika perlu

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))

def Visualize(matrix, title="Matrix Visualization", path=None, algo_name="unknown", matrix_name="unknown", folder="Output/Data"):
    os.environ["SDL_VIDEODRIVER"] = "dummy"  # Mode headless, tidak munculkan window
    pygame.init()

    color_map = {
        0: (255, 255, 255),
        1: (0, 0, 0),
        2: (0, 255, 0),
        3: (0, 0, 255),
        4: (169, 169, 169),
        5: (255, 165, 0),
        6: (160, 32, 240),
    }

    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    window_size = 720
    margin = 1
    cell_size = (window_size - (cols * margin)) // cols

    width = height = window_size
    screen = pygame.Surface((width, height))  # Render langsung ke surface tanpa window
    screen.fill((214, 214, 214))

    for y in range(rows):
        for x in range(cols):
            value = matrix[y][x]
            color = color_map.get(value, (255, 0, 255))
            rect = pygame.Rect(
                x * (cell_size + margin) + margin,
                y * (cell_size + margin) + margin,
                cell_size,
                cell_size
            )
            pygame.draw.rect(screen, color, rect)

    if path:
        for i in range(1, len(path)):
            x1, y1 = path[i - 1]
            x2, y2 = path[i]
            pygame.draw.line(
                screen,
                (160, 32, 240),
                (
                    y1 * (cell_size + margin) + margin + cell_size // 2,
                    x1 * (cell_size + margin) + margin + cell_size // 2,
                ),
                (
                    y2 * (cell_size + margin) + margin + cell_size // 2,
                    x2 * (cell_size + margin) + margin + cell_size // 2,
                ),
                max(1, cell_size // 3)
            )

    os.makedirs(folder, exist_ok=True)
    file_name = f"{algo_name}_{matrix_name}.png"
    save_path = os.path.join(folder, file_name)
    pygame.image.save(screen, save_path)
    print(f"Gambar disimpan otomatis: {save_path}")

    pygame.quit()


# ==== CONTOH PENGGUNAAN ====

data = np.load('VarianMatrix.npz')

start = (2, 2)
goal = (62, 62)
size = "matrix_64x64"

matrix_ori = data[size]
matrix_ori[matrix_ori == 1] = 255

methods = [astar, jps, astar_br, jps_br, astar_gl, jps_gl, astar_tp, jps_tp]

result_times = {}  # Untuk menyimpan waktu eksekusi

for method in methods:
    matrix = matrix_ori.copy()

    (points, exec_time) = method.method(matrix, start, goal, 2)

    for (x, y) in points:
        matrix[x, y] = 6

    matrix[matrix == 255] = 1

    algo_name = method.__name__.capitalize()

    Visualize(matrix, path=points, algo_name=algo_name, matrix_name=size)

    print(f"{algo_name} selesai dalam waktu {exec_time:.4f} detik")

    result_times[algo_name] = exec_time

# Simpan ke file JSON
os.makedirs("Output/Data", exist_ok=True)
with open("Output/Data/waktu_eksekusi.json", "w") as f:
    json.dump(result_times, f, indent=4)

print("\nWaktu eksekusi semua algoritma disimpan di Output/Data/waktu_eksekusi.json")
