from day19a import *


start_x = 17
start_y = 30

# x = start_x
# y = start_y

x = start_x
y = start_y
while True:
    while True:
        out = get_bit(x,y)
        if out == 0:
            print(" ", end="")
        else:
            print("#", end="")
        if out == True:
            # first out=1 encountered
            # check if it can fit a 100,100 square
            minx = x 
            maxx = x + 99
            miny = y - 99
            maxy = y

            print("y =",y)

            if miny >= 0 and \
               get_bit(minx,miny) and \
               get_bit(minx,maxy) and \
               get_bit(maxx,maxy) and \
               get_bit(maxx,miny):
                print("Square success",minx,miny,maxx,maxy)
                print(minx*10000 + miny)
                exit(0)
            break
        else:
            x += 1
    y += 1
    print("")
