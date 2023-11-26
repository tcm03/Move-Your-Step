from queue import Queue
from custom_parser import *
import sys

INF = 1000000000

def breadth_first_search(school_map):
    """
    Description:
        Find the shortest path from the start to the goal using breadth-first search.
    Args:
        school_map: a 3D array of strings, representing the school map with multiple floors
    Returns:
        a tuple (d, path), where d is the shortest path length and path is a list of coordinates
        [(x1, y1), (x2, y2), ..., (xk, yk)] such that (x1, y1) is the start, (xk, yk) is the goal,
        and (xi, yi) and (xi+1, yi+1) are adjacent cells in the path.
        If there is no path, return None.
    """
    D = len(school_map)
    N = len(school_map[0])
    M = len(school_map[0][0])
    num_keys = 0
    for f in range(D):
        for i in range(N):
            for j in range(M):
                if school_map[f][i][j][0] == "K":
                    num_keys = max(num_keys, int(school_map[f][i][j][1:]))
    K = 1 << num_keys

    for f in range(D):
        for i in range(N):
            for j in range(M):
                if school_map[f][i][j][0] == "A":
                    start = (f, i, j, 0) # (floor, x-coordinate, y-coordinate, keyset)
    Q = Queue()
    Q.put(start)
    trace = []
    for _ in range(D):
        floor = []
        for _ in range(N):
            arr = []
            for _ in range(M):
                sub_arr = []
                for _ in range(K):
                    sub_arr.append((-1, -1, -1, -1))
                arr.append(sub_arr)
            floor.append(arr)
        trace.append(floor)
    dist = []
    for _ in range(D):
        floor = []
        for _ in range(N):
            arr = []
            for _ in range(M):
                sub_arr = []
                for _ in range(K):
                    sub_arr.append(INF)
                arr.append(sub_arr)
            floor.append(arr)
        dist.append(floor)
    dist[start[0]][start[1]][start[2]][start[3]] = 0
    goal = (-1, -1, -1, -1)
    while Q.qsize() > 0:
        if goal != (-1, -1, -1, -1):
            break
        f, x, y, keyset = Q.get()
        moves = [(0, 0, 1), (0, 1, 0), (0, 0, -1), (0, -1, 0), (0, -1, -1), (0, -1, 1), (0, 1, -1), (0, 1, 1)]
        if school_map[f][x][y] == "UP":
            moves.append((1, 0, 0))
        elif school_map[f][x][y] == "DO":
            moves.append((-1, 0, 0))
        for f_offset, x_offset, y_offset in moves:
            next_f, next_x, next_y = f + f_offset, x + x_offset, y + y_offset
            assert 0 <= next_f < D, f"Error: {next_f} is not a valid floor number"
            # invalid next cell
            if next_x < 0 or next_x >= N or next_y < 0 or next_y >= M:
                continue
            # next cell is a wall
            if school_map[next_f][next_x][next_y] == "-1":
                continue
            # in case of a diagonal move
            if abs(next_x - x) + abs(next_y - y) == 2:
                assert next_f == f, "Error: cannot move diagonally between floors"
                # check if neighboring cells are walls
                valid = True
                for u in [min(x, next_x), max(x, next_x)]:
                    for v in [min(y, next_y), max(y, next_y)]:
                        if school_map[f][u][v] == "-1":
                            valid = False
                            break
                if not valid:
                    continue
            if school_map[next_f][next_x][next_y][0] == "D" and school_map[next_f][next_x][next_y][1] != "O":
                # check if the key is available
                num = int(school_map[next_f][next_x][next_y][1:])
                # this door has no corresponding key
                if num > num_keys:
                    continue
                # this door has a corresponding key, but the key is not available
                if keyset & (1 << (num-1)) == 0:
                    continue
            new_keyset = keyset
            if school_map[next_f][next_x][next_y][0] == "K":
                new_keyset |= (1 << (int(school_map[next_f][next_x][next_y][1:]) - 1))
            # next cell is already visited
            if dist[next_f][next_x][next_y][new_keyset] != INF:
                continue
            dist[next_f][next_x][next_y][new_keyset] = dist[f][x][y][keyset] + 1
            trace[next_f][next_x][next_y][new_keyset] = (f, x, y, keyset)
            # the destination is here!
            if school_map[next_f][next_x][next_y][0] == "T":
                goal = (next_f, next_x, next_y, new_keyset)
                break
            Q.put((next_f, next_x, next_y, new_keyset))
    if goal == (-1, -1, -1, -1):
        return None
    else:
        d = dist[goal[0]][goal[1]][goal[2]][goal[3]]
        path = []
        while goal != (-1, -1, -1, -1):
            path.append(goal)
            goal = trace[goal[0]][goal[1]][goal[2]][goal[3]]
        path.reverse()
        return d, path


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
        for f, x, y, keyset in path:
            print(f"({f}, {x}, {y}, {bin(keyset)})")
    else:
        print("No solution.")

if __name__ == "__main__":
    main()
