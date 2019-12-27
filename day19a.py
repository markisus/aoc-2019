from day9a import *

with open("day19.txt") as f:
    memory_list = [int(s.strip()) for s in f.readline().split(",")]

memory = make_memory(memory_list)

def get_bit(x,y):
    computer = IntCodeComputer(memory.copy())
    computer.keep_stepping()
    computer.push_input(x)
    computer.push_input(y)
    computer.keep_stepping()
    out = computer.pop_output()
    return out
    
if __name__ == '__main__':
    num_ones = 0
    for y in range(50):
        for x in range(50):
            out = get_bit(x,y)
            if out == 0:
                print(" ", end="")
            else:
                print("#", end="")
            num_ones += out
        print("")

    print(num_ones)

