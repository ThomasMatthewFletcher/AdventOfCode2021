#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple, Set

@dataclass(frozen=True)
class Vector:
    x: int
    y: int
    z: int

    def roll(self, turns: int) -> Vector:
        cos = Vector.simple_cos(turns)
        sin = Vector.simple_sin(turns)

        return Vector(
            self.x,
            cos*self.y + sin*self.z,
            -sin*self.y + cos*self.z
        )

    def pitch(self, turns: int) -> Vector:
        cos = Vector.simple_cos(turns)
        sin = Vector.simple_sin(turns)

        return Vector(
            cos*self.x - sin*self.z,
            self.y,
            sin*self.x + cos*self.z
        )

    def yaw(self, turns: int) -> Vector:
        cos = Vector.simple_cos(turns)
        sin = Vector.simple_sin(turns)

        return Vector(
            cos*self.x + sin*self.y,
            -sin*self.x + cos*self.y,
            self.z
        )

    @staticmethod
    def simple_cos(turns: int) -> int:
        turns %= 4
        return [1,0,-1,0][turns]

    @staticmethod
    def simple_sin(turns: int) -> int:
        turns %= 4
        return [0,1,0,-1][turns]

    def __add__(self, other: Vector) -> Vector:
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other: Vector) -> Vector:
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __repr__(self) -> str:
        return f'({self.x},{self.y},{self.z})'



class Scanner:
    def __init__(self, id: int):
        self.id = id
        self.beacon_signals: Set[Vector] = set()
        self.orientations: List[Set[Vector]] = [set() for _ in range(24)]
        self.abs_beacons: Optional[Set[Vector]] = None

    def add_beacon_signal(self, b: Vector):
        self.beacon_signals.add(b)

        orientation_index = 0

        for roll in range(4):
            r = b.roll(roll)
            for pitch in range(4):
                o = r.pitch(pitch)
                self.orientations[orientation_index].add(o)
                orientation_index += 1

        for yaw in [-1, 1]:
            y = b.yaw(yaw)
            for pitch in range(4):
                o = y.pitch(pitch)
                self.orientations[orientation_index].add(o)
                orientation_index += 1

    def set_absolute_location(self, pos: Vector, orientation_index: int):
        self.abs_beacons = offset_all(self.orientations[orientation_index], pos)


def main():
    scanners = read_scanners()

    scanners[0].set_absolute_location(Vector(0,0,0), 0)

    known_scanners = [scanners[0]]
    unchecked_scanners = [scanners[0]]

    while unchecked_scanners and (len(known_scanners) != len(scanners)):
        this_scanner = unchecked_scanners.pop(0)
        print(f'Looking at scanner {this_scanner.id}')

        for other_scanner in scanners:
            if other_scanner in known_scanners:
                continue

            print(f'Comparing to scanner {other_scanner.id}')

            overlap_location = get_overlap(this_scanner, other_scanner)

            if (overlap_location):
                (relative_pos, orientation_index) = overlap_location
                # other_scanner_pos = this_scanner.abs_position + relative_pos
                # print(relative_pos)
                other_scanner.set_absolute_location(relative_pos, orientation_index)
                known_scanners.append(other_scanner)
                unchecked_scanners.append(other_scanner)

    beacons: Set[Vector] = set()

    for scanner in scanners:
        assert scanner.abs_beacons
        for beacon in scanner.abs_beacons:
            beacons.add(beacon)

    print(f'Answer: {len(beacons)}')


def get_overlap(scanner_a: Scanner, scanner_b: Scanner) -> Optional[Tuple[Vector, int]]:
    beacons_a = scanner_a.abs_beacons
    assert beacons_a
    for orientation_index in range(24):
        # print(f'Orientation: {orientation_index}')
        beacons_b = scanner_b.orientations[orientation_index]
        offset_position = get_offset_position(beacons_a, beacons_b)

        if offset_position:
            print('FOUND')
            print(offset_position)
            return (offset_position, orientation_index)

    return None


def get_offset_position(beacons_a: Set[Vector], beacons_b: Set[Vector]) -> Optional[Vector]:

    for anchor_a in beacons_a:
        for anchor_b in beacons_b:
            # print(f'Trying anchor: {anchor_a} to {anchor_b}')
            offset = anchor_a - anchor_b
            beacons_b_offset = offset_all(beacons_b, offset)
            # print(beacons_b_offset)

            common_beacons = beacons_a.intersection(beacons_b_offset)

            if len(common_beacons) >= 12:
                return offset

    return None


def offset_all(beacons: Set[Vector], offset: Vector) -> Set[Vector]:
    return {b + offset for b in beacons}

def read_scanners() -> List[Scanner]:
    with open('input.txt') as f:
        text = f.read()

    scanner_texts = text.split('\n\n')
    return [parse_scanner(s) for s in scanner_texts]

def parse_scanner(scanner_text: str) -> Scanner:
    scanner_lines = scanner_text.strip().split('\n')
    id_line = scanner_lines[0]
    scanner_id = int(id_line.split()[2])

    scanner = Scanner(scanner_id)

    for beacon_text in scanner_lines[1:]:
        b = parse_beacon(beacon_text)
        scanner.add_beacon_signal(b)

    return scanner

def parse_beacon(beacon_text: str) -> Vector:
    parts = beacon_text.strip().split(',')
    return Vector(
        int(parts[0]),
        int(parts[1]),
        int(parts[2])
    )

if __name__ == '__main__':
    main()
