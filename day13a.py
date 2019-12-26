from day9a import *

with open("day13.txt") as f:
    memory_list = [int(s.strip()) for s in f.readline().split(",")]

memory = make_memory(memory_list)

if __name__ == '__main__':
    output = deque()
    run_program(memory, deque(), output)
    num_block_tiles = 0
    for tile in list(output)[2::3]:
        if tile == 2:
            num_block_tiles += 1

    print(num_block_tiles)

