#!/usr/bin/env python3
from __future__ import annotations
from typing import NamedTuple, Set, List
from dataclasses import dataclass
import re

class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __repr__(self):
        return f'({self.x},{self.y},{self.z})'

@dataclass
class Cuboid:
    min_point: Point
    max_point: Point

    def get_points(self) -> Set[Point]:
        points: Set[Point] = set()

        for x in range(self.min_point.x, self.max_point.x):
            for y in range(self.min_point.y, self.max_point.y):
                for z in range(self.min_point.z, self.max_point.z):
                    points.add(Point(x,y,z))

        return points

    def intersects(self, other: Cuboid) -> bool:
        return (
            (other.max_point.x > self.min_point.x) and
            (other.max_point.y > self.min_point.y) and
            (other.max_point.z > self.min_point.z) and
            (self.max_point.x > other.min_point.x) and
            (self.max_point.y > other.min_point.y) and
            (self.max_point.z > other.min_point.z)
        )

class Step(NamedTuple):
    on: bool
    cuboid: Cuboid

def main():
    steps = read_steps()

    on_points: Set[Point] = set()

    initialization_region = Cuboid(Point(-50,-50,-50), Point(51,51,51))

    for step in steps:
        if not step.cuboid.intersects(initialization_region):
            continue

        points = step.cuboid.get_points()

        if step.on:
            on_points = on_points.union(points)
        else:
            on_points = on_points.difference(points)

        # print(on_points)
    print(len(on_points))

def read_steps() -> List[Step]:
    with open('input.txt') as f:
        return [parse_step(line) for line in f]


def parse_step(line: str) -> Step:
    match = re.match(r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', line)
    assert match

    on = match.group(1) == 'on'

    min_x = int(match.group(2))
    max_x = int(match.group(3)) + 1
    min_y = int(match.group(4))
    max_y = int(match.group(5)) + 1
    min_z = int(match.group(6))
    max_z = int(match.group(7)) + 1

    cuboid = Cuboid(
        Point(min_x, min_y, min_z),
        Point(max_x, max_y, max_z)
    )

    return Step(on, cuboid)


if __name__ == '__main__':
    main()
