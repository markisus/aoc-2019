from day7a import amp_control_software
from day5b import step_program
from collections import deque
from itertools import permutations

# debug
# amp_control_software = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
# 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

class ProgramState(object):
    def __init__(self, mem, in_stream, out_stream):
        self.instruction_ptr = 0
        self.mem = mem.copy()
        for _ in range(3):
            # memory padding
            # implementation detail, see day5b
            self.mem.append(0)
        self.in_stream = in_stream
        self.out_stream = out_stream

    def step(self):
        if self.instruction_ptr < 0:
            return
        self.instruction_ptr = step_program(
            self.instruction_ptr,
            self.mem,
            self.in_stream,
            self.out_stream)

    def is_done(self):
        return self.instruction_ptr < 0


def run_amp_seq(pa, pb, pc, pd, pe):
    in_a, in_b, in_c, in_d, in_e = (deque() for _ in range(5))
    in_a.append(pa)
    in_a.append(0)
    in_b.append(pb)
    in_c.append(pc)
    in_d.append(pd)
    in_e.append(pe)

    prog_a = ProgramState(amp_control_software.copy(), in_a, in_b)
    prog_b = ProgramState(amp_control_software.copy(), in_b, in_c)
    prog_c = ProgramState(amp_control_software.copy(), in_c, in_d)
    prog_d = ProgramState(amp_control_software.copy(), in_d, in_e)
    prog_e = ProgramState(amp_control_software.copy(), in_e, in_a)

    while not prog_e.is_done():
        for prog in prog_a, prog_b, prog_c, prog_d, prog_e:
            prog.step()

    return in_a[-1]

def find_best():
    best = -float("inf")
    for pa, pb, pc, pd, pe in permutations(range(5, 10)):
        value = run_amp_seq(pa,pb,pc,pd,pe)
        if value > best:
            best = value
            print("Best is now", best)
    return best

print(find_best())


