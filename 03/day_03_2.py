#!/usr/bin/env python3
from typing import List
from enum import Enum

class BitCriteria(Enum):
    MOST_COMMON = 1
    LEAST_COMMON = 2

def main():
    report = read_report()

    oxygen_generator_rating = filter_values(report, BitCriteria.MOST_COMMON)
    co2_scrubber_rating = filter_values(report, BitCriteria.LEAST_COMMON)

    oxygen_generator_rating = int(oxygen_generator_rating, 2)
    co2_scrubber_rating = int(co2_scrubber_rating, 2)

    answer = oxygen_generator_rating * co2_scrubber_rating
    print(f'Answer: {answer}')


def filter_values(values: List[str], bit_criteria: BitCriteria) -> str:
    for bit in range(len(values[0])):
        bits = [int(v[bit]) for v in values]

        ones = sum(bits)
        zeros = len(values) - ones

        if ones >= zeros:
            most_common = 1
        else:
            most_common = 0

        if bit_criteria == BitCriteria.MOST_COMMON:
            keep_bit = most_common
        else:
            keep_bit = 1 - most_common

        values = [v for v in values if int(v[bit]) == keep_bit]

        if len(values) == 1:
            break

    return values[0]


def read_report() -> List[str]:
    with open('input.txt') as f:
        return [l.strip() for l in f]

if __name__ == '__main__':
    main()
