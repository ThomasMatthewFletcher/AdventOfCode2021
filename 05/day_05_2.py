#!/usr/bin/env python3
from __future__ import annotations
from typing import List, Optional, DefaultDict
from collections import defaultdict
import re


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __str__(self) -> str:
        return f'{self.x},{self.y}'


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def get_points(self) -> List[Point]:
        current_point = self.p1
        points = [current_point]

        diff = self.p2 - self.p1

        dx = Line._get_direction(diff.x)
        dy = Line._get_direction(diff.y)

        delta = Point(dx, dy)

        while current_point != self.p2:
            current_point += delta
            points.append(current_point)

        return points

    @staticmethod
    def _get_direction(diff: int) -> int:
        if diff > 0:
            return 1
        if diff < 0:
            return -1
        return 0

    def __str__(self):
        return f'{self.p1} -> {self.p2}'


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
