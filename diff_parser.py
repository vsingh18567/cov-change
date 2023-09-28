from collections import defaultdict
from typing import Any
from enum import Enum


class Additions:
    def __init__(self):
        self.additions : dict[str, list[tuple[int, int]]] = defaultdict(list) # file ->[(line_start, line_end_inclusive)]
    
    def __getitem__(self, key : str) -> list[tuple[int, int]]:
        return self.additions[key]
    
    def __setitem__(self, key : str, value : list[tuple[int, int]]) -> None:
        self.additions[key] = value
    
    def __iter__(self):
        return self.additions.__iter__()
    
    def __len__(self):
        return self.additions.__len__()
    
    def __str__(self):
        s = ""
        for k, v in self.additions.items():
            s += f"{k}: \n"
            for tup in v:
                s += f"\t{tup}\n"
        return s
    
class DiffParser:

    def __init__(self, file_name : str):
        self.file_name : str = file_name
        self.curr_file : str = None
        self.additions = Additions()

    def parse_line(self, line : str) -> None:
        if line.startswith('+++'):
            self.curr_file = line[6:].strip() # strip "+++ b/"
        elif line.startswith('@@'):
            parts = line.split(" ")
            part = parts[2] # "@@ -1,1 +1,1 @@"
            if "," in part:
                start, length = part.split(",")
                if length == "0":
                    return

                start = int(start)
                length = int(length)
                end = start + length - 1
            else:
                start = int(part)
                end = start
            self.additions[self.curr_file].append((start, end))

    def parse(self) -> Any:
        with open(self.file_name, 'r') as f:
            f.seek(0)
            for line in f:
                self.parse_line(line.rstrip())

if __name__ == "__main__":
    diff_parser = DiffParser("gdiff.diff")
    diff_parser.parse()
    print(diff_parser.additions)
