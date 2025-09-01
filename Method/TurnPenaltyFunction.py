from math import gcd #Sama dengan FPB (Faktor Persekutuan Terbesar).

def get_slope(a, b):
    dx = b[1] - a[1]  # kolom
    dy = b[0] - a[0]  # baris
    if dx == 0: return 'inf'  # Vertikal
    return dy / dx

def TurnPenalty(prev, current, next_point, K=1):
    if prev == (0, 0) or current == (0, 0) or next_point == (0, 0):
        return 0

    slope1 = get_slope(prev, current)
    slope2 = get_slope(current, next_point)

    return K if slope1 != slope2 else 0

def TurnPenalty(prev, current, next_point, K=1):

    if prev == (0, 0) or current == (0, 0) or next_point == (0, 0):
        return 0
    
    n1, n2 = current
    g1, g2 = next_point
    s1, s2 = prev

    dx1 = abs(g1 - n1)
    dy1 = abs(g2 - n2)

    dx2 = abs(g1 - s1)
    dy2 = abs(g2 - s2)

    penalty = abs(dx1 * dy2 - dx2 * dy1) * K

    # print(f"Dari titik {prev} ke titik {current} ke titik {next_point} nilai penalty = {penalty}")

    return penalty

def normalize(dx, dy):
    if dx == 0 and dy == 0:
        return (0, 0)
    g = gcd(abs(dx), abs(dy))
    return (dx // g, dy // g)

def Turn(path):
    turns = []

    for i in range(1, len(path) - 1):
        x_prev, y_prev = path[i - 1]
        x_curr, y_curr = path[i]
        x_next, y_next = path[i + 1]

        dir1 = normalize(x_curr - x_prev, y_curr - y_prev)
        dir2 = normalize(x_next - x_curr, y_next - y_curr)

        if dir1 != dir2:
            turns.append(path[i])

    return turns

if __name__ == "__main__":
    prev = (1,1)
    current = (1,2)
    neighbor = (1,12)

    turn = TurnPenalty(prev, current, neighbor)
    print(turn)



