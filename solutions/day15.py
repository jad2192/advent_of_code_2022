import math
import re
from collections import defaultdict
from typing import Dict, List, Tuple, TypeAlias

Coord: TypeAlias = Tuple[int, int]
ClosedInterval: TypeAlias = Tuple[int, int]


def l1_dist(c1: Coord, c2: Coord) -> int:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def interval_union(intervals: List[ClosedInterval]) -> List[ClosedInterval]:
    if len(intervals) < 2:
        return intervals
    sorted_ints = sorted(intervals, key=lambda i: i[0])
    res = [sorted_ints.pop(0)]
    int1 = res[0]
    while sorted_ints:
        int2 = sorted_ints.pop(0)
        if int2[0] <= int1[1] + 1:
            int1 = (int1[0], max(int1[1], int2[1]))
            res[-1] = int1
        else:
            res.append(int2)
            int1 = int2
    return res


class SensorGrid:
    def __init__(self, sensor_positions: List[str]):
        self.grid = defaultdict(lambda: ".")
        self.sensors = dict()
        self.xmin = math.inf
        self.xmax = -math.inf
        for sensor_info in sensor_positions:
            x_pos = [int(v) for v in re.findall(r"x=(-?\d+)", sensor_info)]
            y_pos = [int(v) for v in re.findall(r"y=(-?\d+)", sensor_info)]
            sensor_pos = (x_pos[0], y_pos[0])
            beacon_pos = (x_pos[1], y_pos[1])
            self.xmin = min(self.xmin, x_pos[0] - l1_dist(sensor_pos, beacon_pos))
            self.xmax = max(self.xmax, x_pos[0] + l1_dist(sensor_pos, beacon_pos))
            self.sensors[sensor_pos] = l1_dist(sensor_pos, beacon_pos)
            self.grid[sensor_pos] = "S"
            self.grid[beacon_pos] = "B"

    def fill_signal_ball(self, sensor_coord: Coord, beacon_coord: Coord):
        D = l1_dist(sensor_coord, beacon_coord)
        for x in range(-D, D + 1):
            for y in range(abs(x) - D, D + 1 - abs(x)):
                if self.grid[(x, y)] == ".":
                    self.grid[(x, y)] = "#"

    def within_coverage(self, coord: Coord, sensor: Coord):
        assert sensor in self.sensors, f"{sensor} is not a valid sensor coordinate."
        return l1_dist(coord, sensor) <= self.sensors[sensor]

    def count_impossible_beacon_coords(self, y_pos: int) -> int:
        count = 0
        for x in range(int(self.xmin), int(self.xmax) + 1):
            for sensor in self.sensors:
                if self.grid[(x, y_pos)] in {"S", "B"}:
                    break
                elif self.within_coverage((x, y_pos), sensor):
                    count += 1
                    break
        return count

    def get_signal_tuning_freq(self, max_xy: int) -> int:
        valid_sensors = [
            sensor
            for sensor in self.sensors
            if any([0 <= sensor[k] + sgn * self.sensors[sensor] <= max_xy for k in {0, 1} for sgn in {-1, 1}])
        ]
        y_intervals = defaultdict(list)
        for sensor in valid_sensors:
            D = self.sensors[sensor]
            for y in range(max(0, sensor[1] - D), min(max_xy, sensor[1] + D) + 1):
                dx = D - abs(sensor[1] - y)
                y_intervals[y].append((max(0, sensor[0] - dx), min(max_xy, sensor[0] + dx)))
        for y, interval_list in y_intervals.items():
            unioned_list = interval_union(interval_list)
            if unioned_list[0][0] > 0:
                return 4000000 * (unioned_list[0][0] - 1) + y
            elif unioned_list[-1][1] < max_xy:
                return 4000000 * (unioned_list[-1][1] + 1) + y
            elif len(unioned_list) > 1:
                return 4000000 * (unioned_list[0][1] + 1) + y
        return 0


# Tests
test_grid = SensorGrid(sensor_positions=open("inputs/day15_test.txt").read().split("\n"))
assert test_grid.count_impossible_beacon_coords(y_pos=10) == 26
assert test_grid.get_signal_tuning_freq(20) == 56000011


grid = SensorGrid(sensor_positions=open("inputs/day15.txt").read().split("\n"))
print("Part 1: ", grid.count_impossible_beacon_coords(y_pos=2000000))
print("Part 2: ", grid.get_signal_tuning_freq(4000000))
