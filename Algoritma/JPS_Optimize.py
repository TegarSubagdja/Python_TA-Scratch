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


def dblock(cX, cY, dX, dY, matrix):
    if matrix[cX - dX][cY] == 255 and matrix[cX][cY - dY] == 255:
        return True
    else:
        return False


def direction(cX, cY, pX, pY):
    dX = int(math.copysign(1, cX - pX))
    dY = int(math.copysign(1, cY - pY))
    if cX - pX == 0:
        dX = 0
    if cY - pY == 0:
        dY = 0
    return (dX, dY)


def nodeNeighbours(cX, cY, p, matrix):
    neighbours = []
    if type(p) != tuple:
        for dX, dY in [
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]:
             if not blocked(cX, cY, dX, dY, matrix):
                neighbours.append((cX + dX, cY + dY))

        return neighbours
    dX, dY = direction(cX, cY, p[0], p[1])

    if dX != 0 and dY != 0:
        if not blocked(cX, cY, 0, dY, matrix):
            neighbours.append((cX, cY + dY))
        if not blocked(cX, cY, dX, 0, matrix):
            neighbours.append((cX + dX, cY))
        if (
            not blocked(cX, cY, 0, dY, matrix)
            or not blocked(cX, cY, dX, 0, matrix)
        ) and not blocked(cX, cY, dX, dY, matrix):
            neighbours.append((cX + dX, cY + dY))
        if blocked(cX, cY, -dX, 0, matrix) and not blocked(
            cX, cY, 0, dY, matrix
        ):
            neighbours.append((cX - dX, cY + dY))
        if blocked(cX, cY, 0, -dY, matrix) and not blocked(
            cX, cY, dX, 0, matrix
        ):
            neighbours.append((cX + dX, cY - dY))

    else:
        if dX == 0:
            if not blocked(cX, cY, dX, 0, matrix):
                if not blocked(cX, cY, 0, dY, matrix):
                    neighbours.append((cX, cY + dY))
                if blocked(cX, cY, 1, 0, matrix):
                    neighbours.append((cX + 1, cY + dY))
                if blocked(cX, cY, -1, 0, matrix):
                    neighbours.append((cX - 1, cY + dY))

        else:
            if not blocked(cX, cY, dX, 0, matrix):
                if not blocked(cX, cY, dX, 0, matrix):
                    neighbours.append((cX + dX, cY))
                if blocked(cX, cY, 0, 1, matrix):
                    neighbours.append((cX + dX, cY + 1))
                if blocked(cX, cY, 0, -1, matrix):
                    neighbours.append((cX + dX, cY - 1))
    return neighbours


def jump(cX, cY, dX, dY, matrix, goal):

    nX = cX + dX
    nY = cY + dY
    if blocked(nX, nY, 0, 0, matrix):
        return None

    if (nX, nY) == goal:
        return (nX, nY)
    
    oX = nX
    oY = nY

    if dX != 0 and dY != 0:
        while True:
            if (
                not blocked(oX, oY, -dX, dY, matrix)
                and blocked(oX, oY, -dX, 0, matrix)
                or not blocked(oX, oY, dX, -dY, matrix)
                and blocked(oX, oY, 0, -dY, matrix)
            ):
                return (oX, oY)

            if (
                jump(oX, oY, dX, 0, matrix, goal) != None
                or jump(oX, oY, 0, dY, matrix, goal) != None
            ):
                return (oX, oY)

            oX += dX
            oY += dY

            if blocked(oX, oY, 0, 0, matrix):
                return None

            if dblock(oX, oY, dX, dY, matrix):
                return None

            if (oX, oY) == goal:
                return (oX, oY)
    else:
        if dX != 0:
            while True:
                if (
                    not blocked(oX, nY, dX, 1, matrix)
                    and blocked(oX, nY, 0, 1, matrix)
                    or not blocked(oX, nY, dX, -1, matrix)
                    and blocked(oX, nY, 0, -1, matrix)
                ):
                    return (oX, nY)

                oX += dX

                if blocked(oX, nY, 0, 0, matrix):
                    return None

                if (oX, nY) == goal:
                    return (oX, nY)

        else:
            while True:
                if (
                    not blocked(nX, oY, 1, dY, matrix)
                    and blocked(nX, oY, 1, 0, matrix)
                    or not blocked(nX, oY, -1, dY, matrix)
                    and blocked(nX, oY, -1, 0, matrix)
                ):
                    return (nX, oY)

                oY += dY

                if blocked(nX, oY, 0, 0, matrix):
                    return None

                if (nX, oY) == goal:
                    return (nX, oY)

    # return jump(nX, nY, moveX, moveY, matrix, goal) #Rekursif


def identifySuccessors(cX, cY, came_from, matrix, goal):
    successors = []
    neighbours = nodeNeighbours(cX, cY, came_from.get((cX, cY), 0), matrix)

    for cell in neighbours:
        moveX = cell[0] - cX
        moveY = cell[1] - cY

        jumpPoint = jump(cX, cY, moveX, moveY, matrix, goal)

        if jumpPoint != None:
            successors.append(jumpPoint)
        
    return successors


def method(matrix, start, goal, hchoice, TPF=False, BRC=False, GLF=False, PPO=False, show=False, speed=60, k=0.5):

    if show:
        surface, cell_size = Z_GetMap.Init_Visual(matrix)
        clock = pygame.time.Clock()

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
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path = path[::-1]
            if PPO:
                path = Prunning(path, matrix)
            endtime = time.time()
            if show:

                Z_GetMap.Render(surface, matrix, cell_size, open_list, close_list, path)
                clock.tick(speed)  # Batasi ke 200 FPS
                
                # Tunggu sampai tombol ditekan
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.KEYDOWN:
                            waiting = False

                # Handle event disini
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
            return (path, round(endtime - starttime, 6)), open_list, close_list

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

            v1 = TP(came_from.get(jumpPoint, jumpPoint), current, jumpPoint, k) if TPF else 0
            v2 = BR(jumpPoint, goal, matrix) or 1 if BRC else 1
            v3 = GL(start, goal, jumpPoint) if GLF else 0

            tentative_gn = gn[current] + lenght(
                current, jumpPoint, hchoice
            )

            if tentative_gn < gn.get(
                jumpPoint, 0
            ) or jumpPoint not in [j[1] for j in open_list]:
                came_from[jumpPoint] = current
                gn[jumpPoint] = tentative_gn
                if BRC:
                    fn[jumpPoint] = tentative_gn + (heuristic(
                        jumpPoint, 
                        goal, 
                        hchoice) * (1-math.log(v2))) + v1 + v3
                else:
                    fn[jumpPoint] = tentative_gn + heuristic(
                        jumpPoint, 
                        goal, 
                        hchoice
                    ) + v1 + v3
                heapq.heappush(open_list, (fn[jumpPoint], jumpPoint))

            if show:

                Z_GetMap.Render(surface, matrix, cell_size, open_list, close_list)
                clock.tick(speed)  # Batasi ke 200 FPS

                # Handle event disini
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()

        # pygame.image.save(surface, "Loop Pertama JPS.jpg")
        # sys.exit()

    endtime = time.time()
    return (0, round(endtime - starttime, 6)), 0, 0

def methodBds(matrix, start, goal, hchoice, TPF=False, BRC=False, GLF=False, PPO=False, show=False, speed=60, k=0.5):
    
    if show:
        surface, cell_size = Z_GetMap.Init_Visual(matrix)
        clock = pygame.time.Clock()

    if not isinstance(start, tuple):
        start = tuple(start)
    if not isinstance(goal, tuple):
        goal = tuple(goal)

    # Forward
    came_from_f = {}
    open_f = []
    close_f = set()
    gn_f = {start: 0}
    fn_f = {start: heuristic(start, goal, hchoice)}

    # Backward
    came_from_b = {}
    open_b = []
    close_b = set()
    gn_b = {goal: 0}
    fn_b = {goal: heuristic(goal, start, hchoice)}

    current_f, current_b = start, goal
    
    heapq.heappush(open_f, (fn_f[start], start))
    heapq.heappush(open_b, (fn_b[goal], goal))

    startTime = time.time()
    meet_point = None

    while open_f and open_b and not meet_point:
        
        # ============ Forward Expand ============
        if open_f:
            _, current_f = heapq.heappop(open_f)
            close_f.add(current_f)

            successors = identifySuccessors(current_f[0], current_f[1], came_from_f, matrix, goal)
            
            for succ in successors:
                if succ in close_f:
                    continue

                # Single-line conditional calculations
                v1 = TP(came_from_f.get(current_f, current_f), current_f, succ, k) if TPF else 0
                v2 = BR(succ, goal, matrix) or 1 if BRC else 1
                v3 = GL(start, goal, succ) if GLF else 0

                tentative_g = gn_f[current_f] + lenght(current_f, succ, hchoice)

                if succ not in gn_f or tentative_g < gn_f[succ]:
                    came_from_f[succ] = current_f
                    gn_f[succ] = tentative_g

                    # Pre-compute heuristic values
                    hn_f = heuristic(succ, goal, hchoice)
                    
                    # Optimized f-value calculation
                    if BRC:
                        fn_f[succ] = tentative_g + (hn_f * (1 - math.log(v2))) + v1 + v3 
                    else:
                        fn_f[succ] = tentative_g + hn_f + v1 + v3 

                    heapq.heappush(open_f, (fn_f[succ], succ))

                # Meeting point check
                if succ in close_b:
                    meet_point = succ
                    break

        # ============ Backward Expand ============
        if open_b and not meet_point:
            _, current_b = heapq.heappop(open_b)
            close_b.add(current_b)

            successors_b = identifySuccessors(current_b[0], current_b[1], came_from_b, matrix, start)
            
            for succ in successors_b:
                if succ in close_b:
                    continue

                # Single-line conditional calculations
                v1 = TP(came_from_b.get(current_b, current_b), current_b, succ, k) if TPF else 0
                v2 = BR(succ, start, matrix) or 1 if BRC else 1
                v3 = GL(goal, start, succ) if GLF else 0

                tentative_g = gn_b[current_b] + lenght(current_b, succ, hchoice)

                if succ not in gn_b or tentative_g < gn_b[succ]:
                    came_from_b[succ] = current_b
                    gn_b[succ] = tentative_g

                    # Pre-compute heuristic values
                    hn_b = heuristic(succ, start, hchoice)
                    
                    # Optimized f-value calculation
                    if BRC:
                        # Cache log calculation
                        fn_b[succ] = tentative_g + (hn_b * (1 - math.log(v2))) + v1 + v3
                    else:
                        fn_b[succ] = tentative_g + hn_b + v1 + v3 

                    heapq.heappush(open_b, (fn_b[succ], succ))

                # Meeting point check
                if succ in close_f:
                    meet_point = succ
                    break

        if show:
            # Combine sets sekali saja
            combined_open = open_f + open_b
            combined_close = close_f | close_b  # Operator | lebih cepat dari union()
            Z_GetMap.Render(surface, matrix, cell_size, combined_open, combined_close)
            clock.tick(speed)

            # Event handling yang lebih efisien
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
    
    if meet_point is None:
        endTime = time.time()
        return (0, round(endTime - startTime, 6)), 0, 0

    # ============ Path Reconstruction ============
    # Forward path
    path_f = []
    node = meet_point
    while node in came_from_f:
        path_f.append(node)
        node = came_from_f[node]
    path_f.append(start)
    path_f.reverse()

    # Backward path
    path_b = []
    node = meet_point
    while node in came_from_b:
        node = came_from_b[node]
        path_b.append(node)

    # Combine path tanpa duplikasi
    path = path_f + path_b

    if PPO:
        path = Prunning(path, matrix)

    endTime = time.time()

    if show:
        Z_GetMap.Render(surface, matrix, cell_size, open_f + open_b, close_f | close_b, path)
        clock.tick(speed)
        time.sleep(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

    return (path, round(endTime - startTime, 6)), (open_f + open_b), (close_f | close_b)

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