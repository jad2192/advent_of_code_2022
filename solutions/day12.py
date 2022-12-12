import math
from collections import defaultdict
from queue import PriorityQueue
from typing import Dict, List, Optional, Tuple, TypeAlias

Node: TypeAlias = Tuple[int, int]


class MountainGraph:
    def __init__(self, input_rows: List[str]):
        self.nodes: Dict[Node, int] = dict()
        self.nrows = len(input_rows)
        self.start_node = (0, 0)
        self.end_node = (0, 0)
        for row_ix, row in enumerate(input_rows):
            for col_ix, height in enumerate(list(row)):
                match height:
                    case "S":
                        self.start_node = (row_ix, col_ix)
                        self.nodes[(row_ix, col_ix)] = 0
                    case "E":
                        self.end_node = (row_ix, col_ix)
                        self.nodes[(row_ix, col_ix)] = 25
                    case let if let.islower():
                        self.nodes[(row_ix, col_ix)] = ord(height) - ord("a")
        self.ncols = len(input_rows[0])
        self.dist = defaultdict(lambda: math.inf)  # Shortest path (distance) to source node (0, 0)
        self.dist[self.start_node] = 0

    def update_dist(self, node: Node, new_dist: int):
        self.dist[node] = new_dist

    def update_start_node(self, new_start: Node):
        self.dist = defaultdict(lambda: math.inf)
        self.start_node = new_start
        self.dist[new_start] = 0

    def neighbors(self, node: Node) -> List[Node]:
        neighbors = []
        # Up
        if 0 < node[0] and self.nodes[(node[0] - 1, node[1])] <= self.nodes[node] + 1:
            neighbors.append((node[0] - 1, node[1]))
        # Left
        if 0 < node[1] and self.nodes[(node[0], node[1] - 1)] <= self.nodes[node] + 1:
            neighbors.append((node[0], node[1] - 1))
        # Down
        if self.nrows > 1 + node[0] and self.nodes[(node[0] + 1, node[1])] <= self.nodes[node] + 1:
            neighbors.append((node[0] + 1, node[1]))
        # Right
        if self.ncols > 1 + node[1] and self.nodes[(node[0], node[1] + 1)] <= self.nodes[node] + 1:
            neighbors.append((node[0], node[1] + 1))
        return neighbors


def dijkstra_climb(mountain: MountainGraph, start_node: Optional[Node] = None) -> Dict:
    if start_node is not None:
        mountain.update_start_node(start_node)
    pqueue = PriorityQueue()
    pqueue.put((0, mountain.start_node))
    while not pqueue.empty():
        cur_d, cur_node = pqueue.get()
        for node in mountain.neighbors(cur_node):
            if cur_d + 1 < mountain.dist[node]:
                mountain.update_dist(node, cur_d + 1)
                pqueue.put((mountain.dist[node], node))
    return mountain.dist


def shortest_max_height_climb(mountain: MountainGraph) -> int:
    start_points = [node for node, height in mountain.nodes.items() if height == 0]
    shortest = math.inf
    for node in start_points:
        path_dists = dijkstra_climb(mountain, start_node=node)
        shortest = min(shortest, path_dists[mountain.end_node])
    return int(shortest)


# Tests
mountain_rows_test = open("inputs/day12_test.txt").read().split("\n")
mountain_graph = MountainGraph(mountain_rows_test)
path_dists = dijkstra_climb(mountain_graph)
assert path_dists[mountain_graph.end_node] == 31


mountain_rows = open("inputs/day12.txt").read().split("\n")
mountain_graph = MountainGraph(mountain_rows)
path_dists = dijkstra_climb(mountain_graph)
print("Part 1: ", path_dists[mountain_graph.end_node])
print("Part 2: ", shortest_max_height_climb(mountain_graph))
