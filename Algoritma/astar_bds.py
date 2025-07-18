import math, heapq, time

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
        
def reconstruct_path(came_from_forward, came_from_backward, intersection_node):
    path_forward = []
    current = intersection_node
    while current in came_from_forward:
        path_forward.append(current)
        current = came_from_forward[current]
    path_forward.append(current)  
    path_forward = path_forward[::-1] 
    path_backward = []
    current = intersection_node
    while current in came_from_backward:
        current = came_from_backward[current]
        path_backward.append(current)
    return path_forward + path_backward
    
def method(matrix, start, goal, hchoice):
    open_list_backward = []
    close_list_forward = set()
    came_from_forward = {}
    gn_forward = {start: 0}
    fn_forward = {start: heuristic(start, goal, hchoice)}
    heapq.heappush(open_list_backward, (fn_forward[start], start))
    open_list_backward = []
    close_list_backward = set()
    came_from_backward = {}
    gn_backward = {goal: 0}
    fn_backward = {goal: heuristic(goal, start, hchoice)}
    heapq.heappush(open_list_backward, (fn_backward[goal], goal))
    starttime = time.time()
    intersection = None
    best_path_length = float('inf')
    while open_list_backward and open_list_backward:
        current_forward = heapq.heappop(open_list_backward)[1]
        if current_forward in close_list_backward:
            path_length = gn_forward[current_forward] + gn_backward[current_forward]
            if path_length < best_path_length:
                best_path_length = path_length
                intersection = current_forward
        close_list_forward.add(current_forward)
        for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0), 
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if blocked(current_forward[0], current_forward[1], dX, dY, matrix):
                continue
            neighbour = current_forward[0] + dX, current_forward[1] + dY
            if hchoice == 1:
                if dX != 0 and dY != 0:
                    tentative_g_score = gn_forward[current_forward] + 14  
                else:
                    tentative_g_score = gn_forward[current_forward] + 10  
            elif hchoice == 2:
                if dX != 0 and dY != 0:
                    tentative_g_score = gn_forward[current_forward] + math.sqrt(2)  
                else:
                    tentative_g_score = gn_forward[current_forward] + 1  
            if neighbour in close_list_forward:
                continue
            if tentative_g_score < gn_forward.get(neighbour, float('inf')) or neighbour not in [i[1] for i in open_list_backward]:
                came_from_forward[neighbour] = current_forward
                gn_forward[neighbour] = tentative_g_score
                fn_forward[neighbour] = tentative_g_score + heuristic(neighbour, goal, hchoice)
                heapq.heappush(open_list_backward, (fn_forward[neighbour], neighbour))
        current_backward = heapq.heappop(open_list_backward)[1]
        if current_backward in close_list_forward:
            path_length = gn_forward[current_backward] + gn_backward[current_backward]
            if path_length < best_path_length:
                best_path_length = path_length
                intersection = current_backward
        close_list_backward.add(current_backward)
        for dX, dY in [(0, 1), (0, -1), (1, 0), (-1, 0), 
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if blocked(current_backward[0], current_backward[1], dX, dY, matrix):
                continue
            neighbour = current_backward[0] + dX, current_backward[1] + dY
            if hchoice == 1:
                if dX != 0 and dY != 0:
                    tentative_g_score = gn_backward[current_backward] + 14  
                else:
                    tentative_g_score = gn_backward[current_backward] + 10  
            elif hchoice == 2:
                if dX != 0 and dY != 0:
                    tentative_g_score = gn_backward[current_backward] + math.sqrt(2)  
                else:
                    tentative_g_score = gn_backward[current_backward] + 1  
            if neighbour in close_list_backward:
                continue
            if tentative_g_score < gn_backward.get(neighbour, float('inf')) or neighbour not in [i[1] for i in open_list_backward]:
                came_from_backward[neighbour] = current_backward
                gn_backward[neighbour] = tentative_g_score
                fn_backward[neighbour] = tentative_g_score + heuristic(neighbour, start, hchoice)
                heapq.heappush(open_list_backward, (fn_backward[neighbour], neighbour))
    endtime = time.time()
    if intersection:
        path = reconstruct_path(came_from_forward, came_from_backward, intersection)
        return (path, round(endtime - starttime, 6))
    else:
        return (0, round(endtime - starttime, 6))
