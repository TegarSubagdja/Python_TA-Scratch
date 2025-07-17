import cv2
import serial
import serial.tools.list_ports
import numpy as np

# Kirim dua nilai PWM ke serial
def pwm(ser, kiri, kanan):
    try:
        data = f"{kiri},{kanan}\n"
        ser.write(data.encode())
        print("Terkirim:", data.strip())
    except Exception as e:
        print("Gagal mengirim:", e)

# Deteksi port
ports = serial.tools.list_ports.comports()
available_ports = [port.device for port in ports]

print("=== Pilih Port Serial ===")
if not available_ports:
    print("⚠️ Tidak ada port COM terdeteksi. Lanjutkan tanpa koneksi.")
    port_selected = None
else:
    for i, p in enumerate(available_ports):
        print(f"{i+1}. {p}")
    try:
        index = int(input("Masukkan nomor port yang ingin digunakan: ")) - 1
        port_selected = available_ports[index]
    except:
        print("Input tidak valid, tidak memilih port.")
        port_selected = None

ser = None
connected = False
BAUDRATE = 9600

# GUI
cv2.namedWindow("Control Panel")
cv2.createTrackbar("PWM Kiri", "Control Panel", 0, 255, lambda x: None)
cv2.createTrackbar("PWM Kanan", "Control Panel", 0, 255, lambda x: None)

print("\nTekan 'c' untuk konek ke port")
print("Tekan 's' untuk kirim data")
print("Tekan ESC untuk keluar")

while True:
    img = 255 * np.ones((160, 400, 3), dtype=np.uint8)

    status = "CONNECTED" if connected else "NOT CONNECTED"
    color = (0, 200, 0) if connected else (0, 0, 255)
    cv2.putText(img, f"Status: {status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(img, "'c' Connect", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
    cv2.putText(img, "'s' Send", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
    cv2.putText(img, "'ESC' Exit", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)

    cv2.imshow("Control Panel", img)
    key = cv2.waitKey(10) & 0xFF

    if key == 27:  # ESC
        break

    elif key == ord('c') and port_selected:
        try:
            ser = serial.Serial(port_selected, BAUDRATE, timeout=1)
            print(f"Tersambung ke {port_selected}")
            connected = True
        except serial.SerialException as e:
            print(f"Gagal koneksi ke {port_selected}: {e}")
            connected = False

    elif key == ord('s') and connected:
        pwm_kiri = cv2.getTrackbarPos("PWM Kiri", "Control Panel")
        pwm_kanan = cv2.getTrackbarPos("PWM Kanan", "Control Panel")
        pwm(ser, pwm_kiri, pwm_kanan)

if ser and ser.is_open:
    ser.close()
cv2.destroyAllWindows()
