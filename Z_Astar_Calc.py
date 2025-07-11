import pygame
import numpy as np

# ======= Fungsi Manual A* =======
def euclidean(a, b):
    return round(np.linalg.norm(np.array(a) - np.array(b)), 4)

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def octile(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return round(max(dx, dy) + (2 ** 0.5 - 1) * min(dx, dy), 4)

HEURISTICS = {
    "euclidean": euclidean,
    "manhattan": manhattan,
    "octile": octile
}

current_heuristic = "euclidean"

# ======= Pergerakan Cost Berdasarkan Heuristik =======
def movement_cost(a, b):
    if current_heuristic == "manhattan":
        return 1 if a[0] == b[0] or a[1] == b[1] else 1.4
    elif current_heuristic == "octile":
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return 1 if dx == 0 or dy == 0 else 1.4142
    else:
        return euclidean(a, b)

# ======= A* Manual State Reset =======
def reset_astar_state():
    return {
        "start": None,
        "goal": None,
        "visited": set(),
        "gn": {},
        "came_from": {},
        "open_set": set(),
        "fn_map": {},
        "current": None
    }

# ======= Neighbor Detection =======
def get_neighbors(pos, grid):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
            if grid[nx, ny] != 1:
                neighbors.append((nx, ny))
    return neighbors

# ======= Trace Back and Print fn, hn, gn =======
def trace_back_path(clicked, state):
    path = []
    node = clicked
    while node in state["came_from"]:
        g = state["gn"].get(node, 0)
        h = HEURISTICS[current_heuristic](node, state["goal"])
        f = g + h
        print(f"Node: {node}, g: {g:.3f}, h: {h:.3f}, f: {f:.3f}")
        path.append(node)
        node = state["came_from"][node]
    if node == state["start"]:
        g = state["gn"].get(node, 0)
        h = HEURISTICS[current_heuristic](node, state["goal"])
        f = g + h
        print(f"Node: {node}, g: {g:.3f}, h: {h:.3f}, f: {f:.3f}")
        path.append(node)
    print("\nUrutan mundur selesai.")

# ======= Manual A* Logic per Click =======
def handle_manual_astar_click(clicked, grid, state):
    if grid[clicked] == 1:
        return state

    if clicked in state["visited"]:
        trace_back_path(clicked, state)
        return state

    if state["start"] is None:
        found = np.argwhere(grid == 2)
        if found.size != 0:
            state["start"] = tuple(found[0])
            state["gn"][state["start"]] = 0
            state["current"] = state["start"]

    if state["goal"] is None:
        found = np.argwhere(grid == 3)
        if found.size != 0:
            state["goal"] = tuple(found[0])

    if state["start"] is None or state["goal"] is None:
        return state

    state["current"] = clicked
    if clicked in state["open_set"]:
        state["open_set"].remove(clicked)

    state["visited"].add(clicked)

    for neighbor in get_neighbors(clicked, grid):
        if neighbor in state["visited"]:
            continue
        tentative_g = state["gn"].get(clicked, float('inf')) + movement_cost(clicked, neighbor)
        h = HEURISTICS[current_heuristic](neighbor, state["goal"])
        f = tentative_g + h

        if neighbor not in state["gn"] or tentative_g < state["gn"][neighbor]:
            state["gn"][neighbor] = tentative_g
            state["came_from"][neighbor] = clicked
            state["fn_map"][neighbor] = f
            state["open_set"].add(neighbor)

    grid[clicked] = 6
    for n in state["open_set"]:
        if grid[n] != 6:
            grid[n] = 5

    return state

# ======= Visualisasi Pygame =======
GRID_SIZE = 16
WIDTH = 512
HEIGHT = 512
CELL_SIZE = WIDTH // GRID_SIZE

COLOR_DICT = {
    0: (255, 255, 255),  # Kosong
    1: (23, 37, 42),     # Rintangan
    2: (58, 175, 169),   # Start
    3: (255, 0, 33),     # Goal
    5: (255, 255, 0),    # Open list
    6: (255, 165, 0),    # Close list
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Manual A* Visualizer")
font = pygame.font.SysFont(None, 12)

map_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
astar_state = reset_astar_state()
active_mode = 1
running = True
is_dragging = False
show_coordinates = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            is_dragging = True
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE
            clicked = (row, col)

            if active_mode == 1:
                map_grid[clicked] = 1
            elif active_mode == 2:
                map_grid[map_grid == 2] = 0
                map_grid[clicked] = 2
            elif active_mode == 3:
                map_grid[map_grid == 3] = 0
                map_grid[clicked] = 3
            elif active_mode == 10:
                astar_state = handle_manual_astar_click(clicked, map_grid, astar_state)

        elif event.type == pygame.MOUSEMOTION and is_dragging:
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE
            clicked = (row, col)
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                if active_mode == 1:
                    map_grid[clicked] = 1

        elif event.type == pygame.MOUSEBUTTONUP:
            is_dragging = False

        elif event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if event.key == pygame.K_r:
                mask = (map_grid != 1) & (map_grid != 2) & (map_grid != 3)
                map_grid[mask] = 0
                astar_state = reset_astar_state()
            elif mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT and event.key == pygame.K_o:
                map_grid[map_grid == 1] = 0
            elif event.key == pygame.K_1:
                active_mode = 1
            elif event.key == pygame.K_2:
                active_mode = 2
            elif event.key == pygame.K_3:
                active_mode = 3
            elif event.key == pygame.K_k:
                active_mode = 10
                astar_state = reset_astar_state()
            elif event.key == pygame.K_h:
                keys = list(HEURISTICS.keys())
                current_idx = keys.index(current_heuristic)
                current_heuristic = keys[(current_idx + 1) % len(keys)]
                print(f"Heuristik saat ini: {current_heuristic}")
            elif mods & pygame.KMOD_CTRL:
                if event.key == pygame.K_s:
                    active_mode = 2
                elif event.key == pygame.K_g:
                    active_mode = 3
                elif event.key == pygame.K_i:
                    show_coordinates = not show_coordinates

    screen.fill((220, 220, 220))

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = map_grid[row, col]
            color = COLOR_DICT.get(value, (255, 255, 255))
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (200, 200, 200), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            fn_val = astar_state["fn_map"].get((row, col))
            if fn_val is not None:
                label = font.render(f"{fn_val:.3f}", True, (255, 0, 0))
                screen.blit(label, (col * CELL_SIZE + 2, row * CELL_SIZE + 2))

            if show_coordinates:
                coord_text = font.render(f"{row},{col}", True, (0, 0, 0))
                text_width, text_height = font.size(f"{row},{col}")
                screen.blit(coord_text, (col * CELL_SIZE + CELL_SIZE - text_width - 2, row * CELL_SIZE + CELL_SIZE - text_height - 2))

    mode_texts = {
        1: "Mode: Obstacle (1)",
        2: "Mode: Start (2 / Ctrl+S)",
        3: "Mode: Goal (3 / Ctrl+G)",
        10: "Mode: Manual A* (K)"
    }
    mode_label = font.render(mode_texts.get(active_mode, "Unknown"), True, (0, 0, 0))
    heuristic_label = font.render(f"Heuristic: {current_heuristic.title()} (H) ", True, (0, 0, 0))
    screen.blit(mode_label, (10, HEIGHT - 50))
    screen.blit(heuristic_label, (10, HEIGHT - 30))

    pygame.display.flip()

pygame.quit()
