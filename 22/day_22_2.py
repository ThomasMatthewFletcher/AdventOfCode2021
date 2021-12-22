#!/usr/bin/env python3
from __future__ import annotations
from typing import NamedTuple, Set, List, Optional
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

    def get_volume(self) -> int:
        width  = abs(self.max_point.x - self.min_point.x)
        height = abs(self.max_point.y - self.min_point.y)
        depth  = abs(self.max_point.z - self.min_point.z)
        return width * height * depth

    def subtract(self, other: Cuboid) -> List[Cuboid]:

        cuboids: List[Cuboid] = []

        # Left
        cuboid = create_cuboid(self,
            Point(self.min_point.x, self.min_point.y, self.min_point.z),
            Point(other.min_point.x, self.max_point.y, self.max_point.z)
        )
        if cuboid:
            cuboids.append(cuboid)

        # Middle Top
        cuboid = create_cuboid(self,
            Point(other.min_point.x, other.max_point.y, self.min_point.z),
            Point(other.max_point.x, self.max_point.y, self.max_point.z)
        )
        if cuboid:
            cuboids.append(cuboid)

        # Middle Back
        cuboid = create_cuboid(self,
            Point(other.min_point.x, other.min_point.y, self.min_point.z),
            Point(other.max_point.x, other.max_point.y, other.min_point.z)
        )
        if cuboid:
            cuboids.append(cuboid)


        # Middle Front
        cuboid = create_cuboid(self,
            Point(other.min_point.x, other.min_point.y, other.max_point.z),
            Point(other.max_point.x, other.max_point.y, self.max_point.z)
        )
        if cuboid:
            cuboids.append(cuboid)


        # Middle Bottom
        cuboid = create_cuboid(self,
            Point(other.min_point.x, self.min_point.y, self.min_point.z),
            Point(other.max_point.x, other.min_point.y, self.max_point.z)
        )
        if cuboid:
            cuboids.append(cuboid)


        # Right
        cuboid = create_cuboid(self,
            Point(other.max_point.x, self.min_point.y, self.min_point.z),
            Point(self.max_point.x, self.max_point.y, self.max_point.z)
        )
        if cuboid:
            cuboids.append(cuboid)

        return cuboids


def create_cuboid(contain: Cuboid, min_point: Point, max_point: Point) -> Optional[Cuboid]:
    min_point_x = max(min_point.x, contain.min_point.x)
    min_point_y = max(min_point.y, contain.min_point.y)
    min_point_z = max(min_point.z, contain.min_point.z)

    min_point = Point(min_point_x, min_point_y, min_point_z)

    max_point_x = min(max_point.x, contain.max_point.x)
    max_point_y = min(max_point.y, contain.max_point.y)
    max_point_z = min(max_point.z, contain.max_point.z)

    max_point = Point(max_point_x, max_point_y, max_point_z)

    if min_point.x >= max_point.x or min_point.y >= max_point.y or min_point.z >= max_point.z:
        return None

    return Cuboid(min_point, max_point)



class Step(NamedTuple):
    on: bool
    cuboid: Cuboid

def main():
    steps = read_steps()

    cuboids: List[Cuboid] = []

    step_count = 1

    for step in steps:
        print('Step', step_count)
        step_count += 1
        new_cuboids: List[Cuboid] = []
        for cuboid in cuboids:
            if cuboid.intersects(step.cuboid):
                new_cuboids.extend(cuboid.subtract(step.cuboid))
            else:
                new_cuboids.append(cuboid)

        if step.on:
            new_cuboids.append(step.cuboid)

        cuboids = new_cuboids
        # print(cuboids)

    total_volume = sum([c.get_volume() for c in cuboids])
    print(f'Answer: {total_volume}')

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
