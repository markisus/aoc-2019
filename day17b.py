from day17a import *

computer_1 = IntCodeComputer(memory.copy())

tile_locations = set()
while not computer_1.done():
    computer_1.keep_stepping()
    x = 0
    y = 0
    while computer_1.output_len():        
        tile = chr(computer_1.pop_output())
        # print(tile, end="")
        if tile == "\n":
            y += 1
            x = 0
            continue
        if tile == "#":
            tile_locations.add((x,y))
        elif tile == "^":
            start_location = (x,y)
        x += 1

print("Start location", start_location)

def num_neighbors(tile_location):
    x, y = tile_location
    num_neighbors = 0
    num_neighbors += int((x+1,y) in tile_locations)
    num_neighbors += int((x-1,y) in tile_locations)
    num_neighbors += int((x,y+1) in tile_locations)
    num_neighbors += int((x,y-1) in tile_locations)
    return num_neighbors

for tile_location in tile_locations:
    x,y = tile_location
    if num_neighbors(tile_location) == 1 and y > 20:
        end_location = tile_location
        break

print("End location", end_location)

path = []
curr_location = start_location
prev_location = curr_location
curr_direction = "^"
while curr_location != end_location:
    curr_x, curr_y = curr_location
    if curr_direction == "^":
        next_location = (curr_x, curr_y - 1)
    if curr_direction == "<":
        next_location = (curr_x - 1, curr_y)
    if curr_direction == ">":
        next_location = (curr_x + 1, curr_y)
    if curr_direction == "v":
        next_location = (curr_x, curr_y + 1)

    if next_location in tile_locations and next_location != prev_location:
        prev_location = curr_location
        curr_location = next_location
        path.append(1)
    else:
        if curr_direction == "^":
            curr_direction = ">"
        elif curr_direction == ">":
            curr_direction = "v"
        elif curr_direction == "v":
            curr_direction = "<"
        elif curr_direction == "<":
            curr_direction = "^"
        path.append("R")
# print(path)

def collapse_ones(path):
    prev = None
    path_0 = []
    one_count = 0
    for s in path:
        if s != 1 and prev == 1:
            path_0.append(one_count)
            one_count = 0
        if s == 1:
            one_count += 1
        else:
            path_0.append(s)
        prev = s
    if s == 1:
        path_0.append(one_count)
    return path_0

# compress path
# part 1, compress three R's into an L
path_1 = []
R_count = 0
prev = None
for s in path:
    if s != "R" and prev == "R":
        if R_count == 3:
            path_1.append("L")
        else:
            for _ in range(R_count):
                path_1.append("R")
        R_count = 0
    if s == "R":
        R_count += 1
    else:
        path_1.append(s)
    prev = s
if s == "R":
    if R_count == 3:
        path_1.append("L")
    else:
        for _ in range(R_count):
            path_1.append("R")
    R_count = 0
path = path_1
# print("path",path)

def get_path_to_end(path, starting_idx, 
                  len_a,
                  len_b, 
                  len_c,
                  a = None,
                  b = None,
                  c = None,
                  ascii_path = []):

    if len(ascii_path) > 20:
        return False

    if starting_idx == len(path):
        return (ascii_path, 
                collapse_ones(a), 
                collapse_ones(b),
                collapse_ones(c))
                

    if a == None:
        a = path[starting_idx:starting_idx+len_a]
        if len(a) != len_a:
            return False
    if a == path[starting_idx:starting_idx+len_a]:
        answer = get_path_to_end(path, starting_idx+len_a,
                     len_a, len_b, len_c,
                     a, b, c, ascii_path + ["A"])
        if answer:
            return answer

    if b == None:
        b = path[starting_idx:starting_idx+len_b]
        if len(b) != len_b:
            return False
    if a == b:
        return False
    if b == path[starting_idx:starting_idx+len_b]:
        answer = get_path_to_end(path, starting_idx+len_b,
                     len_a, len_b, len_c,
                     a, b, c, ascii_path + ["B"])
        if answer:
            return answer

    if c == None:
        c = path[starting_idx:starting_idx+len_c]
        if len(c) != len_c:
            return False
    if a == c:
        return False
    if b == c:
        return False
    if c == path[starting_idx:starting_idx+len_c]:
        answer = get_path_to_end(path, starting_idx+len_c,
                     len_a, len_b, len_c,
                     a, b, c, ascii_path + ["C"])
        if answer:
            return answer

    return False

answer = None
for a_len in range(1,50):
    if answer: 
        break
    for b_len in range(1,50):
        if answer:
            break
        for c_len in range(1,50):
            answer = get_path_to_end(path, 0, a_len, b_len, c_len)
            if answer:
                print(answer)
                break

assert answer, "Compression failed"

def step_and_dump(computer):
    computer.keep_stepping()
    last = None
    while computer.output_len():        
        last = computer.pop_output()
        tile = chr(last)
        print(tile, end="")
    print(last)

def to_ascii_string(ascii_list):
    ascii_list = [str(s) for s in ascii_list]
    ascii_string = ",".join(ascii_list)
    return ascii_string

def push_ascii(computer, ascii_list):
    print("Got", ascii_list)
    ascii_string = to_ascii_string(ascii_list)
    print("Pushing", ascii_string)
    codes = [ord(c) for c in ascii_string]
    codes.append(ord("\n"))
    for code in codes:
        computer.push_input(code)

memory_cpy = memory.copy()
memory_cpy[0] = 2
computer_2 = IntCodeComputer(memory_cpy)
step_and_dump(computer_2)
push_ascii(computer_2, answer[0])
step_and_dump(computer_2)
push_ascii(computer_2, answer[1])
step_and_dump(computer_2)
push_ascii(computer_2, answer[2])
step_and_dump(computer_2)
push_ascii(computer_2, answer[3])
step_and_dump(computer_2)
push_ascii(computer_2, "n")
step_and_dump(computer_2)


