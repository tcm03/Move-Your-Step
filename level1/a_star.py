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
    available_moves = []

    for x_offset, y_offset in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        next_x, next_y = current[0] + x_offset, current[1] + y_offset
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

        available_moves.append((current_x + x_offset, current_y + y_offset))

    return available_moves


def a_star(school_map):
    
    record_list = []
    N = len(school_map)  # number of rows
    M = len(school_map[0])  # number of columns

    start = (0, 0)
    goal = (0, 0)
    for i in range(N):
        for j in range(M):
            if school_map[i][j][0] == "A":
                start = (i, j)  # start cell
            if school_map[i][j][0] == "T":
                goal = (i, j)  # start cell

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

    frontier = PriorityQueue()

    # add starting node into frontier
    frontier.put((evaluate_euclidean_distance(current=start, goal=goal), start))

    while not frontier.empty():

        f_value, (x, y) = frontier.get()
        record_list.append((x,y))

        # check cell is goal
        if (x, y) == goal:
            d = dist[goal[0]][goal[1]]
            path = []
            while goal != (-1, -1):
                path.append(goal)
                goal = trace[goal[0]][goal[1]]
            path.reverse()
            return d, path, record_list

        available_moves = next_move(current=(x, y), school_map=school_map)

        for next_x, next_y in available_moves:
            # next cell is already visited
            if dist[next_x][next_y] != INF:
                continue

            # update path and heuristic
            dist_next = dist[x][y] + 1
            heuristic_next = evaluate_euclidean_distance(current=(next_x, next_y), goal=goal)
            dist[next_x][next_y] = dist_next
            trace[next_x][next_y] = (x, y)

            #
            # check cell exists in frontier and update if needed
            #

            frontier.put((dist_next+heuristic_next, (next_x, next_y)))

    return None,None, None
