#!/usr/bin/env python3
from collections import defaultdict
from typing import NamedTuple, Dict


def main():
    (polymer, rules) = read_input()

    pair_counts = count_pairs(polymer)
    element_counts = count_elements(polymer)

    for _ in range(40):
        pair_counts = step(pair_counts, element_counts, rules)

    max_count = max(element_counts.values())
    min_count = min(element_counts.values())

    answer = max_count - min_count

    print(f'Answer: {answer}')


def step(pair_counts: Dict[str, int], element_counts: Dict[str, int], rules: Dict[str, str]) -> Dict[str, int]:
    new_pair_counts: Dict[str, int] = defaultdict(int)

    for (pair, count) in pair_counts.items():
        insert_element = rules[pair]
        new_pair_1 = pair[0] + insert_element
        new_pair_2 = insert_element + pair[1]
        new_pair_counts[new_pair_1] += count
        new_pair_counts[new_pair_2] += count
        element_counts[insert_element] += count

    return new_pair_counts


def count_pairs(polymer: str) -> Dict[str, int]:
    pair_counts: Dict[str, int] = defaultdict(int)

    for i in range(len(polymer) - 1):
        pair = polymer[i:i+2]
        pair_counts[pair] += 1

    return pair_counts


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
