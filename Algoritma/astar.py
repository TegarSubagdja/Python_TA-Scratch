import math, heapq, time


def blocked(cX, cY, dX, dY, matrix):
    if cX + dX < 0 or cX + dX >= matrix.shape[0]:
        return True
    if cY + dY < 0 or cY + dY >= matrix.shape[1]:
        return True
    if dX != 0 and dY != 0:
        if matrix[cX + dX][cY] == 255 and matrix[cX][cY + dY] == 255:
            return True
        if matrix[cX + dX][cY + dY] == 255:
            return True
    else:
        if dX != 0:
            if matrix[cX + dX][cY] == 255:
                return True
        else:
            if matrix[cX][cY + dY] == 255:
                return True
    return False


def heuristic(start, goal, hchoice):
    if hchoice == 255:
        xdist = math.fabs(goal[0] - start[0])
        ydist = math.fabs(goal[1] - start[1])
        if xdist > ydist:
            return 14 * ydist + 10 * (xdist - ydist)
        else:
            return 14 * xdist + 10 * (ydist - xdist)
    if hchoice == 2:
        return math.sqrt((goal[0] - start[0]) ** 2 + (goal[1] - start[1]) ** 2)


def method(matrix, start, goal, hchoice):

    close_list = set()
    came_from = {}
    gn = {start: 0}
    fn = {start: heuristic(start, goal, hchoice)}

    open_list = []

    heapq.heappush(open_list, (fn[start], start))

    starttime = time.time()

    while open_list:

        current = heapq.heappop(open_list)[1]
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path = path[::-1]
            #print(gscore[goal])
            endtime = time.time()
            return (path, round(endtime - starttime, 6)), open_list, close_list

        close_list.add(current)
        for dX, dY in [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]:

            if blocked(current[0], current[1], dX, dY, matrix):
                continue

            neighbour = current[0] + dX, current[1] + dY

            if hchoice == 255:
                if dX != 0 and dY != 0:
                    tentative_gn = gn[current] + 14
                else:
                    tentative_gn = gn[current] + 10
            elif hchoice == 2:
                if dX != 0 and dY != 0:
                    tentative_gn = gn[current] + math.sqrt(2)
                else:
                    tentative_gn = gn[current] + 1

            if (
                neighbour in close_list
            ):  # and tentative_g_score >= gscore.get(neighbour,0):
                continue

            if tentative_gn < gn.get(
                neighbour, 0
            ) or neighbour not in [i[1] for i in open_list]:
                came_from[neighbour] = current
                gn[neighbour] = tentative_gn
                fn[neighbour] = tentative_gn + heuristic(
                    neighbour, goal, hchoice
                )
                heapq.heappush(open_list, (fn[neighbour], neighbour))
        endtime = time.time()
    return (0, round(endtime - starttime, 6))