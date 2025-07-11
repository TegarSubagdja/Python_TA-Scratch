import pygame
import cv2
import numpy as np
import math

# Inisialisasi pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid with Dragable Markers & Draw Mode")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (220, 220, 220)

# Grid config
CELL_SIZE = 16
GRID_COLS = WIDTH // CELL_SIZE
GRID_ROWS = HEIGHT // CELL_SIZE

# Grid 2D: 0 = kosong, 1 = rintangan
grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

# Mode gambar
draw_mode = False
draw_toggle_ready = True
drawing = False  # apakah mouse sedang menahan klik kiri
dragging_marker = None  # marker mana yang sedang digeser
save_on_mouseup = False

# Fungsi konversi cv2 ke pygame surface
def cvimg_to_pygame(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.rot90(image)
    return pygame.surfarray.make_surface(image)

# Load ArUco marker 1
aruco_img1_cv = cv2.imread("Aruco/Marker/aruco_marker_id_0DICT_4X4_50.png")
aruco_img1_cv = cv2.resize(aruco_img1_cv, (0, 0), fx=0.05, fy=0.05)
if aruco_img1_cv is None:
    raise FileNotFoundError("Marker 1 tidak ditemukan.")
aruco_surface1 = cvimg_to_pygame(aruco_img1_cv)

# Load ArUco marker 2
aruco_img2_cv = cv2.imread("Aruco/Marker/aruco_marker_id_1DICT_4X4_50.png")
aruco_img2_cv = cv2.resize(aruco_img2_cv, (0, 0), fx=0.05, fy=0.05)
if aruco_img2_cv is None:
    raise FileNotFoundError("Marker 2 tidak ditemukan.")
aruco_surface2 = cvimg_to_pygame(aruco_img2_cv)

# Ukuran marker (gunakan salah satu)
marker_size = aruco_surface1.get_size()

# Posisi awal 2 robot
marker1_pos = np.array([WIDTH // 3, HEIGHT // 2], dtype=float)
marker2_pos = np.array([2 * WIDTH // 3, HEIGHT // 2], dtype=float)

# Fungsi menggambar grid dan rintangan
def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[row][col] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

# Loop utama
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)
    mouse_pos = np.array(pygame.mouse.get_pos(), dtype=float)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Toggle draw mode (Ctrl+G)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if (pygame.key.get_mods() & pygame.KMOD_CTRL) and event.key == pygame.K_g and draw_toggle_ready:
                draw_mode = not draw_mode
                draw_toggle_ready = False
                print("Draw mode:", draw_mode)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_g:
                draw_toggle_ready = True

        # Klik kiri tekan
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                drawing = True

                # Cek apakah klik pada marker
                for i, pos in enumerate([marker1_pos, marker2_pos]):
                    rect = pygame.Rect(0, 0, *marker_size)
                    rect.center = pos
                    if rect.collidepoint(mx, my):
                        dragging_marker = i
                        break

                # Jika mode gambar dan bukan marker, aktifkan penggambaran
                if draw_mode and dragging_marker is None:
                    col, row = mx // CELL_SIZE, my // CELL_SIZE
                    if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
                        grid[row][col] = 1 if grid[row][col] == 0 else 0

        # Lepas klik kiri
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                dragging_marker = None
                save_on_mouseup = True  # Aktifkan simpan di akhir frame

        # Mouse digerakkan saat klik kiri ditahan
        elif event.type == pygame.MOUSEMOTION:
            if draw_mode and drawing and dragging_marker is None:
                mx, my = pygame.mouse.get_pos()
                col, row = mx // CELL_SIZE, my // CELL_SIZE
                if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
                    grid[row][col] = 1

    # Update posisi marker jika sedang diseret
    if dragging_marker is not None:
        if dragging_marker == 0:
            marker1_pos = mouse_pos
        elif dragging_marker == 1:
            marker2_pos = mouse_pos

    # Gambar grid
    draw_grid()

    # Gambar markers
    rotated1 = pygame.transform.rotate(aruco_surface1, 0)
    rect1 = rotated1.get_rect(center=marker1_pos)
    screen.blit(rotated1, rect1)

    rotated2 = pygame.transform.rotate(aruco_surface2, 0)
    rect2 = rotated2.get_rect(center=marker2_pos)
    screen.blit(rotated2, rect2)

    # Teks mode
    font = pygame.font.SysFont(None, 24)
    if draw_mode:
        text = font.render("Draw Mode [ON] - Ctrl+G to toggle", True, RED)
        screen.blit(text, (10, 10))

    pygame.display.flip()

    if save_on_mouseup:
        pygame.image.save(screen, "hasil.png")
        print("Tampilan disimpan sebagai hasil.png")
        save_on_mouseup = False  # reset flag
        
    clock.tick(60)

pygame.quit()
