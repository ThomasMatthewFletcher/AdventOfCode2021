#!/usr/bin/env python3
from typing import List

CYCLE_START = 6
NEW_START = 8

class Species:
    def __init__(self, initial_states: List[int]):
        self.state_counts = [0] * (NEW_START + 1)

        for state in initial_states:
            self.state_counts[state] += 1

    def increment_days(self, days: int):
        for _ in range(days):
            self.increment_day()

    def increment_day(self):
        zero_count = self.state_counts.pop(0)
        self.state_counts[CYCLE_START] += zero_count
        self.state_counts.append(zero_count)

    def count(self) -> int:
        return sum(self.state_counts)


def main():
    initial_states = read_initial_states()

    species = Species(initial_states)
    species.increment_days(80)

    answer = species.count()
    print(f'Answer: {answer}')



def read_initial_states() -> List[int]:
    with open('input.txt') as f:
        return [int(s) for s in f.readline().split(',')]

if __name__ == '__main__':
    main()
