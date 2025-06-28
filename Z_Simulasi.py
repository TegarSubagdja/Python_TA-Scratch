from Utils import *  # Pastikan ada getPath dan GetOrientation

# ===== Inisialisasi Pygame =====
pygame.init()
WIDTH, HEIGHT = 2000/2, 920/2
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Follower")

# ===== Load Asset =====
background = pygame.image.load("Image/1.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

robot_original = pygame.image.load("aruco.png")
robot_original = pygame.transform.scale(robot_original, (25, 25))

font = pygame.font.SysFont('Arial', 30)  # Font untuk teks

# ===== Variabel Utama =====
rotation_angle = 0
path = None
idx = 0
mark_size = None

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
        path, mark_size = getPath(screenshot_gray, 20, 0, 7)
        print(path)

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

        # Dapatkan Orientasi
        y, x = path[idx]
        dt = GetOrientation(screenshot_gray, (x, y), 0, False)
        if dt and dt != 0:
            start = dt['koordinat']['start']
            distance = int(dt['distance'])
            error = int(dt['error_orientasi_derajat'])
            orientation = int(dt['orientasi_robot'])

            if start:
                pygame.draw.line(window, (64, 0, 64), start, (x, y), 3)
                
                # Teks yang ingin ditampilkan
                texts = [
                    "ROBOT",
                    f"Jarak: {distance} cm",
                    f"Arah: {error}°",
                    f"Orientasi: {orientation}"
                ]

                spacing = 30  # Jarak antar baris teks
                margin_x = 20  # Jarak dari sisi kiri layar
                margin_y = 20  # Jarak dari sisi bawah layar

                for i, txt in enumerate(texts):
                    text_surface = font.render(txt, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(topleft=(margin_x, window.get_height() - margin_y - (len(texts) - i) * spacing))
                    window.blit(text_surface, text_rect)

            if distance == None or distance <= mark_size+(mark_size/2):
                path.pop(0)
            
    # ===== Gambar Robot =====
    window.blit(rotated_robot, robot_rect.topleft)

    pygame.display.flip()

# ===== Keluar Program =====
pygame.quit()
sys.exit()
