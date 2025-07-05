from Utils import *

def pwm(ser, left_pwm, right_pwm):
    """
    Mengirimkan dua nilai PWM (0-255) ke ESP32 melalui Serial.
    Format pengiriman: byte[0] = 255 (start byte), byte[1] = left_pwm, byte[2] = right_pwm
    """
    if not (0 <= left_pwm <= 255 and 0 <= right_pwm <= 255):
        print("Nilai PWM harus antara 0-255")
        return

    paket = bytes([255, left_pwm, right_pwm])  # Start byte = 255, biar ESP32 mudah sinkron
    ser.write(paket)