#!/usr/bin/env python3
from typing import List, Dict, Tuple, NamedTuple, Optional
from queue import PriorityQueue

class Point(NamedTuple):
    x: int
    y: int

Path = List[Point]

class Map:
    def __init__(self, risk_levels: List[List[int]]):
        self.risk_levels: List[List[int]] = []

        original_height = len(risk_levels)
        original_width = len(risk_levels[0])

        for grid_row in range(5):
            for y in range(original_height):
                row: List[int] = []
                for grid_col in range(5):
                    for x in range(original_width):
                        risk_level = ((risk_levels[y][x] + grid_row + grid_col - 1) % 9) + 1
                        row.append(risk_level)

                self.risk_levels.append(row)

        self.width = len(self.risk_levels[0])
        self.height = len(self.risk_levels)

    def find_lowest_path_risk(self, source: Point, target: Point) -> Optional[int]:
        queue: PriorityQueue[Tuple[int, Point]] = PriorityQueue()

        dist: Dict[Point, int] = {}
        dist[source] = 0
        queue.put((0, source))

        prev: Dict[Point, Point] = {}

        while queue:
            (_, this_point) = queue.get()

            if this_point == target:
                return dist[this_point]

            neighbours = self.get_neighbours(this_point)

            for neighbour in neighbours:
                this_dist_to_neighbour = dist[this_point] + self.risk_levels[neighbour.y][neighbour.x]
                current_dist_to_neighbour = dist.get(neighbour)

                if not current_dist_to_neighbour or this_dist_to_neighbour < current_dist_to_neighbour:
                    dist[neighbour] = this_dist_to_neighbour
                    prev[neighbour] = this_point

                    queue.put((this_dist_to_neighbour, neighbour))

        return None

    def get_neighbours(self, p: Point) -> List[Point]:
        neighbours: List[Point] = []

        if p.x > 0:
            neighbours.append(Point(p.x - 1, p.y))

        if p.x < self.width - 1:
            neighbours.append(Point(p.x + 1, p.y))

        if p.y > 0:
            neighbours.append(Point(p.x, p.y - 1))

        if p.y < self.height - 1:
            neighbours.append(Point(p.x, p.y + 1))

        return neighbours

    def __str__(self) -> str:
        output = ''

        for y in range(self.height):
            for x in range(self.width):
                output += str(self.risk_levels[y][x])
            output += '\n'

        return output


def main():
    m = read_map()

    source = Point(0, 0)
    target = Point(m.width - 1, m.height - 1)

    risk = m.find_lowest_path_risk(source, target)
    print(f'Answer: {risk}')


def read_map() -> Map:
    risk_levels: List[List[int]] = []

    with open('input.txt') as f:
        for line in f:
            row = [int(r) for r in line.strip()]
            risk_levels.append(row)

    return Map(risk_levels)

if __name__ == '__main__':
    main()
