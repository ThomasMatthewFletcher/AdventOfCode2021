#!/usr/bin/env python3
from __future__ import annotations
from typing import List, NamedTuple, Optional, Union, Literal, Dict
from dataclasses import dataclass

class Instruction(NamedTuple):
    op: str
    v1: str
    v2: Optional[Union[str,int]]

Program = List[Instruction]

@dataclass(frozen=True)
class InputOperand:
    index: int

    def __repr__(self) -> str:
        return f'I{self.index}'

OpType = Literal['+', '*', '/', '%', '==']

op_symbols: Dict[str, OpType] = {
    'add': '+',
    'mul': '*',
    'div': '/',
    'mod': '%',
    'eql': '=='
}


@dataclass(frozen=True)
class Operation:
    op_type: OpType
    operand_1: Operand
    operand_2: Operand

    def __repr__(self) -> str:
        return f'({self.operand_1} {self.op_type} {self.operand_2})'

    def optimize(self) -> Operand:
        if isinstance(self.operand_1, int) and isinstance(self.operand_2, int):
            return self.calculate()

        if self.op_type == '*' and (self.operand_1 == 0 or self.operand_2 == 0):
            return 0

        if self.op_type == '/' and self.operand_2 == 1:
            return self.operand_1

        if self.op_type == '+' and self.operand_1 == 0:
            return self.operand_2

        if self.op_type == '+' and self.operand_2 == 0:
            return self.operand_1

        if self.op_type == '*' and self.operand_1 == 1:
            return self.operand_2

        if self.op_type == '*' and self.operand_2 == 1:
            return self.operand_1

        if self.op_type == '==':
            if isinstance(self.operand_1, InputOperand) and isinstance(self.operand_2, int) and (self.operand_2 >= 10 or self.operand_2 <= 0):
                return 0

            if isinstance(self.operand_2, InputOperand) and isinstance(self.operand_1, int) and (self.operand_1 >= 10 or self.operand_1 <= 0):
                return 0

        return self

    def calculate(self) -> int:
        assert isinstance(self.operand_1, int) and isinstance(self.operand_2, int)
        if self.op_type == '+':
            return self.operand_1 + self.operand_2
        if self.op_type == '*':
            return self.operand_1 * self.operand_2
        if self.op_type == '/':
            return int(self.operand_1 / self.operand_2)
        if self.op_type == '%':
            return self.operand_1 % self.operand_2
        if self.op_type == '==':
            return 1 if self.operand_1 == self.operand_2 else 0

        raise ValueError('op is unknown')

Operand = Union[Operation,int,InputOperand]


class ALU:
    def __init__(self, program: Program):
        self.program = program

    def execute(self, inputs: List[int]):
        self.inputs = inputs
        self.variables = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0
        }

        for instruction in self.program:
            print(instruction)
            v1 = self.variables[instruction.v1]
            v2 = self.get_value(instruction.v2)

            self.variables[instruction.v1] = self.execute_instruction(instruction.op, v1, v2)
            print(self.variables)

    def get_variable(self, variable: str):
        return self.variables[variable]

    def get_value(self, variable: Optional[Union[str,int]]) -> Optional[int]:
        if variable is None:
            return None
        if isinstance(variable, str):
            return self.variables[variable]
        return variable

    def execute_instruction(self, op: str, v1: int, v2: Optional[int]) -> int:
        if op == 'inp':
            return self.inputs.pop(0)

        # Instructions with 2 operands
        assert v2 is not None
        if op == 'add':
            return v1 + v2
        if op == 'mul':
            return v1 * v2
        if op == 'div':
            return int(v1 / v2)
        if op == 'mod':
            return v1 % v2
        if op == 'eql':
            return 1 if v1 == v2 else 0

        raise ValueError('op is unknown')


def main():
    program = read_program()

    alu = ALU(program)

    model   = 16811412161117

    digits = [int(d) for d in str(model)]

    alu.execute(digits)
    print(alu.get_variable('z'))

def convert_program_to_tree(program: Program) -> Dict[str, Operand]:
    variables: Dict[str, Operand] = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0
    }

    instruction_index = 0

    for instruction in program:
        # print(instruction)

        if instruction.op == 'inp':
            variables[instruction.v1] = InputOperand(instruction_index)
            instruction_index += 1
            continue

        v1_operand = variables[instruction.v1]
        assert v1_operand is not None

        if isinstance(instruction.v2, str):
            v2_operand = variables[instruction.v2]
        else:
            v2_operand = instruction.v2

        assert v2_operand is not None

        op_type = op_symbols[instruction.op]
        variables[instruction.v1] = Operation(op_type, v1_operand, v2_operand).optimize()

    # print(variables)

    return variables


def read_program() -> Program:
    with open('input.txt') as f:
        return [parse_instruction(l) for l in f]

def parse_instruction(line: str) -> Instruction:
    parts = line.split()
    op = parts[0]
    v1 = parts[1]

    if len(parts) == 2:
        v2 = None
    elif parts[2].strip('-').isnumeric():
        v2 = int(parts[2])
    else:
        v2 = parts[2]

    return Instruction(op, v1, v2)


if __name__ == '__main__':
    main()
