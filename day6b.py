from day6a import data

orbitees = {}

for line in data.split("\n"):
    try:
        orbitee, orbiter = line.split(")")
        orbitees[orbiter] = orbitee
    except:
        continue


my_parents = {}
santas_parents = {}

my_node = "YOU"
santas_node = "SAN"

i = 0
while True:
    my_node = orbitees[my_node]
    my_parents[my_node] = i

    santas_node = orbitees[santas_node]
    santas_parents[santas_node] = i

    if santas_node in my_parents:
        distance = i + my_parents[santas_node]
        break
    if my_node in santas_parents:
        distance = i + santas_parents[my_node]
        break

    i += 1

print("Distance", distance)


