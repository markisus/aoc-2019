from day10a import *
from collections import defaultdict
from itertools import cycle, chain

# group asteroid deltas by their rays to the best_ab
asteroids_to_vaporize = defaultdict(list)
for a, b in asteroids:
    da = a - best_ab[0]
    db = b - best_ab[1]
    if da == 0 and db == 0:
        # self asteroid is not vaporizable
        continue
    asteroids_to_vaporize[normalize(da, db)].append((da, db))

# revese sort them by closeness to best_ab
for asteroids in asteroids_to_vaporize.values():
    asteroids.sort(key = lambda w: -w[0]**2 - w[1]**2)

# come up with an iteration order for rays
first_half = sorted(((a,b) for a,b in asteroids_to_vaporize.keys() if a >= 0),
                    key = lambda w: w[1] / (w[0]**2 + w[1]**2)**0.5)
second_half = sorted(((a,b) for a,b in asteroids_to_vaporize.keys() if a < 0),
                     key = lambda w: -w[1] / (w[0]**2 + w[1]**2)**0.5)
ray_order = cycle(chain(first_half, second_half))

num_asteroids_vaporized = 0
while num_asteroids_vaporized < 200:
    ray = next(ray_order)
    asteroids = asteroids_to_vaporize[ray]
    if asteroids:
        last_vaporized = asteroids.pop()
        num_asteroids_vaporized += 1

# convert last_vaporized to absolute coordinates
a = last_vaporized[0] + best_ab[0]
b = last_vaporized[1] + best_ab[1]
print(a, b)
print("Answer", a*100 + b)
    
    

