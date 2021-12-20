#!/usr/bin/env python3
from __future__ import annotations
from typing import List, Tuple

class Pixel:
    ON = '#'
    OFF = '.'

class Image:
    def __init__(self, data: List[str], infinite_pixels: str):
        self.data = data
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.infinite_pixels = infinite_pixels

    def enhance(self, algorithm: str) -> Image:
        new_image_data: List[str] = []

        for y in range(-1, self.height + 1):
            new_image_line = ''
            for x in range(-1, self.width + 1):
                new_image_line += self.enhance_pixel(x, y, algorithm)

            new_image_data.append(new_image_line)

        new_infinite_pixels = self.enhance_infinite_pixels(algorithm)

        return Image(new_image_data, new_infinite_pixels)

    def enhance_infinite_pixels(self, algorithm: str) -> str:
        if self.infinite_pixels == Pixel.OFF:
            return algorithm[0]
        else:
            return algorithm[511]

    def enhance_pixel(self, x: int, y: int, algorithm: str) -> str:
        algorithm_index = 0
        for yd in range(-1, 2):
            yo = y + yd

            for xd in range(-1, 2):
                algorithm_index <<= 1
                xo = x + xd

                pixel = self.get_pixel_at(xo, yo)

                if pixel == Pixel.ON:
                    algorithm_index += 1

        return algorithm[algorithm_index]

    def get_pixel_at(self, x: int, y: int) -> str:
        if x < 0 or x >= self.width:
            return self.infinite_pixels

        if y < 0 or y >= self.height:
            return self.infinite_pixels

        return self.data[y][x]

    def count_lit_pixels(self):
        count = 0
        for line in self.data:
            count += sum(1 for p in line if p == Pixel.ON)
        return count

    def __str__(self):
        return '\n'.join(self.data)

def main():
    (algorithm, image) = read_input()

    image = image.enhance(algorithm)
    image = image.enhance(algorithm)

    count = image.count_lit_pixels()
    print(f'Answer: {count}')



def read_input() -> Tuple[str, Image]:
    with open('input.txt') as f:
        algorithm = f.readline().strip()
        f.readline()

        image = Image([line.strip() for line in f.readlines()], Pixel.OFF)

    return algorithm, image

if __name__ == '__main__':
    main()
