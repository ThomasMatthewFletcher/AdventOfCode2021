#!/usr/bin/env python3
from typing import List, Optional
from statistics import median

MATCHING_CHAR = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

CHAR_SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def main():
    lines = read_lines()

    scores: List[int] = []

    for line in lines:
        completion_chars = get_completion_chars(line)

        if completion_chars:
            score = calculate_completion_score(completion_chars)
            scores.append(score)

    middle_score = median(scores)
    print(f'Answer: {middle_score}')


def get_completion_chars(line: str) -> Optional[List[str]]:
    closing_stack: List[str] = []

    for char in line:
        if char in MATCHING_CHAR:
            closing_char = MATCHING_CHAR[char]
            closing_stack.append(closing_char)
        else:
            expected_char = closing_stack.pop()
            actual_char = char

            if expected_char != actual_char:
                return None

    return list(reversed(closing_stack))


def calculate_completion_score(chars: List[str]) -> int:
    score = 0

    for char in chars:
        score *= 5
        score += CHAR_SCORES[char]

    return score


def read_lines() -> List[str]:
    with open('input.txt') as f:
        return [l.strip() for l in f]


if __name__ == '__main__':
    main()