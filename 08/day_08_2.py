#!/usr/bin/env python3
from typing import Set, List, Optional, Callable

Config = Set[str]

class Display:
    def __init__(self, configs: List[Config], outputs: List[Config]):
        self.outputs = outputs

        self.digit_configs: List[Optional[Config]] = [None] * 10

        config_one = self._find_config(configs, lambda c: len(c) == 2)
        self.digit_configs[1] = config_one

        self.digit_configs[4] = self._find_config(configs, lambda c: len(c) == 4)
        self.digit_configs[7] = self._find_config(configs, lambda c: len(c) == 3)
        self.digit_configs[8] = self._find_config(configs, lambda c: len(c) == 7)

        config_three = self._find_config(configs, lambda c: len(c) == 5 and config_one.issubset(c))
        self.digit_configs[3] = config_three

        self.digit_configs[9] = self._find_config(configs, lambda c: len(c) == 6 and config_three.issubset(c))

        self.digit_configs[0] = self._find_config(configs, lambda c: len(c) == 6 and config_one.issubset(c))
        config_six = self._find_config(configs, lambda c: len(c) == 6)
        self.digit_configs[6] = config_six

        self.digit_configs[5] = self._find_config(configs, lambda c: len(c) == 5 and c.issubset(config_six))
        self.digit_configs[2] = self._find_config(configs, lambda c: len(c) == 5)

    def _find_config(self, configs: List[Config], func: Callable[[Config], bool]) -> Config:
        config = next(c for c in configs if func(c))
        configs.remove(config)
        return config

    def get_value(self) -> int:
        value = 0

        value += self._get_digit(self.outputs[0]) * 1000
        value += self._get_digit(self.outputs[1]) * 100
        value += self._get_digit(self.outputs[2]) * 10
        value += self._get_digit(self.outputs[3]) * 1

        return value

    def _get_digit(self, config: Config) -> int:
        return self.digit_configs.index(config)


def main():
    displays = read_displays()

    total = sum(d.get_value() for d in displays)

    print(f'Answer: {total}')


def read_displays() -> List[Display]:
    with open('input.txt') as f:
        return [parse_display(l) for l in f]

def parse_display(line: str):
    configurations, outputs = line.split('|')
    configurations = [set(c) for c in configurations.split()]
    outputs = [set (o) for o in outputs.split()]
    return Display(configurations, outputs)


if __name__ == '__main__':
    main()
