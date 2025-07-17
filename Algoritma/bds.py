from Utils import *

def blocked(cX, cY, dX, dY, matrix):
    if cX + dX < 0 or cX + dX >= matrix.shape[0]:
        return True
    if cY + dY < 0 or cY + dY >= matrix.shape[1]:
        return True
    if dX != 0 and dY != 0:
        # if matrix[cX + dX][cY] == 255 and matrix[cX][cY + dY] == 255:
        #     return True
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

def heuristic(a, b, hchoice):
    if hchoice == 1:
        xdist = math.fabs(b[0] - a[0])
        ydist = math.fabs(b[1] - a[1])
        if xdist > ydist:
            return 14 * ydist + 10 * (xdist - ydist)
        else:
            return 14 * xdist + 10 * (ydist - xdist)
    if hchoice == 2:
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def method(map, start, goal, hchoice=2, TPF=False, BRC=False, GLF=False, PPO=False, show=False, speed=30):

    if show:
        surface, cell_size = Z_GetMap.Init_Visual(map)
        clock = pygame.time.Clock()

    v1, v2, v3 = 0, 0, 0

    open_list_fwd, open_list_bwd = [], []
    close_list_fwd, close_list_bwd = set(), set()
    came_from_fwd, came_from_bwd = {}, {}

    gn_fwd = {start: 0}
    gn_bwd = {goal: 0}
    fn_fwd = {start: heuristic(start, goal, hchoice)}
    fn_bwd = {goal: heuristic(goal, start, hchoice)}

    heapq.heappush(open_list_fwd, (fn_fwd[start], start))
    heapq.heappush(open_list_bwd, (fn_bwd[goal], goal))

    meeting_point = None
    starttime = time.time()

    while open_list_fwd and open_list_bwd:

        # --- Forward Search ---
        current_fwd = heapq.heappop(open_list_fwd)[1]
        close_list_fwd.add(current_fwd)

        if current_fwd in close_list_bwd:
            meeting_point = current_fwd
            break

        for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if blocked(current_fwd[0], current_fwd[1], dX, dY, map):
                continue

            neighbour = current_fwd[0] + dX, current_fwd[1] + dY

            if hchoice == 1:
                cost = 14 if dX != 0 and dY != 0 else 10
            else:
                cost = math.sqrt(2) if dX != 0 and dY != 0 else 1

            tentative_gn = gn_fwd[current_fwd] + cost
            if neighbour in close_list_fwd:
                continue

            v1 = TP(came_from_fwd.get(current_fwd, current_fwd), current_fwd, neighbour, 0.6) if TPF else 0
            v2 = BR(neighbour, goal, map) or 1 if BRC else 1
            v3 = GL(start, goal, neighbour) if GLF else 0

            if tentative_gn < gn_fwd.get(neighbour, float('inf')):
                came_from_fwd[neighbour] = current_fwd
                gn_fwd[neighbour] = tentative_gn
                fn = tentative_gn + heuristic(neighbour, goal, hchoice)
                if BRC:
                    fn += (heuristic(neighbour, goal, hchoice) * (1 - math.log(v2)))
                fn += v1 + v3
                fn_fwd[neighbour] = fn
                heapq.heappush(open_list_fwd, (fn, neighbour))

        # --- Backward Search ---
        current_bwd = heapq.heappop(open_list_bwd)[1]
        close_list_bwd.add(current_bwd)

        if current_bwd in close_list_fwd:
            meeting_point = current_bwd
            break

        for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if blocked(current_bwd[0], current_bwd[1], dX, dY, map):
                continue

            neighbour = current_bwd[0] + dX, current_bwd[1] + dY

            if hchoice == 1:
                cost = 14 if dX != 0 and dY != 0 else 10
            else:
                cost = math.sqrt(2) if dX != 0 and dY != 0 else 1

            tentative_gn = gn_bwd[current_bwd] + cost
            if neighbour in close_list_bwd:
                continue

            v1 = TP(came_from_bwd.get(current_bwd, current_bwd), current_bwd, neighbour, 0.6) if TPF else 0
            v2 = BR(neighbour, start, map) or 1 if BRC else 1
            v3 = GL(goal, start, neighbour) if GLF else 0

            if tentative_gn < gn_bwd.get(neighbour, float('inf')):
                came_from_bwd[neighbour] = current_bwd
                gn_bwd[neighbour] = tentative_gn
                fn = tentative_gn + heuristic(neighbour, start, hchoice)
                if BRC:
                    fn += (heuristic(neighbour, start, hchoice) * (1 - math.log(v2)))
                fn += v1 + v3
                fn_bwd[neighbour] = fn
                heapq.heappush(open_list_bwd, (fn, neighbour))

        # --- Visualisasi ---
        if show:
            path_preview = [meeting_point] if meeting_point else []
            Z_GetMap.Render(surface, map, cell_size, open_list_fwd + open_list_bwd, close_list_fwd.union(close_list_bwd), path_preview)
            clock.tick(speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()

    endtime = time.time()

    if meeting_point is None:
        return (0, round(endtime - starttime, 6)), 0, 0

    # --- Rekonstruksi Jalur ---
    path_fwd = []
    node = meeting_point
    while node in came_from_fwd:
        path_fwd.append(node)
        node = came_from_fwd[node]
    path_fwd.append(start)
    path_fwd.reverse()

    path_bwd = []
    node = meeting_point
    while node in came_from_bwd:
        node = came_from_bwd[node]
        path_bwd.append(node)
    path = path_fwd + path_bwd

    if PPO:
        path = Prunning(path, map)

    if show:
        Z_GetMap.Render(surface, map, cell_size, open_list_fwd + open_list_bwd, close_list_fwd.union(close_list_bwd), path)
        clock.tick(speed)
        time.sleep(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

    return (path, round(endtime - starttime, 6)), open_list_fwd + open_list_bwd, close_list_fwd.union(close_list_bwd)
