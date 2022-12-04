from typing import List


def load_data() -> List[List[int]]:
    lines = open("inputs/day4.txt").read().split("\n")
    return [[int(l) for l in line.split(",")[0].split("-") + line.split(",")[1].split("-")] for line in lines]


def part_1() -> int:
    elf_ranges = load_data()
    return sum(
        any([(rng[0] <= rng[-2]) * (rng[-1] <= rng[1]), (rng[-2] <= rng[0]) * (rng[1] <= rng[-1])])
        for rng in elf_ranges
    )


def part_2() -> int:
    elf_ranges = load_data()
    return sum(any([rng[0] <= rng[-2] <= rng[1], rng[-2] <= rng[0] <= rng[-1]]) for rng in elf_ranges)


print("Part 1: ", part_1())
print("Part 2: ", part_2())
