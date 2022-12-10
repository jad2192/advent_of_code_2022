from typing import List, TypeAlias

Program: TypeAlias = List[str]


def get_signal(program: Program) -> List[int]:
    signal = [1, 1]  # Even indices indicate starting state of cycle, odd end state.
    for instruction in program:
        match instruction.split():
            case ["noop"]:
                signal.extend([signal[-1]] * 2)
            case ["addx", units]:
                signal.extend([signal[-1]] * 3 + [signal[-1] + int(units)])
    return signal


def signal_strength(program: Program, start_cycle: int, cycle_step: int, cycles: int) -> int:
    signal = get_signal(program)
    return sum([c_ix * signal[2 * c_ix] for c_ix in range(start_cycle, start_cycle + cycle_step * cycles, cycle_step)])


def draw_pixels(program, pixel_width: int = 40, pixel_height: int = 6) -> None:
    signal = get_signal(program)
    pixel_sequence = ""
    for k in range(pixel_width * pixel_height):
        next_char = "#" if (abs(signal[2 * k + 2] - (k % pixel_width)) <= 1) else "."
        pixel_sequence += next_char
    for k in range(0, pixel_width * pixel_height, pixel_width):
        print(pixel_sequence[k : k + pixel_width])


# Tests
test_program: Program = open("inputs/day10_test.txt").read().split("\n")
assert get_signal(test_program)[40 : 40 + 80 * 6 : 80] == [21, 19, 18, 21, 16, 18]
assert signal_strength(test_program, 20, 40, 6) == 13140
draw_pixels(test_program)


program: Program = open("inputs/day10.txt").read().split("\n")
print("Part 1: ", signal_strength(program, 20, 40, 6))
print("Part 2: ")
draw_pixels(program)
