#!/usr/bin/env python3
from typing import List

WINNING_SCORE = 1000
DIE_MAX = 100
TRACK_SIZE = 10

class DeterministicDie:
    def __init__(self):
        self.value = 0
        self.rolls = 0

    def roll(self) -> int:
        self.rolls += 1
        self.value = (self.value % DIE_MAX) + 1
        return self.value

    def roll_3(self) -> int:
        return sum(self.roll() for _ in range(3))

class Player:
    def __init__(self, id: int, start: int):
        self.id = id
        self.position = start
        self.score = 0

    def move(self, spaces: int):
        self.position += spaces
        self.position = ((self.position - 1) % TRACK_SIZE) + 1
        self.score += self.position

    def has_won(self) -> bool:
        return self.score >= WINNING_SCORE


def main():
    die = DeterministicDie()
    players = read_players()

    turn = 0
    current_player = players[turn]

    while True:
        move = die.roll_3()
        current_player.move(move)

        if current_player.has_won():
            break

        turn = (turn + 1) % len(players)
        current_player = players[turn]

    losing_player_index = (turn + 1) % len(players)
    losing_player = players[losing_player_index]
    answer = losing_player.score * die.rolls
    print(f'Answer: {answer}')


def read_players() -> List[Player]:
    with open('input.txt') as f:
        return [parse_player(l) for l in f]

def parse_player(line: str) -> Player:
    parts = line.split()
    player_id = int(parts[1])
    player_start = int(parts[4])
    return Player(player_id, player_start)

if __name__ == '__main__':
    main()
