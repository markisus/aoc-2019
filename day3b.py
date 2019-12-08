from day3a import *

# data = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
# U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""

# modified traverse path
def traverse(path):
    total_steps = 0
    current_x = 0
    current_y = 0
    positions = dict()
    for segment in path:
        direction, steps = segment
        if direction == "U":
            delta_x, delta_y = (0, 1)
        elif direction == "D":
            delta_x, delta_y = (0, -1)
        elif direction == "L":
            delta_x, delta_y = (-1, 0)
        elif direction == "R":
            delta_x, delta_y = (1, 0)
        for _ in range(steps):
            total_steps += 1
            current_x += delta_x
            current_y += delta_y
            if (current_x, current_y) not in positions:
                positions[(current_x, current_y)] = total_steps
    return positions

l1, l2 = data.split("\n")
traversed_a, traversed_b = (traverse(parse_line(l)) for l in data.split("\n"))

min_cost = float("inf")
for k, v in traversed_a.items():
    cost = v + traversed_b.get(k, float("inf"))
    if cost < min_cost:
        min_cost = cost

print("Answer:", min_cost)
