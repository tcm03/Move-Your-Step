from queue import Queue
from custom_parser import *
import sys
import random
import copy

"""

Rule of thumb:
- Each agent, at its current position, consider adjacent agents (if any) to be present (except for A1), and 
ignore agents elsewhere (if any), in order to find the best path to its target.
  + If the next move on the best path is blocked by A1, the agent stands still (to wait for A1 to move).
  + If the next best move is available, move.
  + If there is no path to the target, move to an adjacent empty cell that is nearest to the target in terms of
    Manhattan distance.
  + If there is no adjacent empty cell, stand still (to wait for an adjacent cell to become empty).

"""

INF = 1000000000

def breadth_first_search(original_map, num_keys, agent_number, initial_pos, target_pos, original_keyset):
    print(f"agent: {agent_number}, keyset: {bin(original_keyset)}")
    school_map = copy.deepcopy(original_map)
    D = len(school_map)
    N = len(school_map[0])
    M = len(school_map[0][0])
    for x_offset, y_offset in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        next_x, next_y = initial_pos[1] + x_offset, initial_pos[2] + y_offset
        # invalid next cell
        if next_x < 0 or next_x >= N or next_y < 0 or next_y >= M:
            continue
        if school_map[initial_pos[0]][next_x][next_y][0] == "A":
            num = int(school_map[initial_pos[0]][next_x][next_y][1:])
            if num != 1:
                # view the agent as present and need to avoid
                school_map[initial_pos[0]][next_x][next_y] = "-1"
    
    K = 1 << num_keys
    start = (initial_pos[0], initial_pos[1], initial_pos[2], original_keyset)
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
        if school_map[f][x][y] == "UP" and agent_number == 1:
            moves.append((1, 0, 0))
        elif school_map[f][x][y] == "DO" and agent_number == 1:
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
                # check if neighboring cells are walls or other agents
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
            # print("num_keys:", num_keys, "K:", K)
            # print("cur:",f, x, y, bin(keyset))
            # print("next:",next_f, next_x, next_y, bin(new_keyset))
            # print("dist dimensions:", len(dist), len(dist[0]), len(dist[0][0]), len(dist[0][0][0]))
            if dist[next_f][next_x][next_y][new_keyset] != INF:
                continue
            dist[next_f][next_x][next_y][new_keyset] = dist[f][x][y][keyset] + 1
            trace[next_f][next_x][next_y][new_keyset] = (f, x, y, keyset)
            # the destination is here!
            if school_map[next_f][next_x][next_y][0] == "T" and int(school_map[next_f][next_x][next_y][1:]) == agent_number:
                goal = (next_f, next_x, next_y, new_keyset)
                break
            Q.put((next_f, next_x, next_y, new_keyset))
    
    print(f"{agent_number}: {goal[0]}, {goal[1]}, {goal[2]}, {bin(goal[3])}")
    if goal == (-1, -1, -1, -1):
        available_moves = []
        x, y = start[1], start[2]
        for x_offset, y_offset in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            next_x, next_y = x + x_offset, y + y_offset
            # invalid next cell
            if next_x < 0 or next_x >= N or next_y < 0 or next_y >= M:
                continue
            # in case of a diagonal move
            if abs(next_x - x) + abs(next_y - y) == 2:
                valid = True
                for u in [min(x, next_x), max(x, next_x)]:
                    for v in [min(y, next_y), max(y, next_y)]:
                        if school_map[f][u][v] == "-1":
                            valid = False
                            break
                if not valid:
                    continue
            if school_map[start[0]][next_x][next_y] == "0":
                available_moves.append((next_x, next_y))
        print(f"available moves: {available_moves}")
        if len(available_moves) == 0:
            return original_map, original_keyset
        next_move = (INF, 0, 0)
        for x, y in available_moves:
            if abs(x - target_pos[1]) + abs(y - target_pos[2]) < next_move[0]:
                next_move = (abs(x - target_pos[1]) + abs(y - target_pos[2]), x, y)
        print(f"next move: {next_move}")
        school_map = copy.deepcopy(original_map)
        school_map[start[0]][start[1]][start[2]] = "0"
        school_map[start[0]][next_move[1]][next_move[2]] = "A" + str(agent_number)
        return school_map, goal[3]

    else:
        # d = dist[goal[0]][goal[1]][goal[2]][goal[3]]
        # path = []
        while goal != (-1, -1, -1, -1) and trace[goal[0]][goal[1]][goal[2]][goal[3]] != start:
            # Convert goal[3] to a string representation of the keyset
            # keyset_str = bin(goal[3])[2:].zfill(num_keys)
            # keyset_str = keyset_str[::-1]
            # path.append((goal[0], goal[1], goal[2], keyset_str))
            goal = trace[goal[0]][goal[1]][goal[2]][goal[3]]
        # path.reverse()
        # return d, path
        print(f"next move: {goal}")
        if school_map[goal[0]][goal[1]][goal[2]] == "A1":
            # stand still to wait for A1 to move
            return original_map, original_keyset
        else:
            # move to the next cell
            print(f"move from {start} to {goal}")
            school_map = copy.deepcopy(original_map)
            school_map[start[0]][start[1]][start[2]] = "0"
            school_map[goal[0]][goal[1]][goal[2]] = "A" + str(agent_number)
            return school_map, goal[3]
    

def print_map(school_map):
    D = len(school_map)
    N = len(school_map[0])
    M = len(school_map[0][0])
    for f in range(D):
        print(f"floor {f+1}")
        for i in range(N):
            for j in range(M):
                print(school_map[f][i][j], end=",")
            print()
        print()

def update_map(original_map, num_agents):
    """
    If A1 has reached T1 (or T1 is missing from the map): return True, None
    Else: If any of the targets T2, ..., Tn is missing, randomly generate a new corresponding target. Then,
        return False, new_school_map
    """
    school_map = copy.deepcopy(original_map)
    D = len(school_map)
    N = len(school_map[0])
    M = len(school_map[0][0])
    existing_targets = []
    for f in range(D):
        for i in range(N):
            for j in range(M):
                if school_map[f][i][j][0] == "T":
                    existing_targets.append(int(school_map[f][i][j][1:]))
    print(f"existing_targets: {existing_targets}")
    if 1 not in existing_targets:
        return None
    for anum in range(2, num_agents+1):
        if anum not in existing_targets:
            print(f"Target {anum} is missing")
            # randomly generate a new target
            while True:
                f = random.randint(0, D-1)
                i = random.randint(0, N-1)
                j = random.randint(0, M-1)
                if school_map[f][i][j] == "0":
                    print(f"Put T{anum} at ({f}, {i}, {j})")
                    school_map[f][i][j] = "T" + str(anum)
                    break
    return school_map

def run_simulation(school_map):
    """
    Description:
        Find the shortest path from the start to the goal using breadth-first search.
    Args:
        school_map: a 2D array of strings, representing the school map
    Returns:
        a tuple (d, path), where d is the shortest path length and path is a list of coordinates
        [(x1, y1, s1), (x2, y2, s2), ..., (xk, yk, sk)] such that (x1, y1, s1) is the start, 
        (xk, yk, sk) is the goal, (xi, yi, si) and (xi+1, yi+1, si+1) are adjacent cells in the path, and:
        - xi: x-coordinate
        - yi: y-coordinate
        - si: keyset (represented as an binary integer)
        If there is no path, return None.
    """
    D = len(school_map)
    N = len(school_map[0])
    M = len(school_map[0][0])
    num_keys = 0
    num_agents = 0
    # assuming that initially, agents and keys are on the first floor
    for f in range(D):
        for i in range(N):
            for j in range(M):
                if school_map[f][i][j][0] == "K":
                    num_keys = max(num_keys, int(school_map[f][i][j][1:]))
                if school_map[f][i][j][0] == "A":
                    num_agents += 1

    keysets = {}
    for i in range(1, num_agents+1):
        keysets[i] = 0
    map_snapshot = []
    while True:
        map_snapshot.append(copy.deepcopy(school_map))
        positions = {}
        targets = {}
        for f in range(D):
            for i in range(N):
                for j in range(M):
                    if school_map[f][i][j][0] == "A":
                        positions[int(school_map[f][i][j][1:])] = (f, i, j)
                    if school_map[f][i][j][0] == "T":
                        targets[int(school_map[f][i][j][1:])] = (f, i, j)
        make_progress = False
        for i in range(1, num_agents+1):
            print(f"At {i}")
            # print_map(school_map)
            new_map, keysets[i] = breadth_first_search(school_map, num_keys, i, positions[i], targets[i], keysets[i])
            assert new_map is not None, "The breadth_first_search() never returns None"
            if new_map != school_map:
                make_progress = True
                school_map = update_map(new_map, num_agents)
                print("Make progress")
            if school_map is None:
                # A1 reached T1
                return map_snapshot
            else:
                # print_map(school_map)
                map_snapshot.append(copy.deepcopy(school_map))
            
        if not make_progress:
            return None

def main():
    if len(sys.argv) < 2:
        sys.exit("Please enter the input file name.")
    elif len(sys.argv) > 2:
        sys.exit("Too many arguments.")
    school_map = read_input(sys.argv[1])
    map_snapshot = run_simulation(school_map)
    if map_snapshot is None:
        print("Simulation failed. All agents are stuck.")
    else:
        with open("output.txt", "w") as file:
            for school_map in map_snapshot:
                for idx, floor in enumerate(school_map):
                    file.write(f"[floor{idx+1}]\n")
                    for row in floor:
                        file.write(",".join(row) + "\n")
                    file.write("\n")
                file.write("\n")
    # answer = breadth_first_search(school_map)
    # if answer:
    #     d, path = answer
    #     print(f"Shortest path length: {d}")
    #     print("Path:")
    #     for x, y, keyset in path:
    #         print(f"({x}, {y}, {bin(keyset)})")
    # else:
    #     print("No solution.")

if __name__ == "__main__":
    main()
