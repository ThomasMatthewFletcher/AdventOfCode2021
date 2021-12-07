#!/usr/bin/env python3
from typing import List

def main():
    positions = read_positions()

    min_p = min(positions)
    max_p = max(positions)


    fuel_required = [calculate_total_fuel(positions, p) for p in range(min_p, max_p + 1)]
    min_fuel = min(fuel_required)
    print(f'Answer: {min_fuel}')


def calculate_total_fuel(positions: List[int], p: int):
    return sum([calculate_fuel_between(a, p) for a in positions])

def calculate_fuel_between(a: int, b: int):
    n = abs(b - a)
    return n*(n+1)//2

def read_positions() -> List[int]:
    with open('input.txt') as f:
        return [int(p) for p in f.readline().split(',')]

if __name__ == '__main__':
    main()
