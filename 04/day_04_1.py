#!/usr/bin/env python3
from typing import List, NamedTuple, Optional

BOARD_SIZE = 5

class Board:
    def __init__(self, numbers: List[List[int]]):
        self.numbers = numbers
        self.called = [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def call_number(self, number: int):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.numbers[y][x] == number:
                    self.called[y][x] = True
                    return

    def is_win(self):
        # Check rows:
        for row in self.called:
            if all(row):
                return True

        # Check cols
        for x in range(BOARD_SIZE):
            if self._is_col_called(x):
                return True

        return False

    def get_uncalled_sum(self):
        sum = 0
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if not self.called[y][x]:
                    sum += self.numbers[y][x]
        return sum

    def _is_col_called(self, x: int):
        for y in range(BOARD_SIZE):
            if not self.called[y][x]:
                return False

        return True

    def cell_to_str(self, x: int, y: int) -> str:
        number = self.numbers[y][x]
        called = self.called[y][x]

        if called:
            return f"\033[1m{number:2}\033[0m"

        return f"{number:2}"

    def __str__(self):
        lines: List[str] = []

        for y in range(BOARD_SIZE):
            line: List[str] = []
            for x in range(BOARD_SIZE):
                line.append(self.cell_to_str(x, y) + '')

            lines.append(' '.join(line))

        return '\n'.join(lines)


class Bingo:
    def __init__(self, boards: List[Board]):
        self.boards = boards

    def call_number(self, number: int):
        for board in self.boards:
            board.call_number(number)

    def get_winning_board(self) -> Optional[Board]:
        for board in self.boards:
            if board.is_win():
                return board

        return None


class Input(NamedTuple):
    draw_order: List[int]
    boards: List[Board]


def main():
    input = read_input()
    bingo = Bingo(input.boards)

    winning_board = None
    draw_number = None

    for draw_number in input.draw_order:
        bingo.call_number(draw_number)

        winning_board = bingo.get_winning_board()

        if winning_board:
            break

    print('Winning Board:')
    print(winning_board)
    print()

    if draw_number and winning_board:
        uncalled_sum = winning_board.get_uncalled_sum()
        answer = uncalled_sum * draw_number

        print(f'Uncalled Sum: {uncalled_sum}')
        print(f'Draw Number: {draw_number}')
        print(f'Answer: {answer}')


def read_input() -> Input:
    with open('input.txt') as f:
        parts = f.read().strip().split('\n\n')

    draw_order_line = parts.pop(0)
    draw_order = [int(n) for n in draw_order_line.split(',')]

    boards: List[Board] = []

    for part in parts:
        numbers = [[int(n) for n in line.split()] for line in part.split('\n')]
        boards.append(Board(numbers))

    return Input(draw_order, boards)


if __name__ == '__main__':
    main()
