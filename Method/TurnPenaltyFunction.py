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