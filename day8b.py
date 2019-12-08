from day8a import *

# data = list("0222112222120000")
# xd = 2
# yd = 2
# x_stride = 1
# y_stride = xd
# z_stride = yd * xd
# num_layers = 4

def get_idx(z, y, x):
    return z * z_stride + y * y_stride + x * x_stride

# output buffer
out = list("2"*(xd*yd))

for i in range(yd*xd):
    # Search until we get a non transparent
    for z in range(num_layers):
        pixel = data[z * z_stride + i]
        if pixel != "2":
            out[i] = pixel
            break

for y in range(yd):
    for x in range(xd):
        data = out[get_idx(0, y, x)]
        viz = " "
        if data == "1":
            viz = "#"
        print(viz, end = "")
    print()
