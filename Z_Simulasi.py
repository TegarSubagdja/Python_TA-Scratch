from Utils import*
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
pointIdx = 0
dt = None

# Loop Utama
running = True
# Loop Utama
running = True

while running:
    # Cari path jika belum ada
    if not path or path:
        screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
        screenshot = np.transpose(screenshot, (1, 0, 2))  # Swap axis width <-> height
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)  # Konversi ke grayscale
        path = getPath(screenshot, 16, 0, 7)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_p:
                screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
                screenshot = np.transpose(screenshot, (1, 0, 2))
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
                filename = f"Output/normal.jpg"
                cv2.imwrite(filename, screenshot)
                print(f"Gambar disimpan sebagai {filename}")

            if event.key == pygame.K_LEFT:
                rotation_angle += 10

            if event.key == pygame.K_RIGHT:
                rotation_angle -= 10

    # Dapatkan posisi mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Rotate gambar robot
    rotated_robot = pygame.transform.rotate(robot_original, rotation_angle)
    robot_rect = rotated_robot.get_rect(center=(mouse_x, mouse_y))

    # Gambar ke window
    window.blit(background, (0, 0))

    # Gambar path jika ada
    if path:
        dt = GetOrientation(screenshot, path[pointIdx], 0, False)
        if dt:
            for i in range(len(path)):
                x, y = path[i]
                # Gambar titik
                pygame.draw.circle(window, (255, 0, 255), (y, x), 8)
                # Gambar garis ke titik berikutnya jika ada
                if i < len(path) - 1:
                    next_x, next_y = path[i + 1]
                    pygame.draw.line(window, (255, 0, 255), (y, x), (next_y, next_x), 3)
            # pygame.draw.line(window, (255, 0, 255), dt['koordinat'], path[pointIdx], 3)

    window.blit(rotated_robot, robot_rect.topleft)
    pygame.display.flip()

pygame.quit()
sys.exit()

