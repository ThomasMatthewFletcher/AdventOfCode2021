#!/usr/bin/env python3
from typing import List


def main():
    report = read_report()

    gamma_rate = calculate_gamma_rate(report)
    epsilon_rate = convert_gamma_to_epsilon(gamma_rate)

    gamma_rate = int(gamma_rate, 2)
    epsilon_rate = int(epsilon_rate, 2)

    answer = gamma_rate * epsilon_rate
    print(f'Answer: {answer}')


def calculate_gamma_rate(report: List[str]) -> str:
    gamma_rate = ''

    num_lines = len(report)

    for d in range(len(report[0])):
        digits = [int(l[d]) for l in report]
        ones = sum(digits)
        zeros = num_lines - ones

        if ones > zeros:
            gamma_rate += '1'
        else:
            gamma_rate += '0'

    return gamma_rate


def convert_gamma_to_epsilon(gamma_rate: str) -> str:
    epsilon_rate = ''

    for d in gamma_rate:
        if d == '1':
            epsilon_rate += '0'
        else:
            epsilon_rate += '1'

    return epsilon_rate


def read_report() -> List[str]:
    with open('input.txt') as f:
        return [l.strip() for l in f]

if __name__ == '__main__':
    main()
