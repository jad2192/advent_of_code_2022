from typing import List
from functools import reduce


def get_signal(program: List[str]) -> List[int]:
    signal = [1]
    for instruction in program:
        match instruction.split():
            case ["noop"]:
                signal.append(signal[-1])
            case ["addx", units]:
                signal.extend([signal[-1], signal[-1] + int(units)])
    return signal
        
