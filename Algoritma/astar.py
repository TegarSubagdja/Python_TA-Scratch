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
        
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal, hchoice)}

    pqueue = []

    heapq.heappush(pqueue, (fscore[start], start))

    starttime = time.time()

    while pqueue:

        current = heapq.heappop(pqueue)[1]
        # print("="*100)
        # print(f"# Titik saat ini : {current}")
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path = path[::]
            print(gscore[goal])
            endtime = time.time()
            return (path, round(endtime - starttime, 6))

        close_set.add(current)
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
                    tentative_g_score = gscore[current] + 14
                else:
                    tentative_g_score = gscore[current] + 10
            elif hchoice == 2:
                if dX != 0 and dY != 0:
                    tentative_g_score = gscore[current] + math.sqrt(2)
                else:
                    tentative_g_score = gscore[current] + 1

            if (
                neighbour in close_set
            ):  # and tentative_g_score >= gscore.get(neighbour,0):
                continue

            if tentative_g_score < gscore.get(
                neighbour, 0
            ) or neighbour not in [i[1] for i in pqueue]:
                came_from[neighbour] = current
                gscore[neighbour] = tentative_g_score
                fscore[neighbour] = tentative_g_score + heuristic(
                    neighbour, goal, hchoice
                )
                # print(f"* Untuk tetangga : {neighbour}")
                # print(f"gn : {tentative_g_score}")
                # print(f"hn : {heuristic(neighbour, goal, hchoice)}")
                # print(f"fn : {fscore[neighbour]}")
                # print("\n")
                heapq.heappush(pqueue, (fscore[neighbour], neighbour))

            if show:
                Z_GetMap.Render(surface, map, cell_size, pqueue, close_set)
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
        # print(f"Total Open List : {pqueue}")
        endtime = time.time()
    return (0, round(endtime - starttime, 6))