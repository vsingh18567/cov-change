from diff_parser import DiffParser
import json

class CoverageParser:

    def __init__(self, file_name: str, diff_parser: DiffParser):
        with open(file_name, 'r') as f:
            self.coverage_data = json.load(f)
        self.diff_parser: DiffParser = diff_parser

    @staticmethod
    def get_overlap(line_intervals : list[tuple[int, int]], line_nos: list[int]) -> int:
        """
        key property: line_intervals and line_nos are sorted
        """
        interval_idx = 0
        count = 0
        for line in line_nos:
            while interval_idx < len(line_intervals) and line_intervals[interval_idx][1] < line:
                interval_idx += 1
            if interval_idx < len(line_intervals) and line_intervals[interval_idx][0] <= line <= line_intervals[interval_idx][1]:
                count += 1
        return count

    def parse(self) -> None:
        for file_name, file_data in self.coverage_data['files'].items():
            if file_name not in self.diff_parser.additions:
                continue
            line_intervals : list[tuple[int, int]] = self.diff_parser.additions[file_name]
            executed_line_nos : list[int] = file_data['executed_lines']
            print(file_name)
            executed_line_nos_overlap = CoverageParser.get_overlap(line_intervals, executed_line_nos)
            print(f"Executed: {executed_line_nos_overlap} lines")
            missed_line_nos : list[int] = file_data['missing_lines']
            missed_line_nos_overlap = CoverageParser.get_overlap(line_intervals, missed_line_nos)
            print(f"Missed: {missed_line_nos_overlap} lines")

