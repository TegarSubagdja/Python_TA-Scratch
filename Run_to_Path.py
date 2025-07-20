from Utils import *

# Setup Serial
ser = None
selected_port = "COM9"
try:
    ser = serial.Serial(selected_port, 9600, timeout=1)
    print(f"Tersambung ke {selected_port}")
except Exception as e:
    print(f"Gagal membuka port {selected_port}: {e}")
    exit()

# Set Path
path = None

# Setup kamera
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
desired_width = 1280
desired_height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

# Set current dengan waktu terkini
current = time.time()

# Variabel untuk informasi
errDist, errDegree, avg_degree = 0, 0, 0
left_speed, right_speed = 0, 0
marker_lost_time = time.time()
last_time = time.time()

# Paramerter Control
base_speed = 40
MAX_SPEED = 40
MIN_PWM = 0
correction_limit = MAX_SPEED  # agar max total speed = 60 ± 20 = 80
pid = PID(Kp=0.45, Ki=0.1, Kd=0.13, dt=0.1, output_limit=correction_limit, integral_limit=MAX_SPEED)

#Buffer untuk error yang stabil
degree_buffer = deque(maxlen=3)

running = True
while running:
    ret, frame = cap.read()
    if not ret:
        break

    # Rubah frama kedalam bentuk grayscale
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Cari posisi robot
    start, goal, marksize = Pos(img)

    if start is None and goal is None:
        if marker_lost_time is None:
            marker_lost_time = time.time()
        elif time.time() - marker_lost_time >= 2:
            path = None
    else:
        # Marker muncul kembali, reset timer
        marker_lost_time = None

    if (not path and start and goal):

        # Cari error ke posisi goal
        errDist, errDegree = Error(img.copy(), start, goal)

        if errDist < ( 2 * marksize):
            cv2.imshow("Frame", img)
            if cv2.waitKey(1) & 0xFF == 27:
                running = False
                continue

        left_speed = 0
        right_speed = 0

        if ser: pwm(ser, 0, 0)

        map = Prep(img.copy(), start, goal, markSize=marksize)

        pStart, pGoal = PrepCoord(start, goal)

        (path, times), *_ = Astar_Optimize.methodBds(map, pStart, pGoal, 2, PPO=True)

        if path:
            pStart, pGoal, path = PrepCoord(pStart, pGoal, path)
            path.pop(0)

    elif (start and goal): 
        marker_lost_time = None

        # Cari error ke posisi goal
        target = tuple(path[0])

        errDist, errDegree = Error(img, start, target)

        # Buffer untuk degree
        degree_buffer.append(errDegree)
        avg_degree = sum(degree_buffer) / len(degree_buffer)

        # Hitung dt secara real time
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        # Update PID dengan dt yang sebenarnya
        pid.dt = dt
        correction = pid.calc(avg_degree)

        # Clamp ke max speed dan min PWM
        left_speed = int(base_speed + correction + 5)
        right_speed = int(base_speed - correction)
        left_speed = max(MIN_PWM, min(MAX_SPEED, left_speed))
        right_speed = max(MIN_PWM, min(MAX_SPEED, right_speed))

        if ser: pwm(ser, left_speed, right_speed)

        # Gambar seluruh path dan beri teks nomor
        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i + 1]
            cv2.line(img, p1, p2, 255, 2)

            # Tambahkan teks koordinat path di titik p1
            cv2.circle(img, p1, 4, 255, -1)
            cv2.putText(img, str(p1), (p1[0] + 10, p1[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1, cv2.LINE_AA)

        # Jika jarak robot ke tujuan sudah dekat, keluarkan titik tujuan
        if len(path) == 1:
            if errDist < (3 * marksize):
                # if ser: pwm(ser, 0, 0)
                # pid.reset()
                path = None
        elif errDist < (marksize):
            # if ser: pwm(ser, 0, 0)
            # pid.reset()
            path.pop(0)
    
    # Tampilkan informasi
    cv2.putText(img, f"Dist   : {int(errDist)}", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255), 2)
    cv2.putText(img, f"Degree : {int(avg_degree)}", (10, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255), 2)
    cv2.putText(img, f"Left Speed  : {left_speed}", (10, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255), 2)
    cv2.putText(img, f"Right Speed : {right_speed}", (10, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (255), 2)

    cv2.imshow("Frame", img)
    if cv2.waitKey(1) & 0xFF == 27:
        if ser: pwm(ser, 0, 0)
        running = False

cap.release()
cv2.destroyAllWindows()