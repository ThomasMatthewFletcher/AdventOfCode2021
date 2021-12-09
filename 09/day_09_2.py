#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List, NamedTuple

class Point(NamedTuple):
    x: int
    y: int

Region = List[Point]

@dataclass
class Map:
    map: List[List[int]]

    def __post_init__(self):
        self.height = len(self.map)
        self.width = len(self.map[0])

    def __str__(self) -> str:
        lines: List[str] = []

        for y in range(self.height):
            line: List[str] = []
            for x in range(self.width):
                height = str(self.map[y][x])

                if self.is_low_point(x, y):
                    height = f"\033[1m{height}\033[0m"

                line.append(height)

            lines.append(''.join(line))

        return '\n'.join(lines)

    def get_regions(self) -> List[Region]:
        low_points = self.get_low_points()
        regions: List[Region] = []

        for low_point in low_points:
            region = self.get_region(low_point)
            regions.append(region)

        return regions

    def get_region(self, start_point: Point) -> Region:
        region = [start_point]
        unvisited = [start_point]

        while unvisited:
            next_point = unvisited.pop()

            neighbours = self.get_neighbours(next_point)

            for neighbour in neighbours:
                if self.get_height(neighbour) == 9:
                    continue

                if neighbour in region:
                    continue

                region.append(neighbour)
                unvisited.append(neighbour)

        return region

    def get_low_points(self) -> List[Point]:
        low_points: List[Point] = []

        for y in range(self.height):
            for x in range(self.width):
                point = Point(x, y)
                if self.is_low_point(point):
                    low_points.append(point)

        return low_points

    def is_low_point(self, point: Point) -> bool:
        neighbours = self.get_neighbours(point)
        current_height = self.get_height(point)

        for neighbour in neighbours:
            if current_height >= self.get_height(neighbour):
                return False

        return True

    def get_neighbours(self, point: Point) -> List[Point]:
        neighbours: List[Point] = []

        if point.x > 0:
            neighbours.append(Point(point.x-1, point.y))

        if point.x < self.width - 1:
            neighbours.append(Point(point.x+1, point.y))

        if point.y > 0:
            neighbours.append(Point(point.x, point.y-1))

        if point.y < self.height - 1:
            neighbours.append(Point(point.x, point.y+1))

        return neighbours

    def get_height(self, point: Point) -> int:
        return self.map[point.y][point.x]


def main():
    map = read_map()

    regions = map.get_regions()
    region_sizes = [len(region) for region in regions]
    region_sizes.sort()

    mult = 1
    for region_size in region_sizes[-3:]:
        mult *= region_size

    print(f'Answer: {mult}')




def read_map() -> Map:
    with open('input.txt') as f:
        return Map([[int(x) for x in l.strip()] for l in f])


if __name__ == '__main__':
    main()
