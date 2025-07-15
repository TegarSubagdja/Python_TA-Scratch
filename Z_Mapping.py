from Utils import *
from Algoritma import Astar_Komentar
from Method.PathPolylineOptimization import Prunning

# Variabel untuk ketebalan garis
LINE_WIDTH = 2  # Menentukan ketebalan garis, bisa diubah sesuai kebutuhan
LINE_COLOR = "#0E88EF"

# Variabel untuk pengaturan warna dan ukuran bulatan
CIRCLE_RADIUS = 10  # Ukuran radius bulatan (dalam pixel)
CIRCLE_COLOR = "#000000"  # Warna bulatan, misalnya tomat

# Konfigurasi grid
GRID_SIZE = 16
WIDTH = 512 #GRID_SIZE * CELL_SIZE
HEIGHT = 512 #GRID_SIZE * CELL_SIZE
CELL_SIZE = WIDTH//GRID_SIZE

# Inisialisasi Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Grid Editor")
font = pygame.font.SysFont(None, 16)

# Warna untuk setiap elemen grid dalam kode HEX
colors = {
    0: "#FFFFFF",  # Ruang kosong
    1: "#17252a",  # Rintangan
    2: "#3aafa9",  # Start
    3: "#FF0021",  # Goal
    4: "#3f6184",  # Garis
    5: "#FFFF00",  # Open List (kuning)
    6: "#FFA500",  # Close List (oranye)
    7: "#778899",  # Warna abu-abu
    8: "#e8175d",  # Warna pink
}

# Inisialisasi grid
map_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
# Status aktif (0 = ruang kosong, 1 = rintangan, 2 = start, 3 = goal, 4 = garis, 5 = open, 6 = close, 7 = gray)
active_mode = 1  # Default mode rintangan
lines = []  # Menyimpan semua garis sebagai ((x1, y1), (x2, y2))

# Variabel untuk mengontrol apakah koordinat ditampilkan atau tidak
show_coordinates = False

# Variabel untuk drag drawing
is_dragging = False
last_cell = None  # Menyimpan sel terakhir yang diproses saat drag

# Variabel untuk metode yang digunakan
method = 1

# Fungsi untuk mengonversi kode HEX menjadi tuple RGB
def hex_to_rgb(hex_code):
    """Mengubah kode HEX menjadi tuple RGB."""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))

def save_grid_to_json(fixed_path="Map/JSON/Map.json"):
    try:
        # Ambil direktori, nama file tanpa ekstensi, dan ekstensi
        directory, filename = os.path.split(fixed_path)
        name, ext = os.path.splitext(filename)

        # Tentukan nama file akhir jika file sudah ada
        counter = 1
        new_path = fixed_path
        while os.path.exists(new_path):
            new_path = os.path.join(directory, f"{name}_{counter}{ext}")
            counter += 1

        # Konversi dan simpan
        grid_list = map_grid.tolist()  # Pastikan map_grid sudah tersedia di global
        with open(new_path, 'w') as f:
            json.dump(grid_list, f, indent=4)
        print(f"Grid berhasil disimpan ke '{new_path}'")

    except Exception as e:
        print(f"Gagal menyimpan grid: {e}")


# Fungsi untuk menggambar grid, termasuk koordinat jika diaktifkan
def draw_grid(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row, col]
            color = hex_to_rgb(colors.get(value, "#FFFFFF"))
            pygame.draw.rect(
                screen,
                color,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            # Gambar garis grid
            pygame.draw.rect(
                screen,
                (200, 200, 200),
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1
            )
            # Jika koordinat diaktifkan, tampilkan koordinat di pojok kanan atas
            if show_coordinates:
                label = f"{row},{col}"
                coord_text = font.render(label, True, (0, 0, 0))
                text_width, text_height = font.size(label)
                
                # Posisi pojok kanan bawah sel, dikurangi sedikit margin
                text_x = col * CELL_SIZE + CELL_SIZE - text_width - 2
                text_y = row * CELL_SIZE + CELL_SIZE - text_height - 2

                screen.blit(coord_text, (text_x, text_y))


# Fungsi untuk menampilkan mode aktif di layar
def display_mode(text):
    mode_text = font.render(f"Mode: {text}", True, (0, 0, 0))
    screen.blit(mode_text, (10, HEIGHT - 30))

# Fungsi untuk menggambar garis-garis
def draw_lines():
    """Menggambar semua garis yang tersimpan di daftar lines."""
    for line in lines:
        pygame.draw.line(screen, hex_to_rgb(LINE_COLOR), line[0], line[1], LINE_WIDTH)  # Width dapat disesuaikan

        # Titik awal dan akhir garis (tambah bulatan kecil)
        start_x, start_y = line[0]
        end_x, end_y = line[1]
        
        # Menambahkan bulatan di titik awal
        pygame.draw.circle(screen, hex_to_rgb(CIRCLE_COLOR), (start_x, start_y), CIRCLE_RADIUS)  # Radius sesuai variabel
        
        # Menambahkan bulatan di titik akhir
        pygame.draw.circle(screen, hex_to_rgb(CIRCLE_COLOR), (end_x, end_y), CIRCLE_RADIUS)  # Radius sesuai variabel

# Fungsi untuk menyimpan gambar dengan nama yang dipilih pengguna
def save_image(replace=False, default_filename='grid_image.png'):
    """
    Menyimpan grid dan path sebagai file gambar PNG.
    
    Parameters:
    - replace (bool): Jika True, akan menimpa file yang sudah ada 
                      Jika False, akan memunculkan dialog pemilihan file baru
    - default_filename (str): Nama file default jika mode replace aktif
    """
    root = tk.Tk()
    root.withdraw()  # Menyembunyikan jendela utama tkinter

    if replace:
        # Mode replace - gunakan nama file default atau path yang sudah ada
        file_path = default_filename
    else:
        # Menampilkan dialog penyimpanan file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", 
            initialfile=default_filename,
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save Image As"
        )

    if file_path:  # Jika ada path file
        try:
            pygame.image.save(screen, file_path)
            print(f"Grid dan path berhasil disimpan sebagai '{file_path}'")
            return True
        except Exception as e:
            print(f"Gagal menyimpan gambar: {e}")
            return False

# Fungsi untuk memproses sel pada saat drag
def process_cell(row, col):
    """Memproses sel berdasarkan mode aktif saat ini."""
    if active_mode == 1:  # Mode rintangan
        map_grid[row, col] = 1
    elif active_mode == 0:  # Mode kosong (clear)
        map_grid[row, col] = 0
    elif active_mode == 5:  # Mode open list
        map_grid[row, col] = 5
    elif active_mode == 6:  # Mode close list
        map_grid[row, col] = 6
    elif active_mode == 7:  # Mode abu-abu
        map_grid[row, col] = 7
    elif active_mode == 8:  # Mode pink
        map_grid[row, col] = 8
    elif active_mode == 9:  # Mode pink
        map_grid[row, col] = 8
    # Mode 2 (start) dan 3 (goal) ditangani khusus di event klik
# Program utama
running = True
drawing_line = False  # Apakah sedang menggambar garis
start_cell = None     # Titik awal garis dalam koordinat grid
path_result = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Klik kiri untuk menggambar atau menetapkan sel di grid
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE
            
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:  # Pastikan dalam batas grid
                if active_mode == 4:  # Mode garis
                    if not drawing_line:
                        start_cell = (row, col)  # Titik awal dalam koordinat grid
                        drawing_line = True
                    else:
                        end_cell = (row, col)  # Titik akhir dalam koordinat grid
                        # Hitung titik tengah untuk kedua sel
                        start_center = (start_cell[1] * CELL_SIZE + CELL_SIZE // 2, start_cell[0] * CELL_SIZE + CELL_SIZE // 2)
                        end_center = (end_cell[1] * CELL_SIZE + CELL_SIZE // 2, end_cell[0] * CELL_SIZE + CELL_SIZE // 2)
                        lines.append((start_center, end_center))  # Simpan garis
                        drawing_line = False
                elif active_mode == 2:  # Mode start
                    map_grid[map_grid == 2] = 0  # Hapus start lama
                    map_grid[row, col] = 2
                elif active_mode == 3:  # Mode goal
                    map_grid[map_grid == 3] = 0  # Hapus goal lama
                    map_grid[row, col] = 3
                elif active_mode == 9:
                    clicked = (row, col)
                    start = np.argwhere(map_grid == 2)
                    goal = np.argwhere(map_grid == 3)
                    if start.size != 0 and goal.size != 0:
                        start = tuple(map(int, start[0]))
                        goal = tuple(map(int, goal[0]))

                        def euclidean(a, b):
                            return round(np.linalg.norm(np.array(a) - np.array(b)), 4)

                        jarak_ke_start = euclidean(clicked, start)
                        jarak_ke_goal = euclidean(clicked, goal)

                        print(f"\n📍 Diklik di titik: {clicked}")
                        print(f"↔️  Jarak ke START {start}: {jarak_ke_start}")
                        print(f"↔️  Jarak ke GOAL  {goal}: {jarak_ke_goal}")
                        print(f"↔️  Total  {start, goal}: {jarak_ke_start + jarak_ke_goal}\n")
                    else:
                        print("⚠️  Start atau Goal belum ditentukan.")
                else:  # Mode yang bisa di-drag (obstacle, clear, dll)
                    is_dragging = True
                    last_cell = (row, col)
                    process_cell(row, col)

        # Mouse bergerak saat tombol ditahan (drag)
        elif event.type == pygame.MOUSEMOTION:
            if is_dragging:
                x, y = pygame.mouse.get_pos()
                col, row = x // CELL_SIZE, y // CELL_SIZE
                
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:  # Pastikan dalam batas grid
                    current_cell = (row, col)
                    if current_cell != last_cell:  # Hanya proses jika sel berubah
                        process_cell(row, col)
                        last_cell = current_cell

        # Lepas tombol mouse
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_dragging = False
            last_cell = None

        # Ganti mode dengan kombinasi tombol
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_mods() & pygame.KMOD_CTRL:  # Jika Ctrl ditekan
                if event.key == pygame.K_s:  # Ctrl + S untuk start
                    active_mode = 2
                    is_dragging = False  # Pastikan drag tidak aktif saat ganti mode
                elif event.key == pygame.K_g:  # Ctrl + G untuk goal
                    active_mode = 3
                    is_dragging = False
                elif event.key == pygame.K_o:  # Ctrl + O untuk obstacle
                    active_mode = 1
                elif event.key == pygame.K_c:  # Ctrl + C untuk ruang kosong
                    active_mode = 0
                elif event.key == pygame.K_l:  # Ctrl + L untuk garis
                    active_mode = 4
                    is_dragging = False
                elif event.key == pygame.K_u:  # Ctrl + U untuk open list
                    active_mode = 5
                elif event.key == pygame.K_x:  # Ctrl + X untuk close list
                    active_mode = 6
                elif event.key == pygame.K_e:  # Ctrl + E untuk warna abu-abu
                    active_mode = 7
                elif event.key == pygame.K_q:  # Ctrl + Q untuk warna pink
                    active_mode = 8
                elif event.key == pygame.K_h:  # Ctrl + Q untuk warna pink
                    active_mode = 9
                    is_dragging = False
                elif event.key == pygame.K_p:  # Ctrl + P untuk save
                    save_image(replace=False)
                elif event.key == pygame.K_r:  # Ctrl + R untuk reset grid
                    map_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
                    lines = []
                elif event.key == pygame.K_i:  # Ctrl + I untuk menampilkan koordinat
                    show_coordinates = not show_coordinates
                elif event.key == pygame.K_t:  # Ctrl + T untuk menghapus garis terakhir
                    if lines:
                        lines.pop()  # Hapus garis terakhir
                elif event.key == pygame.K_m:  # Ctrl + M untuk JPS
                    map_grid[(map_grid == 6) | (map_grid == 5) | (map_grid == 8)] = 0
                    start = np.argwhere(map_grid == 2)
                    goal = np.argwhere(map_grid == 3)
                    pqueue = None
                    closet = None
                    if start.size != 0 or goal.size != 0:
                        start = tuple(map(int, start[0]))
                        goal = tuple(map(int, goal[0]))
                        if method == 1:
                            path_result, closet, pqueue = astar.method(map_grid, start, goal, 2)
                        elif method == 2:
                            path_result, closet, pqueue = jps.method(map_grid, start, goal, 2)
                    else:
                        path_result = jps.method(map_grid, (0,0), (2,2), 2)
                    path_result = path_result[0]
                    path_result = path_result[1:-1]

                elif event.key == pygame.K_n:
                    map_grid[(map_grid == 6) | (map_grid == 5) | (map_grid == 8)] = 0
                    with open("Output/grid_output.txt", "w") as file:
                        file.write("[\n")
                        for row in map_grid:  # loop per baris
                            # Ubah setiap elemen ke int biasa (bukan np.int32 misalnya)
                            row_list = [int(item) for item in row]
                            file.write(f"    {row_list},\n")
                        file.write("]\n")
                        print("Berhasil disimpan")

                elif event.key == pygame.K_f:  # Ctrl + f untuk JPS
                    with open("Output/grid_output.txt", "r") as file:
                        content = file.read()
                        grid_list = ast.literal_eval(content)
                    map_grid = np.array(grid_list)

                elif event.key == pygame.K_b:
                    start = np.argwhere(map_grid == 2)
                    goal = np.argwhere(map_grid == 3)
                    if start.size != 0 or goal.size != 0:
                        start = tuple(map(int, start[0]))
                        goal = tuple(map(int, goal[0]))
                        print(f"Start adalah {start} dan goal adalah {goal}")
                        path_result, closet, pqueue = Astar_Komentar.method(map_grid, start, goal, 2)
                        path_prunning = Prunning(path_result[0], map_grid)
                        print(f"Path asli adalah : {path_result}")
                        print(f"Path prunning adalah : {path_prunning}")
                
                elif event.key == pygame.K_1:
                    method = 1
                elif event.key == pygame.K_2:
                    method = 2
                elif event.key == pygame.K_3:
                    method = 3
                elif event.key == pygame.K_4:
                    method = 4
                elif event.key == pygame.K_j:  # Ctrl + J untuk save ke JSON
                    save_grid_to_json()
            elif event.key == pygame.K_ESCAPE:  
                running = False
    # Gambar ulang layar
    screen.fill(hex_to_rgb("#FFFFFF"))
    draw_grid(map_grid)
    draw_lines()  # Gambar semua garis

    # Tampilkan teks mode aktif
    mode_texts = {
        0: "Clear (Ctrl + C)",
        1: "Obstacle (Ctrl + O)",
        2: "Start (Ctrl + S)",
        3: "Goal (Ctrl + G)",
        4: "Line (Ctrl + L)",
        5: "Open List (Ctrl + U)",
        6: "Close List (Ctrl + X)",
        7: "Gray (Ctrl + E)",
        8: "Pink (Ctrl + Q)",
        9: "Euclidean Measure (Ctrl + H)"
    }
    display_mode(mode_texts.get(active_mode, "Unknown"))

    pygame.display.flip()

pygame.quit()