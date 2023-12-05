import sys
import re


def is_valid_token(s):
    pattern = r"^(0|-1|A\d+|T\d+|D\d+|K\d+|UP|DO)$"
    if re.match(pattern, s):
        return True
    else:
        return False


def read_input(filename):
    with open(filename, "r") as file:
        try:
            N, M = tuple(map(int, file.readline().strip().split(",")))
        except ValueError:
            sys.exit("The first line should contain two positive integers, separated by a comma.")
        location = []
        floor = 1

        while True:
            line = file.readline().strip()
            if not line:
                break
            if not line.startswith(f"[floor{floor}]"):
                sys.exit(f"Invalid format: expected [floor{floor}] but got {line}")

            floor_location = []
            for i in range(N):
                line = file.readline().strip()
                if not line:
                    sys.exit(f"At floor {floor}, line {i} (zero-indexed) is empty.")
                arr = []
                for cell in line.split(","):
                    s = cell.strip()
                    if not is_valid_token(s):
                        sys.exit(f"At line: {line}\nInvalid token: {s}")
                    arr.append(s)
                if len(arr) != M:
                    sys.exit(f"Invalid number of tokens in line: {line}")
                floor_location.append(arr)
            if len(floor_location) != N:
                sys.exit(f"Invalid number of lines for floor {floor}")

            location.append(floor_location)
            floor += 1

        return location
