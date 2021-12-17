#!/usr/bin/env python3
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class Vector:
    x: int
    y: int

    def __iadd__(self, other: Vector):
        self.x += other.x
        self.y += other.y
        return self


@dataclass
class Area:
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def contains(self, p: Vector) -> bool:
        return (
            p.x >= self.x_min and
            p.x <= self.x_max and
            p.y >= self.y_min and
            p.y <= self.y_max
        )


class Probe:
    def __init__(self, velocity: Vector):
        self.position = Vector(0, 0)
        self.velocity = velocity

    def step(self):
        self.position += self.velocity

        # Drag
        if self.velocity.x > 0:
            self.velocity.x -= 1
        elif self.velocity.x < 0:
            self.velocity.x += 1

        # Gravity
        self.velocity.y -= 1


def main():
    target = read_target_area()

    highest_point = find_highest_point(target)

    if highest_point:
        print(f'Answer: {highest_point}')


def find_highest_point(target: Area) -> Optional[int]:
    min_v_x = get_min_velocity_x(target.x_min)
    max_v_x = target.x_max

    max_v_y = -target.y_min
    min_v_y = 0

    for y in range(max_v_y, min_v_y, -1):
        for x in range(min_v_x, max_v_x + 1):

            highest_point = test_velocity(target, Vector(x, y))

            if highest_point:
                return highest_point

    return None

def get_min_velocity_x(dist: int) -> int:
    total = 0
    i = 0

    while total < dist:
        i += 1
        total += i

    return i


def test_velocity(target: Area, v: Vector) -> Optional[int]:
    probe = Probe(v)
    hit = False

    largest_y = 0

    while not hit:
        probe.step()

        if probe.position.y > largest_y:
            largest_y = probe.position.y

        hit = target.contains(probe.position)

        if (probe.position.x > target.x_max or probe.position.y < target.y_min):
            return None

    return largest_y



def read_target_area() -> Area:
    with open('input.txt') as f:
        line = f.readline()

    match = re.match(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', line)

    assert match

    x_min = int(match.group(1))
    x_max = int(match.group(2))
    y_min = int(match.group(3))
    y_max = int(match.group(4))

    return Area(x_min, x_max, y_min, y_max)


if __name__ == '__main__':
    main()
