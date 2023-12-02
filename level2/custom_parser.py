import sys
import re

def is_valid_token(s):
    pattern = r"^(0|-1|A\d+|T\d+|D\d+|K\d+)$"
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
        for line in file:
            arr = []
            for cell in line.strip().split(","):
                s = cell.strip()
                if not is_valid_token(s):
                    sys.exit(f"At line: {line}\nInvalid token: {s}")
                arr.append(s)
            if len(arr) != M:
                sys.exit(f"Invalid number of tokens in line: {line}")
            location.append(arr)
        if len(location) != N:
            sys.exit(f"Invalid number of lines: {len(location)}")
        return location


