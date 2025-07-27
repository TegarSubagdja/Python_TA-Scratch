from Utils import *

surface, cell_size = None, None

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

# Modified jump function to pass back potential jump points for visualization
def jump(currentX, currentY, moveX, moveY, matrix, goal, jump_points_visual_list=None):

    nX = currentX + moveX
    nY = currentY + moveY
    if blocked(nX, nY, 0, 0, matrix):
        return None

    if (nX, nY) == goal:
        if jump_points_visual_list is not None:
            jump_points_visual_list.append((nX, nY))
        return (nX, nY)
    
    oX = nX
    oY = nY

    while True:
        # Add the current (oX, oY) to the list for visualization
        if jump_points_visual_list is not None:
            jump_points_visual_list.append((oX, oY))

        if moveX != 0 and moveY != 0:
            if (
                not blocked(oX, oY, -moveX, moveY, matrix)
                and blocked(oX, oY, -moveX, 0, matrix)
                or not blocked(oX, oY, moveX, -moveY, matrix)
                and blocked(oX, oY, 0, -moveY, matrix)
            ):
                return (oX, oY)

            if (
                jump(oX, oY, moveX, 0, matrix, goal, jump_points_visual_list) != None
                or jump(oX, oY, 0, moveY, matrix, goal, jump_points_visual_list) != None
            ):
                return (oX, oY)

        else: # moveX == 0 or moveY == 0 (straight moves)
            if moveX != 0: # Horizontal move
                if (
                    not blocked(oX, oY, moveX, 1, matrix)
                    and blocked(oX, oY, 0, 1, matrix)
                    or not blocked(oX, oY, moveX, -1, matrix)
                    and blocked(oX, oY, 0, -1, matrix)
                ):
                    return (oX, oY)
            else: # Vertical move
                if (
                    not blocked(oX, oY, 1, moveY, matrix)
                    and blocked(oX, oY, 1, 0, matrix)
                    or not blocked(oX, oY, -1, moveY, matrix)
                    and blocked(oX, oY, -1, 0, matrix)
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


def identifySuccessors(currentX, currentY, came_from, matrix, goal, jump_points_visual_list=None):
    successors = []
    neighbours = nodeNeighbours(currentX, currentY, came_from.get((currentX, currentY), 0), matrix)

    for cell in neighbours:
        moveX = cell[0] - currentX
        moveY = cell[1] - currentY

        # Pass the visualization list to the jump function
        jumpPoint = jump(currentX, currentY, moveX, moveY, matrix, goal, jump_points_visual_list)

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

    i = 0
    
    heapq.heappush(open_list, (fn[start], start))

    starttime = time.time()

    while open_list:

        current = heapq.heappop(open_list)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            data = data[::-1]
            if PPO:
                data = Prunning(data, matrix)
            endtime = time.time()
            if show:
                # Clear jump_points_to_display for final render
                Z_GetMap.Render(surface, matrix, cell_size, open_list, close_list, data)
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

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
            return (data, round(endtime - starttime, 6)), open_list, close_list

        close_list.add(current)
        
        current_jump_points_for_display = []
        successors = identifySuccessors(
            current[0], current[1], came_from, matrix, goal, current_jump_points_for_display
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
                # Temporary list to accumulate points for rendering
                temp_points_to_render = [] 
                
                # Loop through each point in current_jump_points_for_display
                for point_to_show in current_jump_points_for_display:
                    # Add the current point to the temporary accumulation list
                    temp_points_to_render.append(point_to_show)
                    
                    # Render with the accumulated points
                    Z_GetMap.Render(surface, matrix, cell_size, open_list, close_list, None, temp_points_to_render)
                    
                    # Add a small delay for step-by-step visualization
                    clock.tick(speed * 4) # Adjust speed as needed for step-by-step jump animation
                    
                    # Handle Pygame events during the delay
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                
                # After the loop, current_jump_points_for_display already holds the full jump path.
                # You might want a final render of the complete path for this jump before clearing.
                # This is effectively already done by the last iteration of the loop,
                # but an explicit call here can ensure it's shown for a moment longer if desired.
                # Z_GetMap.Render(surface, matrix, cell_size, open_list, close_list, None, current_jump_points_for_display)
                # clock.tick(speed) 
                
                # Clear the list for the next iteration (important for new jump paths)
                current_jump_points_for_display.clear() 
                
                # Handle Pygame events after the full jump path (if not cleared)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

        i+=1
        print(f"Iterasi ke-{i}")
        print(f"titik saat ini : {current}")
        print(f"open list adalah : {open_list}")
        print(f"close list adalah : {close_list}")
        print(f"fn : {fn[current]}")

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
    g_f = {start: 0}
    f_f = {start: heuristic(start, goal, hchoice)}

    # Backward
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
        
        # New list to store points for visualization during successor identification for forward search
        current_jump_points_for_display_f = []
        # New list to store points for visualization during successor identification for backward search
        current_jump_points_for_display_b = []

        # ============ Forward Expand ============
        if open_f:
            _, current_f = heapq.heappop(open_f)
            close_f.add(current_f)

            successors = identifySuccessors(current_f[0], current_f[1], came_from_f, matrix, goal, current_jump_points_for_display_f)
            
            for succ in successors:
                if succ in close_f:
                    continue

                v1 = TP(came_from_f.get(current_f, current_f), current_f, succ, k) if TPF else 0
                v2 = BR(succ, goal, matrix) or 1 if BRC else 1
                v3 = GL(start, goal, succ) if GLF else 0

                tentative_g = g_f[current_f] + lenght(current_f, succ, hchoice)

                if succ not in g_f or tentative_g < g_f[succ]:
                    came_from_f[succ] = current_f
                    g_f[succ] = tentative_g

                    h_to_goal = heuristic(succ, goal, hchoice)
                    
                    if BRC:
                        f_f[succ] = tentative_g + (h_to_goal * (1 - math.log(v2))) + v1 + v3 
                    else:
                        f_f[succ] = tentative_g + h_to_goal + v1 + v3 

                    heapq.heappush(open_f, (f_f[succ], succ))

                if succ in close_b:
                    meet_point = succ
                    break

        # ============ Backward Expand ============
        if open_b and not meet_point:
            _, current_b = heapq.heappop(open_b)
            close_b.add(current_b)

            successors_b = identifySuccessors(current_b[0], current_b[1], came_from_b, matrix, start, current_jump_points_for_display_b)
            
            for succ in successors_b:
                if succ in close_b:
                    continue

                v1 = TP(came_from_b.get(current_b, current_b), current_b, succ, k) if TPF else 0
                v2 = BR(succ, start, matrix) or 1 if BRC else 1
                v3 = GL(goal, start, succ) if GLF else 0

                tentative_g = g_b[current_b] + lenght(current_b, succ, hchoice)

                if succ not in g_b or tentative_g < g_b[succ]:
                    came_from_b[succ] = current_b
                    g_b[succ] = tentative_g

                    h_to_start = heuristic(succ, start, hchoice)
                    
                    if BRC:
                        f_b[succ] = tentative_g + (h_to_start * (1 - math.log(v2))) + v1 + v3 
                    else:
                        f_b[succ] = tentative_g + h_to_start + v1 + v3 

                    heapq.heappush(open_b, (f_b[succ], succ))

                if succ in close_f:
                    meet_point = succ
                    break

        if show:
            combined_open = open_f + open_b
            combined_close = close_f | close_b 
            # Combine jump points from both forward and backward searches for display
            combined_jump_points = current_jump_points_for_display_f + current_jump_points_for_display_b
            Z_GetMap.Render(surface, matrix, cell_size, combined_open, combined_close, None, combined_jump_points)
            
            current_jump_points_for_display_f.clear()
            current_jump_points_for_display_b.clear()

            clock.tick(speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
    
    if meet_point is None:
        endTime = time.time()
        return (0, round(endTime - startTime, 6)), 0, 0

    # ============ Path Reconstruction ============
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
        full_path = Prunning(full_path, matrix)

    endTime = time.time()

    if show:
        # Final render with the full path, and no current jump points
        Z_GetMap.Render(surface, matrix, cell_size, open_f + open_b, close_f | close_b, full_path)
        clock.tick(speed)
        time.sleep(2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

    return (full_path, round(endTime - startTime, 6)), (open_f + open_b), (close_f | close_b)

def lenght(current, jumppoint, hchoice):
    moveX, moveY = direction(current[0], current[1], jumppoint[0], jumppoint[1])
    # Correction: direction returns the actual step (-1, 0, or 1), not difference
    # For length calculation, we need the absolute difference in coordinates
    lX = math.fabs(current[0] - jumppoint[0])
    lY = math.fabs(current[1] - jumppoint[1])

    if hchoice == 1: # Manhattan or Octile based
        if lX != 0 and lY != 0: # Diagonal jump
            # Each diagonal step costs 14, each straight step costs 10.
            # A jump point covers multiple steps, so calculate true distance.
            min_dim = min(lX, lY)
            max_dim = max(lX, lY)
            # Octile distance formula for the length of the jump
            length = min_dim * 14 + (max_dim - min_dim) * 10
            return length
        else: # Straight jump (horizontal or vertical)
            length = (lX + lY) * 10 # Only one of lX or lY will be non-zero
            return length
    if hchoice == 2: # Euclidean
        return math.sqrt(
            (current[0] - jumppoint[0]) ** 2 + (current[1] - jumppoint[1]) ** 2
        )