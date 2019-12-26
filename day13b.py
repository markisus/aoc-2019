from day13a import *

memory[0] = 2

computer = IntCodeComputer(memory)
score = 0
screen = {}
minx = float('inf')
miny = float('inf')
maxx = -float('inf')
maxy = -float('inf')

last_ox = None

while not computer.done():
    computer.keep_stepping()
    while computer.output_len():
        x = computer.pop_output()
        y = computer.pop_output()
        t = computer.pop_output()

        if x == -1 and y == 0:
            score = t
            continue

        screen[(x,y)] = t
        minx = min(minx,x)
        maxx = max(maxx,x)
        miny = min(miny,y)
        maxy = max(maxy,y)

    paddlex = 0
    ballx = 0
    print("Score: {}".format(score))
    for y in range(int(miny), int(maxy)+1):
        print ("{:03d}".format(y), end="")
        for x in range(int(minx), int(maxx)+1):
            t = screen.get((x,y), None)
            if t == 1:
                print("#", end="")
            elif t == 2:
                print("B", end="")
            elif t == 3:
                print("-", end="")
                paddlex = x
            elif t == 4:
                print("O", end="")
                ballx = x
            else:
                print(" ", end="")
        print()

    # control = input("<-a/s/d->, e=auto")
    control = "e"
    if control == "a":
        computer.push_input(-1)
    elif control == "d":
        computer.push_input(1)
    elif control == "e":
        if ballx == paddlex:
            computer.push_input(0)
        elif ballx < paddlex:
            computer.push_input(-1)
        else:
            computer.push_input(1)
    else:
        computer.push_input(0)

print("Final Score:", score)
