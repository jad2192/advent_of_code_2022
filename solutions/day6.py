def load_data() -> str:
    return open("inputs/day6.txt").read().strip()


def signal_decoder(packet_length: int) -> int:
    """I know this is less efficient than using a stack, but I am a sucker for
    that sweet python list comprehension."""
    signal_string = load_data()
    num_packet_chars = [
        len(set(signal_string[k - packet_length : k])) for k in range(packet_length, len(signal_string))
    ]
    return [k for k, length in enumerate(num_packet_chars) if length == packet_length][0] + packet_length


print("Part 1: ", signal_decoder(4))
print("Part 2: ", signal_decoder(14))
