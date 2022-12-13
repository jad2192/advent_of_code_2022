from functools import reduce
from typing import Dict, List, Optional, Tuple, TypeAlias, Union, cast

MonkeyTracker: TypeAlias = Dict[int, "Monkey"]
MonkeyList: TypeAlias = List[str]
MonkeyItem = Union[int, List[int]]


class RingProduct:
    """Class to represent the ring `Z/n1Z x Z/n2Z x ... Z/nmZ` and homomorphism from Z onto it."""

    def __init__(self, moduli: List[int]):
        self.moduli = moduli
        self.moduli_ix = {mod: k for k, mod in enumerate(moduli)}
        self.op_dict = {"+": lambda a, b: self.ring_addition(a, b), "*": lambda a, b: self.ring_mult(a, b)}

    def map_z_to_ring(self, z: int) -> List[int]:
        return [z % modulus for modulus in self.moduli]

    def ring_addition(self, r1: List[int], r2: List[int]) -> List[int]:
        return [(r1[k] + r2[k]) % modulus for k, modulus in enumerate(self.moduli)]

    def ring_mult(self, r1: List[int], r2: List[int]) -> List[int]:
        return [(r1[k] * r2[k]) % modulus for k, modulus in enumerate(self.moduli)]


BIN_OP_DICT = {"+": lambda a, b: a + b, "*": lambda a, b: a * b}


class Monkey:
    def __init__(
        self,
        start_items: List[MonkeyItem],
        worry_modifier_params: Tuple[str, str, str],
        modulus: int,
        true_monkey: int,
        false_monkey: int,
        ring_product: Optional[RingProduct] = None,
    ):
        self.held_items = start_items
        self.worry_modifier_params = worry_modifier_params
        self.modulus = modulus
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspection_count = 0
        self.ring_product = ring_product

    def worry_modifier(self, item: MonkeyItem) -> MonkeyItem:
        op_dict = BIN_OP_DICT if self.ring_product is None else self.ring_product.op_dict
        match self.worry_modifier_params:
            case (bin_op, "old"):
                return op_dict[bin_op](item, item)
            case (bin_op, modifier):
                return op_dict[bin_op](item, modifier)
        return item

    def throw(self, item: MonkeyItem) -> int:
        condition = (
            (cast(int, item) % self.modulus == 0)
            if self.ring_product is None
            else (cast(List[int], item)[self.ring_product.moduli_ix[self.modulus]] == 0)
        )
        return self.true_monkey if condition else self.false_monkey

    def catch_item(self, item: MonkeyItem):
        self.held_items.append(item)

    def inspect_and_throw(self) -> Tuple[int, MonkeyItem]:
        item = self.worry_modifier(self.held_items.pop(0))
        print(item)
        item = cast(int, item) // 3 if self.ring_product is None else item
        self.inspection_count += 1
        target_monkey = self.throw(item)
        return target_monkey, item


def initialize_monkey_state(monkey_input: MonkeyList, use_ring_product: bool = False) -> MonkeyTracker:
    monkey_tracker = dict()
    monkey_moduli = set()
    for k, monkey in enumerate(monkey_input):
        monkey_info = [line.split() for line in monkey.split("\n")]
        modulus = int(monkey_info[3][-1])
        monkey_moduli.add(modulus)
        start_items = [cast(MonkeyItem, int(item.replace(",", ""))) for item in monkey_info[1][2:]]
        print(start_items)
        modifier_params = monkey_info[2][-2:]
        monkey_tracker[k] = Monkey(
            start_items=start_items,
            worry_modifier_params=tuple(modifier_params),
            modulus=modulus,
            true_monkey=int(monkey_info[4][-1]),
            false_monkey=int(monkey_info[5][-1]),
        )
    if use_ring_product:
        ring_product = RingProduct(list(monkey_moduli))
        for monkey in monkey_tracker.values():
            monkey.ring_product = ring_product
            monkey.held_items = [ring_product.map_z_to_ring(item) for item in monkey.held_items]
            match monkey.worry_modifier_params:
                case (op, mod) if type(mod) == int:
                    monkey.worry_modifier_params = (op, ring_product.map_z_to_ring(mod))
    return monkey_tracker


def simulate_monkey_rounds(monkey_tracker: MonkeyTracker, num_rounds: int) -> MonkeyTracker:
    end_state = monkey_tracker
    for _ in range(num_rounds):
        for k in range(len(monkey_tracker)):
            monkey = monkey_tracker[k]
            while monkey.held_items:
                target_monkey, item = monkey.inspect_and_throw()
                end_state[target_monkey].catch_item(item)
    return monkey_tracker


def get_monkey_business(monkey_input: MonkeyList, num_rounds: int, use_ring_product: bool = False) -> int:
    monkey_state = initialize_monkey_state(monkey_input, use_ring_product)
    monkey_state = simulate_monkey_rounds(monkey_state, num_rounds)
    monkiness = sorted([monkey.inspection_count for monkey in monkey_state.values()])
    return reduce(lambda m1, m2: m1 * m2, monkiness[-2:])


# Tests
monkey_input_test: MonkeyList = open("inputs/day11_test.txt").read().split("\n\n")
assert get_monkey_business(monkey_input_test, num_rounds=20) == 10605
# assert get_monkey_business(monkey_input_test, 10000, use_ring_product=True) == 2713310158


monkey_input: MonkeyList = open("inputs/day11.txt").read().split("\n\n")
print("Part 1: ", get_monkey_business(monkey_input, num_rounds=20))
# print("Part 2: ", get_monkey_business(monkey_input, num_rounds=10000, use_ring_product=True))
