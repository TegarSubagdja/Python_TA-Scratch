import pygame
import sys
import cv2
import numpy as np

# Inisialisasi Pygame
pygame.init()

# Ukuran Window
WIDTH, HEIGHT = 1920, 1024
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Follower")

# Load Background dan Gambar Robot
background = pygame.image.load("Image/1.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Gambar asli robot disimpan untuk rotasi berulang tanpa rusak kualitas
robot_original = pygame.image.load("aruco.png")
robot_original = pygame.transform.scale(robot_original, (64, 64))

# Variabel untuk sudut rotasi
rotation_angle = 0

# Loop Utama
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # Tekan P untuk simpan screenshot
            if event.key == pygame.K_p:
                screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
                screenshot = np.transpose(screenshot, (1, 0, 2))  # Swap axis width <-> height
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Konversi ke BGR OpenCV
                filename = f"Output/screenshot_live.jpg"
                cv2.imwrite(filename, screenshot)
                print(f"Gambar disimpan sebagai {filename}")

            # Tombol panah kiri = rotate CCW
            if event.key == pygame.K_LEFT:
                rotation_angle += 10  # putar 10 derajat CCW

            # Tombol panah kanan = rotate CW
            if event.key == pygame.K_RIGHT:
                rotation_angle -= 10  # putar 10 derajat CW

    # Dapatkan posisi mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Rotate gambar berdasarkan sudut saat ini
    rotated_robot = pygame.transform.rotate(robot_original, rotation_angle)
    robot_rect = rotated_robot.get_rect(center=(mouse_x, mouse_y))

    # Gambar ke layar
    window.blit(background, (0, 0))
    window.blit(rotated_robot, robot_rect.topleft)

    pygame.display.flip()

pygame.quit()
sys.exit()
