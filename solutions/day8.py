from collections import defaultdict
from typing import DefaultDict, Dict, List, Set, Tuple


def generate_lr_max_dicts(tree_line: str) -> Tuple[DefaultDict, DefaultDict]:
    L = len(tree_line)
    left_max: DefaultDict[int, Tuple[str, int]] = defaultdict(lambda: ("-1", -1))
    right_max: DefaultDict[int, Tuple[str, int]] = defaultdict(lambda: ("-1", L))
    for k in range(L):
        left_max[k] = (tree_line[k], k) if tree_line[k] > left_max[k - 1][0] else left_max[k - 1]
        right_max[L - k - 1] = (
            (tree_line[L - k - 1], L - k - 1) if tree_line[L - k - 1] > right_max[L - k][0] else right_max[L - k]
        )
    return left_max, right_max


def get_visible_trees(tree_line: str) -> List[int]:
    left_max, right_max = generate_lr_max_dicts(tree_line)
    return [
        k
        for k in range(len(tree_line))
        if any(
            [left_max[k][1] == k, left_max[k][0] < tree_line[k], right_max[k][1] == k, right_max[k][0] < tree_line[k]]
        )
    ]


def get_visible_tree_positions(tree_line_rows: List[str]) -> Set[Tuple[int, int]]:
    tree_line_cols = list("".join(t) for t in zip(*tree_line_rows))
    visible_positions = set()
    for k, tree_line in enumerate(tree_line_rows):
        visible_positions = visible_positions.union((k, ix) for ix in get_visible_trees(tree_line))
    for k, tree_line in enumerate(tree_line_cols):
        visible_positions = visible_positions.union((ix, k) for ix in get_visible_trees(tree_line))
    return visible_positions


def generate_view_distances(tree_line: str) -> Tuple[DefaultDict, DefaultDict]:
    L = len(tree_line)
    vd_forward: DefaultDict[int, int] = defaultdict(lambda: 0)
    vd_backward: DefaultDict[int, int] = defaultdict(lambda: 0)
    for k in range(1, L - 1):
        backs = [j for j, h in enumerate(tree_line[:k]) if h >= tree_line[k]]
        forwards = [k + j + 1 for j, h in enumerate(tree_line[k + 1 :]) if h >= tree_line[k]]
        vd_backward[k] = k if not backs else k - backs[-1]
        vd_forward[k] = L - 1 - k if not forwards else forwards[0] - k
    return vd_backward, vd_forward


def get_scenic_score(row_ix, col_ix, distance_dict_row: Dict, distance_dict_col: Dict) -> int:
    vd_l = distance_dict_row["left"][row_ix]
    vd_r = distance_dict_row["right"][row_ix]
    vd_u = distance_dict_col["up"][col_ix]
    vd_d = distance_dict_col["down"][col_ix]
    return vd_l * vd_r * vd_u * vd_d


def get_max_scenic_score(tree_line_rows: List[str]) -> int:
    tree_line_cols = list("".join(t) for t in zip(*tree_line_rows))
    M, N = len(tree_line_rows[0]), len(tree_line_cols[0])
    distance_dict_rows = defaultdict(dict)
    distance_dict_cols = defaultdict(dict)
    scores = []
    for k in range(M):
        for j in range(N):
            if not distance_dict_rows[k]:
                left, right = generate_view_distances(tree_line_rows[k])
                distance_dict_rows[k]["left"] = left
                distance_dict_rows[k]["right"] = right
            if not distance_dict_cols[j]:
                up, down = generate_view_distances(tree_line_cols[j])
                distance_dict_cols[j]["up"] = up
                distance_dict_cols[j]["down"] = down
            scores.append(get_scenic_score(j, k, distance_dict_rows[k], distance_dict_cols[j]))
    return max(scores)


# Tests
tree_lines_test = open("inputs/day8_test.txt").read().split("\n")
tree_cols_test = list("".join(t) for t in zip(*tree_lines_test))
assert get_visible_trees(tree_lines_test[2]) == [0, 1, 3, 4]
assert len(get_visible_tree_positions(tree_lines_test)) == 21
assert get_max_scenic_score(tree_lines_test) == 8

print("Part 1: ", len(get_visible_tree_positions(open("inputs/day8.txt").read().split("\n"))))
print("Part 2: ", get_max_scenic_score(open("inputs/day8.txt").read().split("\n")))
