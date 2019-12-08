# modes
POSITION = "0"
IMMEDIATE = "1"

# opcodes
STOP = "99"
ADD = "01"
MULT = "02"
INPUT = "03"
OUTPUT = "04"

def parse_op(op):
    op = str(op).zfill(5)
    opcode = op[-2:]
    parsed = [opcode]
    num_modes = len(op) - 2
    for i in range(num_modes):
        parsed.append(op[-(3 + i)])
    return parsed

def step_program(instruction_ptr, memory, input_stream, output_stream):
    """executes operation and returns the distance to next instruction"""
    # print("Memory:", memory[instruction_ptr])
    op = parse_op(memory[instruction_ptr])
    # print("Unparsed op", memory[instruction_ptr])
    # print("Current op", op)
    opcode = op[0]

    if opcode == STOP:
        return 0

    base = instruction_ptr

    if opcode == ADD or opcode == MULT:
        mode_a, mode_b = op[1:3]
        # It's technically allowed to provide mode_c,
        # but it has to be position mode if it exists
        param_a = memory[instruction_ptr + 1]
        param_b = memory[instruction_ptr + 2]
        address_c = memory[instruction_ptr + 3]
        if mode_a == IMMEDIATE:
            a = param_a
        else:
            a = memory[param_a]
        if mode_b == IMMEDIATE:
            b = param_b
        else:
            b = memory[param_b]
        if opcode == ADD:
            memory[address_c] = a + b
        elif opcode == MULT:
            memory[address_c] = a * b
        return 4 # next instruction distance, no output
    elif opcode == INPUT:
        # It's technically allowed to provide mode
        # but it must be position
        address = memory[instruction_ptr + 1]
        memory[address] = input_stream.pop()
        return 2 # next instruction distance, no output
    elif opcode == OUTPUT:
        mode = op[1]
        param = memory[instruction_ptr + 1]
        if mode == IMMEDIATE:
            output_val = param
        else:
            output_val = memory[param]
        # print("Outputing", output_val)
        output_stream.append(output_val)
        return 2 # next instruction distance, output
    else:
        raise RuntimeError("Malformed input")
    
def run_program(memory, input_stream, output_stream):
    # print("Processing", memory)
    instruction_ptr = -1
    next_instruction_distance = 1
    while next_instruction_distance != 0:
        # print("Memory current", memory[:20])
        instruction_ptr += next_instruction_distance
        next_instruction_distance = step_program(instruction_ptr, memory, input_stream, output_stream)
    return memory


program = """3,225,1,225,6,6,1100,1,238,225,104,0,2,171,209,224,1001,224,-1040,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,102,65,102,224,101,-3575,224,224,4,224,102,8,223,223,101,2,224,224,1,223,224,223,1102,9,82,224,1001,224,-738,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1101,52,13,224,1001,224,-65,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1102,82,55,225,1001,213,67,224,1001,224,-126,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1,217,202,224,1001,224,-68,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1002,176,17,224,101,-595,224,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,1102,20,92,225,1102,80,35,225,101,21,205,224,1001,224,-84,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1101,91,45,225,1102,63,5,225,1101,52,58,225,1102,59,63,225,1101,23,14,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,677,224,1002,223,2,223,1006,224,329,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,344,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,359,1001,223,1,223,8,677,226,224,102,2,223,223,1005,224,374,1001,223,1,223,1107,677,226,224,102,2,223,223,1006,224,389,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,419,1001,223,1,223,1007,677,677,224,102,2,223,223,1006,224,434,1001,223,1,223,107,226,226,224,1002,223,2,223,1005,224,449,1001,223,1,223,1008,677,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1007,677,226,224,1002,223,2,223,1005,224,479,1001,223,1,223,108,677,677,224,1002,223,2,223,1006,224,494,1001,223,1,223,108,226,226,224,1002,223,2,223,1006,224,509,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,524,101,1,223,223,107,677,226,224,1002,223,2,223,1005,224,539,1001,223,1,223,8,226,226,224,102,2,223,223,1005,224,554,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,569,101,1,223,223,108,677,226,224,102,2,223,223,1006,224,584,1001,223,1,223,7,677,677,224,1002,223,2,223,1005,224,599,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,614,1001,223,1,223,1107,226,677,224,102,2,223,223,1006,224,629,101,1,223,223,1107,226,226,224,102,2,223,223,1005,224,644,1001,223,1,223,1108,677,677,224,1002,223,2,223,1005,224,659,101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226"""

memory = [int(s) for s in program.split(",")]
# print("Memory start", memory[:10])

output_stream = []
run_program(memory, [1], output_stream)
print(output_stream)
