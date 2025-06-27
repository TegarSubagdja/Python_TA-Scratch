import pygame
import cv2
import numpy as np
import sys
from Utils import *  # Pastikan ada getPath di sini

# Inisialisasi Pygame
pygame.init()

# Ukuran Window
WIDTH, HEIGHT = 2000, 920
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Follower")

# Load Background dan Gambar Robot
background = pygame.image.load("Image/1.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Gambar asli robot disimpan untuk rotasi berulang tanpa rusak kualitas
robot_original = pygame.image.load("aruco.png")
robot_original = pygame.transform.scale(robot_original, (100, 100))

# Variabel untuk sudut rotasi
rotation_angle = 0
path = None
idx = 0

# Loop Utama
running = True
while running:

    screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
    screenshot = np.transpose(screenshot, (1, 0, 2))
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_p:
                filename = "Output/normal.jpg"
                cv2.imwrite(filename, screenshot)
                print(f"Gambar disimpan sebagai {filename}")

            if event.key == pygame.K_LEFT:
                rotation_angle += 10

            if event.key == pygame.K_RIGHT:
                rotation_angle -= 10

            if event.key == pygame.K_r:
                path = None  

    # Dapatkan posisi mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Rotate gambar robot
    rotated_robot = pygame.transform.rotate(robot_original, rotation_angle)
    robot_rect = rotated_robot.get_rect(center=(mouse_x, mouse_y))

    # Screenshot layar untuk proses path
    if path is None:
        screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
        screenshot = np.transpose(screenshot, (1, 0, 2))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Pastikan getPath mengembalikan list atau None
        path = getPath(screenshot, 10, 0, 7)

    # === Gambar ke Window ===

    window.blit(background, (0, 0))

    # Gambar path jika ada
    if path != None and path != 0:
        for i in range(len(path)):
            x, y = path[i]
            pygame.draw.circle(window, (255, 0, 255), (y, x), 8)
            if i < len(path) - 1:
                next_x, next_y = path[i + 1]
                pygame.draw.line(window, (255, 0, 255), (y, x), (next_y, next_x), 3)

    if path != None and path != 0:
        cv2.imwrite('gambar.jpg', screenshot)
        y, x = path[idx]
        dt = GetOrientation(screenshot, path[idx], 0, False)
        if dt and dt != 0:
            start = dt['koordinat']['start']
            if start != None:
                pygame.draw.line(window, (128, 64, 128), start, (x, y), 3)

    # Gambar robot
    window.blit(rotated_robot, robot_rect.topleft)

    pygame.display.flip()

pygame.quit()
sys.exit()
