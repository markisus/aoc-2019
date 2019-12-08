STOP = 99
ADD = 1
MULT = 2

def step_program(current_instruction, memory):
    # print("Current instruction", current_instruction)
    current_opcode = memory[4*current_instruction]
    # print("Opcode", current_opcode)

    if current_opcode == STOP:
        return False # doesn't have next

    base = 4*current_instruction
    address_a = memory[base + 1]
    address_b = memory[base + 2]
    address_c = memory[base + 3]

    # print("&a", address_a)
    # print("&b", address_b)
    # print("&c", address_c)

    a = memory[address_a]
    b = memory[address_b]

    # print("a", a)
    # print("b", b)

    if current_opcode == ADD:
        memory[address_c] = a + b
    elif current_opcode == MULT:
        memory[address_c] = a * b
    else:
        raise RuntimeError("Malformed input")

    return True # has next
    

def run_program(memory):
    # print("Processing", memory)
    current_instruction = 0
    has_next = step_program(current_instruction, memory)
    while has_next:
        current_instruction += 1
        has_next = step_program(current_instruction, memory)
    return memory

# print(run_program([1,0,0,0,99]))
# print(run_program([2,3,0,3,99]))
# print(run_program([2,4,4,5,99,0]))
# print(run_program([1,1,1,4,99,5,6,0,99]))

memory = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,19,5,23,2,23,6,27,1,27,5,31,2,6,31,35,1,5,35,39,2,39,9,43,1,43,5,47,1,10,47,51,1,51,6,55,1,55,10,59,1,59,6,63,2,13,63,67,1,9,67,71,2,6,71,75,1,5,75,79,1,9,79,83,2,6,83,87,1,5,87,91,2,6,91,95,2,95,9,99,1,99,6,103,1,103,13,107,2,13,107,111,2,111,10,115,1,115,6,119,1,6,119,123,2,6,123,127,1,127,5,131,2,131,6,135,1,135,2,139,1,139,9,0,99,2,14,0,0]

if __name__ == "__main__":
    # Alterations specified by the question
    memory[1] = 12
    memory[2] = 2
    print("Answer", run_program(memory)[0])



