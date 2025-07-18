from Utils import *
import cv2
from serial.tools import list_ports

def pilih_serial():
    ports = list(list_ports.comports())
    if not ports:
        print("Tidak ada port serial yang terdeteksi.")
        exit()

    print("Pilih port serial yang tersedia:")
    for i, port in enumerate(ports):
        print(f"[{i}] {port.device} - {port.description}")

    try:
        # pilihan = int(input("Masukkan nomor port yang dipilih: "))
        # selected_port = ports[pilihan].device
        selected_port = "COM9"
    except (IndexError, ValueError):
        print("Pilihan tidak valid.")
        exit()

    try:
        ser = serial.Serial(selected_port, 9600, timeout=1)
        print(f"Tersambung ke {selected_port}")
        return ser
    except Exception as e:
        print(f"Gagal membuka port {selected_port}: {e}")
        exit()

def pwm(ser, kiri, kanan):
    if not (0 <= kiri <= 255 and 0 <= kanan <= 255):
        print("Nilai PWM harus antara 0-255")
        return
    data = f"{kiri},{kanan}\n"
    ser.write(data.encode())

# ===== Main Program =====
ser = pilih_serial()
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ==============================
# PARAMETER KONTROL
# ==============================
base_speed = 50
MAX_SPEED = 50
MIN_PWM = 0
correction_limit = 40  # agar max total speed = 60 ± 20 = 80
pid = PID(Kp=0.52, Ki=0.5, Kd=0.26, dt=0.5, output_limit=correction_limit, integral_limit=10)
degree_buffer = deque(maxlen=3)

# ==============================
# VARIABLE UTAMA
# ==============================
running = True
left_speed = 0
right_speed = 0
errDist, errDegree, avg_degree = 0, 0, 0
marker_lost_time = None
last_time = time.time()

while running:
    ret, frame = cap.read()
    if not ret:
        print("Frame gagal dibaca.")
        break

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    start, goal, marksize = Pos(img)

    if not start or not goal:
        if marker_lost_time is None:
            marker_lost_time = time.time()
        elif time.time() - marker_lost_time >= 1:
            left_speed = 0
            right_speed = 0
            if ser: pwm(ser, 0, 0)
    else:
        marker_lost_time = None
        errDist, errDegree = Error(img, start, goal)

        # Buffer untuk degree
        degree_buffer.append(errDegree)
        avg_degree = sum(degree_buffer) / len(degree_buffer)

        if errDist > 3 * marksize:

            # Hitung dt secara real time
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            # Update PID dengan dt yang sebenarnya
            pid.dt = dt
            correction = pid.calc(avg_degree)

            left_speed = int(base_speed + correction)
            right_speed = int(base_speed - correction)

            # Clamp ke max speed dan min PWM
            left_speed = max(MIN_PWM, min(MAX_SPEED, left_speed))
            right_speed = max(MIN_PWM, min(MAX_SPEED, right_speed))

            if ser:
                pwm(ser, left_speed, right_speed)
        else:
            left_speed = 0
            right_speed = 0
            if ser:
                pwm(ser, 0, 0)

    # Tampilkan informasi
    cv2.putText(img, f"Dist   : {int(errDist)}", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255), 2)
    cv2.putText(img, f"Degree : {int(avg_degree)}", (10, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255), 2)
    cv2.putText(img, f"Left Speed  : {left_speed}", (10, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255), 2)
    cv2.putText(img, f"Right Speed : {right_speed}", (10, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (255), 2)

    cv2.imshow("Tracking", img)
    if cv2.waitKey(1) & 0xFF == 27:
        if ser: pwm(ser, 0, 0)
        break

cap.release()
ser and ser.close()
cv2.destroyAllWindows()