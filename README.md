# Move-Your-Step
Project 1 - CS420 Intro2AI - Term I 2023-2024

**TEST CASE GENERATION:**
parameters: (agents, keys, floors, N, M)
where:
- agents: number of agents in the test case
- keys: number of keys in the test case
- floors: number of floors in the test case
- N: number of rows in the matrix
- M: number of columns in the matrix

Constraints:
keys <= 10
N, M <= 200

**Level 1:**
- agents = 1
- keys = 0
- floors = 1

**Level 2:**
- agents = 1
- keys <= 10
- floors = 1

**Level 3:**
- agents = 1
- keys <= 10
- floors <= 10

**Level 4:**
- agents <= 10
- keys <= 10
- floors <= 10


**Anomalies:**
(1) Some doors don't have corresponding keys.
(2) Some keys are fully surrounded by obstacles that cannot be obtained.
(3) We need to open door i to get key j, but we also need to open door j to get key i.
(4) There is not path to the target cell.

**Normalization algorithm**:
```
keyset = []
for:
    doors that don't have corresponding keys in keyset are as obstacles
    doors that have corresponding keys in keyset become blank
    go to all cells that are reachable
    if no progress is made:
        break
all unreachable cells are turned to obstacles (even the target cell)
re-number keys and doors
```

Time and memory complexity: O(NM)
Results:
- No keys are unachievable.
- No doors cannot be opened.
- There is at least one path from the start cell to the target cell.