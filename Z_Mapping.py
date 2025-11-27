from Utils import *
from Method.PathPolylineOptimization import Prunning

# =======================================================
# KONFIGURASI GRID (KAMU BEBAS GANTI)
# =======================================================

GRID_COLS = 40     # jumlah kolom (horizontal)
GRID_ROWS = 25     # jumlah baris (vertical)

CELL_SIZE = 30     # ukuran cell kotak (20x20 px)

WIDTH  = GRID_COLS * CELL_SIZE
HEIGHT = GRID_ROWS * CELL_SIZE

# =======================================================
# KONFIGURASI WARNA & GARIS
# =======================================================

CIRCLE_RADIUS = CELL_SIZE // 4
LINE_WIDTH = max(2, CELL_SIZE // 8)
LINE_COLOR = "#590a6f"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Grid Editor")
font = pygame.font.SysFont(None, 16)

colors = {
    0: "#FFFFFF",
    1: "#17252a",
    2: "#3aafa9",
    3: "#FF0021",
    4: "#3f6184",
    5: "#FFFF00",
    6: "#FFA500",
    7: "#DEDEDE",
    8: "#e8175d",
}

map_grid = np.zeros((GRID_ROWS, GRID_COLS), dtype=int)

active_mode = 1
lines = []
show_coordinates = False
is_dragging = False
last_cell = None
method = 1


# =======================================================
# UTILITY
# =======================================================

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


def shorten_line(start, end, cut_length=10):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)

    if length == 0:
        return start, end

    ratio = (length - cut_length) / length
    new_end = (start[0] + dx * ratio, start[1] + dy * ratio)
    return start, new_end


def draw_arrowhead(start, end, color, size=10, angle_degrees=30):
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    angle = math.atan2(dy, dx)

    angle1 = angle + math.radians(angle_degrees)
    angle2 = angle - math.radians(angle_degrees)

    x1 = end[0] - size * math.cos(angle1)
    y1 = end[1] - size * math.sin(angle1)
    x2 = end[0] - size * math.cos(angle2)
    y2 = end[1] - size * math.sin(angle2)

    pygame.draw.polygon(screen, color, [(end[0], end[1]), (x1, y1), (x2, y2)])


# =======================================================
# DRAW GRID
# =======================================================

def draw_grid(grid):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            value = grid[row, col]
            color = hex_to_rgb(colors.get(value, "#FFFFFF"))

            pygame.draw.rect(
                screen,
                color,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

            pygame.draw.rect(
                screen,
                (200, 200, 200),
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1
            )

            if show_coordinates:
                label = f"{row},{col}"
                text = font.render(label, True, (0, 0, 0))
                tw, th = font.size(label)
                screen.blit(
                    text,
                    (col * CELL_SIZE + CELL_SIZE - tw - 1,
                     row * CELL_SIZE + CELL_SIZE - th - 1)
                )


# =======================================================
# DRAW LINES & BULLET
# =======================================================

def draw_lines():
    for start, end in lines:
        color = hex_to_rgb(LINE_COLOR)

        # potong garis sebelum panah
        new_start, new_end = shorten_line(start, end, cut_length=12)

        pygame.draw.line(screen, color, new_start, new_end, LINE_WIDTH)

        # panah
        arrow_size = CELL_SIZE // 2
        draw_arrowhead(start, end, color, size=arrow_size)

        # bulatan di titik awal
        pygame.draw.circle(screen, color, start, CELL_SIZE // 5)


# =======================================================
# PROCESS CELL
# =======================================================

def process_cell(row, col):
    if active_mode == 1:
        map_grid[row, col] = 1
    elif active_mode == 0:
        map_grid[row, col] = 0
    elif active_mode == 5:
        map_grid[row, col] = 5
    elif active_mode == 6:
        map_grid[row, col] = 6
    elif active_mode == 7:
        map_grid[row, col] = 7
    elif active_mode == 8:
        map_grid[row, col] = 8


# =======================================================
# MAIN LOOP
# =======================================================

running = True
drawing_line = False
start_cell = None

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # --------------------------------------------------
        # MOUSE DOWN
        # --------------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE

            if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:

                if active_mode == 4:   # mode garis
                    if not drawing_line:
                        start_cell = (row, col)
                        drawing_line = True
                    else:
                        end_cell = (row, col)

                        start_center = (
                            start_cell[1] * CELL_SIZE + CELL_SIZE // 2,
                            start_cell[0] * CELL_SIZE + CELL_SIZE // 2
                        )

                        end_center = (
                            end_cell[1] * CELL_SIZE + CELL_SIZE // 2,
                            end_cell[0] * CELL_SIZE + CELL_SIZE // 2
                        )

                        lines.append((start_center, end_center))
                        drawing_line = False

                elif active_mode == 2:  # Start
                    map_grid[map_grid == 2] = 0
                    map_grid[row, col] = 2

                elif active_mode == 3:  # Goal
                    map_grid[map_grid == 3] = 0
                    map_grid[row, col] = 3

                else:
                    is_dragging = True
                    last_cell = (row, col)
                    process_cell(row, col)

        # --------------------------------------------------
        # DRAG
        # --------------------------------------------------
        elif event.type == pygame.MOUSEMOTION and is_dragging:
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE

            if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
                if (row, col) != last_cell:
                    process_cell(row, col)
                    last_cell = (row, col)

        # --------------------------------------------------
        # MOUSE UP
        # --------------------------------------------------
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_dragging = False
            last_cell = None

        # --------------------------------------------------
        # KEY INPUTS
        # --------------------------------------------------
        if event.type == pygame.KEYDOWN:

            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                if event.key == pygame.K_o: active_mode = 1
                elif event.key == pygame.K_c: active_mode = 0
                elif event.key == pygame.K_s: active_mode = 2
                elif event.key == pygame.K_g: active_mode = 3
                elif event.key == pygame.K_l: active_mode = 4
                elif event.key == pygame.K_u: active_mode = 5
                elif event.key == pygame.K_x: active_mode = 6
                elif event.key == pygame.K_e: active_mode = 7
                elif event.key == pygame.K_q: active_mode = 8
                elif event.key == pygame.K_i: show_coordinates = not show_coordinates
                elif event.key == pygame.K_t:
                    if lines:
                        lines.pop()

            elif event.key == pygame.K_ESCAPE:
                running = False

    # =======================================================
    # RENDER
    # =======================================================

    screen.fill((255, 255, 255))
    draw_grid(map_grid)
    draw_lines()

    pygame.display.flip()

pygame.quit()
