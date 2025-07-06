from Utils import *

# Konfigurasi Serial
PORT = 'COM11 '
BAUDRATE = 9600
last_send_time = time.time()
send_interval = 0.1  # 100ms
current_time = None

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"Tersambung ke {PORT}")
except serial.SerialException as e:
    print(f"Gagal membuka port serial: {e}")
    exit()

pwm(ser, 0, 0)