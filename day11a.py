from day9a import *
from collections import defaultdict

canvas_state = defaultdict(lambda: 0);

output_stream = deque()
input_stream = deque()

cur_x = 0
cur_y = 0

# pointing up
dir_x = 0
dir_y = 1

# load program
with open("day11.txt") as f:
    memory_list = [int(s.strip()) for s in f.readline().split(",")]
memory = make_memory(memory_list)

instruction_ptr = 0

if __name__ == "__main__":
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

    print(len(canvas_state))

        
