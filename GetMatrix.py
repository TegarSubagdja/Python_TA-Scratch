from Utils import *

def hex_to_rgb(hex_code):
    """Mengubah kode HEX menjadi tuple RGB."""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))

def upscale_matrix(matrix, scale_factor):
    return np.repeat(np.repeat(matrix, scale_factor, axis=0), scale_factor, axis=1)

def draw_matrix_interactive(rows=16, cols=16, cell_size=40, margin=1):
    pygame.init()

    # Warna
    color_map = {
        0: (255, 255, 255),  
        1: (0, 0, 0),        
    }

    matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    width = cols * (cell_size + margin) + margin
    height = rows * (cell_size + margin) + margin

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Interactive Matrix Editor")

    dragging = False

    running = True
    while running:
        screen.fill(hex_to_rgb("#D6D6D6"))

        for y in range(rows):
            for x in range(cols):
                color = color_map.get(matrix[y][x], (255, 0, 255))  # fallback pink
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Klik kiri
                    mx, my = pygame.mouse.get_pos()
                    grid_x = mx // (cell_size + margin)
                    grid_y = my // (cell_size + margin)
                    if 0 <= grid_x < cols and 0 <= grid_y < rows:
                        matrix[grid_y][grid_x] = 1
                    dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                mx, my = pygame.mouse.get_pos()
                grid_x = mx // (cell_size + margin)
                grid_y = my // (cell_size + margin)
                if 0 <= grid_x < cols and 0 <= grid_y < rows:
                    matrix[grid_y][grid_x] = 1

            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and event.key == pygame.K_s:
                    print(matrix)
                    matrices = {
                        "matrix_16x16": matrix
                    }
                    for size in [32, 64, 128, 256, 512, 1024]:
                        scale = size // 16
                        matrices[f"matrix_{size}x{size}"] = upscale_matrix(matrix, scale)
                    np.savez("VarianMatrix.npz", **matrices)
                    print("Semua matrix disimpan ke 'Matrixs.npz'")

    pygame.quit()
    sys.exit()

draw_matrix_interactive()