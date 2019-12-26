from collections import defaultdict, deque

# modes
POSITION = "0"
IMMEDIATE = "1"
RELATIVE = "2"

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
INC_REL_BASE = "09"

def memdump(memory):
    for idx in sorted(memory.keys()):
        print("{:05d}:{}".format(idx, memory[idx]))

def parse_op(op):
    op = str(op).zfill(5)
    opcode = op[-2:]
    parsed = [opcode]
    num_modes = len(op) - 2
    for i in range(3):
        parsed.append(op[-(3 + i)])
    return parsed

DEBUG = True
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
    # print("Current op", op[0])
    opcode = op[0]
    if opcode == STOP:
        return -1

    relative_base = memory[-1]

    mode_a, mode_b, mode_c = op[1:]
    param_a = memory[instruction_ptr + 1]
    param_b = memory[instruction_ptr + 2]
    param_c = memory[instruction_ptr + 3]
    
    # print("Params", param_a, param_b, param_c)

    if mode_a == IMMEDIATE:
        value_a = param_a
    elif mode_a == RELATIVE:
        value_a = memory[relative_base + param_a]
        address_a = relative_base + param_a
    else:
        value_a = memory.get(param_a, 0)
        address_a = param_a

    if mode_b == IMMEDIATE:
        value_b = param_b
    elif mode_b == RELATIVE:
        value_b = memory[relative_base + param_b]
        address_b = relative_base + param_b
    else:
        value_b = memory.get(param_b, 0)
        address_b = param_b

    if mode_c == IMMEDIATE:
        value_c = param_c
    elif mode_c == RELATIVE:
        value_c = memory[relative_base + param_c]
        address_c = relative_base + param_c
    else:
        value_c = memory.get(param_c, 0)
        address_c = param_c
        
    if opcode == ADD:
        memory[address_c] = value_a + value_b
        return instruction_ptr + 4
    elif opcode == MULT:
        memory[address_c] = value_a * value_b
        return instruction_ptr + 4
    elif opcode == INPUT:
        if not input_stream:
            if DEBUG:
                print("Waiting for input")
            return instruction_ptr
        input_value = input_stream.popleft()
        memory[address_a] = input_value
        return instruction_ptr + 2
    elif opcode == OUTPUT:
        output_stream.append(value_a)
        return instruction_ptr + 2
    elif opcode == JUMP_T:
        if value_a != 0:
            return value_b
        else:
            return instruction_ptr + 3
    elif opcode == JUMP_F:
        if value_a == 0:
            return value_b
        else:
            return instruction_ptr + 3
    elif opcode == LT:
        memory[address_c] = int(value_a < value_b)
        return instruction_ptr + 4
    elif opcode == EQ:
        memory[address_c] = int(value_a == value_b)
        return instruction_ptr + 4
    elif opcode == INC_REL_BASE:
        memory[-1] += value_a
        return instruction_ptr + 2
    else:
        raise RuntimeError("Malformed input at instruction ", instruction_ptr, " opcode", opcode)
    
def run_program(memory, input_stream, output_stream):
    # print("Processing", memory)
    instruction_ptr = 0
    while instruction_ptr >= 0:
        # print("Instruction:", instruction_ptr)
        # print("Memory current")
        # memdump(memory)
        instruction_ptr = step_program(instruction_ptr, memory, input_stream, output_stream)
    return memory

def make_memory(memory_list):
    memory = defaultdict(lambda: 0)
    memory[-1] = 0 # relative base init
    for idx, val in enumerate(memory_list):
        memory[idx] = val
    return memory

# memory_list = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
# memory_list = [1102,34915192,34915192,7,4,7,99,0]
# memory_list = [104,1125899906842624,99]
with open("day9.txt") as f:
    memory_list = [int(s.strip()) for s in f.readline().split(",")]

memory = make_memory(memory_list)

class IntCodeComputer:
    def __init__(self, memory):
        self.instruction_ptr = 0
        self.memory = memory
        self.input_stream = deque()
        self.output_stream = deque()

    def step(self):
        if self.done():
            raise RuntimeError("Cannot step, already done")

        self.instruction_ptr = \
            step_program(self.instruction_ptr, 
                         self.memory, 
                         self.input_stream, 
                         self.output_stream)
        return self.instruction_ptr

    def keep_stepping(self):
        if self.done():
            raise RuntimeError("Cannot step, already done")
        prev_instruction_ptr = self.instruction_ptr
        while not self.done():
            self.step()
            if prev_instruction_ptr == self.instruction_ptr:
                break
            prev_instruction_ptr = self.instruction_ptr

    def push_input(self, d):
        self.input_stream.append(d)

    def output_len(self):
        return len(self.output_stream)

    def pop_output(self):
        return self.output_stream.popleft()

    def done(self):
        return self.instruction_ptr < 0

    def copy(self):
        mem_copy = self.memory.copy()
        istream = self.input_stream.copy()
        ostream = self.output_stream.copy()
        return IntCodeComputer(mem_copy)

if __name__ == "__main__":
    # memdump(memory)
    output = deque()
    run_program(memory, deque((1,)), output)
    print(output[0])        
