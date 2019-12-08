with open("day8.txt", "r") as f:
    data = f.readline().strip()

# 25 wide
# 6 tall

# ..... 25
# ..... 50
# .....
# ..... 25 * 6

yd = 6
xd = 25

x_stride = 1
y_stride = xd
z_stride = yd * xd

num_layers = len(data) // z_stride

if __name__ == "__main__":
    min_zero_digits = float("inf")
    best_layer = -1
    for layer in range(num_layers):
        zero_digits = 0
        for i in range(xd*yd):
            idx = i + layer * z_stride
            if data[idx] == "0":
                zero_digits += 1
        if zero_digits < min_zero_digits:
            min_zero_digits = zero_digits
            best_layer = layer

    num_ones = 0
    num_twos = 0
    for i in range(xd*yd):
        idx = i + best_layer * z_stride 
        if data[idx] == "1":
            num_ones += 1
        if data[idx] == "2":
            num_twos += 1

    print(num_ones * num_twos)
    
            
