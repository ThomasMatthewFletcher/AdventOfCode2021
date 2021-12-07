#!/usr/bin/env python3
from typing import List

def main():
    positions = read_positions()
    p = median(positions)
    fuel = calculate_fuel(positions, p)

    print(f'Answer: {fuel}')

def calculate_fuel(positions: List[int], p: int):
    total = 0
    for x in positions:
        total += abs(x - p)
    return total

def median(values: List[int]):
    middle_index = len(values) // 2
    return sorted(values)[middle_index]

def read_positions() -> List[int]:
    with open('input.txt') as f:
        return [int(p) for p in f.readline().split(',')]

if __name__ == '__main__':
    main()
