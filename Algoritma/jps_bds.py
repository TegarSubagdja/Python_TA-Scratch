import math, time, heapq
def heuristic(a, b, hchoice):
    if hchoice == 1:
        xdist = math.fabs(b[0] - a[0])
        ydist = math.fabs(b[1] - a[1])
        if xdist > ydist:
            return 14 * ydist + 10 * (xdist - ydist)
        else:
            return 14 * xdist + 10 * (ydist - xdist)
    if hchoice == 2:        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
    
def blocked(cX, cY, dX, dY, matrix):
    if cX + dX < 0 or cX + dX >= matrix.shape[0]:
        return True
    if cY + dY < 0 or cY + dY >= matrix.shape[1]:
        return True
    if dX != 0 and dY != 0:
        if matrix[cX + dX][cY] == 1 and matrix[cX][cY + dY] == 1:
            return True
        if matrix[cX + dX][cY + dY] == 1:
            return True
    else:
        if dX != 0:
            if matrix[cX + dX][cY] == 1:
                return True
        else:
            if matrix[cX][cY + dY] == 1:
                return True
    return False
    
def dblock(cX, cY, dX, dY, matrix):
    if matrix[cX - dX][cY] == 1 and matrix[cX][cY - dY] == 1:
        return True
    return False
    
def direction(cX, cY, pX, pY):
    dX = int(math.copysign(1, cX - pX))
    dY = int(math.copysign(1, cY - pY))
    if cX - pX == 0:
        dX = 0
    if cY - pY == 0:
        dY = 0
    return (dX, dY)
    
def nodeNeighbours(cX, cY, parent, matrix):
    neighbours = []
    if type(parent) != tuple:
        for i, j in [(-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
            if not blocked(cX, cY, i, j, matrix):
                neighbours.append((cX + i, cY + j))
        return neighbours
    dX, dY = direction(cX, cY, parent[0], parent[1])
    if dX != 0 and dY != 0:
        if not blocked(cX, cY, 0, dY, matrix):
            neighbours.append((cX, cY + dY))
        if not blocked(cX, cY, dX, 0, matrix):
            neighbours.append((cX + dX, cY))
        if (not blocked(cX, cY, 0, dY, matrix) or not blocked(cX, cY, dX, 0, matrix)) and not blocked(cX, cY, dX, dY, matrix):
            neighbours.append((cX + dX, cY + dY))
        if blocked(cX, cY, -dX, 0, matrix) and not blocked(cX, cY, 0, dY, matrix):
            neighbours.append((cX - dX, cY + dY))
        if blocked(cX, cY, 0, -dY, matrix) and not blocked(cX, cY, dX, 0, matrix):
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
            if (not blocked(oX, oY, -dX, dY, matrix) and blocked(oX, oY, -dX, 0, matrix)
                or not blocked(oX, oY, dX, -dY, matrix) and blocked(oX, oY, 0, -dY, matrix)):
                return (oX, oY)
            if (jump(oX, oY, dX, 0, matrix, goal) != None
                or jump(oX, oY, 0, dY, matrix, goal) != None):
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
                if (not blocked(oX, nY, dX, 1, matrix) and blocked(oX, nY, 0, 1, matrix)
                    or not blocked(oX, nY, dX, -1, matrix) and blocked(oX, nY, 0, -1, matrix)):
                    return (oX, nY)
                oX += dX
                if blocked(oX, nY, 0, 0, matrix):
                    return None
                if (oX, nY) == goal:
                    return (oX, nY)
        else:
            while True:
                if (not blocked(nX, oY, 1, dY, matrix) and blocked(nX, oY, 1, 0, matrix)
                    or not blocked(nX, oY, -1, dY, matrix) and blocked(nX, oY, -1, 0, matrix)):
                    return (nX, oY)
                oY += dY
                if blocked(nX, oY, 0, 0, matrix):
                    return None
                if (nX, oY) == goal:
                    return (nX, oY)
    return jump(nX, nY, dX, dY, matrix, goal)
    
def identifySuccessors(cX, cY, came_from, matrix, goal):
    successors = []
    neighbours = nodeNeighbours(cX, cY, came_from.get((cX, cY), 0), matrix)
    for cell in neighbours:
        dX = cell[0] - cX
        dY = cell[1] - cY
        jumpPoint = jump(cX, cY, dX, dY, matrix, goal)
        if jumpPoint != None:
            successors.append(jumpPoint)
    return successors
    
def reconstruct_path(came_from_forward, came_from_backward, intersection_node, start, goal):
    path_forward = []
    current = intersection_node
    while current in came_from_forward:
        path_forward.append(current)
        current = came_from_forward[current]
    path_forward.append(start)
    path_forward = path_forward[::-1]
    path_backward = []
    current = intersection_node
    while current in came_from_backward:
        current = came_from_backward[current]
        path_backward.append(current)
    return path_forward + path_backward
    
def method(matrix, start, goal, hchoice):
    came_from_forward = {}
    close_set_forward = set()
    gscore_forward = {start: 0}
    fscore_forward = {start: heuristic(start, goal, hchoice)}
    open_set_forward = []
    heapq.heappush(open_set_forward, (fscore_forward[start], start))
    came_from_backward = {}
    close_set_backward = set()
    gscore_backward = {goal: 0}
    fscore_backward = {goal: heuristic(goal, start, hchoice)}
    open_set_backward = []
    heapq.heappush(open_set_backward, (fscore_backward[goal], goal))
    starttime = time.time()
    intersection = None
    best_path_length = float('inf')
    while open_set_forward and open_set_backward:
        current_forward = heapq.heappop(open_set_forward)[1]
        if current_forward in close_set_backward:
            path_length = gscore_forward[current_forward] + gscore_backward[current_forward]
            if path_length < best_path_length:
                best_path_length = path_length
                intersection = current_forward
        close_set_forward.add(current_forward)
        successors_forward = identifySuccessors(current_forward[0], current_forward[1], came_from_forward, matrix, goal)
        for successor in successors_forward:
            jumpPoint = successor
            if jumpPoint in close_set_forward:
                continue
            tentative_g_score = gscore_forward[current_forward] + lenght(current_forward, jumpPoint, hchoice)
            if tentative_g_score < gscore_forward.get(jumpPoint, float('inf')) or jumpPoint not in [j[1] for j in open_set_forward]:
                came_from_forward[jumpPoint] = current_forward
                gscore_forward[jumpPoint] = tentative_g_score
                fscore_forward[jumpPoint] = tentative_g_score + heuristic(jumpPoint, goal, hchoice)
                heapq.heappush(open_set_forward, (fscore_forward[jumpPoint], jumpPoint))
                if jumpPoint in close_set_backward:
                    path_length = gscore_forward[jumpPoint] + gscore_backward[jumpPoint]
                    if path_length < best_path_length:
                        best_path_length = path_length
                        intersection = jumpPoint
        current_backward = heapq.heappop(open_set_backward)[1]
        if current_backward in close_set_forward:
            path_length = gscore_forward[current_backward] + gscore_backward[current_backward]
            if path_length < best_path_length:
                best_path_length = path_length
                intersection = current_backward
        close_set_backward.add(current_backward)
        successors_backward = identifySuccessors(current_backward[0], current_backward[1], came_from_backward, matrix, start)
        for successor in successors_backward:
            jumpPoint = successor
            if jumpPoint in close_set_backward:
                continue
            tentative_g_score = gscore_backward[current_backward] + lenght(current_backward, jumpPoint, hchoice)
            if tentative_g_score < gscore_backward.get(jumpPoint, float('inf')) or jumpPoint not in [j[1] for j in open_set_backward]:
                came_from_backward[jumpPoint] = current_backward
                gscore_backward[jumpPoint] = tentative_g_score
                fscore_backward[jumpPoint] = tentative_g_score + heuristic(jumpPoint, start, hchoice)
                heapq.heappush(open_set_backward, (fscore_backward[jumpPoint], jumpPoint))
                if jumpPoint in close_set_forward:
                    path_length = gscore_forward[jumpPoint] + gscore_backward[jumpPoint]
                    if path_length < best_path_length:
                        best_path_length = path_length
                        intersection = jumpPoint
        if intersection and best_path_length < float('inf'):
            min_f_forward = open_set_forward[0][0] if open_set_forward else float('inf')
            min_f_backward = open_set_backward[0][0] if open_set_backward else float('inf')
            if min_f_forward + min_f_backward >= best_path_length:
                path = reconstruct_path(came_from_forward, came_from_backward, intersection, start, goal)
                endtime = time.time()
                return (path, round(endtime - starttime, 6)), open_list, close_list
    endtime = time.time()
    if intersection:
        path = reconstruct_path(came_from_forward, came_from_backward, intersection, start, goal)
        return (path, round(endtime - starttime, 6)), open_list, close_list
    else:
        return (0, round(endtime - starttime, 6))
        
def lenght(current, jumppoint, hchoice):
    dX, dY = direction(current[0], current[1], jumppoint[0], jumppoint[1])
    dX = math.fabs(dX)
    dY = math.fabs(dY)
    lX = math.fabs(current[0] - jumppoint[0])
    lY = math.fabs(current[1] - jumppoint[1])
    if hchoice == 1:
        if dX != 0 and dY != 0:
            lenght = lX * 14
            return lenght
        else:
            lenght = (dX * lX + dY * lY) * 10
            return lenght
    if hchoice == 2:
        return math.sqrt((current[0] - jumppoint[0]) ** 2 + (current[1] - jumppoint[1]) ** 2)