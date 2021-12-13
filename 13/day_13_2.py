#!/usr/bin/env python3
from typing import NamedTuple, List, Set
import re


class Dot(NamedTuple):
    x: int
    y: int

class Fold(NamedTuple):
    axis: str
    pos: int

class Sheet:
    def __init__(self):
        self.dots: Set[Dot] = set()

    def add_dot(self, dot: Dot):
        self.dots.add(dot)

    def fold(self, fold: Fold):
        new_dots: Set[Dot] = set()

        for dot in self.dots:
            new_dot = dot

            if fold.axis == 'x' and dot.x > fold.pos:
                new_dot = Dot(2*fold.pos - dot.x, dot.y)
            elif fold.axis == 'y' and dot.y > fold.pos:
                new_dot = Dot(dot.x, 2*fold.pos - dot.y)

            new_dots.add(new_dot)

        self.dots = new_dots

    def count_dots(self):
        return len(self.dots)

    def __str__(self):
        output = ''

        x_positions = [d.x for d in self.dots]
        y_positions = [d.y for d in self.dots]

        min_x = min(x_positions)
        max_x = max(x_positions)
        min_y = min(y_positions)
        max_y = max(y_positions)

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if Dot(x, y) in self.dots:
                    output += '#'
                else:
                    output += ' '
            output += '\n'

        return output


class Input(NamedTuple):
    sheet: Sheet
    folds: List[Fold]


def main():
    (sheet, folds) = read_input()

    for fold in folds:
        sheet.fold(fold)

    print(sheet)


def read_input():
    with open('input.txt') as f:
        text = f.read()

    [dots_text, folds_text] = text.split('\n\n')

    sheet = Sheet()
    for dot_text in dots_text.split('\n'):
        [x, y] = dot_text.strip().split(',')
        dot = Dot(int(x), int(y))
        sheet.add_dot(dot)

    folds: List[Fold] = []

    fold_pattern = re.compile(r'(x|y)=(\d+)')

    for fold_match in fold_pattern.finditer(folds_text):
        axis = fold_match.group(1)
        pos = int(fold_match.group(2))

        folds.append(Fold(axis, pos))

    return Input(sheet, folds)








if __name__ == '__main__':
    main()
