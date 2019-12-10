def gcd(a, b):
    bigger = max(abs(a), abs(b))
    smaller = min(abs(a), abs(b))
    if smaller == 0:
        return bigger
    remainder = bigger % smaller
    while remainder != 0:
        bigger = smaller
        smaller = remainder
        remainder = bigger % smaller
    return smaller


# test gcd
# print("5, 3", gcd(5,3))
# print("10, 5", gcd(10,5))
# print("-30, 18", gcd(-30,18))
# print("30, 0", gcd(30,0))

def normalize(a, b):
    """factor out common factors, preserving sign"""
    if a == 0 and b == 0:
        return 0, 0
    gcd_ab = gcd(a,b)
    return a//gcd_ab, b//gcd_ab

# test normalize
# print("5, 3", normalize(5,3))
# print("10, 5", normalize(10,5))
# print("-30, 18", normalize(-30,18))
# print("30, 0", normalize(30,0))

asteroids = []
with open("day10.txt") as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line[:-1]): # skip newline
            if char == "#":
                asteroids.append((x,y))

best_ab = (0, 0)
best_visibles_num = 0
best_visibles = set() 

for a, b in asteroids:
    visibles = set()
    for other_a, other_b in asteroids:
        da = other_a - a
        db = other_b - b
        if da == 0 and db == 0:
            # self asteroid does not count as visible
            continue
        visibles.add(normalize(da, db))
    num_visibles = len(visibles)
    if num_visibles > best_visibles_num:
        best_visibles_num = num_visibles
        best_visibles = visibles
        best_ab = (a, b)

if __name__ == "__main__":
    print("Best", best_ab, "with visibles num:", best_visibles_num)
            
