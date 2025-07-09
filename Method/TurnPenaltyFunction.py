def TurnPenalty(current, next, penalty):
    x1, y1 = current
    x2, y2 = next

    # Cek apakah pergerakan diagonal
    if x1 != x2 and y1 != y2:
        return penalty
    else:
        return 0
