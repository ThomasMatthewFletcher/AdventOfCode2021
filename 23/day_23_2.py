#!/usr/bin/env python3
from typing import List, NamedTuple, Optional, Tuple, Set
import bisect

class Point(NamedTuple):
    x: int
    y: int

    def __str__(self) -> str:
        return f'({self.x},{self.y})'

class Amphipod(NamedTuple):
    type: str
    position: Point

    def __repr__(self) -> str:
        return f'Amphipod({self.type}, {self.position})'

class State(NamedTuple):
    energy: int
    amphipods: List[Amphipod]

amphipod_room_x_positions = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9
}

amphipod_costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

hallway_x_positions = [1,2,4,6,8,10,11]
hallway_points = [Point(x,1) for x in hallway_x_positions]

ROOM_MIN_Y = 2
ROOM_MAX_Y = 5

class Map:
    def __init__(self, map: List[List[str]]):
        self.map = map
        self.amphipods: List[Amphipod] = []
        self.energy = 0

    def set_state(self, state: State):
        self.amphipods = state.amphipods
        self.energy = state.energy

    def get_amphipod_at_position(self, position: Point) -> Optional[Amphipod]:
        for amphipod in self.amphipods:
            if position == amphipod.position:
                return amphipod
        return None

    def is_empty(self, position: Point) -> bool:
        # print(f'Checking if empty at {position}')
        return self.get_amphipod_at_position(position) is None

    def get_move_options(self, amphipod_index: int) -> List[State]:
        amphipod = self.amphipods[amphipod_index]

        # Check if already in the right room
        if amphipod.position.y >= ROOM_MIN_Y:
            is_correct_pos = True

            for y in range(amphipod.position.y, ROOM_MAX_Y + 1):
                point = Point(amphipod.position.x, y)
                point_amphipod = self.get_amphipod_at_position(point)
                assert point_amphipod
                if point_amphipod.position.x != amphipod_room_x_positions[point_amphipod.type]:
                    is_correct_pos = False
                    break

            if is_correct_pos:
                return []

        if amphipod.position.y == 1: # In the hallway, going into a room
            x_pos = amphipod_room_x_positions[amphipod.type]

            for y in range(ROOM_MAX_Y, ROOM_MIN_Y-1, -1):
                room_pos = Point(x_pos, y)

                point_amphipod = self.get_amphipod_at_position(room_pos)

                if point_amphipod and point_amphipod.type != amphipod.type:
                    return []

                if not point_amphipod and self.check_can_move(amphipod, room_pos):
                    new_state = self.amphipods.copy()
                    new_state[amphipod_index] = Amphipod(amphipod.type, room_pos)
                    move_cost = self.move_cost(amphipod, room_pos)
                    return [State(self.energy + move_cost, new_state)]

        else: # In a room, going into the hallway
            new_states: List[State] = []
            # can_move_anywhere = False
            for hallway_point in hallway_points:
                # print(hallway_point)
                if self.check_can_move(amphipod, hallway_point):
                    # can_move_anywhere = True

                    new_state = self.amphipods.copy()
                    new_state[amphipod_index] = Amphipod(amphipod.type, hallway_point)
                    move_cost = self.move_cost(amphipod, hallway_point)
                    new_states.append(State(self.energy + move_cost, new_state))
                    # print(f'Amphipod {amphipod.type} at {amphipod.position} can move to {hallway_point}')

            # if not can_move_anywhere:
                # print(f'Amphipod {amphipod.type} at {amphipod.position} cannot move')

            return new_states

        return []

    def move_cost(self, amphipod: Amphipod, position: Point) -> int:
        amphipod_cost_per_step = amphipod_costs[amphipod.type]
        return self.manhatten_dist(amphipod.position, position) * amphipod_cost_per_step


    def manhatten_dist(self, point_1: Point, point_2: Point):
        x_diff = abs(point_2.x - point_1.x)
        y_diff = abs(point_2.y - point_1.y)
        return x_diff + y_diff

    def get_all_move_options(self) -> List[State]:
        new_states: List[State] = []
        for amphipod_index in range(len(self.amphipods)):
            amphipod_new_states = self.get_move_options(amphipod_index)
            new_states.extend(amphipod_new_states)
        return new_states

    def check_can_move(self, amphipod: Amphipod, position: Point):
        # print(f'Checking if {amphipod} can move to {position}')

        # Check empty
        if not self.is_empty(position):
            return False

        # Check empty above (coming out)
        if amphipod.position.y >= ROOM_MIN_Y:
            for y in range(ROOM_MIN_Y, amphipod.position.y):
                if not self.is_empty(Point(amphipod.position.x, y)):
                    return False

        # Check empty left to right
        [x_min, x_max] = sorted([amphipod.position.x, position.x])
        for x in range(x_min, x_max + 1):
            pos = Point(x,1)
            if (pos != amphipod.position) and (not self.is_empty(pos)):
                return False

        # Check empty above (going in)
        if position.y >= ROOM_MIN_Y:
            for y in range(ROOM_MIN_Y, position.y):
                if not self.is_empty(Point(position.x, y)):
                    return False

        return True

    def is_complete(self) -> bool:
        for x_pos in hallway_x_positions:
            amphipod = self.get_amphipod_at_position(Point(x_pos, 1))
            if amphipod:
                return False


        for amphipod_type, x_pos in amphipod_room_x_positions.items():
            room_pos_1 = Point(x_pos, 2)
            amphipod = self.get_amphipod_at_position(room_pos_1)
            if amphipod and amphipod.type != amphipod_type:
                return False

            room_pos_2 = Point(x_pos, 2)
            amphipod = self.get_amphipod_at_position(room_pos_2)
            if amphipod and amphipod.type != amphipod_type:
                return False

        return True


    def __str__(self) -> str:
        output = ''
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                amphipod = self.get_amphipod_at_position(Point(x,y))
                if amphipod:
                    output += amphipod.type
                else:
                    output += char
            output += '\n'
        return output



def main():
    map, initial_state = read_map()

    states: List[State] = [initial_state]
    seen_states: Set[Tuple[Amphipod, ...]] = set()

    step = 0

    while states:
        step += 1
        if step % 10000 == 0:
            print(map)
        this_state = states.pop(0)
        this_amphipods = tuple(this_state.amphipods)

        if this_amphipods in seen_states:
            continue

        seen_states.add(this_amphipods)

        map.set_state(this_state)

        if map.is_complete():
            break

        new_states = map.get_all_move_options()

        for new_state in new_states:
            bisect.insort(states, new_state)

        # print(map)

    print(f'Answer: {map.energy}')


def read_map() -> Tuple[Map, State]:
    with open('input.txt') as f:
        rows = [list(l.rstrip()) for l in f]

    rows.insert(3, list('  #D#C#B#A#'))
    rows.insert(4, list('  #D#B#A#C#'))

    amphipods: List[Amphipod] = []

    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char in ['A','B','C','D']:
                amphipod = Amphipod(char, Point(x,y))
                amphipods.append(amphipod)
                rows[y][x] = '.'

    initial_state = State(0, amphipods)
    return Map(rows), initial_state


if __name__ == '__main__':
    main()
