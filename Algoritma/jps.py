import math, time, heapq
from Method import BarrierRasterCoefficient as br, Guideline as gl, TurnPenaltyFunction as tp

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


def method(matrix, start, goal, hchoice):

    came_from = {}
    close_list = set()
    gn = {start: 0}
    fn = {start: heuristic(start, goal, hchoice)}

    open_list = []

    heapq.heappush(open_list, (fn[start], start))

    starttime = time.time()

    while open_list:

        current = heapq.heappop(open_list)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            data = data[::-1]
            endtime = time.time()
            return (data, round(endtime - starttime, 6)), open_list, close_list

        close_list.add(current)

        successors = identifySuccessors(
            current[0], current[1], came_from, matrix, goal
        )

        for successor in successors:
            jumpPoint = successor

            if (
                jumpPoint in close_list
            ):  # and tentative_gn >= gn.get(jumpPoint,0):
                continue

            tentative_gn = gn[current] + lenght(
                current, jumpPoint, hchoice
            )

            if tentative_gn < gn.get(
                jumpPoint, 0
            ) or jumpPoint not in [j[1] for j in open_list]:
                came_from[jumpPoint] = current
                gn[jumpPoint] = tentative_gn
                fn[jumpPoint] = tentative_gn + heuristic(jumpPoint, goal, hchoice) 
                heapq.heappush(open_list, (fn[jumpPoint], jumpPoint))
        endtime = time.time()
    return (0, round(endtime - starttime, 6))


def lenght(current, jumppoint, hchoice):
    moveX, moveY = direction(current[0], current[1], jumppoint[0], jumppoint[1])
    moveX = math.fabs(moveX)
    moveY = math.fabs(moveY)
    lX = math.fabs(current[0] - jumppoint[0])
    lY = math.fabs(current[1] - jumppoint[1])
    if hchoice == 255:
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