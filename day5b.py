from collections import deque

# modes
POSITION = "0"
IMMEDIATE = "1"

# opcodes
STOP = "99"
ADD = "01"
MULT = "02"
INPUT = "03"
OUTPUT = "04"
JUMP_T = "05"
JUMP_F = "06"
LT = "07"
EQ = "08"

def memdump(memory):
    for idx, mem in enumerate(memory):
        print("{:05d}:{}".format(idx, mem))

def parse_op(op):
    op = str(op).zfill(5)
    opcode = op[-2:]
    parsed = [opcode]
    num_modes = len(op) - 2
    for i in range(3):
        parsed.append(op[-(3 + i)])
    return parsed

def step_program(instruction_ptr, memory, input_stream, output_stream):
    """
    executes operation and returns the distance to next instruction
    halt command sets next instruction to -1
    input command is a no-op if input stream is empty, otherwise poplefts
    """
    # print("Instruction:", instruction_ptr)
    # print("Memory chunk:", memory[instruction_ptr:instruction_ptr + 10])
    op = parse_op(memory[instruction_ptr])
    # print("Unparsed op", memory[instruction_ptr])
    # print("Current op", op)
    opcode = op[0]
    if opcode == STOP:
        return -1

    mode_a, mode_b, mode_c = op[1:]
    param_a = memory[instruction_ptr + 1]
    param_b = memory[instruction_ptr + 2]
    param_c = memory[instruction_ptr + 3]
    
    # print("Params", param_a, param_b, param_c)

    if mode_a == IMMEDIATE:
        value_a = param_a
    elif param_a < len(memory):
        value_a = memory[param_a]
    if mode_b == IMMEDIATE:
        value_b = param_b
    elif param_b < len(memory):
        value_b = memory[param_b]
    if mode_c == IMMEDIATE:
        value_c = param_c
    elif param_c < len(memory):
        value_c = memory[param_c]
        
    if opcode == ADD:
        memory[param_c] = value_a + value_b
        return instruction_ptr + 4
    elif opcode == MULT:
        memory[param_c] = value_a * value_b
        return instruction_ptr + 4
    elif opcode == INPUT:
        if not input_stream:
            # print("Waiting for input")
            return instruction_ptr
        memory[param_a] = input_stream.popleft()
        return instruction_ptr + 2
    elif opcode == OUTPUT:
        output_stream.append(value_a)
        return instruction_ptr + 2
    elif opcode == JUMP_T:
        # print("JUMP_T")
        if value_a != 0:
            # print("Success, jumping to ", value_b)
            return value_b
        else:
            return instruction_ptr + 3
    elif opcode == JUMP_F:
        if value_a == 0:
            return value_b
        else:
            return instruction_ptr + 3
    elif opcode == LT:
        memory[param_c] = int(value_a < value_b)
        return instruction_ptr + 4
    elif opcode == EQ:
        memory[param_c] = int(value_a == value_b)
        return instruction_ptr + 4
    else:
        raise RuntimeError("Malformed input at instruction ", instruction_ptr, " opcode", opcode)
    
def run_program(memory, input_stream, output_stream):
    for i in range(3):
        memory.append(0) # pad memory to prevent index error from simplified param parsing code

    # print("Processing", memory)
    instruction_ptr = 0
    while instruction_ptr >= 0:
        # print("Instruction:", instruction_ptr)
        # print("Memory current")
        # memdump(memory)
        instruction_ptr = step_program(instruction_ptr, memory, input_stream, output_stream)
    return memory

if __name__ == "__main__":
    program = """3,225,1,225,6,6,1100,1,238,225,104,0,2,171,209,224,1001,224,-1040,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,102,65,102,224,101,-3575,224,224,4,224,102,8,223,223,101,2,224,224,1,223,224,223,1102,9,82,224,1001,224,-738,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1101,52,13,224,1001,224,-65,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1102,82,55,225,1001,213,67,224,1001,224,-126,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1,217,202,224,1001,224,-68,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1002,176,17,224,101,-595,224,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,1102,20,92,225,1102,80,35,225,101,21,205,224,1001,224,-84,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1101,91,45,225,1102,63,5,225,1101,52,58,225,1102,59,63,225,1101,23,14,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,677,224,1002,223,2,223,1006,224,329,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,344,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,359,1001,223,1,223,8,677,226,224,102,2,223,223,1005,224,374,1001,223,1,223,1107,677,226,224,102,2,223,223,1006,224,389,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,419,1001,223,1,223,1007,677,677,224,102,2,223,223,1006,224,434,1001,223,1,223,107,226,226,224,1002,223,2,223,1005,224,449,1001,223,1,223,1008,677,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1007,677,226,224,1002,223,2,223,1005,224,479,1001,223,1,223,108,677,677,224,1002,223,2,223,1006,224,494,1001,223,1,223,108,226,226,224,1002,223,2,223,1006,224,509,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,524,101,1,223,223,107,677,226,224,1002,223,2,223,1005,224,539,1001,223,1,223,8,226,226,224,102,2,223,223,1005,224,554,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,569,101,1,223,223,108,677,226,224,102,2,223,223,1006,224,584,1001,223,1,223,7,677,677,224,1002,223,2,223,1005,224,599,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,614,1001,223,1,223,1107,226,677,224,102,2,223,223,1006,224,629,101,1,223,223,1107,226,226,224,102,2,223,223,1005,224,644,1001,223,1,223,1108,677,677,224,1002,223,2,223,1005,224,659,101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226"""

    # Debug program
    # program = """
    # 3,21,
    # 1008,21,8,20,
    # 1005,20,
    # 22,107,8,
    # 21,20,1006,20,31,
    # 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
    # 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"""

    # Output for debug program
    # for i in range(10):
    #     output_stream = []
    #     print("Input", i)
    #     run_program(memory, [i], output_stream)
    #     print(output_stream)


    memory = [int(s) for s in program.split(",")]
    # print("Memory start", memory[:10])

    output_stream = deque()
    run_program(memory, deque((5,)), output_stream)
    print(output_stream)
