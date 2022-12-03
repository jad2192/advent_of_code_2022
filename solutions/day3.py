from functools import reduce
from typing import List, Tuple


def get_input() -> List[Tuple[str, int]]:
    return [(line, len(line) // 2) for line in open("inputs/day3.txt").read().split("\n")]


def get_priority(item: str) -> int:
    return ord(item.lower()) - ord("a") + 26 * item.isupper() + 1


def get_part_1() -> int:
    load_outs = get_input()
    return sum(
        get_priority(next(iter(set(pack[0][: pack[1]]).intersection(set(pack[0][pack[1] :]))))) for pack in load_outs
    )


def get_part_2() -> int:
    load_outs = get_input()
    elf_loads = [[elf[0] for elf in load_outs[k : k + 3]] for k in range(0, len(load_outs), 3)]
    return sum(
        get_priority(next(iter(reduce(set.intersection, [set(elf) for elf in elf_load])))) for elf_load in elf_loads
    )


print("Part 1: ", get_part_1())
print("Part 2: ", get_part_2())
