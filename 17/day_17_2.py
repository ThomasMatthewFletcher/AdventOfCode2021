#!/usr/bin/env python3
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List

@dataclass
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector):
        return Vector(
            self.x + other.x,
            self.y + other.y
        )


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
            self.velocity += Vector(-1, 0)
        elif self.velocity.x < 0:
            self.velocity += Vector(1, 0)

        # Gravity
        self.velocity += Vector(0, -1)


def main():
    target = read_target_area()
    velocities = find_valid_velocities(target)

    print(f'Answer: {len(velocities)}')


def find_valid_velocities(target: Area) -> List[Vector]:
    min_v_x = get_min_velocity_x(target.x_min)
    max_v_x = target.x_max

    max_v_y = -target.y_min
    min_v_y = target.y_min

    valid_velocities: List[Vector] = []

    for y in range(max_v_y, min_v_y - 1, -1):
        for x in range(min_v_x, max_v_x + 1):
            velocity = Vector(x, y)
            hit = test_velocity(target, velocity)

            if hit:
                # print(velocity)
                valid_velocities.append(velocity)

    return valid_velocities

def get_min_velocity_x(dist: int) -> int:
    total = 0
    i = 0

    while total < dist:
        i += 1
        total += i

    return i


def test_velocity(target: Area, v: Vector) -> bool:
    probe = Probe(v)
    hit = False

    while not hit:
        probe.step()
        hit = target.contains(probe.position)

        if (probe.position.x > target.x_max or probe.position.y < target.y_min):
            break

    return hit



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
