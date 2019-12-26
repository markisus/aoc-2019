from itertools import cycle

with open("day16.txt") as f:
    for l in f:
        digits = list(int(i) for i in l.strip())

# digits = [1,2,3,4,5,6,7,8] # example

base_pattern = [0, 1, 0, -1]

def make_base_pattern(iteration):
    pattern = []
    for d in base_pattern:
        for i in range(iteration):
            pattern.append(d)
    return pattern

def get_output_digit(input_digits, output_idx):
    pattern = make_base_pattern(output_idx + 1)
    repeated_pattern = cycle(pattern)
    next(repeated_pattern) # discard the first 
    result = 0
    for d in digits:
        multiplier = next(repeated_pattern)
        result += d * multiplier
    result = abs(result) % 10
    return result

def iterate(input_digits):
    output_digits = []
    for idx in range(len(input_digits)):
        output_digit = get_output_digit(input_digits, idx)
        output_digits.append(output_digit)
    return output_digits

if __name__ == '__main__':
    for phase in range(100):
        digits = iterate(digits)
        if ((phase+1) % 10 == 0):
            print("Phase",phase,"digits",digits)

    print(digits[:8])
