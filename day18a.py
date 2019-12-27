from collections import defaultdict, deque

tunnel_map = defaultdict(lambda : "#")

min_x = 0
x = 0
y = 0

tunnel_keys = []

with open("day18.txt") as f:
    for l in f:
        x = 0
        for c in l.strip():
            if c == "@":
                start = (x,y)
            elif c.islower():
                tunnel_keys.append(c)
            tunnel_map[(x,y)] = c
            x += 1
        y += 1

print(tunnel_keys)
lastx = x
lasty = y

def print_tunnels(tunnel_map):
    for y in range(lasty):
        for x in range(lastx):
            print(tunnel_map[(x,y)], end="")
        print("")

def get_neighbors(loc):
    x,y = loc
    return [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]

def get_junctions(tunnel_map):
    junctions = set()
    for y in range(lasty):
        for x in range(lastx):
            tile = tunnel_map[(x,y)]
            if tile == "@":
                junctions.add((x,y))
            elif tile == ".":
                num_options = 0
                for neighbor in get_neighbors((x,y)):
                    if tunnel_map[neighbor] != "#":
                        num_options += 1
                if num_options >= 3:
                    junctions.add((x,y))
            elif tile != "#": # tile is a key
                junctions.add((x,y))
    return junctions

# for each junction, walk it out 
def get_junction_map(tunnel_map, junctions):
    junction_map = defaultdict(list)
    for junction in junctions:
        tile = tunnel_map[junction]
        if not (tile.islower() or tile.isupper() or tile == "@"):
            continue # skip non key, non gate junctions

        visited = set((junction, 0))
        q = deque((n, 1) for n in get_neighbors(junction))
        while q:
            location, steps = q.popleft()

            if location in visited:
                continue

            visited.add(location)

            tile = tunnel_map[location]
            if tile.islower() or tile.isupper() or tile == "@":
                junction_map[junction].append((location, steps))
                continue
            if tile == "#":
                continue
            assert tile == ".", "Unexpected tile {}".format(tile)
            for neighbor in get_neighbors(location):
                if neighbor not in visited:
                    q.append((neighbor, steps+1))

    return junction_map

if __name__ == '__main__':
    junctions = get_junctions(tunnel_map)
    junction_map = get_junction_map(tunnel_map, junctions)
    junctions = set(junction_map.keys())

    print_junctions = False
    if print_junctions:
        for y in range(lasty):
            for x in range(lastx):
                if (x,y) in junction_map:
                    tile = "%"
                elif (x,y) in junctions:
                    tile = "&"
                else:
                    tile = tunnel_map[(x,y)]
                print(tile, end="")
            print("")


    assert start in junctions, "start must be in junctions"

    # junction -> list of states=(num_steps, keys)
    historical_states = defaultdict(list)
    historical_states[start] = [(0, set())] # 0 steps, 0 keys
    active_states = [(start, 0, set())]

    best_score = float('inf')

    while active_states:
        print("#Active states:", len(active_states), "Best score:", best_score)
        next_active_states = []
        for junction, steps, keys in active_states:
            if steps >= best_score:
                continue
            # print("Evaluating",loc)
            neighbor_infos = junction_map[junction]
            # print("Neighbor infos of", junction, "was", neighbor_infos)
            for neighbor, neighbor_steps in neighbor_infos:
                tile = tunnel_map[neighbor]
                # print("Seeing if",neighbor,"reachable, tile was",tile)
                if tile == "." or tile == "@":
                    # junction was a non-key, non-door
                    next_active_states.append(
                        (neighbor, steps+neighbor_steps, keys.copy()))
                elif tile.islower():
                    # junction was a key
                    keys_copy = keys.copy()
                    keys_copy.add(tile)
                    next_active_states.append(
                        (neighbor, steps+neighbor_steps, keys_copy))
                else:
                    assert tile.isupper(), "unexpected junction {}".format(tile)
                    # junction was a door
                    if tile.lower() in keys:
                        next_active_states.append(
                            (neighbor, steps+neighbor_steps, keys.copy()))

        # print("next_active_states before domination is now", next_active_states)
        # print("historical states is", historical_states)
        # kill next active states which are dominated
        undominated_active_states = []
        for loc, steps, keys in next_active_states:
            for historical_steps, historical_keys in historical_states[loc]:
                if historical_steps <= steps and \
                   keys.issubset(historical_keys):
                    # this active state is dominated
                    # print(loc,steps,keys,"was dominated by", historical_steps, historical_keys)
                    break
            else:
                # this active state is not dominated            
                undominated_active_states.append((loc,steps,keys))


                # filter historical states which are dominated by this state
                undominated_historical_states = [(steps,keys)]
                for historical_steps, historical_keys in historical_states[loc]:
                    if historical_steps > steps and \
                       historical_keys.issubset(keys):
                        continue
                    else:
                        undominated_historical_states.append((historical_steps, historical_keys))
                historical_states[loc] = undominated_historical_states
        active_states = undominated_active_states

        non_winning_active_states = []
        for loc, num_steps, keys in active_states:
            if len(keys) == len(tunnel_keys):
                if num_steps < best_score:
                    best_score = num_steps
            else:
                non_winning_active_states.append((loc, num_steps, keys))
                    
        active_states = non_winning_active_states
    print("Best score", best_score)






