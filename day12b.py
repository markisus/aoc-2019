from day12a import *
from day10a import gcd

def simulate_single_dimension_one_step(planet_states):
    """planet_states is a list where each item is of the form
    [position,velocity]
    """
    # apply gravity:
    for i in range(len(planet_states)):
        planet_a = planet_states[i]
        for j in range(i+1, len(planet_states)):
            planet_b = planet_states[j]
            
            pos_a = planet_a[0]
            pos_b = planet_b[0]
            if pos_a == pos_b:
                continue
            delta = 1 if pos_a < pos_b else -1
            planet_a[1] += delta
            planet_b[1] -= delta

    # apply velocity:
    for planet in planet_states:
        planet[0] += planet[1]

def hash_planet_states(planets):
    return tuple(tuple(p) for p in planets)

def get_period(planet_states):
    seen_states = {}
    i = 0
    original_hashed_state = hash_planet_states(planet_states)

    while True:
        i += 1
        simulate_single_dimension_one_step(planet_states)
        hashed_state = hash_planet_states(planet_states)
        if hashed_state == original_hashed_state:
            break
    return i

periods = []
for i in range(3):
    states = []
    for p in planet_states:
        states.append([p[i + 0], p[i + 3]])
    periods.append(get_period(states))


print("Periods", periods)

lcm_1 = periods[0]*periods[1]//gcd(periods[0], periods[1])
lcm_2 = lcm_1 * periods[2] // gcd(lcm_1, periods[2])

# LCM
print(lcm_2)
