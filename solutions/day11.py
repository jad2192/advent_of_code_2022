from functools import reduce
from typing import Dict, List, Tuple, TypeAlias

MonkeyTracker: TypeAlias = Dict[int, "Monkey"]
MonkeyList: TypeAlias = List[str]
PrimeModulus: TypeAlias = Tuple[int, int, int, int, int, int, int, int, int]


PRIMES = {2: 0, 3: 1, 5: 2, 7: 3, 11: 4, 13: 5, 17: 6, 19: 7, 23: 8}
PRIME_IX = {val: key for key, val in PRIMES.items()}
INV_3 = (1, 1, 2, 5, 4, 9, 6, 13, 8)

def get_prime_modulus(num: int) -> PrimeModulus:
    return tuple([num % PRIME_IX[k] for k in range(9)])

def add_prime_modulus(pm1: PrimeModulus, pm2: PrimeModulus) -> PrimeModulus:
    return tuple([(pm1[k] + pm2[k]) % PRIME_IX[k] for k in range(9)])

def mult_prime_modulus(pm1: PrimeModulus, pm2: PrimeModulus) -> PrimeModulus:
    return tuple([(pm1[k] * pm2[k]) % PRIME_IX[k] for k in range(9)])

BIN_OP_DICT = {"+": lambda a, b: add_prime_modulus(a, b), "*": lambda a, b: mult_prime_modulus(a, b)}


class Monkey:
    def __init__(
        self,
        start_items: List[PrimeModulus],
        worry_modifier_params: Tuple[str, str, str],
        modulus: int,
        true_monkey: int,
        false_monkey: int,
    ):
        self.held_items = start_items
        self.worry_modifier_params = worry_modifier_params
        self.modulus = modulus
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspection_count = 0

    def worry_modifier(self, item: PrimeModulus) -> PrimeModulus:
        match self.worry_modifier_params:
            case ("old", bin_op, "old"):
                return BIN_OP_DICT[bin_op](item, item)
            case ("old", bin_op, modifier):
                return BIN_OP_DICT[bin_op](item, get_prime_modulus(int(modifier)))
        return item

    def throw(self, item: PrimeModulus) -> int:
        return self.true_monkey if item[PRIMES[self.modulus]] == 0 else self.false_monkey

    def catch_item(self, item: PrimeModulus):
        self.held_items.append(item)

    def inspect_and_throw(self, easement: int = 3) -> Tuple[int, PrimeModulus]:
        item = self.worry_modifier(self.held_items.pop(0))
        if easement == 3:
            item = mult_prime_modulus(item, INV_3)
        self.inspection_count += 1
        target_monkey = self.throw(item)
        return target_monkey, item


def initialize_monkey_state(monkey_input: MonkeyList) -> MonkeyTracker:
    monkey_tracker = dict()
    for k, monkey in enumerate(monkey_input):
        monkey_info = [line.split() for line in monkey.split("\n")]
        modulus = int(monkey_info[3][-1])
        start_items = [get_prime_modulus(int(item.replace(",", ""))) for item in monkey_info[1][2:]]
        modifier_params = monkey_info[2][-3:]
        monkey_tracker[k] = Monkey(
            start_items=start_items,
            worry_modifier_params=tuple(modifier_params),
            modulus=modulus,
            true_monkey=int(monkey_info[4][-1]),
            false_monkey=int(monkey_info[5][-1]),
        )
    return monkey_tracker


def simulate_monkey_rounds(monkey_tracker: MonkeyTracker, num_rounds: int, easement: int = 3) -> MonkeyTracker:
    end_state = monkey_tracker
    for _ in range(num_rounds):
        for k in range(len(monkey_tracker)):
            monkey = monkey_tracker[k]
            while monkey.held_items:
                target_monkey, item = monkey.inspect_and_throw(easement)
                end_state[target_monkey].catch_item(item)
    return monkey_tracker


def get_monkey_business(monkey_input: MonkeyList, num_rounds: int, easement: int = 3) -> int:
    monkey_state = initialize_monkey_state(monkey_input)
    monkey_state = simulate_monkey_rounds(monkey_state, num_rounds, easement)
    monkiness = sorted([monkey.inspection_count for monkey in monkey_state.values()])
    return reduce(lambda m1, m2: m1 * m2, monkiness[-2:])


# Tests
monkey_input_test: MonkeyList = open("inputs/day11_test.txt").read().split("\n\n")
#assert get_monkey_business(monkey_input_test, num_rounds=20, easement=3) == 10605
assert get_monkey_business(monkey_input_test, 10000, easement=1) == 2713310158


monkey_input: MonkeyList = open("inputs/day11.txt").read().split("\n\n")
print("Part 1: ", get_monkey_business(monkey_input, num_rounds=20))
print("Part 2: ", get_monkey_business(monkey_input, num_rounds=10000, easement=1))
