#!/usr/bin/env python3
from collections import defaultdict
from typing import NamedTuple, Dict


def main():
    (polymer, rules) = read_input()

    for _ in range(10):
        polymer = step(polymer, rules)

    element_counts = count_elements(polymer)
    max_count = max(element_counts.values())
    min_count = min(element_counts.values())

    answer = max_count - min_count

    print(f'Answer: {answer}')


def step(polymer: str, rules: Dict[str, str]) -> str:
    new_polymer = polymer[0]

    for i in range(len(polymer) - 1):
        elements = polymer[i:i+2]
        insert_element = rules[elements]
        new_polymer += insert_element + elements[1]

    return new_polymer


def count_elements(polymer: str) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)

    for element in polymer:
        counts[element] += 1

    return counts


class Input(NamedTuple):
    template: str
    rules: Dict[str, str]

def read_input() -> Input:
    with open('input.txt') as f:
        [template, rules_str] = f.read().split('\n\n')

    template = template.strip()
    rules: Dict[str, str] = {}

    for rule in rules_str.strip().split('\n'):
        [from_elements, insert_element] = rule.split(' -> ')
        rules[from_elements] = insert_element

    return Input(template, rules)


if __name__ == '__main__':
    main()
