import serial
import time

# Sesuaikan dengan port ESP32 kamu
PORT = 'COM11'
BAUDRATE = 9600

try:
    # Buka koneksi serial
    with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
        print(f"Tersambung ke {PORT}")
        
        time.sleep(2)  # Tunggu ESP32 siap

        while True:
            # Kirim '1' → nyalakan LED
            ser.write(b'1')
            print("LED ON")
            time.sleep(1)

            # Kirim '0' → matikan LED
            ser.write(b'0')
            print("LED OFF")
            time.sleep(1)

except serial.SerialException as e:
    print(f"Gagal membuka port serial: {e}")
except KeyboardInterrupt:
    print("\nDihentikan oleh user.")
