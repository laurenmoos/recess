import numpy as np
from scipy.sparse import coo_matrix

from collections import deque
from env.data_models import  Inst


def execute(code, input_data, num_registers, num_data_registers, make_trace):
    """
    :param code: vector of instructions in prefix notation
    :param input_data: binary input vector with size == number of test_data registers
    :param num_registers: total number of program registers
    :param num_data_registers: number of writeable or test_data registers
    :param make_trace: boolean indicating whether an execution trace should be collected
    :return: state of output registers after program is executed and optional call stack
    """
    # now it is evaluating columns of instruction? not sure
    return _execute_vec(code, input_data, num_registers, num_data_registers, make_trace)


def _initialize_with_input(input_data, num_registers, num_data_registers):
    reg = np.zeros(num_registers)
    assert len(input_data) <= num_data_registers

    reg[:len(input_data)] = input_data
    return reg


def _execute_vec(code, input_data, num_registers, num_data_registers, make_trace):
    steps = 0

    call_stack = deque()

    regs = _initialize_with_input(input_data, num_registers, num_data_registers)

    print(f"Code looks like {code}")
    for (pc, inst) in enumerate(code):
        print(f"Instruction is {str(inst)}")
        # this operation has side effects on regs
        out = _evaluate_inst_vec(inst, regs)
        print(f"Resulting program state is {regs}")

        if make_trace:
            call_stack.appendleft(out)
        steps += 1

    # returns the output values of the program and optionally the trace
    return regs, call_stack


def _evaluate_inst_vec(inst: Inst, regs):
    # regs is an adjacency list with rows being the source registers and columns the writeable registers

    if inst.op.arity == 2:
        args = [loc(inst.dst, regs), loc(inst.src, regs)]
    elif inst.op.arity == 1:
        print(f"Operation with arity 1 is {loc(inst.src, regs)}")
        args = [loc(inst.src, regs)]
    else:
        args = inst.op.fx([])
    regs[inst.dst - 1] = inst.op.fx(*args)
    return regs[inst.dst - 1]


def loc(dst, data):
    return data[abs(dst) % abs(len(data))]
