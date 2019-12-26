from day16a import *


digits = digits * 10000

offset_list = digits[:7]
print("Offset list", offset_list)

power = 1
offset = 0
for p in range(7):
    offset += offset_list[6-p]*power
    power *= 10
print("Offset", offset)

assert offset >= len(digits)/2, "Trick only works if offset is big enough"

digits = digits[offset:]
for iteration in range(100):
    if ((iteration+1) % 10) == 0:
        print("Iteration", iteration+1)
    total = 0
    for i in reversed(range(len(digits))):
        total += digits[i]
        total = total % 10
        digits[i] = total

print(digits[:8])
