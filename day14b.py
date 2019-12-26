from day14a import *

# debts = defaultdict(lambda : 0)
# debts["FUEL"] = 1
# print(discharge_fuel_debt(debts))
def discharge_debts_opt(debts):
    ore_used = 0
    no_debts = False
    while not no_debts:
        no_debts = True
        for item in ingredients.keys():
            if debts[item] > 0:
                no_debts = False
                amnt, sources = ingredients[item]
                multiplier = debts[item] // amnt
                if (debts[item] % amnt) != 0:
                    multiplier += 1
                debts[item] -= amnt * multiplier
                for amnt, source in sources:
                    debts[source] += amnt * multiplier
        ore_used += debts["ORE"]
        debts["ORE"] = 0
    return ore_used

# init
fuel_low = 1
debts = defaultdict(lambda : 0)
debts["FUEL"] = fuel_low
ore_needed_low = discharge_debts_opt(debts)

ore_needed_high = ore_needed_low
fuel_high = 1
while ore_needed_high < int(1e12):
    fuel_high *= 2
    debts = defaultdict(lambda : 0)
    debts["FUEL"] = fuel_high
    ore_needed_high = discharge_debts_opt(debts)

# Loop invariant
#  fuel_high > fuel_low
#  ore_needed_high > ore_needed_low
# Desired terminal condition
#  fuel_high = 1+fuel_low
#  ore_needed_high > 1e12 >= ore_needed_low
while True:
    if fuel_high == fuel_low + 1:
        break
    fuel_mid = (fuel_high + fuel_low) // 2
    debts = defaultdict(lambda : 0)
    debts["FUEL"] = fuel_mid
    ore_needed_mid = discharge_debts_opt(debts)

    if ore_needed_mid <= int(1e12):
        fuel_low = fuel_mid
        ore_needed_low = ore_needed_mid
    else:
        fuel_high = fuel_mid
        ore_needed_high = ore_needed_mid

print("Ore needed", ore_needed_low)
print("Fuel made", fuel_low)

    


