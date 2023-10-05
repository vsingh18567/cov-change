from collections import defaultdict
from typing import Any
from enum import Enum

    
class DiffParser:

    def __init__(self, data : str):
        self.data : str = data
        self.curr_file : str | None = None
        self.additions : dict[str, list[tuple[int, int]]] = defaultdict(list)

    def parse_line(self, line : str) -> None:
        if line.startswith('+++'):
            self.curr_file = line[6:].strip() # strip "+++ b/"
        elif line.startswith('@@'):
            parts = line.split(" ")
            part = parts[2] # "@@ -1,1 +1,1 @@"
            if "," in part:
                start_str, length_str = part.split(",")
                if length_str == "0":
                    return
                start = int(start_str)
                length = int(length_str)
            else:
                start = int(part)
                length = 1
            end = start + length - 1
            assert self.curr_file is not None, "curr_file is None"
            self.additions[self.curr_file].append((start, end))

    def parse(self) -> Any:
        for line in self.data.split("\n"):
            self.parse_line(line.rstrip())
    
    def __str__(self) -> str:
        s = ""
        for k, v in self.additions.items():
            s += f"{k}: \n"
            for tup in v:
                s += f"\t{tup}\n"
        return s

if __name__ == "__main__":
    diff_parser = DiffParser("gdiff.diff")
    diff_parser.parse()
    print(diff_parser.additions)
