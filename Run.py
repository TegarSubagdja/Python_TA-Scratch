from Utils import *

pid = PID(Kp=1, Ki=1, Kd=1, dt=0.1, output_limit=255, integral_limit=200)

target = 10
current = 20

correction = pid.calc(setpoint=target, current_value=current)

print(correction)

#Mulai
