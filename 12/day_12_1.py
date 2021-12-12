#!/usr/bin/env python3
from __future__ import annotations
from typing import List, Dict


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.is_big = self.name.isupper()
        self.adjacent_caves: List[Cave] = []

    def add_adjacent_cave(self, other: Cave):
        self.adjacent_caves.append(other)

    def get_adjacent_caves(self):
        return self.adjacent_caves

    def __repr__(self) -> str:
        return self.name

Path = List[Cave]

class Map:
    def __init__(self):
        self.caves: Dict[str, Cave] = {}

    def get_cave(self, name: str) -> Cave:
        # Create a new cave if it doesn't exist
        if name not in self.caves:
            self.caves[name] = Cave(name)

        return self.caves[name]

    def add_connection(self, cave_a_name: str, cave_b_name: str):
        cave_a = self.get_cave(cave_a_name)
        cave_b = self.get_cave(cave_b_name)

        cave_a.add_adjacent_cave(cave_b)
        cave_b.add_adjacent_cave(cave_a)

    def get_all_paths(self) -> List[Path]:

        start_cave = self.get_cave('start')
        end_cave = self.get_cave('end')

        complete_paths: List[Path] = []
        partial_paths: List[Path] = [[start_cave]]

        while partial_paths:
            current_path = partial_paths.pop(0)
            current_cave = current_path[-1]

            next_caves = current_cave.get_adjacent_caves()
            next_caves = [c for c in next_caves if c.is_big or c not in current_path]

            for next_cave in next_caves:
                next_path = current_path.copy()
                next_path.append(next_cave)

                if (next_cave == end_cave):
                    complete_paths.append(next_path)
                else:
                    partial_paths.append(next_path)

        return complete_paths


def main():
    map = read_map()
    all_paths = map.get_all_paths()

    print(f'Answer: {len(all_paths)}')



def read_map() -> Map:
    map = Map()
    with open('input.txt') as f:
        for line in f:
            line = line.strip()
            [cave_a, cave_b] = line.split('-')
            map.add_connection(cave_a, cave_b)
    return map


if __name__ == '__main__':
    main()
