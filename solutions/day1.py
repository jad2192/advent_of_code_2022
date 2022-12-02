from typing import List


def load_elf_data() -> List[List[int]]:
    res = []
    with open("inputs/day1.txt", "r") as handle:
        cur_elf = []
        for line in handle.readlines():
            if line.strip() == "":
                res.append(cur_elf)
                cur_elf = []
            else:
                cur_elf.append(int(line.strip()))
    return res


def get_max_cal_elf() -> int:
    """Part Solve Part 1"""
    elf_data = load_elf_data()
    return sum(sorted(elf_data, key=lambda elf: sum(elf))[-1])


def test_day1_part1():
    assert get_max_cal_elf() == 68292
