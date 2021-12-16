#!/usr/bin/env python3
from enum import IntEnum

class PacketType(IntEnum):
    LITERAL = 4

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

    version = packet.read_int(3)
    type_id = packet.read_int(3)

    version_sum = version

    if type_id == PacketType.LITERAL:
        value = packet.read_long_int()
        print(f'Packet value: {value}')
    else:
        length_type_id = packet.read_int(1)

        if length_type_id == LengthType.BIT_LENGTH:
            total_length = packet.read_int(15)
            end_pos = packet.pos + total_length

            while packet.pos < end_pos:
                version_sum += parse_packet(packet)

        elif length_type_id == LengthType.SUB_PACKETS:
            sub_packets = packet.read_int(11)

            for _ in range(sub_packets):
                version_sum += parse_packet(packet)

    return version_sum


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
