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

def method(matrix, start, goal, hchoice, TPF=False, BRC=False, GLF=False, PPO=False, show=False, speed=60):
    if show:
        surface, cell_size = Z_GetMap.Init_Visual(matrix)
        clock = pygame.time.Clock()

    v1, v2, v3 = 0, 0, 0

    open_forward = []
    open_backward = []

    # Tambahan set untuk mengecek openlist lawan
    open_set_forward = {start}
    open_set_backward = {goal}

    came_from_forward = {}
    came_from_backward = {}

    g_forward = {start: 0}
    g_backward = {goal: 0}

    f_forward = {start: heuristic(start, goal, hchoice)}
    f_backward = {goal: heuristic(goal, start, hchoice)}

    closed_forward = set()
    closed_backward = set()

    current_forward = start
    current_backward = goal

    heapq.heappush(open_forward, (f_forward[start], start))
    heapq.heappush(open_backward, (f_backward[goal], goal))

    deltas = [
        (0, 1), (0, -1), (1, 0), (-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]

    start_time = time.time()
    meet_point = None

    while open_forward and open_backward:
        # Ekspansi sisi Forward
        if open_forward:
            _, current_forward = heapq.heappop(open_forward)
            open_set_forward.discard(current_forward)

            if current_forward in closed_backward or current_forward in open_set_backward:
                meet_point = current_forward
                break

            closed_forward.add(current_forward)

            for dX, dY in deltas:
                if blocked(current_forward[0], current_forward[1], dX, dY, matrix):
                    continue

                neighbor = current_forward[0] + dX, current_forward[1] + dY
                if neighbor in closed_forward:
                    continue

                v1 = TP(came_from_forward.get(current_forward, current_forward), current_forward, neighbor, 2) if TPF else 0
                v2 = BR(neighbor, goal, matrix) or 1 if BRC else 1
                v3 = GL(start, goal, neighbor) if GLF else 0

                cost = 14 if hchoice == 1 and dX != 0 and dY != 0 else (10 if hchoice == 1 else (math.sqrt(2) if dX != 0 and dY != 0 else 1))
                tentative_g = g_forward.get(current_forward, 0) + cost

                if neighbor not in g_forward or tentative_g < g_forward[neighbor]:
                    g_forward[neighbor] = tentative_g

                    h_to_current_b = 0 #heuristic(neighbor, current_backward, 2)

                    if BRC:
                        f_forward[neighbor] = tentative_g + (heuristic(neighbor, goal, hchoice) * (1 - math.log(v2))) + v1 + v3 + h_to_current_b
                    else:
                        f_forward[neighbor] = tentative_g + heuristic(neighbor, goal, hchoice) + v1 + v3 + h_to_current_b
                    came_from_forward[neighbor] = current_forward
                    heapq.heappush(open_forward, (f_forward[neighbor], neighbor))
                    open_set_forward.add(neighbor)

        # Ekspansi sisi Backward
        if open_backward:
            _, current_backward = heapq.heappop(open_backward)
            open_set_backward.discard(current_backward)

            if current_backward in closed_forward or current_backward in open_set_forward:
                meet_point = current_backward
                break

            closed_backward.add(current_backward)

            for dX, dY in deltas:
                if blocked(current_backward[0], current_backward[1], dX, dY, matrix):
                    continue

                neighbor = current_backward[0] + dX, current_backward[1] + dY
                if neighbor in closed_backward:
                    continue

                v1 = TP(came_from_backward.get(current_backward, current_backward), current_backward, neighbor, 2) if TPF else 0
                v2 = BR(neighbor, start, matrix) or 1 if BRC else 1
                v3 = GL(goal, start, neighbor) if GLF else 0

                cost = 14 if hchoice == 1 and dX != 0 and dY != 0 else (10 if hchoice == 1 else (math.sqrt(2) if dX != 0 and dY != 0 else 1))
                tentative_g = g_backward.get(current_backward, 0) + cost

                if neighbor not in g_backward or tentative_g < g_backward[neighbor]:
                    g_backward[neighbor] = tentative_g

                    h_to_current_f = 0 #heuristic(neighbor, current_backward, 2)

                    if BRC:
                        f_backward[neighbor] = tentative_g + (heuristic(neighbor, start, hchoice) * (1 - math.log(v2))) + v1 + v3 + h_to_current_f
                    else:
                        f_backward[neighbor] = tentative_g + heuristic(neighbor, start, hchoice) + v1 + v3 + h_to_current_f

                    came_from_backward[neighbor] = current_backward
                    heapq.heappush(open_backward, (f_backward[neighbor], neighbor))
                    open_set_backward.add(neighbor)

        if show:
            combined_open = open_forward + open_backward
            combined_closed = closed_forward.union(closed_backward)
            Z_GetMap.Render(surface, matrix, cell_size, combined_open, combined_closed)
            clock.tick(speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()

    end_time = time.time()

    if meet_point:
        path_forward = []
        node = meet_point
        while node in came_from_forward:
            path_forward.append(node)
            node = came_from_forward[node]
        path_forward.append(start)
        path_forward.reverse()

        path_backward = []
        node = meet_point
        while node in came_from_backward:
            node = came_from_backward[node]
            path_backward.append(node)

        full_path = path_forward + path_backward

        if show:
            Z_GetMap.Render(surface, matrix, cell_size, combined_open, combined_closed, full_path)
            clock.tick(speed)
            time.sleep(2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()

        return (full_path, round(end_time - start_time, 6)), (open_forward + open_backward), closed_forward.union(closed_backward)

    
    return (0, round(end_time - start_time, 6)), 0, 0