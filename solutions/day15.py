from functools import reduce
import re
from collections import defaultdict
from typing import List, Optional, Tuple, TypeAlias

Coord: TypeAlias = Tuple[int, int]
ClosedInterval: TypeAlias = Tuple[int, int]


def l1_dist(c1: Coord, c2: Coord) -> int:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def interval_union(intervals: List[ClosedInterval]) -> List[ClosedInterval]:
    if len(intervals) < 2:
        return intervals
    sorted_ints = sorted(intervals, key=lambda i: i[0])
    res = [sorted_ints[0]]
    for intv in sorted_ints[1:]:
        if intv[0] <= res[-1][1] + 1:
            res[-1] = (res[-1][0], max(res[-1][1], intv[1]))
        else:
            res.append(intv)
    return res


class AffineRelation:
    def __init__(self, c1: Coord, c2: Coord):
        self.A = c1[1] - c2[1]
        self.B = c2[0] - c1[0]
        self.C = c1[0] * self.A + c1[1] * self.B

    def det(self, l2: "AffineRelation") -> int:
        return self.A * l2.B - self.B * l2.A

    def intersection_point(self, l2: "AffineRelation") -> Optional[Coord]:
        det = self.det(l2)
        if det == 0:
            return None
        else:
            return ((l2.B * self.C - self.B * l2.C) // det, (self.A * l2.C - l2.A * self.C) // det)


class SensorGrid:
    def __init__(self, sensor_positions: List[str]):
        self.sensors = dict()
        self.beacons = defaultdict(set)
        for sensor_info in sensor_positions:
            x_pos = [int(v) for v in re.findall(r"x=(-?\d+)", sensor_info)]
            y_pos = [int(v) for v in re.findall(r"y=(-?\d+)", sensor_info)]
            sensor_pos = (x_pos[0], y_pos[0])
            beacon_pos = (x_pos[1], y_pos[1])
            self.sensors[sensor_pos] = l1_dist(sensor_pos, beacon_pos)
            self.beacons[y_pos[1]].add(beacon_pos)

    def sensor_boundary_lines(self, sensor: Coord) -> List[AffineRelation]:
        x, y = sensor
        D = self.sensors[sensor] + 1
        return [AffineRelation((x, y + i * D), (x + j * D, y)) for i in {-1, 1} for j in {-1, 1}]

    def count_impossible_beacon_coords(self, y_pos: int) -> int:
        intervals = []
        for sensor, D in self.sensors.items():
            if sensor[1] - D <= y_pos <= sensor[1] + D:
                dx = D - abs(sensor[1] - y_pos)
                intervals.append((sensor[0] - dx, sensor[0] + dx))
        return sum([(1 + intv[1] - intv[0]) for intv in interval_union(intervals)]) - len(self.beacons[y_pos])

    def get_signal_tuning_freq(self, max_xy: int) -> int:
        valid_sensors = [
            sensor
            for sensor in self.sensors
            if any([0 <= sensor[k] + sgn * self.sensors[sensor] <= max_xy for k in {0, 1} for sgn in {-1, 1}])
        ]
        lines = reduce(lambda l1, l2: l1 + l2, [self.sensor_boundary_lines(sensor) for sensor in valid_sensors])
        intxs_pnts = set()
        for l1 in lines:
            for l2 in lines:
                if l1 != l2:
                    cross_coord = l1.intersection_point(l2)
                    if cross_coord is not None and all([(0 <= cross_coord[k] <= max_xy) for k in range(2)]):
                        intxs_pnts.add(cross_coord)
        for coord in intxs_pnts:
            if all([l1_dist(coord, sensor) > self.sensors[sensor] for sensor in valid_sensors]):
                return 4000000 * coord[0] + coord[1]
        return 0


# Tests
test_grid = SensorGrid(sensor_positions=open("inputs/day15_test.txt").read().split("\n"))
assert test_grid.count_impossible_beacon_coords(y_pos=10) == 26
assert test_grid.get_signal_tuning_freq(20) == 56000011


grid = SensorGrid(sensor_positions=open("inputs/day15.txt").read().split("\n"))
print("Part 1: ", grid.count_impossible_beacon_coords(y_pos=2000000))
print("Part 2: ", grid.get_signal_tuning_freq(4000000))
