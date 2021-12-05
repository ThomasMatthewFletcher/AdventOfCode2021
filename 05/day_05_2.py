#!/usr/bin/env python3
from typing import NamedTuple, List, Optional, DefaultDict
from collections import defaultdict
import re


class Point(NamedTuple):
    x: int
    y: int


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def get_points(self) -> List[Point]:
        current_point = self.p1
        points = [current_point]

        diff_x = self.p2.x - self.p1.x
        diff_y = self.p2.y - self.p1.y

        if diff_x > 0:
            dx = 1
        elif diff_x < 0:
            dx = -1
        else:
            dx = 0

        if diff_y > 0:
            dy = 1
        elif diff_y < 0:
            dy = -1
        else:
            dy = 0

        while current_point != self.p2:
            next_x = current_point.x + dx
            next_y = current_point.y + dy
            current_point = Point(next_x, next_y)
            points.append(current_point)

        return points

    def __str__(self):
        return f'{self.p1.x},{self.p1.y} -> {self.p2.x},{self.p2.y}'


class Map:
    def __init__(self):
        self.points: DefaultDict[Point, int] = defaultdict(int)

    def add_line(self, line: Line):
        points = line.get_points()

        for point in points:
            self.points[point] += 1

    def count_overlapping_points(self):
        return sum(1 for count in self.points.values() if count >= 2)


def main():
    lines = read_lines()
    map = Map()

    for line in lines:
        map.add_line(line)

    answer = map.count_overlapping_points()
    print(f'Answer: {answer}')


def read_lines() -> List[Line]:
    with open('input.txt') as f:
        lines = [parse_line(l) for l in f]
        return list(filter(None, lines))

def parse_line(line: str) -> Optional[Line]:
    match = re.search(r'(\d+),(\d+) -> (\d+),(\d+)', line)

    if not match:
        return

    x1 = int(match.group(1))
    y1 = int(match.group(2))
    x2 = int(match.group(3))
    y2 = int(match.group(4))

    return Line(Point(x1, y1), Point(x2, y2))

if __name__ == '__main__':
    main()
