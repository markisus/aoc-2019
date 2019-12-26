from day9a import *

with open("day17.txt") as f:
    memory_list = [int(s.strip()) for s in f.readline().split(",")]

memory = make_memory(memory_list)
computer = IntCodeComputer(memory)

if __name__ == '__main__':
    tile_locations = set()
    while not computer.done():
        computer.keep_stepping()
        x = 0
        y = 0
        while computer.output_len():        
            tile = chr(computer.pop_output())
            print(tile, end="")
            if tile == "\n":
                y += 1
                x = 0
                continue
            if tile == "#":
                tile_locations.add((x,y))
            x += 1



    param = 0
    for tile_location in tile_locations:
        x,y = tile_location
        if (x+1,y) in tile_locations \
           and (x-1,y) in tile_locations \
           and (x,y-1) in tile_locations \
           and (x,y+1) in tile_locations:
            print("intersection at",x,y)
            param += x*y

    print(param)

