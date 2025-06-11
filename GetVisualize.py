import pygame
import sys

def hex_to_rgb(hex_code):
    """Mengubah kode HEX menjadi tuple RGB."""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))

def save_matrix():
    None

def visualize_matrix(matrix, cell_size=40, margin=1, title="Matrix Visualization"):
    pygame.init()

    # Skema warna lengkap
    color_map = {
        0: (255, 255, 255),   # 0 - Putih (jalan)
        1: (0, 0, 0),         # 1 - Hitam (rintangan)
        2: (0, 255, 0),       # 2 - Hijau (start)
        3: (0, 0, 255),       # 3 - Biru (goal)
        4: (169, 169, 169),   # 4 - Abu-abu (visited)
        5: (255, 165, 0),     # 5 - Jingga (frontier / tetangga)
        6: (160, 32, 240),    # 6 - Ungu (jalur akhir)
    }

    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    width = cols * (cell_size + margin) + margin
    height = rows * (cell_size + margin) + margin

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    running = True
    while running:
        screen.fill(hex_to_rgb("#D6D6D6"))

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

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:  
                    if event.key == pygame.K_s:
                        save_matrix()  

    pygame.quit()
    sys.exit()

    visualize_matrix()