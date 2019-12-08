def check_num(num):
    str_num = str(num)
    has_adjacent = False
    last_char = str_num[0]
    chain_length = 0
    for char in str_num[1:]:
        if last_char == char:
            chain_length += 1
        else:
            # chain has ended
            if chain_length == 1:
                has_adjacent = True
            # reset chain counter
            chain_length = 0

        if char < last_char:
            return False
        last_char = char

    has_adjacent = has_adjacent or chain_length == 1
    return has_adjacent

if __name__ == "__main__":
    count = 0
    for i in range(158126, 624574):
        if check_num(i):
            # print("pass", i)
            count += 1
    print(count)
    
