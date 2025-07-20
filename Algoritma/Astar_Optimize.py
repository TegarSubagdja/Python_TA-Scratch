from Utils import *

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
    if hchoice == 1:
        xdist = math.fabs(goal[0] - start[0])
        ydist = math.fabs(goal[1] - start[1])
        if xdist > ydist:
            return 14 * ydist + 10 * (xdist - ydist)
        else:
            return 14 * xdist + 10 * (ydist - xdist)
    if hchoice == 2:
        return math.sqrt((goal[0] - start[0]) ** 2 + (goal[1] - start[1]) ** 2)

def method(map, start, goal, hchoice=2, TPF=False, BRC=False, GLF=False, PPO=False, show=False, speed=30, k=0.5):

    if show:
        surface, cell_size = Z_GetMap.Init_Visual(map)
        clock = pygame.time.Clock()

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
            if PPO:
                path = Prunning(path, map)
            endtime = time.time()
            if show:
                Z_GetMap.Render(surface, map, cell_size, open_list, close_list, path)
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

            if blocked(current[0], current[1], dX, dY, map):
                continue

            neighbour = current[0] + dX, current[1] + dY

            if hchoice == 1:
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
        
            # Single-line conditional calculations
            v1 = TP(came_from.get(current, current), current, neighbour, k) if TPF else 0
            v2 = BR(neighbour, goal, map) or 1 if BRC else 1
            v3 = GL(start, goal, neighbour) if GLF else 0

            if tentative_gn < gn.get(
                neighbour, 0
            ) or neighbour not in [i[1] for i in open_list]:
                came_from[neighbour] = current
                gn[neighbour] = tentative_gn
                if BRC:
                    fn[neighbour] = tentative_gn + (heuristic(
                        neighbour, 
                        goal, 
                        hchoice) * (1-math.log(v2))) + v1 + v3
                else:
                    fn[neighbour] = tentative_gn + heuristic(
                        neighbour, 
                        goal, 
                        hchoice
                    ) + v1 + v3 # Pengkalian 2 harus dihilangkan

                heapq.heappush(open_list, (fn[neighbour], neighbour))
                    # Visualisasi setiap langkah
            if show:
                Z_GetMap.Render(surface, map, cell_size, open_list, close_list)
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
                
    endtime = time.time()
    return (0, round(endtime - starttime, 6)), 0, 0

def methodBds(map, start, goal, hchoice=2, TPF=False, BRC=False, GLF=False, PPO=False, EL=False, show=False, speed=30, k=0.5):

    if show:
        surface, cell_size = Z_GetMap.Init_Visual(map)
        clock = pygame.time.Clock()

    if not isinstance(start, tuple):
        start = tuple(start)
    if not isinstance(goal, tuple):
        goal = tuple(goal)

    # Forward
    came_from_f = {}
    open_f = []
    close_f = set()
    g_f = {start: 0}
    f_f = {start: heuristic(start, goal, hchoice)}

    #Backward
    came_from_b = {}
    open_b = []
    close_b = set()
    g_b = {goal: 0}
    f_b = {goal: heuristic(goal, start, hchoice)}

    current_f, current_b = start, goal

    heapq.heappush(open_f, (f_f[start], start))
    heapq.heappush(open_b, (f_b[goal], goal))

    startTime = time.time()
    meet_point = None

    while open_f and open_b and not meet_point:

        # --- Forward Search ---
        if open_f:
            _, current_f = heapq.heappop(open_f)
            close_f.add(current_f)

            for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                neighbour = current_f[0] + dX, current_f[1] + dY

                if neighbour in close_f:
                    continue

                if blocked(current_f[0], current_f[1], dX, dY, map):
                    continue

                if hchoice == 1:
                    cost = 14 if dX != 0 and dY != 0 else 10
                else:
                    cost = math.sqrt(2) if dX != 0 and dY != 0 else 1

                tentative_gn = g_f[current_f] + cost
                if neighbour in close_f:
                    continue

                v1 = TP(came_from_f.get(current_f, current_f), current_f, neighbour, k) if TPF else 0
                v2 = BR(neighbour, goal, map) or 1 if BRC else 1
                v3 = GL(start, goal, neighbour) if GLF else 0

                if tentative_gn < g_f.get(neighbour, float('inf')):
                    came_from_f[neighbour] = current_f
                    g_f[neighbour] = tentative_gn

                    h_to_goal = heuristic(neighbour, goal, hchoice)
                    h_to_current_b = heuristic(neighbour, current_b, 2) if EL else 0
                    
                    if BRC:
                        f_f[neighbour] = tentative_gn + (h_to_goal * (1 - math.log(v2))) + v1 + v3 + h_to_current_b
                    else:
                        f_f[neighbour] = tentative_gn + h_to_goal + v1 + v3 + h_to_current_b
                    heapq.heappush(open_f, (f_f[neighbour], neighbour))
                    
                # Meeting point check
                if neighbour in close_b:
                    meet_point = neighbour
                    break

        # --- Backward Search ---
        if open_b and not meet_point:
            _, current_b = heapq.heappop(open_b)
            close_b.add(current_b)

            for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                neighbour = current_b[0] + dX, current_b[1] + dY

                if neighbour in close_b:
                    continue

                if blocked(current_b[0], current_b[1], dX, dY, map):
                    continue

                if hchoice == 1:
                    cost = 14 if dX != 0 and dY != 0 else 10
                else:
                    cost = math.sqrt(2) if dX != 0 and dY != 0 else 1

                v1 = TP(came_from_b.get(current_b, current_b), current_b, neighbour, k) if TPF else 0
                v2 = BR(neighbour, start, map) or 1 if BRC else 1
                v3 = GL(goal, start, neighbour) if GLF else 0

                tentative_gn = g_b[current_b] + cost
                if neighbour in close_b:
                    continue

                if tentative_gn < g_b.get(neighbour, float('inf')):
                    came_from_b[neighbour] = current_b
                    g_b[neighbour] = tentative_gn

                    h_to_start = heuristic(neighbour, start, hchoice)
                    h_to_current_f = heuristic(neighbour, current_f, 2) if EL else 0

                    if BRC:
                        f_b[neighbour] = tentative_gn + (h_to_start * (1 - math.log(v2))) + v1 + v3 + h_to_current_f
                    else:
                        f_b[neighbour] = tentative_gn + h_to_start + v1 + v3 + h_to_current_f

                    heapq.heappush(open_b, (f_b[neighbour], neighbour))

                if neighbour in close_f:
                    meet_point = neighbour
                    break

            # --- Visualisasi ---
            if show:
                path_preview = [meet_point] if meet_point else []
                Z_GetMap.Render(surface, map, cell_size, open_f + open_b, close_f.union(close_b), path_preview)
                clock.tick(speed)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        exit()

    if meet_point is None:
        endTime = time.time()
        return (0, round(endTime - startTime, 6)), 0, 0

    # --- Rekonstruksi Jalur ---
    # Forward path
    path_fwd = []
    node = meet_point
    while node in came_from_f:
        path_fwd.append(node)
        node = came_from_f[node]
    path_fwd.append(start)
    path_fwd.reverse()

    # Backward path
    path_bwd = []
    node = meet_point
    while node in came_from_b:
        node = came_from_b[node]
        path_bwd.append(node)
    
    # Combine path tanpa duplikasi
    path = path_fwd + path_bwd

    if PPO:
        path = Prunning(path, map)

    endTime = time.time()

    if show:
        Z_GetMap.Render(surface, map, cell_size, open_f + open_b, close_f.union(close_b), path)
        clock.tick(speed)

        # Tunggu sampai tombol ditekan
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

    return (path, round(endTime - startTime, 6)), open_f + open_b, close_f.union(close_b)