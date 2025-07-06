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


def method(matrix, start, goal, hchoice=2, glm=False, brm=False , tpm=False, ppom=True, show=False, speed=30):

    if show:
        surface, cell_size = Z_GetMap.Init_Visual(matrix)
        clock = pygame.time.Clock()

    close_list = set()
    came_from = {}
    gn = {start: 0}
    fn = {start: heuristic(start, goal, hchoice)}

    open_list = []
    heapq.heappush(open_list, (fn[start], start))

    starttime = time.time()
    running = True

    while open_list and running:

        current = heapq.heappop(open_list)[1]
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path = path[::-1]
            endtime = time.time()
            return (path, round(endtime - starttime, 6))

        close_list.add(current)

        for dX, dY in [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1),
        ]:
            ny, nx = current[0] + dX, current[1] + dY

            if blocked(current[0], current[1], dX, dY, matrix):
                continue

            neighbour = (ny, nx)

            if hchoice == 1:
                tentative_gn = gn[current] + (14 if dX != 0 and dY != 0 else 10)
            elif hchoice == 2:
                tentative_gn = gn[current] + (math.sqrt(2) if dX != 0 and dY != 0 else 1)

            if neighbour in close_list:
                continue

            if tentative_gn < gn.get(neighbour, 0) or neighbour not in [i[1] for i in open_list]:
                came_from[neighbour] = current
                gn[neighbour] = tentative_gn
                fn[neighbour] = tentative_gn + heuristic(neighbour, goal, hchoice)
                heapq.heappush(open_list, (fn[neighbour], neighbour))

        # Visualisasi setiap langkah
        if show:
            Z_GetMap.Render(surface, matrix, cell_size, open_list, close_list)
            clock.tick(200)  # Batasi ke 60 FPS

    endtime = time.time()
    return (0, round(endtime - starttime, 6))
