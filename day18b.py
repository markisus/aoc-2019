from day18a import *
from collections import defaultdict, deque, namedtuple

start_x, start_y = start
starts = []
# modify tunnel map
for i in range(-1, 2):
    for j in range(-1, 2):
        loc = (start_x + i, start_y + j)
        if abs(i) == 1 and abs(j) == 1:
            tunnel_map[loc] = "@"
        else:
            tunnel_map[loc] = "#"

for k, v in tunnel_map.items():
    if v == "@":
        starts.append(k)

starts.sort(key = lambda t: (t[1], t[0])) # sort row major
print(starts)

print_tunnels(tunnel_map)

junctions = get_junctions(tunnel_map)
junction_map = get_junction_map(tunnel_map, junctions)
junctions = set(junction_map.keys())

# for k, v in junction_map.items():
#     for loc, dist in v:
#         print(tunnel_map[k], "to", tunnel_map[loc], "was", dist)

for v in junction_map.values():
    assert len(v), "no islands"

HyperState = namedtuple("HyperState","num_steps hyperjunction keys")

# 4-tuple of states -> (num_steps, keys)
historical_states = defaultdict(list)
active_states = [HyperState(0, (starts[0], starts[1], starts[2], starts[3]), set())]
best_score = float('inf')
highest_numkeys = 0

def get_hyperneighbors(hyperjunction):
    ja, jb, jc, jd = hyperjunction
    for j, steps in junction_map[ja]:
        # print("yeilding a")
        yield j, (j, jb, jc, jd), steps
    for j, steps in junction_map[jb]:
        # print("yeilding b")
        yield j, (ja, j, jc, jd), steps
    for j, steps in junction_map[jc]:
        # print("yeilding c")
        yield j, (ja, jb, j, jd), steps
    for j, steps in junction_map[jd]:
        # print("yeilding d")
        yield j, (ja, jb, jc, j), steps

reverse_tunnel_map = {}
for loc, tile in tunnel_map.items():
    if tile.islower():
        reverse_tunnel_map[tile] = loc

def get_hyperjunction_str(hyperjunction):
    return "".join(tunnel_map[junction] for junction in hyperjunction)

while active_states:
    print("#Active states", len(active_states), "highest numkeys", highest_numkeys, "best score", best_score)
    next_active_states = []
    for hyperstate in active_states:
        if hyperstate.num_steps >= best_score:
            continue
        hyperjunction = hyperstate.hyperjunction
        hyperjunction_str = get_hyperjunction_str(hyperjunction)

        for neighbor, neighbor_hyperjunction, num_steps in get_hyperneighbors(hyperjunction):
            tile = tunnel_map[neighbor]
            if tile.islower():
                # collect the key
                next_active_states.append(
                    HyperState(
                        hyperstate.num_steps + num_steps,
                        neighbor_hyperjunction,
                        hyperstate.keys | set((tile,))))
            elif tile == "." or tile == "@" or \
                 tile.lower() in hyperstate.keys:
                # the state is reachable from here because it is
                # ., @, or a door for a key we own
                next_active_states.append(
                    HyperState(
                        hyperstate.num_steps + num_steps,
                        neighbor_hyperjunction,
                        hyperstate.keys))

    undominated_active_states = []
    for active_state in next_active_states:
        hyperjunction = active_state.hyperjunction
        for historical_num_steps, historical_keys in historical_states[hyperjunction]:
            if historical_num_steps <= active_state.num_steps and \
               active_state.keys.issubset(historical_keys):
                break #active state is dominated, should no-op
        else:
            undominated_active_states.append(active_state)

            # need to see which historical states might be dominated
            undominated_historical_states = []
            for historical_num_steps, historical_keys in historical_states[hyperjunction]:
                if historical_num_steps >= active_state.num_steps and \
                   historical_keys.issubset(active_state.keys):
                    continue # this item is dominated
                undominated_historical_states.append((historical_num_steps,
                                                     historical_keys))
            undominated_historical_states.append((active_state.num_steps,
                                                 active_state.keys))
            historical_states[hyperjunction] = undominated_historical_states
    active_states = undominated_active_states

    non_winning_active_states = []
    for hyperstate in active_states:
        highest_numkeys = max(highest_numkeys, len(hyperstate.keys))
        if len(hyperstate.keys) == len(tunnel_keys):
            if hyperstate.num_steps < best_score:
                print("Found a new best score", hyperstate)
                best_score = hyperstate.num_steps
        else:
            non_winning_active_states.append(hyperstate)

    active_states = non_winning_active_states

print("Best score", best_score) #1992

