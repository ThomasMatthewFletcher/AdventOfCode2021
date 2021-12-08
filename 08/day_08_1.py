#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List

@dataclass
class Display:
    configurations: List[str]
    outputs: List[str]

def main():
    displays = read_displays()

    total_selected_digits = 0

    for display in displays:
        output_lengths = [len(o) for o in display.outputs]
        selected_digits_count = sum([1 for l in output_lengths if l in [2, 3, 4, 7]])
        total_selected_digits += selected_digits_count

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
