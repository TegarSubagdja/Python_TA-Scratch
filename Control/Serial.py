import serial
import time

PORT = 'COM7'
BAUDRATE = 9600

def pwm(ser, nilai):
    """
    Mengirimkan nilai PWM 0-255 ke ESP32 melalui Serial
    """
    if not (0 <= nilai <= 255):
        print("Nilai PWM harus antara 0-255")
        return

    ser.write(bytes([nilai]))
    print(f"Nilai PWM {nilai} dikirim")

if __name__ == "__main__":
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            print(f"Tersambung ke {PORT}")

            while True:
                nilai = int(input("Masukkan nilai PWM (0-255): "))
                pwm(ser, nilai)

    except serial.SerialException as e:
        print(f"Gagal membuka port serial: {e}")
    except KeyboardInterrupt:
        print("\nDihentikan oleh user.")
