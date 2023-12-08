import heapq

INF = 1000000000

def dijkstra(school_map):
    record_list = []
    N = len(school_map) # number of rows
    M = len(school_map[0]) # number of columns
    num_keys = 0
    for i in range(N):
        for j in range(M):
            if school_map[i][j][0] == "K":
                num_keys = max(num_keys, int(school_map[i][j][1:]))
    K = 1 << num_keys

    for i in range(N):
        for j in range(M):
            if school_map[i][j][0] == "A":
                start = (i, j, 0)
    Q = [] # use a priority queue
    heapq.heappush(Q, (0, start)) # push start node with distance 0
    trace = []
    for i in range(N):
        arr = []
        for j in range(M):
            sub_arr = []
            for k in range(K):
                sub_arr.append((-1, -1, -1))
            arr.append(sub_arr)
        trace.append(arr)
    dist = []
    for i in range(N):
        arr = []
        for j in range(M):
            sub_arr = []
            for k in range(K):
                sub_arr.append(INF)
            arr.append(sub_arr)
        dist.append(arr)
    dist[start[0]][start[1]][start[2]] = 0
    goal = (-1, -1, -1)
    while len(Q) > 0:
        d, (x, y, keyset) = heapq.heappop(Q) # pop the node with the smallest distance
        record_list.append((x,y))
        if d != dist[x][y][keyset]: # this node has already been processed
            continue
    # the destination is here!
        if school_map[x][y][0] == "T":
            goal = (x, y, keyset)
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
                        if school_map[u][v][0] == "D":
                            # check if the key is available
                            num = int(school_map[u][v][1:])
                            # this door has no corresponding key
                            if num > num_keys:
                                valid = False
                                break
                            # this door has a corresponding key, but the key is not available
                            if keyset & (1 << (num-1)) == 0:
                                valid = False
                                break
                if not valid:
                    continue
            if school_map[next_x][next_y][0] == "D":
                # check if the key is available
                num = int(school_map[next_x][next_y][1:])
                # this door has no corresponding key
                if num > num_keys:
                    continue
                # this door has a corresponding key, but the key is not available
                if keyset & (1 << (num-1)) == 0:
                    continue
            new_keyset = keyset
            if school_map[next_x][next_y][0] == "K":
                new_keyset |= (1 << (int(school_map[next_x][next_y][1:]) - 1))
            # next cell is already visited
            if dist[next_x][next_y][new_keyset] != INF:
                continue
            dist[next_x][next_y][new_keyset] = dist[x][y][keyset] + 1
            trace[next_x][next_y][new_keyset] = (x, y, keyset)
            heapq.heappush(Q, (dist[next_x][next_y][new_keyset], (next_x, next_y, new_keyset))) # push the next node into the queue
    if goal == (-1, -1, -1):
        return None,None,None
    else:
        d = dist[goal[0]][goal[1]][goal[2]]
        path = []
        while goal != (-1, -1, -1):
            keyset_str = bin(goal[2])[2:].zfill(num_keys)
            keyset_str = keyset_str[::-1]
            path.append((goal[0], goal[1], keyset_str))
            goal = trace[goal[0]][goal[1]][goal[2]]
        path.reverse()
        return d, path, record_list
