from Utils import *  # Pastikan ada getPath dan GetOrientation

# ===== Inisialisasi Pygame dan Kamera =====
pygame.init()
WIDTH, HEIGHT = 640, 480
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Follower - Realtime Camera")

cap = cv2.VideoCapture(2)  # 0 untuk kamera default laptop, atau ganti ke 1,2 dst jika ada beberapa kamera

robot_original = pygame.image.load("aruco.png")
robot_original = pygame.transform.scale(robot_original, (100, 100))

font = pygame.font.SysFont('Arial', 24)

# ===== Variabel Utama =====
rotation_angle = 0
path = None
idx = 0
mark_size = None

# ===== Loop Utama =====
running = True
while running:

    ret, frame = cap.read()
    if not ret:
        print("Kamera tidak terdeteksi!")
        break

    # frame = cv2.resize(frame, (WIDTH, HEIGHT))
    screenshot_color = frame.copy()
    screenshot_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert BGR OpenCV ke RGB untuk Pygame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.flip(frame, 1)
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))

    # ===== Event Handling =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                cv2.imwrite("Output/cek.jpg", screenshot_gray)
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
        cv2.imwrite('1-getPath.jpg', screenshot_gray)
        path, mark_size = getPath(screenshot_gray, 10, 0, 1)

    # ===== Gambar ke Window =====
    window.blit(frame_surface, (0, 0))

    if path:
        # Gambar Titik dan Garis Path
        for i in range(len(path)):
            x, y = path[i]
            pygame.draw.circle(window, (255, 0, 255), (y, x), 6)
            if i < len(path) - 1:
                next_x, next_y = path[i + 1]
                pygame.draw.line(window, (255, 0, 255), (y, x), (next_y, next_x), 2)

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

                texts = [
                    "ROBOT",
                    f"Jarak: {distance} cm",
                    f"Arah: {error}°",
                    f"Orientasi: {orientation}"
                ]

                for i, txt in enumerate(texts):
                    text_surface = font.render(txt, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(topleft=(20, window.get_height() - 20 - (len(texts) - i) * 25))
                    window.blit(text_surface, text_rect)

            if distance is None or distance <= mark_size + (mark_size / 2):
                path.pop(0)

    # ===== Gambar Robot =====
    # window.blit(rotated_robot, robot_rect.topleft)

    pygame.display.flip()

# ===== Keluar Program =====
cap.release()
pygame.quit()
sys.exit()
