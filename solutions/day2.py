from typing import Dict, List, Set, Tuple


def load_strategy_guide() -> List[str]:
    res = []
    with open("inputs/day2.txt", "r") as handle:
        for line in handle.readlines():
            res.append(line.strip())
    return res


PLAY_D = dict(X=1, Y=2, Z=3, A=1, B=2, C=3)
# Encode three winning situtions as tuples: (my_play, elfs_play)
WIN_D: Set[Tuple[int, int]] = {(1, 3), (2, 1), (3, 2)}


def round_score(match_round: str) -> int:
    elf, me = PLAY_D[match_round[0]], PLAY_D[match_round[-1]]
    return 6 * ((me, elf) in WIN_D) + 3 * (me == elf) + me


def get_my_total() -> int:
    match_rounds = load_strategy_guide()
    return sum([round_score(match) for match in match_rounds])


# Part 2
WIN_D_PT2: Dict[str, str] = {"A": "B", "B": "C", "C": "A"}
LOSE_D_PT2: Dict[str, str] = {val: key for key, val in WIN_D_PT2.items()}
ACTION_D: Dict[str, Dict[str, str]] = {"X": LOSE_D_PT2, "Z": WIN_D_PT2, "Y": {x: x for x in "ABC"}}


def alter_round(match_round: str) -> str:
    elf, me = match_round[0], match_round[-1]
    return f"{elf} {ACTION_D[me][elf]}"


def get_my_total_pt2() -> int:
    altered_rounds = [alter_round(round) for round in load_strategy_guide()]
    return sum([round_score(match) for match in altered_rounds])


print("Part 1: ", get_my_total())
print("Part 2: ", get_my_total_pt2())
