#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List

DIGIT_LENGTHS = [2, 3, 4, 7]

@dataclass
class Display:
    configurations: List[str]
    outputs: List[str]

    def count_digits_with_lengths(self):
        output_lengths = [len(o) for o in self.outputs]
        return sum([1 for l in output_lengths if l in DIGIT_LENGTHS])


def main():
    displays = read_displays()

    total_selected_digits = sum(d.count_digits_with_lengths() for d in displays)

    print(f'Answer: {total_selected_digits}')

def read_displays() -> List[Display]:
    with open('input.txt') as f:
        return [parse_display(l) for l in f]

def parse_display(line: str):
    configurations, outputs = line.split('|')
    configurations = configurations.split()
    outputs = outputs.split()
    return Display(configurations, outputs)


if __name__ == '__main__':
    main()
