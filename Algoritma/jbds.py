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


def methodBds(matrix, start, goal, hchoice, TPF=False, BRC=False, GLF=False, PPO=False, show=False, speed=60):
    if show:
        surface, cell_size = Z_GetMap.Init_Visual(matrix)
        clock = pygame.time.Clock()

    # Forward
    came_from_f = {}
    open_f = []
    open_set_f = {start}
    close_f = set()
    g_f = {start: 0}
    f_f = {start: heuristic(start, goal, hchoice)}

    # Backward
    came_from_b = {}
    open_b = []
    open_set_b = {goal}
    close_b = set()
    g_b = {goal: 0}
    f_b = {goal: heuristic(goal, start, hchoice)}

    current_f, current_b = start, goal
    
    heapq.heappush(open_f, (f_f[start], start))
    heapq.heappush(open_b, (f_b[goal], goal))

    start_time = time.time()
    meet_point = None
    log_cache = {}

    while open_f and open_b and not meet_point:
        # ============ Forward Expand ============
        if open_f:
            _, current_f = heapq.heappop(open_f)
            open_set_f.discard(current_f)
            close_f.add(current_f)

            successors = identifySuccessors(current_f[0], current_f[1], came_from_f, matrix, goal)

            for succ in successors:
                if succ in close_f:
                    continue

                v1 = TP(came_from_f.get(current_f, current_f), current_f, succ, 2) if TPF else 0
                v2 = BR(succ, goal, matrix) or 1 if BRC else 1
                v3 = GL(start, goal, succ) if GLF else 0

                tentative_g = g_f[current_f] + lenght(current_f, succ, hchoice)

                if succ not in g_f or tentative_g < g_f[succ]:
                    came_from_f[succ] = current_f
                    g_f[succ] = tentative_g

                    h_to_goal = heuristic(succ, goal, hchoice)
                    h_to_current_b = heuristic(succ, current_b, 2)

                    if BRC:
                        if v2 not in log_cache:
                            log_cache[v2] = math.log(v2)
                        f_f[succ] = tentative_g + (h_to_goal * (1 - log_cache[v2])) + v1 + v3 + h_to_current_b
                    else:
                        f_f[succ] = tentative_g + h_to_goal + v1 + v3 + h_to_current_b

                    heapq.heappush(open_f, (f_f[succ], succ))
                    open_set_f.add(succ)

                # Meeting point check (tambahan: juga cek open_set_b)
                if succ in close_b or succ in open_set_b:
                    meet_point = succ
                    break

        # ============ Backward Expand ============
        if open_b and not meet_point:
            _, current_b = heapq.heappop(open_b)
            open_set_b.discard(current_b)
            close_b.add(current_b)

            successors_b = identifySuccessors(current_b[0], current_b[1], came_from_b, matrix, start)

            for succ in successors_b:
                if succ in close_b:
                    continue

                v1 = TP(came_from_b.get(current_b, current_b), current_b, succ, 2) if TPF else 0
                v2 = BR(succ, start, matrix) or 1 if BRC else 1
                v3 = GL(goal, start, succ) if GLF else 0

                tentative_g = g_b[current_b] + lenght(current_b, succ, hchoice)

                if succ not in g_b or tentative_g < g_b[succ]:
                    came_from_b[succ] = current_b
                    g_b[succ] = tentative_g

                    h_to_start = heuristic(succ, start, hchoice)
                    h_to_current_f = heuristic(current_f, succ, 2)

                    if BRC:
                        if v2 not in log_cache:
                            log_cache[v2] = math.log(v2)
                        f_b[succ] = tentative_g + (h_to_start * (1 - log_cache[v2])) + v1 + v3 + h_to_current_f
                    else:
                        f_b[succ] = tentative_g + h_to_start + v1 + v3 + h_to_current_f

                    heapq.heappush(open_b, (f_b[succ], succ))
                    open_set_b.add(succ)

                # Meeting point check (tambahan: juga cek open_set_f)
                if succ in close_f or succ in open_set_f:
                    meet_point = succ
                    break

        # ============ Visual ============
        if show:
            combined_open = open_f + open_b
            combined_close = close_f | close_b
            Z_GetMap.Render(surface, matrix, cell_size, combined_open, combined_close)
            clock.tick(speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()

    end_time = time.time()

    # ============ Path Reconstruction ============
    if meet_point:
        path_f = []
        node = meet_point
        while node in came_from_f:
            path_f.append(node)
            node = came_from_f[node]
        path_f.append(start)
        path_f.reverse()

        path_b = []
        node = meet_point
        while node in came_from_b:
            node = came_from_b[node]
            path_b.append(node)

        full_path = path_f + path_b

        if PPO:
            full_path = prunning(full_path, matrix)

        if show:
            Z_GetMap.Render(surface, matrix, cell_size, open_f + open_b, close_f | close_b, full_path)
            clock.tick(speed)
            time.sleep(2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()

        return (full_path, round(end_time - start_time, 6)), (open_f + open_b), (close_f | close_b)

    return 0, round(end_time - start_time, 6)


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