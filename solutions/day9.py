from collections import defaultdict
from typing import DefaultDict, List, Literal, Tuple, TypeAlias

Coord: TypeAlias = Tuple[int, int]  # Coordinate class
CoordMap: TypeAlias = DefaultDict[Coord, int]
CoordUpdate: TypeAlias = Literal[-1, 0, 1]


def signum(i: int) -> int:
    return i // abs(i) if i != 0 else 0


def coords_touching(c1: Coord, c2: Coord) -> bool:
    return max(abs(c1[0] - c2[0]), abs(c1[1] - c2[1])) <= 1  # Touching iff L-inf distance <= 1


def update_coords(H: Coord, T: Coord, update_x: CoordUpdate, update_y: CoordUpdate) -> Tuple[Coord, Coord]:
    new_H = (H[0] + update_x, H[1] + update_y)
    if coords_touching(new_H, T):  # When touching after H moves, do nothing
        new_T = (T[0], T[1])
    else:  # Need to move T diagonally
        new_T = (T[0] + signum(new_H[0] - T[0]), T[1] + signum(new_H[1] - T[1]))
    return new_H, new_T


def simulate_motion(head_motions: List[str]) -> CoordMap:
    coord_map: CoordMap = defaultdict(int)
    cur_H, cur_T = (0, 0), (0, 0)
    coord_map[(0, 0)] += 1
    for motion in head_motions:
        match motion.split():
            case ["R", steps]:
                for _ in range(int(steps)):
                    cur_H, cur_T = update_coords(cur_H, cur_T, 1, 0)
                    coord_map[cur_T] += 1
            case ["L", steps]:
                for _ in range(int(steps)):
                    cur_H, cur_T = update_coords(cur_H, cur_T, -1, 0)
                    coord_map[cur_T] += 1
            case ["U", steps]:
                for _ in range(int(steps)):
                    cur_H, cur_T = update_coords(cur_H, cur_T, 0, 1)
                    coord_map[cur_T] += 1
            case ["D", steps]:
                for _ in range(int(steps)):
                    cur_H, cur_T = update_coords(cur_H, cur_T, 0, -1)
                    coord_map[cur_T] += 1
    return coord_map


# Tests
test_motions = open("inputs/day9_test.txt").read().split("\n")
assert len(simulate_motion(test_motions).keys()) == 13

print("Part 1: ", len(simulate_motion(open("inputs/day9.txt").read().split("\n"))))
