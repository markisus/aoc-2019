from collections import defaultdict, deque

pluto_map = defaultdict(lambda : "#")

min_x = 0
x = 0
y = 0

with open("day20.txt") as f:
    for l in f:
        x = 0
        for c in l[:-1]:
            pluto_map[(x,y)] = c
            x += 1
        y += 1
lastx = x
lasty = y

def print_pluto(pluto_map):
    for y in range(lasty):
        for x in range(lastx):
            print(pluto_map[(x,y)], end="")
        print("")

print_pluto(pluto_map)

portal_names = {}

for x in range(lastx):
    for y in range(lasty):
        # search for letter,letter,x
        # a b c
        a = pluto_map[(x,y)]
        b = pluto_map[(x+1,y)]
        c = pluto_map[(x+2,y)]

        if a.isupper() and b.isupper() and c == ".":
            portal_name = "".join((a,b))
            portal_names[(x+2,y)] = portal_name
            
        if a == "." and b.isupper() and c.isupper():
            portal_name = "".join((b,c))
            portal_names[(x,y)] = portal_name

        # d
        # e
        # f
        d = pluto_map[(x,y)]
        e = pluto_map[(x,y+1)]
        f = pluto_map[(x,y+2)]
        
        if d.isupper() and e.isupper() and f == ".":
            portal_name = "".join((d,e))
            portal_names[(x,y+2)] = portal_name
            
        if d == "." and e.isupper() and f.isupper():
            portal_name = "".join((e,f))
            portal_names[(x,y)] = portal_name

def get_neighbors(loc):
    x,y = loc
    return [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]

for loc, name in portal_names.items():
    if name == "AA":
        start = loc
    if name == "ZZ":
        end = loc

print("start",start,"end",end)

portal_map = {}
for loc1, name1 in portal_names.items():
    for loc2, name2 in portal_names.items():
        if loc1 == loc2:
            continue
        if name1 != name2:
            continue
        print("Linking",loc1,"<-",name1,"->",loc2)
        portal_map[loc1] = loc2
        portal_map[loc2] = loc1

if __name__ == '__main__':
    # bfs until the end
    best_distance = defaultdict(lambda : float('inf'))
    best_distance[start] = 0

    q = deque((start,))
    queued = set((start,))

    while q:
        current = q.popleft()
        queued.remove(current)

        dist_to_current = best_distance[current]

        for neighbor in get_neighbors(current):
            if pluto_map[neighbor] == ".":
                if best_distance[neighbor] > dist_to_current + 1:
                    best_distance[neighbor] = dist_to_current + 1
                    if not neighbor in queued:
                        q.append(neighbor)
                        queued.add(neighbor)
            if current in portal_map:
                portal_out = portal_map[current]
                if best_distance[portal_out] > dist_to_current + 1:
                    best_distance[portal_out] = dist_to_current + 1
                    if not portal_out in queued:
                        q.append(portal_out)
                        queued.add(portal_out)

    print(best_distance[end])
