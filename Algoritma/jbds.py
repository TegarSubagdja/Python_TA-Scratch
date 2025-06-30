from Utils import *

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


def blocked(currentX, currentY, moveX, moveY, matrix):
    if currentX + moveX < 0 or currentX + moveX >= matrix.shape[0]:
        return True
    if currentY + moveY < 0 or currentY + moveY >= matrix.shape[1]:
        return True
    if moveX != 0 and moveY != 0:
        if matrix[currentX + moveX][currentY] == 255 and matrix[currentX][currentY + moveY] == 255:
            return True
        if matrix[currentX + moveX][currentY + moveY] == 255:
            return True
    else:
        if moveX != 0:
            if matrix[currentX + moveX][currentY] == 255:
                return True
        else:
            if matrix[currentX][currentY + moveY] == 255:
                return True
    return False


def dblock(currentX, currentY, moveX, moveY, matrix):
    if matrix[currentX - moveX][currentY] == 255 and matrix[currentX][currentY - moveY] == 255:
        return True
    else:
        return False


def direction(currentX, currentY, parentX, parentY):
    moveX = int(math.copysign(1, currentX - parentX))
    moveY = int(math.copysign(1, currentY - parentY))
    if currentX - parentX == 0:
        moveX = 0
    if currentY - parentY == 0:
        moveY = 0
    return (moveX, moveY)


def nodeNeighbours(currentX, currentY, parent, matrix):
    neighbours = []
    if type(parent) != tuple:
        for moveX, moveY in [
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]:
             if not blocked(currentX, currentY, moveX, moveY, matrix):
                neighbours.append((currentX + moveX, currentY + moveY))

        return neighbours
    moveX, moveY = direction(currentX, currentY, parent[0], parent[1])

    if moveX != 0 and moveY != 0:
        if not blocked(currentX, currentY, 0, moveY, matrix):
            neighbours.append((currentX, currentY + moveY))
        if not blocked(currentX, currentY, moveX, 0, matrix):
            neighbours.append((currentX + moveX, currentY))
        if (
            not blocked(currentX, currentY, 0, moveY, matrix)
            or not blocked(currentX, currentY, moveX, 0, matrix)
        ) and not blocked(currentX, currentY, moveX, moveY, matrix):
            neighbours.append((currentX + moveX, currentY + moveY))
        if blocked(currentX, currentY, -moveX, 0, matrix) and not blocked(
            currentX, currentY, 0, moveY, matrix
        ):
            neighbours.append((currentX - moveX, currentY + moveY))
        if blocked(currentX, currentY, 0, -moveY, matrix) and not blocked(
            currentX, currentY, moveX, 0, matrix
        ):
            neighbours.append((currentX + moveX, currentY - moveY))

    else:
        if moveX == 0:
            if not blocked(currentX, currentY, moveX, 0, matrix):
                if not blocked(currentX, currentY, 0, moveY, matrix):
                    neighbours.append((currentX, currentY + moveY))
                if blocked(currentX, currentY, 1, 0, matrix):
                    neighbours.append((currentX + 1, currentY + moveY))
                if blocked(currentX, currentY, -1, 0, matrix):
                    neighbours.append((currentX - 1, currentY + moveY))

        else:
            if not blocked(currentX, currentY, moveX, 0, matrix):
                if not blocked(currentX, currentY, moveX, 0, matrix):
                    neighbours.append((currentX + moveX, currentY))
                if blocked(currentX, currentY, 0, 1, matrix):
                    neighbours.append((currentX + moveX, currentY + 1))
                if blocked(currentX, currentY, 0, -1, matrix):
                    neighbours.append((currentX + moveX, currentY - 1))
    return neighbours


def jump(currentX, currentY, moveX, moveY, matrix, goal):

    nX = currentX + moveX
    nY = currentY + moveY
    if blocked(nX, nY, 0, 0, matrix):
        return None

    if (nX, nY) == goal:
        return (nX, nY)

    oX = nX
    oY = nY

    if moveX != 0 and moveY != 0:
        while True:
            if (
                not blocked(oX, oY, -moveX, moveY, matrix)
                and blocked(oX, oY, -moveX, 0, matrix)
                or not blocked(oX, oY, moveX, -moveY, matrix)
                and blocked(oX, oY, 0, -moveY, matrix)
            ):
                return (oX, oY)

            if (
                jump(oX, oY, moveX, 0, matrix, goal) != None
                or jump(oX, oY, 0, moveY, matrix, goal) != None
            ):
                return (oX, oY)

            oX += moveX
            oY += moveY

            if blocked(oX, oY, 0, 0, matrix):
                return None

            if dblock(oX, oY, moveX, moveY, matrix):
                return None

            if (oX, oY) == goal:
                return (oX, oY)
    else:
        if moveX != 0:
            while True:
                if (
                    not blocked(oX, nY, moveX, 1, matrix)
                    and blocked(oX, nY, 0, 1, matrix)
                    or not blocked(oX, nY, moveX, -1, matrix)
                    and blocked(oX, nY, 0, -1, matrix)
                ):
                    return (oX, nY)

                oX += moveX

                if blocked(oX, nY, 0, 0, matrix):
                    return None

                if (oX, nY) == goal:
                    return (oX, nY)

        else:
            while True:
                if (
                    not blocked(nX, oY, 1, moveY, matrix)
                    and blocked(nX, oY, 1, 0, matrix)
                    or not blocked(nX, oY, -1, moveY, matrix)
                    and blocked(nX, oY, -1, 0, matrix)
                ):
                    return (nX, oY)

                oY += moveY

                if blocked(nX, oY, 0, 0, matrix):
                    return None

                if (nX, oY) == goal:
                    return (nX, oY)

    return jump(nX, nY, moveX, moveY, matrix, goal)


def identifySuccessors(currentX, currentY, came_from, matrix, goal):
    successors = []
    neighbours = nodeNeighbours(currentX, currentY, came_from.get((currentX, currentY), 0), matrix)

    for cell in neighbours:
        moveX = cell[0] - currentX
        moveY = cell[1] - currentY

        jumpPoint = jump(currentX, currentY, moveX, moveY, matrix, goal)

        if jumpPoint != None:
            successors.append(jumpPoint)
        
    return successors


def method(matrix, start, goal, hchoice, show=False):

    if show:
        surface, cell_size = Z_GetMap.Init_Visual(matrix)
        clock = pygame.time.Clock()

    open_forward = []
    open_backward = []

    came_from_forward = {}
    came_from_backward = {}

    closed_forward = set()
    closed_backward = set()

    g_forward = {start: 0}
    g_backward = {goal: 0}

    f_forward = {start: heuristic(start, goal, hchoice)}
    f_backward = {goal: heuristic(goal, start, hchoice)}

    heapq.heappush(open_forward, (f_forward[start], start))
    heapq.heappush(open_backward, (f_backward[goal], goal))

    starttime = time.time()
    meet_point = None

    while open_forward and open_backward:

        # Forward Search
        _, current_forward = heapq.heappop(open_forward)
        closed_forward.add(current_forward)

        successors_forward = identifySuccessors(
            current_forward[0], current_forward[1], came_from_forward, matrix, goal
        )

        for successor in successors_forward:
            jumpPoint = successor

            if jumpPoint in closed_forward:
                continue

            tentative_g = g_forward[current_forward] + lenght(current_forward, jumpPoint, hchoice)

            if tentative_g < g_forward.get(jumpPoint, 0) or jumpPoint not in [j[1] for j in open_forward]:
                came_from_forward[jumpPoint] = current_forward
                g_forward[jumpPoint] = tentative_g
                f_forward[jumpPoint] = tentative_g + heuristic(jumpPoint, goal, hchoice)
                heapq.heappush(open_forward, (f_forward[jumpPoint], jumpPoint))

            if jumpPoint in closed_backward:
                meet_point = jumpPoint
                break
        if meet_point:
            break

        # Backward Search
        _, current_backward = heapq.heappop(open_backward)
        closed_backward.add(current_backward)

        successors_backward = identifySuccessors(
            current_backward[0], current_backward[1], came_from_backward, matrix, start
        )

        for successor in successors_backward:
            jumpPoint = successor

            if jumpPoint in closed_backward:
                continue

            tentative_g = g_backward[current_backward] + lenght(current_backward, jumpPoint, hchoice)

            if tentative_g < g_backward.get(jumpPoint, 0) or jumpPoint not in [j[1] for j in open_backward]:
                came_from_backward[jumpPoint] = current_backward
                g_backward[jumpPoint] = tentative_g
                f_backward[jumpPoint] = tentative_g + heuristic(jumpPoint, start, hchoice)
                heapq.heappush(open_backward, (f_backward[jumpPoint], jumpPoint))

            if jumpPoint in closed_forward:
                meet_point = jumpPoint
                break
        if meet_point:
            break

        if show:
            combined_open = open_forward + open_backward
            combined_closed = closed_forward.union(closed_backward)
            Z_GetMap.Render(surface, matrix, cell_size, combined_open, combined_closed)
            clock.tick(120)  

    endtime = time.time()

    if meet_point:
        # Rekonstruksi path dari start ke meet_point
        path_forward = []
        node = meet_point
        while node in came_from_forward:
            path_forward.append(node)
            node = came_from_forward[node]
        path_forward.append(start)
        path_forward.reverse()

        # Rekonstruksi path dari meet_point ke goal
        path_backward = []
        node = meet_point
        while node in came_from_backward:
            node = came_from_backward[node]
            path_backward.append(node)

        full_path = path_forward + path_backward

        return (full_path, round(endtime - starttime, 6))

    return (0, round(endtime - starttime, 6))

def lenght(current, jumppoint, hchoice):
    moveX, moveY = direction(current[0], current[1], jumppoint[0], jumppoint[1])
    moveX = math.fabs(moveX)
    moveY = math.fabs(moveY)
    lX = math.fabs(current[0] - jumppoint[0])
    lY = math.fabs(current[1] - jumppoint[1])
    if hchoice == 1:
        if moveX != 0 and moveY != 0:
            lenght = lX * 14
            return lenght
        else:
            lenght = (moveX * lX + moveY * lY) * 10
            return lenght
    if hchoice == 2:
        return math.sqrt(
            (current[0] - jumppoint[0]) ** 2 + (current[1] - jumppoint[1]) ** 2
        )