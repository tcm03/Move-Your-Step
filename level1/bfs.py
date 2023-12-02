from queue import Queue
import sys

from level1.custom_parser import read_input

INF = 1000000000

def breadth_first_search(school_map):
    """
    Description:
        Find the shortest path from the start to the goal using breadth-first search.
    Args:
        school_map: a 2D array of strings, representing the school map
    Returns:
        a tuple (d, path), where d is the shortest path length and path is a list of coordinates
        [(x1, y1), (x2, y2), ..., (xk, yk)] such that (x1, y1) is the start, (xk, yk) is the goal,
        and (xi, yi) and (xi+1, yi+1) are adjacent cells in the path.
        If there is no path, return None.
    """
    N = len(school_map) # number of rows
    M = len(school_map[0]) # number of columns
    for i in range(N):
        for j in range(M):
            if school_map[i][j][0] == "A":
                start = (i, j) # start cell
    record_list = []
    Q = Queue()
    Q.put(start)
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
    while Q.qsize() > 0:
        if goal != (-1, -1):
            break
        x, y = Q.get()
        record_list.append((x,y))
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
            # next cell is already visited
            if dist[next_x][next_y] != INF:
                continue
            dist[next_x][next_y] = dist[x][y] + 1
            trace[next_x][next_y] = (x, y)
            # the destination is here!
            if school_map[next_x][next_y][0] == "T":
                goal = (next_x, next_y)
                break
            Q.put((next_x, next_y))
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

def main():
    if len(sys.argv) < 2:
        sys.exit("Please enter the input file name.")
    elif len(sys.argv) > 2:
        sys.exit("Too many arguments.")
    school_map = read_input(sys.argv[1])
    answer = breadth_first_search(school_map)
    if answer:
        d, path = answer
        print(f"Shortest path length: {d}")
        print("Path:")
        for x, y in path:
            print(f"({x}, {y})")
    else:
        print("No solution.")

if __name__ == "__main__":
    main()