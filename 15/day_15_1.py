#!/usr/bin/env python3
from typing import Set, List, Dict, NamedTuple, Optional

class Point(NamedTuple):
    x: int
    y: int

Path = List[Point]

class Map:
    def __init__(self, risk_levels: List[List[int]]):
        self.risk_levels = risk_levels
        self.width = len(self.risk_levels[0])
        self.height = len(self.risk_levels)

    def find_lowest_path_risk(self, source: Point, target: Point) -> Optional[int]:
        unvisited: Set[Point] = set()

        for y in range(self.height):
            for x in range(self.width):
                unvisited.add(Point(x, y))

        dist: Dict[Point, int] = {}
        dist[source] = 0

        prev: Dict[Point, Point] = {}

        while unvisited:

            this_point: Optional[Point] = None
            this_point_dist = None

            for p in unvisited:
                if (dist.get(p) is not None) and ((this_point_dist is None) or (dist[p] < this_point_dist)):
                    this_point = p
                    this_point_dist = dist[p]

            if not this_point:
                return

            unvisited.remove(this_point)

            if this_point == target:
                return dist[this_point]

            neighbours = self.get_neighbours(this_point)

            for neighbour in neighbours:
                if neighbour in unvisited:
                    this_dist_to_neighbour = dist[this_point] + self.risk_levels[neighbour.y][neighbour.x]
                    current_dist_to_neighbour = dist.get(neighbour)

                    if not current_dist_to_neighbour or this_dist_to_neighbour < current_dist_to_neighbour:
                        dist[neighbour] = this_dist_to_neighbour
                        prev[neighbour] = this_point

        return None


    def get_neighbours(self, p: Point) -> List[Point]:
        neighbours: List[Point] = []

        if p.x > 0:
            neighbours.append(Point(p.x -1, p.y))

        if p.x < self.width - 1:
            neighbours.append(Point(p.x + 1, p.y))

        if p.y > 0:
            neighbours.append(Point(p.x, p.y - 1))

        if p.y < self.height - 1:
            neighbours.append(Point(p.x, p.y + 1))

        return neighbours


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
