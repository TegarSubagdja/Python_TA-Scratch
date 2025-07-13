def TurnPenalty(prev, current, next_point, K=1):
    n1, n2 = prev
    g1, g2 = current
    s1, s2 = next_point

    dx1 = abs(g1 - n1)
    dy1 = abs(g2 - n2)

    dx2 = abs(g1 - s1)
    dy2 = abs(g2 - s2)

    penalty = abs(dx1 * dy2 - dx2 * dy1) * K
    return penalty

def normalize(dx, dy):
    if dx != 0: dx = dx // abs(dx)
    if dy != 0: dy = dy // abs(dy)
    return (dx, dy)

def Turn(path):
    turns = []

    for i in range(1, len(path) - 1):
        x_prev, y_prev = path[i - 1]
        x_curr, y_curr = path[i]
        x_next, y_next = path[i + 1]

        dir1 = normalize(x_curr - x_prev, y_curr - y_prev)
        dir2 = normalize(x_next - x_curr, y_next - y_curr)

        if dir1 != dir2:
            turns.append(path[i])  # titik tengah adalah titik belok

    return turns


