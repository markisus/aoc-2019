from day9a import *
from collections import deque

with open("day15.txt") as f:
    memory_list = [int(s.strip()) for s in f.readline().split(",")]

memory = make_memory(memory_list)

explored_tiles = set()
explored_tiles.add((0,0))
walls = set()
droid_frontier = deque()
droid = IntCodeComputer(memory.copy())
droid_frontier.append((
    0, # x
    0, # y
    0, # num_steps
    droid
))
droid_positions = {}
directions = [(0, -1), # north
              (0, 1), # south
              (-1, 0), # west
              (1, 0),
] # east
while droid_frontier:
    frontier_elem = droid_frontier.popleft()
    x, y, num_steps, droid  = frontier_elem
    for i, direction in enumerate(directions):

        dx, dy = direction
        target = (x + dx, y + dy)
        if target in explored_tiles:
            continue
        explored_tiles.add(target)

        droid_copy = droid.copy()
        droid_copy.push_input(i + 1)
        droid_copy.keep_stepping()
        out = droid_copy.pop_output()

        if out == 0:
            walls.add(target)
            pass
        elif out == 1:
            # movement succeeded
            droid_frontier.append((
                target[0],
                target[1],
                num_steps + 1,
                droid_copy))
        elif out == 2:
            print("Oxygen found:", num_steps+1)
            oxygen_droid = droid_copy


droid_frontier.clear()
droid_frontier.append((
    target[0], # x
    target[1], # y
    0, # num_steps
    oxygen_droid
))
explored_tiles.clear()

diameter = 0
while droid_frontier:
    frontier_elem = droid_frontier.popleft()
    x, y, num_steps, droid  = frontier_elem
    diameter = max(diameter, num_steps)

    for i, direction in enumerate(directions):
        dx, dy = direction
        target = (x + dx, y + dy)
        if target in explored_tiles:
            continue
        explored_tiles.add(target)

        droid_copy = droid.copy()
        droid_copy.push_input(i + 1)
        droid_copy.keep_stepping()
        out = droid_copy.pop_output()

        if out == 0:
            walls.add(target)
            pass
        elif out == 1 or out == 2:
            # movement succeeded
            droid_frontier.append((
                target[0],
                target[1],
                num_steps + 1,
                droid_copy))
        else:
            raise RuntimeError("Unexpected output", out)
print(diameter)        
