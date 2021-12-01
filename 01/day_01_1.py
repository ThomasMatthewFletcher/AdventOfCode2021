#!/usr/bin/env python3

def main():
    depths = read_depths()

    last = None
    increase_count = 0

    for depth in depths:
        if last and depth > last:
            increase_count += 1
        last = depth

    print(f'Answer: {increase_count}')

def read_depths():
    with open('input.txt') as f:
        return [int(x) for x in f]

if __name__ == '__main__':
    main()
