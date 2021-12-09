#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List

@dataclass
class Map:
    map: List[List[int]]

    def __post_init__(self):
        self.height = len(self.map)
        self.width = len(self.map[0])

    def __str__(self) -> str:
        lines: List[str] = []

        for y in range(self.height):
            line: List[str] = []
            for x in range(self.width):
                height = str(self.map[y][x])

                if self.is_low_point(x, y):
                    height = f"\033[1m{height}\033[0m"

                line.append(height)

            lines.append(''.join(line))

        return '\n'.join(lines)

    def get_low_points(self) -> List[int]:
        low_points: List[int] = []

        for y in range(self.height):
            for x in range(self.width):
                if self.is_low_point(x, y):
                    low_points.append(self.map[y][x])

        return low_points

    def is_low_point(self, x: int, y: int) -> bool:
        point = self.map[y][x]

        if x > 0 and self.map[y][x-1] <= point:
            return False

        if x < self.width - 1 and self.map[y][x+1] <= point:
            return False

        if y > 0 and self.map[y-1][x] <= point:
            return False

        if y < self.height - 1 and self.map[y+1][x] <= point:
            return False

        return True


def main():
    map = read_map()

    low_points = map.get_low_points()

    answer = sum(low_points) + len(low_points)
    print(f'Answer: {answer}')


def read_map() -> Map:
    with open('input.txt') as f:
        return Map([[int(x) for x in l.strip()] for l in f])


if __name__ == '__main__':
    main()
