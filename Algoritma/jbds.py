from Utils import *

def heuristic(start, goal, hchoice):
    if hchoice == 1:
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

    if shows:
        scan_points.append((oX, oY))

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

            if shows:
                scan_points.append((oX, oY))

                Z_GetMap.Render(surface, matrix, cell_size, open_list=None, close_list=None ,point=scan_points)
                clock.tick(10)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        exit()

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

                if shows:
                    scan_points.append((oX, oY))

                    Z_GetMap.Render(surface, matrix, cell_size, point=scan_points)
                    clock.tick(10)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            pygame.quit()
                            exit()

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

                if shows:
                    scan_points.append((oX, oY))

                    Z_GetMap.Render(surface, matrix, cell_size, point=scan_points)
                    clock.tick(10)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            pygame.quit()
                            exit()

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

surface = None
cell_size = None
clock = None
scan_points = []
shows = None

def method(matrix, start, goal, hchoice, show=False, speed=30):
    global surface, cell_size, clock, scan_points, shows
    shows = show

    if show:
        surface, cell_size = Z_GetMap.Init_Visual(matrix)
        clock = pygame.time.Clock()

    came_from_fwd = {}
    came_from_bwd = {}
    close_list_fwd = set()
    close_list_bwd = set()
    gn_fwd = {start: 0}
    gn_bwd = {goal: 0}
    fn_fwd = {start: heuristic(start, goal, hchoice)}
    fn_bwd = {goal: heuristic(goal, start, hchoice)}

    open_list_fwd = []
    open_list_bwd = []

    heapq.heappush(open_list_fwd, (fn_fwd[start], start))
    heapq.heappush(open_list_bwd, (fn_bwd[goal], goal))

    starttime = time.time()
    running = True
    meeting_point = None

    while open_list_fwd and open_list_bwd and running:

        # --- Forward Search ---
        current_fwd = heapq.heappop(open_list_fwd)[1]
        close_list_fwd.add(current_fwd)

        if current_fwd in close_list_bwd:
            meeting_point = current_fwd
            break

        successors = identifySuccessors(current_fwd[0], current_fwd[1], came_from_fwd, matrix, goal)
        for successor in successors:
            jumpPoint = successor

            if jumpPoint in close_list_fwd:
                continue

            tentative_gn = gn_fwd[current_fwd] + lenght(current_fwd, jumpPoint, hchoice)
            if tentative_gn < gn_fwd.get(jumpPoint, 0) or jumpPoint not in [j[1] for j in open_list_fwd]:
                came_from_fwd[jumpPoint] = current_fwd
                gn_fwd[jumpPoint] = tentative_gn
                fn_fwd[jumpPoint] = tentative_gn + heuristic(jumpPoint, goal, hchoice)
                heapq.heappush(open_list_fwd, (fn_fwd[jumpPoint], jumpPoint))

        # --- Backward Search ---
        current_bwd = heapq.heappop(open_list_bwd)[1]
        close_list_bwd.add(current_bwd)

        if current_bwd in close_list_fwd:
            meeting_point = current_bwd
            break

        successors = identifySuccessors(current_bwd[0], current_bwd[1], came_from_bwd, matrix, start)
        for successor in successors:
            jumpPoint = successor

            if jumpPoint in close_list_bwd:
                continue

            tentative_gn = gn_bwd[current_bwd] + lenght(current_bwd, jumpPoint, hchoice)
            if tentative_gn < gn_bwd.get(jumpPoint, 0) or jumpPoint not in [j[1] for j in open_list_bwd]:
                came_from_bwd[jumpPoint] = current_bwd
                gn_bwd[jumpPoint] = tentative_gn
                fn_bwd[jumpPoint] = tentative_gn + heuristic(jumpPoint, start, hchoice)
                heapq.heappush(open_list_bwd, (fn_bwd[jumpPoint], jumpPoint))

        if show:
            Z_GetMap.Render(surface, matrix, cell_size, open_list_fwd + open_list_bwd, close_list_fwd.union(close_list_bwd))
            clock.tick(speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()

    endtime = time.time()

    if meeting_point is None:
        return (0, round(endtime - starttime, 6))

    # --- Rekonstruksi jalur dari kedua sisi ---
    path_fwd = []
    current = meeting_point
    while current in came_from_fwd:
        path_fwd.append(current)
        current = came_from_fwd[current]
    path_fwd.append(start)
    path_fwd = path_fwd[::-1]

    path_bwd = []
    current = meeting_point
    while current in came_from_bwd:
        current = came_from_bwd[current]
        path_bwd.append(current)

    full_path = path_fwd + path_bwd
    full_path = prunning(full_path, matrix)

    return (full_path, round(endtime - starttime, 6))

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