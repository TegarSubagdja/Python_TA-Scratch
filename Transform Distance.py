import pygame
import numpy as np
import cv2

# Step 1: Buat matrix dengan beberapa titik pusat (nilai 1)
matrix = np.array([
    [0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,1,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
], dtype=np.uint8)

# Step 2: Hitung distance transform
dist = cv2.distanceTransform(1 - matrix, cv2.DIST_L2, 5)

# Step 3: Threshold buffer radius (3x ukuran marker, misal marker = 1 maka threshold = 3)
buffer_radius = 1.5
buffer_zone = dist <= buffer_radius
buffer_matrix = np.where(buffer_zone, 1, 0)

# Setup pygame
pygame.init()
cell_size = 60
rows, cols = matrix.shape
screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
pygame.display.set_caption("Buffer Expansion")
font = pygame.font.SysFont(None, 24)

def draw_frame(show_buffer=False):
    screen.fill((255, 255, 255))  # Background putih

    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)

            # Gambar buffer zone (warna biru muda transparan)
            if show_buffer and buffer_matrix[y][x] == 1:
                pygame.draw.rect(screen, (128, 128, 128), rect)  # light blue

            # Gambar obstacle hitam
            if matrix[y][x] == 1:
                pygame.draw.rect(screen, (0, 0, 0), rect)

            # Tampilkan nilai jarak (jika tanpa buffer)
            if not show_buffer and matrix[y][x] == 0:
                value = dist[y][x]
                text = font.render(f"{value:.1f}", True, (0, 0, 0))
                text_rect = text.get_rect(center=(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2))
                screen.blit(text, text_rect)

            # Gambar grid terakhir supaya tidak tertutup
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

# Frame 1: Nilai distance
draw_frame(show_buffer=False)
pygame.display.flip()
pygame.image.save(screen, 'Frame_DistanceValue.jpg')
pygame.time.wait(2000)  # Tampilkan selama 2 detik

# Frame 2: Setelah buffer diterapkan
draw_frame(show_buffer=True)
pygame.display.flip()
pygame.image.save(screen, 'Frame_Buffered.jpg')

# Tunggu sampai window ditutup
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
