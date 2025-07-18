from Utils import *

def pwm(ser, kiri, kanan):
    if not (0 <= kiri <= 255 and 0 <= kanan <= 255):
        print("Nilai PWM harus antara 0-255")
        return
    data = f"{kiri},{kanan}\n"
    ser.write(data.encode())
