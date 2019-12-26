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
            print("Done:", num_steps+1)
            exit(0)
        else:
            print("Error!")
            exit(-1)

    min_x = min(pt[0] for pt in explored_tiles)
    min_y = min(pt[1] for pt in explored_tiles)
    max_x = max(pt[0] for pt in explored_tiles)
    max_y = max(pt[1] for pt in explored_tiles)
    # print(min_x,max_x,min_y,max_y)
    print()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if x == 0 and y == 0:
                print("*", end="")
            elif (x,y) in explored_tiles:
                if (x,y) in walls:
                    print("#", end="")
                else:
                    print(" ", end="")
            else:
                print("?", end="")
        print()


