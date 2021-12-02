#!/usr/bin/env python3
from enum import Enum
from typing import NamedTuple

def main():
    instructions = read_instructions()
    submarine = Submarine()

    for instruction in instructions:
        submarine.move(instruction)

    answer = submarine.x * submarine.depth
    print(f'Answer: {answer}')


class Direction(Enum):
    FORWARD = 'forward'
    DOWN = 'down'
    UP = 'up'

class Instruction(NamedTuple):
    direction: Direction
    value: int

class Submarine:

    def __init__(self):
        self.x = 0
        self.depth = 0

        self.move_funcs = {
            Direction.FORWARD: self.moveForward,
            Direction.DOWN: self.moveDown,
            Direction.UP: self.moveUp
        }

    def move(self, instruction: Instruction):
        func = self.move_funcs[instruction.direction]
        func(instruction.value)

    def moveForward(self, value: int):
        self.x += value

    def moveDown(self, value: int):
        self.depth += value

    def moveUp(self, value: int):
        self.depth -= value


def read_instructions():
    with open('input.txt') as f:
        lines = f.readlines()
        return map(parse_instruction, lines)

def parse_instruction(instruction):
    direction, value = instruction.split()
    direction = Direction[direction.upper()]
    value = int(value)
    return Instruction(direction, value)

if __name__ == '__main__':
    main()
