


"""

Rule of thumb:
- Each agent, at its current position, consider adjacent agents (if any) to be present (except for A1), and 
ignore agents elsewhere (if any), in order to find the best path to its target.
  + If the next move on the best path is blocked by A1, the agent stands still (to wait for A1 to move).
  + If the current agent is A1, the next best move is on a target of another agent, and that corresponding agent is
  one step away from its target, the current agent finds another way.
  + If the next best move is available, move.
  + If there is no path to the target, move to an adjacent empty cell that is nearest to the target in terms of
    Manhattan distance, but not the target of another agent that is one step away from its target.
  + If there is no adjacent empty cell, stand still (to wait for an adjacent cell to become empty).

"""
import copy
import sys
from queue import Queue
from level4.custom_parser import read_input

from level4.utils import extract_agents, extract_targets, find_key, find_next_moves_2D, find_next_moves_3D, init_ndarray, update_targets



INF = 1000000000


def breadth_first_search(initial_map, num_keys, agent_number, positions, targets, keysets):
    initial_target = targets[agent_number]
    initial_pos = positions[agent_number]
    initial_keyset = keysets[agent_number]
    school_map = copy.deepcopy(initial_map)
    D = len(school_map)
    N = len(school_map[0])
    M = len(school_map[0][0])
    # print(f"agent: {agent_number}, keyset: {bin(initial_keyset)}")
    # turn adjacent agents (if any) into walls
    for next_x, next_y in find_next_moves_2D(school_map[initial_pos[0]], initial_pos[1], initial_pos[2]):
        for i, (f, x, y) in positions.items():
            if f != initial_pos[0]:
                continue
            if i == agent_number:
                continue
            if (next_x, next_y) == (x, y):
                if i != 1:
                    # view the agent as present and need to avoid
                    school_map[f][next_x][next_y] = "-1"
                else:
                    # if A1 is stuck, the current agent should move to allow A1 to move
                    A1_stuck = True
                    for adj_f, adj_x, adj_y in find_next_moves_3D(school_map, initial_pos[0], next_x, next_y):
                        if (adj_f, adj_x, adj_y) in positions.values():
                            continue
                        if school_map[adj_f][adj_x][adj_y][0] == "D" and school_map[adj_f][adj_x][adj_y][1] != "O":
                            # check if the key is available
                            num = int(school_map[adj_f][adj_x][adj_y][1:])
                            # this door has no corresponding key
                            if num > num_keys:
                                continue
                            # this door has a corresponding key, but the key is not available
                            if keysets[1] & (1 << (num - 1)) == 0:
                                continue
                        A1_stuck = False
                    if A1_stuck:
                        school_map[f][next_x][next_y] = "-1"

    K = 1 << num_keys
    start = (initial_pos[0], initial_pos[1], initial_pos[2], initial_keyset)
    Q = Queue()
    Q.put(start)
    trace = init_ndarray((D, N, M, K), (-1, -1, -1, -1))
    dist = init_ndarray((D, N, M, K), INF)
    dist[start[0]][start[1]][start[2]][start[3]] = 0
    goal = (-1, -1, -1, -1)
    while Q.qsize() > 0:
        if goal != (-1, -1, -1, -1):
            break
        f, x, y, keyset = Q.get()
        # print(f"Expanding ({f}, {x}, {y}, {bin(keyset)})")
        for next_f, next_x, next_y in find_next_moves_3D(school_map, f, x, y):
            # if school_map[next_f][next_x][next_y][0] == "A" and int(school_map[next_f][next_x][next_y][1:]) != agent_number:
            #     continue
            if school_map[next_f][next_x][next_y][0] == "D" and school_map[next_f][next_x][next_y][1] != "O":
                # check if the key is available
                num = int(school_map[next_f][next_x][next_y][1:])
                # this door has no corresponding key
                if num > num_keys:
                    continue
                # this door has a corresponding key, but the key is not available
                if keyset & (1 << (num - 1)) == 0:
                    continue
            # print(f"Considering next move ({next_f}, {next_x}, {next_y})")
            new_keyset = keyset
            # print(f"keyset = {bin(keyset)} & new_keyset = {bin(new_keyset)}")
            if school_map[next_f][next_x][next_y][0] == "K":
                new_keyset |= (1 << (int(school_map[next_f][next_x][next_y][1:]) - 1))
            if dist[next_f][next_x][next_y][new_keyset] != INF:
                continue
            dist[next_f][next_x][next_y][new_keyset] = dist[f][x][y][keyset] + 1
            trace[next_f][next_x][next_y][new_keyset] = (f, x, y, keyset)
            # the destination is here!
            if (next_f, next_x, next_y) == initial_target:
                goal = (next_f, next_x, next_y, new_keyset)
                break
            Q.put((next_f, next_x, next_y, new_keyset))
    # print(f"Goal found: {goal}")
    if goal == (-1, -1, -1, -1):
        # there is no path to the target, so we move to an adjacent empty cell that is nearest to the target
        available_moves = []
        current_f = initial_pos[0]
        # we prioritize the cells that are not targets of other agents
        for next_x, next_y in find_next_moves_2D(school_map[current_f], initial_pos[1], initial_pos[2]):
            # an adjacent cell is empty
            if school_map[current_f][next_x][next_y] == "0" and (
            current_f, next_x, next_y) not in positions.values() and (
            current_f, next_x, next_y) not in targets.values():
                available_moves.append((next_x, next_y))
            # an adjacent cell is a key
            elif school_map[current_f][next_x][next_y][0] == "K":
                available_moves.append((next_x, next_y))
            # an adjacent cell is a door, and the key is available
            elif school_map[current_f][next_x][next_y][0] == "D" and school_map[current_f][next_x][next_y][
                1] != "O" and ((1 << (int(school_map[current_f][next_x][next_y][1:]) - 1)) & initial_keyset) != 0:
                available_moves.append((next_x, next_y))
        # if there is no such cell, we now consider cells that are targets of other agents
        if len(available_moves) == 0:
            for next_x, next_y in find_next_moves_2D(school_map[current_f], initial_pos[1], initial_pos[2]):
                # an adjacent cell is a target of another agent
                if (current_f, next_x, next_y) in targets.values():
                    agent = find_key(targets, (current_f, next_x, next_y))
                    assert agent is not None, f"Error: The cell ({current_f}, {next_x}, {next_y}) is a target, but no agent is assigned to it"
                    (a_f, a_x, a_y) = positions[agent]
                    # if abs(a_f - current_f) + abs(a_x - next_x) + abs(a_y - next_y) > 2:
                    if abs(a_f - current_f) > 1 or abs(a_x - next_x) > 1 or abs(a_y - next_y) > 1:
                        # that agent is sufficiently far from its target for the current agent to move to the target
                        available_moves.append((next_x, next_y))

        # print(f"available moves: {available_moves}")
        if len(available_moves) == 0:
            # stand still and wait for an adjacent cell to become empty
            return
        next_move = (INF, 0, 0)
        for next_x, next_y in available_moves:
            if abs(next_x - initial_target[1]) + abs(next_y - initial_target[2]) < next_move[0]:
                next_move = (abs(next_x - initial_target[1]) + abs(next_y - initial_target[2]), next_x, next_y)
        # print(f"next move: ({initial_pos[0], next_move[1], next_move[2]})")
        positions[agent_number] = (initial_pos[0], next_move[1], next_move[2])
        if school_map[initial_pos[0]][next_move[1]][next_move[2]][0] == "K":
            keysets[agent_number] |= (1 << (int(school_map[initial_pos[0]][next_move[1]][next_move[2]][1:]) - 1))
        return

    else:
        while goal != (-1, -1, -1, -1) and trace[goal[0]][goal[1]][goal[2]][goal[3]] != start:
            goal = trace[goal[0]][goal[1]][goal[2]][goal[3]]
        # print(f"next move: {goal}")
        if (goal[0], goal[1], goal[2]) == positions[1]:
            # stand still to wait for A1 to move
            return
            # move to the next cell
        # print(f"move from {start} to {goal}")
        positions[agent_number] = (goal[0], goal[1], goal[2])
        keysets[agent_number] = goal[3]
        if positions[agent_number] == targets[agent_number]:
            # the agent has reached its target
            del targets[agent_number]
        return


def run_simulation(original_map):
    school_map = copy.deepcopy(original_map)
    agents = extract_agents(school_map)
    agents_log = {}
    for a, coor in agents.items():
        agents_log[a] = [coor]
    targets = extract_targets(school_map)
    targets_log = {}
    for a, coor in targets.items():
        targets_log[a] = [coor]
    D = len(school_map)
    N = len(school_map[0])
    M = len(school_map[0][0])
    num_keys = 0
    # assuming that initially, agents and keys are on the first floor
    for f in range(D):
        for i in range(N):
            for j in range(M):
                if school_map[f][i][j][0] == "K":
                    num_keys = max(num_keys, int(school_map[f][i][j][1:]))

    keysets = {}
    for i in range(1, len(agents) + 1):
        keysets[i] = 0
    max_steps = 1000
    while True:
        if max_steps == 0:
            return agents_log, targets_log
        make_progress = False
        for i in range(1, len(agents) + 1):
            # print(f"At {i}")
            old_pos = agents[i]
            breadth_first_search(school_map, num_keys, i, agents, targets, keysets)
            agents_log[i].append(agents[i])
            # print(f"After bfs:")
            # print_map(get_full_map(school_map, agents, targets))
            if agents[i] != old_pos:
                # print("Make progress")
                make_progress = True
            finish_game = False
            if len(targets) < len(agents):
                # print("Update targets")
                finish_game = update_targets(school_map, agents, targets)
                if i in targets:
                    targets_log[i].append(targets[i])
            # print(f"agents: {agents}")
            # print(f"targets: {targets}")
            # print_map(get_full_map(school_map, agents, targets))
            if finish_game:
                # A1 reached T1
                return agents_log, targets_log

        if not make_progress:
            return agents_log, targets_log
        max_steps -= 1


def main():
    if len(sys.argv) < 2:
        sys.exit("Please enter the input file name.")
    elif len(sys.argv) > 2:
        sys.exit("Too many arguments.")
    school_map = read_input(sys.argv[1])
    positions, targets = run_simulation(school_map)
    with open("output.txt", "w") as file:
        num_agents = len(positions)
        for i in range(1, num_agents + 1):
            file.write(f"AGENT {i}:\n")
            file.write(f"List of positions: {positions[i]}\n")
            file.write(f"List of targets: {targets[i]}\n")


if __name__ == "__main__":
    main()