#!/usr/bin/env python3

WINDOW_SIZE = 3

def main():
    depths = read_depths()

    increase_count = 0
    last_window_sum = None

    for i in range(len(depths) - WINDOW_SIZE + 1):
        next_window_sum = sum(depths[i:i+WINDOW_SIZE])

        if last_window_sum and next_window_sum > last_window_sum:
            increase_count += 1

        last_window_sum = next_window_sum


    print(f'Answer: {increase_count}')

def read_depths():
    with open('input.txt') as f:
        return [int(x) for x in f]

if __name__ == '__main__':
    main()
