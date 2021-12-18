#!/usr/bin/env python3
from __future__ import annotations
from typing import Tuple, Optional, List
import re


class SnailfishNumber:
    def __init__(self, left: SnailfishNumber | int, right: SnailfishNumber | int, parent: Optional[SnailfishNumber]=None):
        self.pair = [left, right]
        self.parent: Optional[SnailfishNumber] = parent

    def magnitude(self) -> int:
        if isinstance(self.pair[0], int):
            left_val = self.pair[0]
        else:
            left_val = self.pair[0].magnitude()

        if isinstance(self.pair[1], int):
            right_val = self.pair[1]
        else:
            right_val = self.pair[1].magnitude()

        return (left_val * 3) + (right_val * 2)

    def reduce(self):
        action_performed = True
        while action_performed:
            action_performed = self.explode()

            if not action_performed:
                action_performed = self.split()


    def explode(self, depth: int = 0) -> bool:
        if isinstance(self.pair[0], SnailfishNumber):
            if depth == 3:
                [left, right] = self.pair[0].pair
                assert isinstance(left, int)
                assert isinstance(right, int)
                self.pair[0].add_to_left(left)
                self.pair[0].add_to_right(right)
                self.pair[0] = 0
                return True
            else:
                if self.pair[0].explode(depth + 1):
                    return True

        if isinstance(self.pair[1], SnailfishNumber):
            if depth == 3:
                [left, right] = self.pair[1].pair
                assert isinstance(left, int)
                assert isinstance(right, int)
                self.pair[1].add_to_left(left)
                self.pair[1].add_to_right(right)
                self.pair[1] = 0
                return True
            else:
                if self.pair[1].explode(depth + 1):
                    return True

        return False

    def add_to_left(self, value: int):
        if not self.parent:
            return

        if self == self.parent.pair[0]:
            self.parent.add_to_left(value)
        else:
            if isinstance(self.parent.pair[0], int):
                self.parent.pair[0] += value
            else:
                self.parent.pair[0].add_to_rightmost_child(value)

    def add_to_rightmost_child(self, value: int):
        if isinstance(self.pair[1], int):
            self.pair[1] += value
        else:
            self.pair[1].add_to_rightmost_child(value)

    def add_to_right(self, value: int):
        if not self.parent:
            return

        if self == self.parent.pair[1]:
            self.parent.add_to_right(value)
        else:
            if isinstance(self.parent.pair[1], int):
                self.parent.pair[1] += value
            else:
                self.parent.pair[1].add_to_leftmost_child(value)

    def add_to_leftmost_child(self, value: int):
        if isinstance(self.pair[0], int):
            self.pair[0] += value
        else:
            self.pair[0].add_to_leftmost_child(value)

    def split(self) -> bool:
        if isinstance(self.pair[0], int):
            if self.pair[0] >= 10:
                self.pair[0] = self.split_number(self.pair[0])
                return True
        else:
            if self.pair[0].split():
                return True

        if isinstance(self.pair[1], int):
            if self.pair[1] >= 10:
                self.pair[1] = self.split_number(self.pair[1])
                return True
        else:
            if self.pair[1].split():
                return True

        return False

    def split_number(self, value: int) -> SnailfishNumber:
        left = value // 2
        right = value - left
        return SnailfishNumber(left, right, self)

    def __repr__(self):
        return str(self.pair)

    def __add__(self, other: SnailfishNumber):
        sum = SnailfishNumber(self, other)
        self.parent = sum
        other.parent = sum
        sum.reduce()
        return sum

def main():
    lines = read_snailfish_lines()

    largest_magnitude = 0

    for num_a in lines:
        for num_b in lines:
            if num_a == num_b:
                continue

            magnitude = (parse_snailfish_number(num_a) + parse_snailfish_number(num_b)).magnitude()

            if magnitude > largest_magnitude:
                largest_magnitude = magnitude

    print(f'Answer: {largest_magnitude}')

def parse_snailfish_number(s: str) -> SnailfishNumber:
    (sn, _) = parse_snailfish_number_recursive(s)
    assert isinstance(sn, SnailfishNumber)
    return sn

def parse_snailfish_number_recursive(s: str) -> Tuple[SnailfishNumber | int, str]:
    if s[0] != '[':
        match = re.search(r'^\d+', s)
        assert match
        digits = match.group()
        value = int(digits)
        return (value, s[len(digits):])

    assert s[0] == '['
    s = s[1:]

    (left, s) = parse_snailfish_number_recursive(s)

    assert s[0] == ','
    s = s[1:]

    (right, s) = parse_snailfish_number_recursive(s)

    assert s[0] == ']'
    s = s[1:]

    total = SnailfishNumber(left, right)

    if isinstance(left, SnailfishNumber):
        left.parent = total

    if isinstance(right, SnailfishNumber):
        right.parent = total

    return (total, s)

def read_snailfish_lines() -> List[str]:
    with open('input.txt') as f:
        return [l.strip() for l in f]

if __name__ == '__main__':
    main()
