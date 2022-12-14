from collections import defaultdict
from typing import Dict, List, Tuple, TypeAlias, cast

Coord: TypeAlias = Tuple[int, int]
CaveState: TypeAlias = Dict[Coord, str]


class Cave:
    def __init__(self, scans: List[str]):
        self.cave_state: CaveState = defaultdict(lambda: ".")
        self.xmin = None
        self.xmax = None
        self.ymax = None
        self.sand_grains = 0
        for scan in scans:
            rock_paths = scan.split(" -> ")
            for k in range(len(rock_paths) - 1):
                x1, y1 = [int(v) for v in rock_paths[k].split(",")]
                x2, y2 = [int(v) for v in rock_paths[k + 1].split(",")]
                self.xmin = min(x1, x2) if self.xmin is None else min(x1, x2, self.xmin)
                self.xmax = max(x1, x2) if self.xmax is None else max(x1, x2, self.xmax)
                self.ymax = max(y1, y2) if self.ymax is None else max(y1, y2, self.ymax)
                if x1 == x2:
                    for y in range(min(y1, y2), max(y1, y2) + 1):
                        self.cave_state[(x1, y)] = "#"
                elif y1 == y2:
                    for x in range(min(x1, x2), max(x1, x2) + 1):
                        self.cave_state[(x, y1)] = "#"

    def sand_drop(self, void: bool):
        pos = (500, 0)
        sand_falling = True
        while sand_falling:
            if pos[1] == cast(int, self.ymax) + 1:
                sand_falling = False  # into the abyss / floor
            elif self.cave_state[(pos[0], pos[1] + 1)] == ".":
                pos = (pos[0], pos[1] + 1)
            elif self.cave_state[(pos[0] - 1, pos[1] + 1)] == ".":
                pos = (pos[0] - 1, pos[1] + 1)
            elif self.cave_state[(pos[0] + 1, pos[1] + 1)] == ".":
                pos = (pos[0] + 1, pos[1] + 1)
            else:
                sand_falling = False
        if pos[1] < cast(int, self.ymax) or not void:
            self.cave_state[pos] = "o"
            self.xmax = max(cast(int, self.xmax), pos[0])
            self.xmin = min(cast(int, self.xmin), pos[0])
            self.sand_grains += 1

    def fill_with_sand_void(self):
        full = False
        sand_grains = 0
        while not full:
            self.sand_drop(void=True)
            full = self.sand_grains == sand_grains
            sand_grains = self.sand_grains

    def fill_with_sand_floor(self):
        while self.cave_state[(500, 0)] == ".":
            self.sand_drop(void=False)

    def __repr__(self):
        rows = [
            "".join([self.cave_state[(x, y)] for x in range(cast(int, self.xmin), cast(int, self.xmax) + 1)])
            for y in range(cast(int, self.ymax) + 1)
        ]
        return "\n".join(rows)


# Tests
test_scans = open("inputs/day14_test.txt").read().split("\n")
cave1, cave2 = Cave(test_scans), Cave(test_scans)
cave1.fill_with_sand_void()
cave2.fill_with_sand_floor()
assert cave1.sand_grains == 24
assert cave2.sand_grains == 93


scans = open("inputs/day14.txt").read().split("\n")
cave1, cave2 = Cave(scans), Cave(scans)
cave1.fill_with_sand_void()
cave2.fill_with_sand_floor()
print("Part 1: ", cave1.sand_grains)
print("Part 2: ", cave2.sand_grains)
