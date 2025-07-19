import time

lastTime = time.time()

while True:
    current = time.time()

    if current - lastTime >= 2:
        print("Ya")
        lastTime = current  # reset waktu
