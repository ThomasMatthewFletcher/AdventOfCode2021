#!/usr/bin/env python3
from typing import List, NamedTuple
import os
from time import sleep

class Point(NamedTuple):
    x: int
    y: int


class Grid:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.flashes = 0
        self.flash_locations: List[Point] = []

    def step(self):
        self.increment()
        self.increase_adjacent()

    def increment(self):
        for y, row in enumerate(self.grid):
            for x, e in enumerate(row):
                if e == 9:
                    self.grid[y][x] = 0
                    self.flashes += 1
                    self.flash_locations.append(Point(x, y))
                else:
                    self.grid[y][x] = e + 1

    def increase_adjacent(self):
        while self.flash_locations:
            location = self.flash_locations.pop(0)

            neighbours = self.get_neighbours(location)

            for neighbour in neighbours:
                neighbour_energy = self.grid[neighbour.y][neighbour.x]

                if neighbour_energy != 0:
                    if neighbour_energy == 9:
                        self.grid[neighbour.y][neighbour.x] = 0
                        self.flash_locations.append(neighbour)
                        self.flashes += 1
                    else:
                        self.grid[neighbour.y][neighbour.x] += 1



    def get_neighbours(self, location: Point) -> List[Point]:
        neighbours: List[Point] = []
        for y in range(location.y - 1, location.y + 2):
            if y < 0 or y >= self.height:
                continue

            for x in range(location.x - 1, location.x + 2):
                if x < 0 or x >= self.width:
                    continue

                neighbours.append(Point(x, y))

        return neighbours



    def __str__(self) -> str:
        output: str = ''
        for row in self.grid:
            for e in row:
                if e == 0:
                    output += f"\033[1m{e}\033[0m"
                else:
                    output += str(e)
            output += '\n'
        return output



def main():
    grid = read_grid()

    clear_screen()
    print(f'Before any steps:')
    print(grid)

    for step in range(100):
        grid.step()
        clear_screen()
        print(f'After step {step+1}:')
        print(grid)
        sleep(0.05)

    print(f'Answer: {grid.flashes}')



def read_grid() -> Grid:
    with open('input.txt') as f:
        return Grid([[int(e) for e in l.strip()] for l in f])


def clear_screen():
    os.system('clear')


if __name__ == '__main__':
    main()
