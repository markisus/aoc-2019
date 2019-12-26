from day11a import *

input_stream.append(1)

max_x = 0
min_x = 0
max_y = 0
min_y = 0
while instruction_ptr >= 0:
    # if dir_x == 1:
    #     print(">")
    #     assert dir_y == 0
    # if dir_y == 1:
    #     print("^")
    #     assert dir_x == 0
    # if dir_y == -1:
    #     print("v")
    #     assert dir_x == 0
    # if dir_x == -1:
    #     print("<")
    #     assert dir_y == 0
    # print("Current square", cur_x, cur_y)

    color = canvas_state[(cur_x, cur_y)]
    input_stream.append(color)

    while len(output_stream) < 2 and instruction_ptr >= 0:
        instruction_ptr = step_program(instruction_ptr, memory, input_stream, output_stream)

    if instruction_ptr < 0:
        break

    new_color = output_stream.popleft()
    direction = output_stream.popleft()

    # color the canvas
    # print("Painting")
    canvas_state[(cur_x, cur_y)] = new_color

    # then turn
    # print("Moving")
    if direction == 0:
        # left turn 90 degrees
        new_x = -dir_y
        new_y = dir_x
    elif direction == 1:
        # turn right 90 degrees
        new_x = dir_y
        new_y = -dir_x
    else:
        print("Unexpected direction", direction)
        raise RuntimeError("Crash")
    dir_x = new_x
    dir_y = new_y
    # then take a step
    cur_x += dir_x
    cur_y += dir_y

    max_x = max(max_x, cur_x)
    min_x = min(min_x, cur_x)
    max_y = max(max_y, cur_y)
    min_y = min(min_y, cur_y)

print("Max x", max_x)
print("Min x", min_x)
print("Max y", max_y)
print("Min y", min_y)

print("")

for y in list(range(min_y, max_y + 1))[::-1]:
    # y = max_y + 1 - y
    for x in range(min_x, max_x + 1):
        if canvas_state[(x, y)] == 1:
            print("#", end = "")
        else:
            print(" ", end = "")
    print("")





