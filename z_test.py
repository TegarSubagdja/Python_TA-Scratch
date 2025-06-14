result = []

for i in range(1, 100): 
    for j in range(1, 100):
        dx = i % j
        dy = i // j
        final = (dy * j) + dx
        print(f"{i} dibagi {j}, sisa {dx}, hasil bagi {dy}, dikembalikan lagi menjadi {final}") 