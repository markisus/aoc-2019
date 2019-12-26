from collections import defaultdict

ingredients = {}

with open("day14.txt") as f:
    for l in f:
        sources, target = l.split("=>")
        source_tokens = [s.strip() for s in sources.split(",")]
        sources_parsed = []
        for token in source_tokens:
            amnt, name = token.split(" ")
            sources_parsed.append((int(amnt), name))
        target_amnt, target_name = target.strip().split(" ")
        ingredients[target_name] = (int(target_amnt), sources_parsed)

def discharge_debts(debts):
    ore_used = 0
    no_debts = False
    while not no_debts:
        no_debts = True
        for item in ingredients.keys():
            if debts[item] > 0:
                no_debts = False
                amnt, sources = ingredients[item]
                debts[item] -= amnt
                for amnt, source in sources:
                    debts[source] += amnt
        ore_used += debts["ORE"]
        debts["ORE"] = 0
    return ore_used

if __name__ == '__main__':
    debts = defaultdict(lambda : 0)
    debts["FUEL"] = 1
    print(discharge_debts(debts))

