from collections import defaultdict
from queue import PriorityQueue
from typing import DefaultDict, Dict, List, Literal, NamedTuple, Optional, Set


class FileSystemObject(NamedTuple):
    type: Literal["dir", "file"]
    parent: Optional["FileSystemObject"]
    path: List[str]
    size: int = 0

    def path_str(self, levels_up: int = 0) -> str:
        return "/".join(self.path) if levels_up == 0 else "/".join(self.path[:-levels_up])


def create_file_tree(terminal_list: List[str]) -> List[FileSystemObject]:
    tree: Dict[str, FileSystemObject] = {"..": FileSystemObject(type="dir", path=[".."], parent=None)}
    cwd: FileSystemObject = tree[".."]
    for line in terminal_list:
        match line.split():
            case ["$", "cd", ".."]:
                cwd = tree[cwd.path_str(levels_up=1)]
            case ["$", "cd", "/"]:
                cwd = tree[".."]
            case ["$", "cd", directory]:
                cwd = tree[f"{cwd.path_str()}/{directory}"]
            case ["dir", directory]:
                new_obj = FileSystemObject(type="dir", path=cwd.path.copy() + [directory], parent=cwd)
                tree[new_obj.path_str()] = new_obj
            case [bytes, file] if bytes.isdigit():
                new_obj = FileSystemObject(type="file", path=cwd.path.copy() + [file], size=int(bytes), parent=cwd)
                tree[new_obj.path_str()] = new_obj
    return list(tree.values())


def get_directory_sizes_dfs(terminal_list: List[str]) -> List[int]:
    file_tree = create_file_tree(terminal_list)
    directory_sizes: DefaultDict = defaultdict(int)
    for file in [obj for obj in file_tree if obj.type == "file"]:
        for k in range(len(file.path)):
            directory_sizes[file.path_str(levels_up=k)] += file.size
    return [directory_sizes[obj.path_str()] for obj in file_tree if obj.type == "dir"]


def get_directory_sizes_bfs(terminal_list: List[str]) -> List[int]:
    file_tree = create_file_tree(terminal_list)
    directory_sizes: DefaultDict = defaultdict(int)
    pqueue: PriorityQueue = PriorityQueue()
    seen_obj: Set = set()
    for file in [obj for obj in file_tree if obj.type == "file"]:
        pqueue.put((len(file_tree) - len(file.path), file))
        directory_sizes[file.path_str()] += file.size
    while not pqueue.empty():
        cur_priority, cur_obj = pqueue.get()
        if cur_obj.parent != None and cur_obj.path_str() not in seen_obj:
            pqueue.put((cur_priority + 1, cur_obj.parent))
            directory_sizes[cur_obj.parent.path_str()] += directory_sizes[cur_obj.path_str()]
        seen_obj.add(cur_obj.path_str())
    return [directory_sizes[obj.path_str()] for obj in file_tree if obj.type == "dir"]


def part1(terminal_list: List[str], graph_search: Literal["dfs", "bfs"] = "dfs") -> int:
    match graph_search:
        case "dfs":
            return sum(val for val in get_directory_sizes_dfs(terminal_list) if val <= 100000)
        case "bfs":
            return sum(val for val in get_directory_sizes_bfs(terminal_list) if val <= 100000)


def part2(terminal_list: List[str], graph_search: Literal["dfs", "bfs"] = "dfs") -> int:
    match graph_search:
        case "dfs":
            dir_sizes = get_directory_sizes_dfs(terminal_list)
            space_target = 30000000 + max(dir_sizes) - 70000000
            return min(val for val in dir_sizes if val >= space_target)
        case "bfs":
            dir_sizes = get_directory_sizes_bfs(terminal_list)
            space_target = 30000000 + max(dir_sizes) - 70000000
            return min(val for val in dir_sizes if val >= space_target)


test_case = open("inputs/day7_test.txt").read().split("\n")
assert part1(test_case) == 95437
assert part1(test_case, "dfs") == part1(test_case, "bfs")
assert part2(test_case) == 24933642
assert part2(test_case, "dfs") == part2(test_case, "bfs")

print("Part 1: ", part1(open("inputs/day7.txt").read().split("\n")))
print("Part 2: ", part2(open("inputs/day7.txt").read().split("\n")))
