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
    
    def reset(self):
        self.integral = 0.0
        self.last_error = 0.0

# Dummy callback
def nothing(x):
    pass