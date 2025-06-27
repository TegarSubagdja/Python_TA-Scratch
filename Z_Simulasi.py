import pygame
import cv2
import numpy as np
import sys
from Utils import *  # Pastikan ada getPath dan GetOrientation

# ===== Inisialisasi Pygame =====
pygame.init()
WIDTH, HEIGHT = 2000, 920
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Follower")

# ===== Load Asset =====
background = pygame.image.load("Image/1.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

robot_original = pygame.image.load("aruco.png")
robot_original = pygame.transform.scale(robot_original, (100, 100))

font = pygame.font.SysFont('Arial', 30)  # Font untuk teks

# ===== Variabel Utama =====
rotation_angle = 0
path = None
idx = 0

# ===== Loop Utama =====
running = True
while running:

    # Ambil Screenshot Sekali Per Loop
    screenshot_array = pygame.surfarray.array3d(pygame.display.get_surface())
    screenshot_array = np.transpose(screenshot_array, (1, 0, 2))

    screenshot_color = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot_array, cv2.COLOR_BGR2GRAY)

    # ===== Event Handling =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                cv2.imwrite("Output/normal.jpg", screenshot_color)
                print("Gambar disimpan ke Output/normal.jpg")
            elif event.key == pygame.K_LEFT:
                rotation_angle += 10
            elif event.key == pygame.K_RIGHT:
                rotation_angle -= 10
            elif event.key == pygame.K_r:
                path = None  # Reset jalur

    # ===== Posisi Robot =====
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rotated_robot = pygame.transform.rotate(robot_original, rotation_angle)
    robot_rect = rotated_robot.get_rect(center=(mouse_x, mouse_y))

    # ===== Hitung Path Jika Belum Ada =====
    if path is None:
        path = getPath(screenshot_gray, 10, 0, 7)

    # ===== Gambar ke Window =====
    window.blit(background, (0, 0))

    if path:
        # Gambar Titik dan Garis Path
        for i in range(len(path)):
            x, y = path[i]
            pygame.draw.circle(window, (255, 0, 255), (y, x), 8)
            if i < len(path) - 1:
                next_x, next_y = path[i + 1]
                pygame.draw.line(window, (255, 0, 255), (y, x), (next_y, next_x), 3)

        # Simpan Screenshot
        cv2.imwrite('gambar.jpg', screenshot_color)

        # Dapatkan Orientasi
        y, x = path[idx]
        dt = GetOrientation(screenshot_gray, path[idx], 0, False)
        if dt and dt != 0:
            start = dt['koordinat']['start']
            if start:
                pygame.draw.line(window, (128, 64, 128), start, (x, y), 3)

                # Tampilkan Teks "ROBOT" di Posisi Start
                text_surface = font.render("ROBOT", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=start)
                window.blit(text_surface, text_rect)

    # ===== Gambar Robot =====
    window.blit(rotated_robot, robot_rect.topleft)

    pygame.display.flip()

# ===== Keluar Program =====
pygame.quit()
sys.exit()
