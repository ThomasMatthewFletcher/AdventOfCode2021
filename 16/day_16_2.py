#!/usr/bin/env python3
from typing import List
from enum import IntEnum
from functools import reduce

class PacketType(IntEnum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7

class LengthType(IntEnum):
    BIT_LENGTH = 0
    SUB_PACKETS = 1

class Packet:
    def __init__(self, data: str):
        self.data = data
        self.pos = 0

    def read_int(self, length: int) -> int:
        segment = self.data[self.pos:self.pos+length]
        self.pos += length
        return int(segment, 2)

    def read_long_int(self) -> int:
        value = 0
        is_last_group = False

        while not is_last_group:
            value <<= 4
            is_last_group = not bool(self.read_int(1))
            group = self.read_int(4)
            value += group

        return value


def main():
    packet_hex = read_packet_hex()
    packet = Packet(hex_to_bin(packet_hex))

    version_sum = parse_packet(packet)
    print(f'Answer: {version_sum}')


def parse_packet(packet: Packet) -> int:

    version = packet.read_int(3) # type: ignore
    type_id = packet.read_int(3)

    sub_packet_values: List[int] = []

    if type_id == PacketType.LITERAL:
        return packet.read_long_int()

    length_type_id = packet.read_int(1)

    if length_type_id == LengthType.BIT_LENGTH:
        total_length = packet.read_int(15)
        end_pos = packet.pos + total_length

        while packet.pos < end_pos:
            value = parse_packet(packet)
            sub_packet_values.append(value)

    elif length_type_id == LengthType.SUB_PACKETS:
        sub_packets = packet.read_int(11)

        for _ in range(sub_packets):
            value = parse_packet(packet)
            sub_packet_values.append(value)

    return calculate(type_id, sub_packet_values)


def calculate(op: int, values: List[int]) -> int:
    if op == PacketType.SUM:
        return sum(values)
    if op == PacketType.PRODUCT:
        return reduce((lambda a, v: a * v), values)
    if op == PacketType.MINIMUM:
        return min(values)
    if op == PacketType.MAXIMUM:
        return max(values)
    if op == PacketType.GREATER_THAN:
        return 1 if values[0] > values[1] else 0
    if op == PacketType.LESS_THAN:
        return 1 if values[0] < values[1] else 0
    if op == PacketType.EQUAL_TO:
        return 1 if values[0] == values[1] else 0

    raise ValueError('Invalid packet type')


def hex_to_bin(hex: str) -> str:
    bin = ''

    for char in hex:
        d = int(char, 16)
        bin += f'{d:04b}'

    return bin

def read_packet_hex() -> str:
    with open('input.txt') as f:
        return f.readline().strip()


if __name__ == '__main__':
    main()
