from typing import List, Literal, Tuple


def load_data() -> Tuple[List[List[str]], List[List[int]]]:
    stacks_transposed, rearrangments = [], []
    for line in open("inputs/day5.txt").read().split("\n"):
        if line.startswith("move"):
            rearrangments.append([int(x) for x in line.split() if x.isdigit()])
        elif "[" in line:
            stacks_transposed.append(list(line[1:][::4]))
    stacks = [[row[k] for row in stacks_transposed if row[k] != " "] for k in range(9)]
    return stacks, rearrangments


def crane_op(crate_stack: List[str], amount: int, version: str) -> List[str]:
    return crate_stack[:amount] if version == "9001" else crate_stack[:amount][::-1]


def restack(crane_version: Literal["9000", "9001"]) -> str:
    stacks, rearrangements = load_data()
    "Operation(opx): [amount, from_ix + 1, to_ix + 1]"
    for opx in rearrangements:
        amt, from_ix, to_ix = opx[0], opx[1] - 1, opx[2] - 1
        stacks[to_ix] = crane_op(stacks[from_ix], amt, crane_version) + stacks[to_ix]
        stacks[from_ix] = stacks[from_ix][amt:]
    return "".join(stack[0] for stack in stacks)


print("Part 1: ", restack(crane_version="9000"))
print("Part 2: ", restack(crane_version="9001"))
