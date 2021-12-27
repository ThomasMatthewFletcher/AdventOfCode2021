#!/usr/bin/env python3
from typing import List
from enum import Enum
import os

class HerdType(str, Enum):
    NONE = '.'
    EAST = '>'
    SOUTH = 'v'

class Map:
    def __init__(self, map: List[List[str]]):
        self.map = map
        self.width = len(map[0])
        self.height = len(map)
        self.did_move = True

    def __str__(self) -> str:
        output = ''
        for row in self.map:
            for cell in row:
                output += cell
            output += '\n'
        return output

    def step(self):
        self.did_move = False
        self.step_east()
        self.step_south()

    def step_east(self):
        self.move_herd(HerdType.EAST, 1, 0)

    def step_south(self):
        self.move_herd(HerdType.SOUTH, 0, 1)

    def move_herd(self, herd_type: HerdType, dx: int, dy: int):
        new_map: List[List[str]] = [[HerdType.NONE] * self.width for _ in range(self.height)]

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == herd_type:
                    new_x = (x + dx) % self.width
                    new_y = (y + dy) % self.height
                    if self.is_empty(new_x, new_y):
                        new_map[new_y][new_x] = herd_type
                        self.did_move = True
                    else:
                        new_map[y][x] = cell
                elif cell != HerdType.NONE:
                    new_map[y][x] = cell

        self.map = new_map

    def is_empty(self, x: int, y: int):
        return self.map[y][x] == HerdType.NONE


def main():
    step = 0
    map = read_map()

    # clear_screen()
    # print(f'Step: {step}')
    # print(map)

    while map.did_move:
        map.step()
        step += 1
        # clear_screen()
        # print(f'Step: {step}')
        # print(map)

    print(f'Answer: {step}')

def read_map() -> Map:
    with open('input.txt') as f:
        return Map([[HerdType(t) for t in l.strip()] for l in f])

def clear_screen():
    os.system('clear')

if __name__ == '__main__':
    main()
