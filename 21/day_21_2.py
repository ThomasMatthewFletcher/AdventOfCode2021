#!/usr/bin/env python3
from typing import Dict, DefaultDict, List, Tuple
from collections import defaultdict

WINNING_SCORE = 21
DIE_MAX = 3
TRACK_SIZE = 10


def main():
    players = read_player_start_positions()

    dice_outcome_counts = get_dice_outcomes()

    player_1_position = players[0] - 1
    player_2_position = players[1] - 1

    player_1_win_count = 0
    player_2_win_count = 0

    player_1_position_scores: List[DefaultDict[int, int]] = [defaultdict(int) for _ in range(TRACK_SIZE)]
    player_1_position_scores[player_1_position][0] = 1

    player_2_position_scores: List[DefaultDict[int, int]] = [defaultdict(int) for _ in range(TRACK_SIZE)]
    player_2_position_scores[player_2_position][0] = 1


    while are_players(player_1_position_scores) and are_players(player_2_position_scores):
        player_1_position_scores, win_count = update_position_scores(player_1_position_scores, dice_outcome_counts)
        player_1_win_count += win_count * count_players(player_2_position_scores)

        player_2_position_scores, win_count = update_position_scores(player_2_position_scores, dice_outcome_counts)
        player_2_win_count += win_count * count_players(player_1_position_scores)


    answer = max([player_1_win_count, player_2_win_count])
    print(f'Answer: {answer}')


def are_players(position_scores: List[DefaultDict[int, int]]) -> bool:
    for score_counts in position_scores:
        if score_counts:
            return True
    return False

def count_players(position_scores: List[DefaultDict[int, int]]) -> int:
    player_count = 0
    for score_counts in position_scores:
        player_count += sum(score_counts.values())
    return player_count

def get_dice_outcomes() -> Dict[int, int]:
    dice_outcome_counts: DefaultDict[int, int] = defaultdict(int)
    for die_1 in range(1, DIE_MAX + 1):
        for die_2 in range(1, DIE_MAX + 1):
            for die_3 in range(1, DIE_MAX + 1):
                outcome = die_1 + die_2 + die_3
                dice_outcome_counts[outcome] += 1
    return dice_outcome_counts

def print_position_scores(position_scores: List[DefaultDict[int, int]]):
    for position, score_counts in enumerate(position_scores):
        print(f'{position}: {dict(score_counts)}')

def update_position_scores(position_scores: List[DefaultDict[int, int]], dice_outcome_counts: Dict[int, int]) -> Tuple[List[DefaultDict[int, int]], int]:
    new_position_scores: List[DefaultDict[int, int]] = [defaultdict(int) for _ in range(TRACK_SIZE)]
    win_count = 0

    for position, score_counts in enumerate(position_scores):
        for score, count in score_counts.items():
            for dice, outcome_count in dice_outcome_counts.items():
                new_position = (position + dice) % TRACK_SIZE
                new_score = score + new_position + 1
                new_count = outcome_count * count

                if new_score < WINNING_SCORE:
                    new_position_scores[new_position][new_score] += new_count
                else:
                    win_count += new_count

    return new_position_scores, win_count

def read_player_start_positions() -> List[int]:
    with open('input.txt') as f:
        return [parse_player(l) for l in f]

def parse_player(line: str) -> int:
    parts = line.split()
    player_start = int(parts[4])
    return player_start

if __name__ == '__main__':
    main()
