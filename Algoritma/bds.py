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

def method(matrix, start, goal, hchoice, show=False):

    if show:
        surface, cell_size = Z_GetMap.Init_Visual(matrix)
        clock = pygame.time.Clock()
        
    open_forward = []
    open_backward = []

    came_from_forward = {}
    came_from_backward = {}

    g_forward = {start: 0}
    g_backward = {goal: 0}

    f_forward = {start: heuristic(start, goal, hchoice)}
    f_backward = {goal: heuristic(goal, start, hchoice)}

    closed_forward = set()
    closed_backward = set()

    heapq.heappush(open_forward, (f_forward[start], start))
    heapq.heappush(open_backward, (f_backward[goal], goal))

    start_time = time.time()

    meet_point = None

    while open_forward and open_backward:
        # Forward direction
        _, current_forward = heapq.heappop(open_forward)
        closed_forward.add(current_forward)

        for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if blocked(current_forward[0], current_forward[1], dX, dY, matrix):
                continue

            neighbor = current_forward[0] + dX, current_forward[1] + dY

            if neighbor in closed_forward:
                continue

            cost = 14 if (dX != 0 and dY != 0) else 10 if hchoice == 1 else math.sqrt(2) if (dX != 0 and dY != 0) else 1
            tentative_g = g_forward[current_forward] + cost

            if neighbor not in g_forward or tentative_g < g_forward[neighbor]:
                g_forward[neighbor] = tentative_g
                f_forward[neighbor] = tentative_g + heuristic(neighbor, goal, hchoice)
                came_from_forward[neighbor] = current_forward
                heapq.heappush(open_forward, (f_forward[neighbor], neighbor))

            if neighbor in closed_backward:
                meet_point = neighbor
                break
        if meet_point:
            break

        # Backward direction
        _, current_backward = heapq.heappop(open_backward)
        closed_backward.add(current_backward)

        for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if blocked(current_backward[0], current_backward[1], dX, dY, matrix):
                continue

            neighbor = current_backward[0] + dX, current_backward[1] + dY

            if neighbor in closed_backward:
                continue

            cost = 14 if (dX != 0 and dY != 0) else 10 if hchoice == 1 else math.sqrt(2) if (dX != 0 and dY != 0) else 1
            tentative_g = g_backward[current_backward] + cost

            if neighbor not in g_backward or tentative_g < g_backward[neighbor]:
                g_backward[neighbor] = tentative_g
                f_backward[neighbor] = tentative_g + heuristic(neighbor, start, hchoice)
                came_from_backward[neighbor] = current_backward
                heapq.heappush(open_backward, (f_backward[neighbor], neighbor))

            if neighbor in closed_forward:
                meet_point = neighbor
                break
        if meet_point:
            break

        if show:
            combined_open = open_forward + open_backward
            combined_closed = closed_forward.union(closed_backward)
            Z_GetMap.Render(surface, matrix, cell_size, combined_open, combined_closed)
            clock.tick(120)  # Contoh 30 FPS

    end_time = time.time()

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
        return (full_path, round(end_time - start_time, 6))
    
    return (0, round(end_time - start_time, 6))
