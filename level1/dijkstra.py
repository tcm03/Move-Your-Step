import heapq

INF = 1000000000

def dijkstra(school_map):
    N = len(school_map) # number of rows
    M = len(school_map[0]) # number of columns
    for i in range(N):
        for j in range(M):
            if school_map[i][j][0] == "A":
                start = (i, j) # start cell
    record_list = []
    Q = []
    heapq.heappush(Q, (0, start)) # push start node with distance 0
    trace = []
    for i in range(N):
        arr = []
        for j in range(M):
            arr.append((-1, -1))
        trace.append(arr)
    dist = []
    for i in range(N):
        arr = []
        for j in range(M):
            arr.append(INF)
        dist.append(arr)
    dist[start[0]][start[1]] = 0
    goal = (-1, -1)
    while len(Q) > 0:
        d, (x, y) = heapq.heappop(Q) # pop the node with the smallest distance
        if d != dist[x][y]: # this node has already been processed
            continue
        record_list.append((x,y))
        # the destination is here!
        if school_map[x][y][0] == "T":
            goal = (x, y)
            break
        for x_offset, y_offset in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            next_x, next_y = x + x_offset, y + y_offset
            # invalid next cell
            if next_x < 0 or next_x >= N or next_y < 0 or next_y >= M:
                continue
            # next cell is a wall
            if school_map[next_x][next_y] == "-1":
                continue
            # in case of a diagonal move
            if abs(next_x - x) + abs(next_y - y) == 2:
                # check if neighboring cells are walls
                valid = True
                for u in [min(x, next_x), max(x, next_x)]:
                    for v in [min(y, next_y), max(y, next_y)]:
                        if school_map[u][v] == "-1":
                            valid = False
                            break
                if not valid:
                    continue
            # relax the edge
            if dist[x][y] + 1 < dist[next_x][next_y]:
                dist[next_x][next_y] = dist[x][y] + 1
                trace[next_x][next_y] = (x, y)
                heapq.heappush(Q, (dist[next_x][next_y], (next_x, next_y))) # push the next node into the queue
    if goal == (-1, -1):
        return None, None, None
    else:
        d = dist[goal[0]][goal[1]]
        path = []
        while goal != (-1, -1):
            path.append(goal)
            goal = trace[goal[0]][goal[1]]
        path.reverse()
        return d, path, record_list
