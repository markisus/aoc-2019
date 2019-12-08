from day1a import fuels

def get_fuel(init_fuel):
    total_fuel = 0
    current_fuel = init_fuel
    while current_fuel > 0:
        total_fuel += current_fuel
        current_fuel = current_fuel // 3 - 2
    return total_fuel

print("Answer", sum(get_fuel(init_fuel) for init_fuel in fuels))
