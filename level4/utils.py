import copy
import random


def find_next_moves_2D(school_map, x, y):
    N = len(school_map)
    M = len(school_map[0])
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    next_moves = []
    for x_offset, y_offset in moves:
        next_x, next_y = x + x_offset, y + y_offset
        # invalid next cell
        if next_x < 0 or next_x >= N or next_y < 0 or next_y >= M:
            continue
        # next cell is a wall
        if school_map[next_x][next_y] == "-1":
            continue
        # in case of a diagonal move
        if abs(next_x - x) + abs(next_y - y) == 2:
            # check if neighboring cells are walls or other agents
            valid = True
            for u in [min(x, next_x), max(x, next_x)]:
                for v in [min(y, next_y), max(y, next_y)]:
                    if school_map[u][v] == "-1":
                        valid = False
                        break
            if not valid:
                continue
        next_moves.append((next_x, next_y))
    return next_moves

def find_next_moves_3D(school_map, f, x, y):
    D = len(school_map)
    N = len(school_map[0])
    M = len(school_map[0][0])
    moves = [(0, 0, 1), (0, 1, 0), (0, 0, -1), (0, -1, 0), (0, -1, -1), (0, -1, 1), (0, 1, -1), (0, 1, 1)]
    if school_map[f][x][y] == "UP":
        moves.append((1, 0, 0))
    elif school_map[f][x][y] == "DO":
        moves.append((-1, 0, 0))
    next_moves = []
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
        next_moves.append((next_f, next_x, next_y))
    return next_moves

def init_ndarray(shape, val):
    if len(shape) == 1:
        return [val for _ in range(shape[0])]
    else:
        return [init_ndarray(shape[1:], val) for _ in range(shape[0])]

def find_key(dic, val):
    for key, value in dic.items():
        if value == val:
            return key
    return None

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

def get_full_map(school_map, agents, targets):
    #print(f"Getting full map with agents: {agents} and targets: {targets}")
    full_map = copy.deepcopy(school_map)
    for a, (f, x, y) in targets.items():
        full_map[f][x][y] = "T" + str(a)
    for a, (f, x, y) in agents.items():
        full_map[f][x][y] = "A" + str(a)
    return full_map

def extract_targets(school_map):
    D = len(school_map)
    N = len(school_map[0])
    M = len(school_map[0][0])
    targets = {}
    for f in range(D):
        for i in range(N):
            for j in range(M):
                if school_map[f][i][j][0] == "T":
                    targets[int(school_map[f][i][j][1:])] = (f, i, j)
                    school_map[f][i][j] = "0"
    return targets

def extract_agents(school_map):
    D = len(school_map)
    N = len(school_map[0])
    M = len(school_map[0][0])
    agents = {}
    for f in range(D):
        for i in range(N):
            for j in range(M):
                if school_map[f][i][j][0] == "A":
                    agents[int(school_map[f][i][j][1:])] = (f, i, j)
                    school_map[f][i][j] = "0"
    return agents

def update_targets(school_map, agents, targets):
    D = len(school_map)
    N = len(school_map[0])
    M = len(school_map[0][0])
    available_cells = []
    for f in range(D):
        for i in range(N):
            for j in range(M):
                if school_map[f][i][j] == "0" and (f, i, j) not in targets.values() and (f, i, j) not in agents.values():
                    available_cells.append((f, i, j))
    for a in range(1, len(agents) + 1):
        if a not in targets:
            if a == 1:
                return True
            f, i, j = random.choice(available_cells)
            available_cells.remove((f, i, j))
            targets[a] = (f, i, j)
    return False