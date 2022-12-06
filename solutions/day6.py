def load_data() -> str:
    return open("inputs/day6.txt").read().strip()


def part_1() -> int:
    """I know this is less efficient than using a stack, but I am a sucker for
    that sweet python list comprehension."""
    signal_string = load_data()
    num_packet_chars = [len(set(signal_string[k - 4 : k])) for k in range(4, len(signal_string))]
    return [k for k, length in enumerate(num_packet_chars) if length == 4][0] + 4


print("Part 1: ", part_1())
