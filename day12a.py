planet_states = []

with open("day12.txt") as f:
    for l in f:
        l = l[1:-2] # strip off < and >\n
        tokens = [t.strip() for t in l.split(",")]
        x = int(tokens[0][2:])
        y = int(tokens[1][2:])
        z = int(tokens[2][2:])
        planet_states.append([x, y, z, 0, 0, 0])

def simulate_one_step(planet_states):
    # apply gravity:
    for i in range(len(planet_states)):
        planet_a = planet_states[i]
        for j in range(i+1, len(planet_states)):
            planet_b = planet_states[j]
            
            for k in range(3):
                pos_a = planet_a[k]
                pos_b = planet_b[k]
                if pos_a == pos_b:
                    continue
                delta = 1 if pos_a < pos_b else -1
                planet_a[3 + k] += delta
                planet_b[3 + k] -= delta
                
    # apply velocity
    for planet in planet_states:
        for i in range(3):
            planet[i] += planet[3 + i]

def get_energy(planet):
    pe = sum(abs(c) for c in planet[:3])
    ke = sum(abs(c) for c in planet[3:])
    return pe*ke

if __name__ == '__main__':
    for i in range(1000):
        simulate_one_step(planet_states)
        # print(i+1, ":",planet_states)

    print(sum(get_energy(p) for p in planet_states))
