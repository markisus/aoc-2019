def check_num(num):
    str_num = str(num)
    has_adjacent = False
    last_char = str_num[0]
    for char in str_num[1:]:
        if last_char == char:
            has_adjacent = True
        if char < last_char:
            return False
        last_char = char
    return has_adjacent

if __name__ == "__main__":
    count = 0
    for i in range(158126, 624574):
        if check_num(i):
            # print("pass", i)
            count += 1
    print(count)
    
