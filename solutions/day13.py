from functools import cmp_to_key, reduce
from typing import List, Literal, Optional, TypeAlias, Union, cast

Packet: TypeAlias = List[Union[int, "Packet"]]


def parse_packet_wo_eval(raw_packet_str: str) -> Packet:
    lists, cur_digit, brack_no = [], "", -1
    for chr in raw_packet_str:
        match chr:
            case "[":
                lists.append([])
                brack_no += 1
            case digit if digit.isdigit():
                cur_digit += digit
            case comma if comma == ",":
                if cur_digit != "":
                    lists[brack_no].append(int(cur_digit))
                    cur_digit = ""
            case "]":
                if cur_digit != "":
                    lists[brack_no].append(int(cur_digit))
                    cur_digit = ""
                if brack_no == 0:
                    return lists.pop()
                lists[brack_no - 1].append(lists.pop())
                brack_no -= 1
    return lists[0]


def load_packets(test=False):
    test_path_mod = "_test" * test
    return [
        [parse_packet_wo_eval(packet_string) for packet_string in block.split("\n")]
        for block in open(f"inputs/day13{test_path_mod}.txt").read().split("\n\n")
    ]


def packet_relation(p_left: Packet, p_right: Packet) -> Optional[bool]:
    p_left, p_right = p_left.copy(), p_right.copy()
    comparison = None
    while p_left and p_right and comparison is None:
        comp_items = [p_left.pop(0), p_right.pop(0)]
        match comp_items:
            case [k, j] if (type(k) == int) and (type(j) == int):
                if cast(int, k) < cast(int, j):
                    comparison = True
                elif cast(int, k) > cast(int, j):
                    comparison = False
            case [p, q] if (type(p) == int) and (type(q) == list):
                comparison = packet_relation([p], cast(Packet, q))
            case [p, q] if (type(p) == list) and (type(q) == int):
                comparison = packet_relation(cast(Packet, p), [q])
            case [p, q] if (type(p) == list) and (type(q) == list):
                comparison = packet_relation(cast(Packet, p), cast(Packet, q))
    if comparison is None and p_left and not p_right:
        return False
    if comparison is None and not p_left and p_right:
        return True
    return comparison


def packet_comparator(p_left, p_right) -> Literal[-1, 0, 1]:
    left_comp_right = packet_relation(p_left, p_right)
    return cast(Literal[1, -1], (2 * int(left_comp_right) - 1)) if left_comp_right is not None else 0


# Tests
assert parse_packet_wo_eval("[1,1,3,1,1]") == [1, 1, 3, 1, 1]
assert parse_packet_wo_eval("[1,[231,[3,[4,[5,6,70]]]],80,9]") == [1, [231, [3, [4, [5, 6, 70]]]], 80, 9]
assert parse_packet_wo_eval("[1,[2,[3,[4,[5,6,7]]]],8,9]") == [1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
packet_pairs_test = load_packets(test=True)
expected_test = {0: True, 1: True, 2: False, 3: True, 4: False, 5: True, 6: False, 7: False}
assert all([packet_relation(packet_pairs_test[k][0], packet_pairs_test[k][1]) == expected_test[k] for k in range(8)])
assert sum([(k + 1) for k, packet in enumerate(packet_pairs_test) if packet_relation(packet[0], packet[1])]) == 13
sorted_test_packets_w_buffers = sorted(
    reduce(lambda l1, l2: l1 + l2, packet_pairs_test + [[[[2]], [[6]]]]),
    key=cmp_to_key(packet_comparator),
    reverse=True,
)
assert (sorted_test_packets_w_buffers.index([[2]]) == 9) and (sorted_test_packets_w_buffers.index([[6]]) == 13)

packet_pairs = load_packets()
true_packet_ix = [(k + 1) for k, packet in enumerate(packet_pairs) if packet_relation(packet[0], packet[1])]
print("Part 1: ", sum(true_packet_ix))
sorted_packets_w_buffers = sorted(
    reduce(lambda l1, l2: l1 + l2, packet_pairs + [[[[2]], [[6]]]]), key=cmp_to_key(packet_comparator), reverse=True
)
print("Part 2: ", (1 + sorted_packets_w_buffers.index([[2]])) * (1 + sorted_packets_w_buffers.index([[6]])))
