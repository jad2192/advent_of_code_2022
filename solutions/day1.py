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


def get_max_cal_elves(top_k: int) -> int:
    """Part Solve Part 1 / 2, sum calories of the top K-th elves carrying the most Calories."""
    sorted_elf_data = sorted(load_elf_data(), key=lambda elf: -sum(elf))
    return sum([sum(elf) for elf in sorted_elf_data[:top_k]])


assert get_max_cal_elves(1) == 68292
assert get_max_cal_elves(3) == 203203
