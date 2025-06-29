import pygame
import numpy as np
import json
import os

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 1024

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

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def load(path="Map/JSON/Map.json"):
    with open(path, 'r') as f:
        data = json.load(f)
        return np.array(data)

def draw(grid, surface, cell_size):
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            value = grid[row, col]
            color = hex_to_rgb(colors.get(value, "#FFFFFF"))
            pygame.draw.rect(surface, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(surface, (200, 200, 200), (col * cell_size, row * cell_size, cell_size, cell_size), 1)

def show(grid, window_width=1024, window_height=1024):
    rows, cols = grid.shape
    cell_w = window_width / cols
    cell_h = window_height / rows
    cell_size = min(cell_w, cell_h)

    window_width = int(cell_size * cols)
    window_height = int(cell_size * rows)

    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
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
        draw(grid, screen, cell_size)
        pygame.display.flip()

    pygame.quit()

def save(grid, save_path="Map/Image/Map.jpg", image_width=1024, image_height=1024):
    rows, cols = grid.shape
    cell_w = image_width / cols
    cell_h = image_height / rows
    cell_size = min(cell_w, cell_h)

    image_width = int(cell_size * cols)
    image_height = int(cell_size * rows)

    os.environ["SDL_VIDEODRIVER"] = "dummy"  # Headless mode supaya tidak muncul window
    pygame.init()
    surface = pygame.Surface((image_width, image_height))

    surface.fill(hex_to_rgb("#FFFFFF"))
    draw(grid, surface, cell_size)

    pygame.image.save(surface, save_path)
    pygame.quit()
    print(f"Gambar grid berhasil disimpan ke {save_path}")


matrix = load()
save(matrix)