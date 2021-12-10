#!/usr/bin/env python3
from typing import List, Optional

MATCHING_CHAR = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

CHAR_SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}


def main():
    lines = read_lines()

    score = 0

    for line in lines:
        incorrect_char = get_first_incorrect_char(line)

        if incorrect_char:
            score += CHAR_SCORES[incorrect_char]

    print(f'Answer: {score}')


def get_first_incorrect_char(line: str) -> Optional[str]:
    closing_stack: List[str] = []

    for char in line:
        if char in MATCHING_CHAR:
            closing_char = MATCHING_CHAR[char]
            closing_stack.append(closing_char)
        else:
            expected_char = closing_stack.pop()
            actual_char = char

            if expected_char != actual_char:
                return actual_char

    return None


def read_lines() -> List[str]:
    with open('input.txt') as f:
        return [l.strip() for l in f]


if __name__ == '__main__':
    main()