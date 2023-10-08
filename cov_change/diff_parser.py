"""
This file contains the DiffParser class, which parses the output of `git diff --unified=0 <diff_branch> <curr_branch>`.
"""
from collections import defaultdict
from typing import Any
from enum import Enum


class DiffParser:
    """
    Parses the output of `git diff --unified=0 <diff_branch> <curr_branch>`.

    Attributes:
        self.additions: { file_name: [ (start, end), ... ] }

    Methods:
        DiffParser.parse() -> None: parses the data
    """

    def __init__(self, data: str):
        self._data: str = data
        self._curr_file: str | None = None
        # { file_name: [ (start, end), ... ] }
        self.additions: dict[str, list[tuple[int, int]]] = defaultdict(list)

    def _parse_line(self, line: str) -> None:
        if line.startswith("+++"):
            # indicates a new file
            self._curr_file = line[6:].strip()  # strip "+++ b/"
        elif line.startswith("@@"):
            # indicates a new section
            parts = line.split(" ")
            part = parts[2]  # "@@ -1,1 +1,1 @@"
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
            assert self._curr_file is not None, "curr_file is None"
            self.additions[self._curr_file].append((start, end))

    def parse(self) -> None:
        for line in self._data.split("\n"):
            self._parse_line(line.rstrip())
        to_pop = []
        for k in self.additions.keys():
            if k.endswith(".py"):  # only care about python files
                to_pop.append(k)
        for k in to_pop:
            self.additions.pop(k)

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
