from Utils import *

class PID:
    def __init__(self, Kp, Ki, Kd, dt, output_limit=255, integral_limit=255):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.last_error = 0.0
        self.integral = 0.0
        self.output_limit = output_limit
        self.integral_limit = integral_limit

    def calc(self, error):
   
        self.integral += error * self.dt

        # Clamp integral to prevent windup
        self.integral = max(-self.integral_limit, min(self.integral, self.integral_limit))

        derivative = (error - self.last_error) / self.dt if self.dt > 0 else 0.0

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        # Clamp output
        output = max(-self.output_limit, min(output, self.output_limit))

        self.last_error = error
        return output

# Dummy callback
def nothing(x):
    pass

if __name__ == "__main__":
    # Buat window dan trackbar
    cv2.namedWindow("PID Control")
    cv2.createTrackbar("Angle Target", "PID Control", 0, 180, nothing)
    cv2.createTrackbar("Angle Sekarang", "PID Control", 0, 180, nothing)

    # Inisialisasi PID controller
    pid = PID(Kp=2, Ki=1, Kd=1, dt=0.01, output_limit=255, integral_limit=200)
    base_speed = 200

    while True:
        target_angle = cv2.getTrackbarPos("Angle Target", "PID Control")
        current_angle = cv2.getTrackbarPos("Angle Sekarang", "PID Control")

        correction = pid.calc(target_angle, current_angle)

        left_speed = max(0, min(255, int(base_speed + correction)))
        right_speed = max(0, min(255, int(base_speed - correction)))

        # Visualisasi
        img = np.zeros((320, 500, 3), dtype=np.uint8)
        cv2.putText(img, f"Target Angle     : {target_angle} deg", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
        cv2.putText(img, f"Current Angle    : {current_angle} deg", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)
        cv2.putText(img, f"Error            : {target_angle - current_angle} deg", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(img, f"PID Output       : {correction:.2f}", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)
        cv2.putText(img, f"Integral Clamped : {pid.integral:.2f}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 150, 255), 2)
        cv2.putText(img, f"Motor Kiri (L)   : {left_speed}", (20, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 100), 2)
        cv2.putText(img, f"Motor Kanan (R)  : {right_speed}", (20, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 100), 2)

        cv2.imshow("PID Control", img)

        if cv2.waitKey(100) == 27:  # ESC to quit
            break

    cv2.destroyAllWindows()
