import math
import sys
from queue import PriorityQueue



INF = 1000000000


def evaluate_euclidean_distance(current, goal):
    return math.sqrt((current[0]-goal[0])**2 + (current[1]-goal[1])**2)


def next_move(school_map, current):
    N = len(school_map)  # number of rows
    M = len(school_map[0])  # number of columns

    current_x = current[0]
    current_y = current[1]
    current_key_set = current[2]
    available_moves = []

    for x_offset, y_offset in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        next_x, next_y, next_key_set = current_x + x_offset, current_y + y_offset, current_key_set
        # invalid next cell
        if next_x < 0 or next_x >= N or next_y < 0 or next_y >= M:
            continue

        if school_map[next_x][next_y] == "-1":
            continue

        if abs(x_offset + y_offset) != 1:
            # check if neighboring cells are walls
            if school_map[current_x + x_offset][current_y + 0] == '-1':
                continue
            if school_map[current_x + 0][current_y + y_offset] == '-1':
                continue
            # check if neighboring cells are doors
            if school_map[current_x + x_offset][current_y + 0][0] == 'D':
                key_number = int(school_map[current_x + x_offset][current_y + 0][1])
                if current_key_set & (1 << (key_number - 1)) == 0:
                    continue
            if school_map[current_x + 0][current_y + y_offset][0] == 'D':
                key_number = int(school_map[current_x + 0][current_y + y_offset][1])
                if current_key_set & (1 << (key_number - 1)) == 0:
                    continue

        if school_map[next_x][next_y][0] == "D":
            # check if the key is available
            key_number = int(school_map[next_x][next_y][1])
            # check whether agent has corresponding key
            if current_key_set & (1 << (key_number - 1)) == 0:
                continue

        if school_map[next_x][next_y][0] == "K":
            key_number = int(school_map[next_x][next_y][1])
            next_key_set |= (1 << (key_number - 1))

        available_moves.append((next_x, next_y, next_key_set))

    return available_moves


def a_star(school_map):
    record_list = []
    N = len(school_map)  # number of rows
    M = len(school_map[0])  # number of columns

    start = (0, 0, 0)
    goal = (0, 0, 0)

    # Find the highest key number and calculate total number of keys
    num_keys = 0
    for i in range(N):
        for j in range(M):
            if school_map[i][j][0] == "K":
                num_keys = max(num_keys, int(school_map[i][j][1:]))

    # Calculate the total number of possible key combinations
    K = 1 << num_keys

    for i in range(N):
        for j in range(M):
            if school_map[i][j][0] == "A":
                start = (i, j, 0)
            if school_map[i][j][0] == "T":
                goal = (i, j, 0)  # start cell

    # Initialize two data structures for backtracking and distance
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

    # Set starting point distance to 0
    dist[start[0]][start[1]][start[2]] = 0

    frontier = PriorityQueue()

    # add starting node into frontier
    frontier.put((evaluate_euclidean_distance(current=start, goal=goal), start))

    while not frontier.empty():

        f_value, (x, y, key_set) = frontier.get()
        record_list.append((x,y))

        # check cell is goal
        if (x, y) == (goal[0], goal[1]):
            d = dist[x][y][key_set]
            path = []
            while (x, y, key_set) != (-1, -1, -1):
                key_set_str = bin(key_set)[2:].zfill(num_keys)[::-1]
                path.append((x, y, key_set_str))
                (x, y, key_set) = trace[x][y][key_set]
            path.reverse()
            return d, path,record_list

        available_moves = next_move(current=(x, y, key_set), school_map=school_map)

        for next_x, next_y, next_key_set in available_moves:
            # next cell is already visited
            if dist[next_x][next_y][next_key_set] != INF:
                continue

            # update path and heuristic
            dist_next = dist[x][y][key_set] + 1
            heuristic_next = evaluate_euclidean_distance(current=(next_x, next_y), goal=goal)
            dist[next_x][next_y][next_key_set] = dist_next
            trace[next_x][next_y][next_key_set] = (x, y, key_set)

            #
            # check cell exists in frontier and update if needed
            #

            frontier.put((dist_next+heuristic_next, (next_x, next_y, next_key_set)))

    return None, None, None
