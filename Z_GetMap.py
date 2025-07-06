import pygame
import numpy as np
import json
import os

# Konfigurasi warna
colors = {
    0: "#FFFFFF",
    1: "#17252a",
    2: "#3aafa9",
    3: "#FF0021",
    4: "#3f6184",
    5: "#FFFF00",
    6: "#FFA500",
    7: "#778899",
    8: "#e8175d",
}

# Konversi HEX ke RGB
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))

# Simpan Arr Map ke JSON
def save_JSON(map, fixed_path="Map/JSON/ArrMap.json"):
    """
    Menyimpan grid ke file JSON pada path tetap.
    
    Parameters:
    - fixed_path (str): Lokasi penyimpanan file JSON, default ke 'Output/Map.json'
    """
    try:
        grid_list = map  # Konversi array ke list
        with open(fixed_path, 'w') as f:
            json.dump(grid_list, f, indent=4)
        print(f"Grid berhasil disimpan ke '{fixed_path}'")
    except Exception as e:
        print(f"Gagal menyimpan grid: {e}")

# Muat grid dari file JSON
def load_grid(path="Map/JSON/Map.json"):
    with open(path, 'r') as f:
        data = json.load(f)
        return np.array(data)

# Upscale grid ke ukuran target
def upscale(grid, target_size):
    rows, cols = grid.shape
    if rows != cols:
        raise ValueError("Grid harus persegi (NxN)")
    if target_size % rows != 0:
        raise ValueError(f"Target size {target_size} harus kelipatan {rows}")

    scale = target_size // rows
    new_grid = np.repeat(np.repeat(grid, scale, axis=0), scale, axis=1)
    return new_grid

# Gambar grid ke permukaan
def draw_grid(grid, surface, cell_size):
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            value = grid[row, col]
            color = hex_to_rgb(colors.get(value, "#FFFFFF"))
            pygame.draw.rect(surface, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(surface, (200, 200, 200), (col * cell_size, row * cell_size, cell_size, cell_size), 1)

# Visualisasi animasi grid + open, close, path
def Init_Visual(grid):
    pygame.init()
    cell_size = 512 / grid.shape[0]
    rows, cols = grid.shape
    surface = pygame.display.set_mode((cols * cell_size, rows * cell_size))
    return surface, cell_size

def Render(surface, grid, cell_size, open_list, close_list, path=None):
    rows, cols = grid.shape
    surface.fill((255, 255, 255))

    # Gambar grid dasar
    for y in range(rows):
        for x in range(cols):
            value = grid[y, x]
            
            if value == 255:
                color = (0, 0, 0)  # Hitam
            else:
                color = hex_to_rgb(colors.get(value, "#FFFFFF"))

            pygame.draw.rect(surface, color, (x * cell_size, y * cell_size, cell_size, cell_size))
            pygame.draw.rect(surface, (200, 200, 200), (x * cell_size, y * cell_size, cell_size, cell_size), 1)

    # Open List
    for item in open_list:
        node = item[1] if isinstance(item, tuple) and len(item) > 1 else item
        y, x = node
        pygame.draw.rect(surface, hex_to_rgb(colors[5]),
                         (x * cell_size, y * cell_size, cell_size, cell_size))

    # Closed List
    for node in close_list:
        y, x = node
        pygame.draw.rect(surface, hex_to_rgb(colors[6]),
                         (x * cell_size, y * cell_size, cell_size, cell_size))

    # Path
    if path:
        for node in path:
            y, x = node
            pygame.draw.rect(surface, hex_to_rgb(colors[4]),
                             (x * cell_size, y * cell_size, cell_size, cell_size))

    pygame.display.flip()

# Tampilkan grid ke layar
def show(grid, window_size=1024):
    rows, cols = grid.shape
    cell_w = window_size / cols
    cell_h = window_size / rows
    cell_size = min(cell_w, cell_h)

    width = int(cell_size * cols)
    height = int(cell_size * rows)

    # Pastikan tidak ada sisa dummy mode sebelumnya
    if "SDL_VIDEODRIVER" in os.environ:
        del os.environ["SDL_VIDEODRIVER"]

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Grid Viewer")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(hex_to_rgb("#FFFFFF"))
        draw_grid(grid, screen, cell_size)
        pygame.display.flip()

    pygame.quit()

# Simpan grid ke gambar tanpa tampil
def save(grid, save_path="Map/Image/Map.jpg", image_size=4096):
    os.environ["SDL_VIDEODRIVER"] = "dummy"  # Headless
    pygame.init()

    rows, cols = grid.shape
    cell_w = image_size / cols
    cell_h = image_size / rows
    cell_size = min(cell_w, cell_h)

    width = int(cell_size * cols)
    height = int(cell_size * rows)

    surface = pygame.Surface((width, height))
    surface.fill(hex_to_rgb("#FFFFFF"))
    draw_grid(grid, surface, cell_size)
    pygame.image.save(surface, save_path)
    pygame.quit()
    print(f"Gambar berhasil disimpan: {save_path}")

# -------------------------------
# Contoh Pemakaian:
if __name__ == "__main__":
    grid = load_grid("Map/JSON/Map.json")

    # Upscale dulu untuk keperluan tampilan dan simpan
    upscaled_grid = upscale(grid, 512)

    # Simpan hasil upscale, bukan grid kecil
    save(upscaled_grid, "Map/Image/Map.jpg", image_size=2048)

    # Tampilkan ke layar
    # show(upscaled_grid, window_size=4096)
