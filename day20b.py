from collections import namedtuple
from day20a import *

first_wall_x = None
first_wall_y = None
last_wall_x = 0
last_wall_y = 0

for x in range(lastx):
    for y in range(lasty):
        if pluto_map[(x,y)] == "#":
            if first_wall_x is None:
                first_wall_x = x
                first_wall_y = y
            last_wall_x = max(last_wall_x, x)
            last_wall_y = max(last_wall_y, y)
            

        
print(first_wall_x,first_wall_y)
print(last_wall_x,last_wall_y)

def is_portal_inner(loc):
    x,y = loc
    return first_wall_x < x < last_wall_x and \
        first_wall_y < y < last_wall_y

# for portal in portal_names:
#     is_inner = is_portal_inner(portal)
#     if is_inner:
#         pluto_map[portal] = "i"
#     else:
#         pluto_map[portal] = "o"
# print_pluto(pluto_map)

MAX_LEVEL = float('inf')
if __name__ == '__main__':
    # bfs until the end
    RecursiveState = namedtuple("RecursiveState", ["loc", "level"])

    recursive_start = RecursiveState(start, 0)
    recursive_end = RecursiveState(end, 0)
    best_distance = defaultdict(lambda : float('inf'))
    best_distance[recursive_start] = 0

    q = deque()
    q.append(recursive_start)
    queued = set()
    queued.add(recursive_start)

    iteration = 0;

    while q:
        iteration += 1
        current = q.popleft()
        queued.remove(current)

        dist_to_current = best_distance[current]
        best_dist_to_end = best_distance[recursive_end]

        if iteration % 1000 == 0:
            print("iteration",iteration,"Q size", len(queued), "Current best distance", best_dist_to_end)
        
        if dist_to_current >= best_dist_to_end:
            # there is no way this path can lead to
            # an improved path to end
            continue

        for neighbor in get_neighbors(current.loc):
            if pluto_map[neighbor] == ".":
                recursive_neighbor = RecursiveState(neighbor, current.level)
                if best_distance[recursive_neighbor] > dist_to_current + 1:
                    best_distance[recursive_neighbor] = dist_to_current + 1
                    if not recursive_neighbor in queued:
                        q.append(recursive_neighbor)
                        queued.add(recursive_neighbor)
            if current.loc in portal_map:
                portal_out = portal_map[current.loc]
                level_delta = 1 if is_portal_inner(current.loc) else -1
                portal_out_recursive = RecursiveState(portal_out, current.level + level_delta)
                if portal_out_recursive.level == -1:
                    continue
                if portal_out_recursive.level > MAX_LEVEL:
                    continue
                
                if best_distance[portal_out_recursive] > dist_to_current + 1:
                    best_distance[portal_out_recursive] = dist_to_current + 1
                    if not portal_out_recursive in queued:
                        q.append(portal_out_recursive)
                        queued.add(portal_out_recursive)

    print(best_distance[recursive_end])
