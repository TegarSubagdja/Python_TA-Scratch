from Utils import *

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obstacle Drawing with Pathfinding")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Konfigurasi obstacle
OBSTACLE_SIZE = (40, 20)  # width x height
obstacles = []  # menyimpan rect obstacle

# Inisialisasi ArUco
detector_params = aruco.DetectorParameters()
detector_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
detector = aruco.ArucoDetector(detector_dict, detector_params)

# Konversi cv2 ke pygame surface
def cvimg_to_pygame(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.rot90(image)
    return pygame.surfarray.make_surface(image)

# Load marker
aruco_img1_cv = cv2.imread("Aruco/Marker/aruco_marker_id_0DICT_4X4_50.png")
aruco_img1_cv = cv2.resize(aruco_img1_cv, (0, 0), fx=0.05, fy=0.05)
aruco_img1_cv = cv2.flip(aruco_img1_cv, 1)
if aruco_img1_cv is None:
    raise FileNotFoundError("Marker 1 tidak ditemukan.")
aruco_surface1 = cvimg_to_pygame(aruco_img1_cv)

aruco_img2_cv = cv2.imread("Aruco/Marker/aruco_marker_id_1DICT_4X4_50.png")
aruco_img2_cv = cv2.resize(aruco_img2_cv, (0, 0), fx=0.05, fy=0.05)
aruco_img2_cv = cv2.flip(aruco_img2_cv, 1)
if aruco_img2_cv is None:
    raise FileNotFoundError("Marker 2 tidak ditemukan.")
aruco_surface2 = cvimg_to_pygame(aruco_img2_cv)

marker_size = aruco_surface1.get_size()
marker1_pos = np.array([WIDTH // 3, HEIGHT // 2], dtype=float)
marker2_pos = np.array([2 * WIDTH // 3, HEIGHT // 2], dtype=float)

draw_mode = False
path = []
save_on_mouseup = False
dragging_marker = None

def toImage(surface):
    rgb_array = pygame.surfarray.array3d(surface)
    rgb_array = np.transpose(rgb_array, (1, 0, 2))
    bgr_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
    return bgr_array


clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)
    mouse_pos = np.array(pygame.mouse.get_pos(), dtype=float)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if (pygame.key.get_mods() & pygame.KMOD_CTRL) and event.key == pygame.K_g:
                draw_mode = not draw_mode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                for i, coord in enumerate([marker1_pos, marker2_pos]):
                    rect = pygame.Rect(0, 0, *marker_size)
                    rect.center = coord
                    if rect.collidepoint(mx, my):
                        dragging_marker = i
                        break

                if draw_mode and dragging_marker is None:
                    rect = pygame.Rect(mx, my, *OBSTACLE_SIZE)
                    obstacles.append(rect)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dragging_marker is not None:
                    save_on_mouseup = True
                dragging_marker = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging_marker is not None:
                if dragging_marker == 0:
                    marker1_pos = mouse_pos
                elif dragging_marker == 1:
                    marker2_pos = mouse_pos

    for rect in obstacles:
        pygame.draw.rect(screen, BLACK, rect)

    rotated1 = pygame.transform.rotate(aruco_surface1, 0)
    rect1 = rotated1.get_rect(center=marker1_pos)
    screen.blit(rotated1, rect1)

    rotated2 = pygame.transform.rotate(aruco_surface2, 0)
    rect2 = rotated2.get_rect(center=marker2_pos)
    screen.blit(rotated2, rect2)

    if draw_mode:
        font = pygame.font.SysFont(None, 24)
        text = font.render("Draw Mode [ON] - Ctrl+G to toggle", True, RED)
        screen.blit(text, (10, 10))

    if save_on_mouseup:
        img = toImage(screen)
        print(img)
        print("Unique values in image:", np.unique(img))
        start, goal, marker_sz = Pos(img)
        img = Prep(img, start, goal)
        err = Error(start, goal)
        cv2.imwrite('hasil_image_rgb.jpg', img)
        path, times = jps.method(img, start[0], goal[0], 2, show=False)
        cv2.imwrite('gray_img.jpg', img)
        save_on_mouseup = False
        pygame.image.save(screen, "hasil_dengan_path.png")

    if path:
        for i in range(len(path) - 1):
            p1 = np.flip(path[i][::-1])
            p2 = np.flip(path[i+1][::-1])
            pygame.draw.line(screen, (0, 255, 0), p1, p2, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()