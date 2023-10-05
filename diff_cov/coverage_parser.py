from diff_cov.diff_parser import DiffParser
import json
from dataclasses import dataclass


@dataclass
class CoverageData:
    executed_lines: list[int]
    missing_lines: list[int]
    coverage_percent: float


class CoverageParser:
    def __init__(self, file_name: str, diff_parser: DiffParser):
        with open(file_name, "r") as f:
            self.coverage_data = json.load(f)
        self.diff_parser: DiffParser = diff_parser
        self.output_data: dict[str, CoverageData] = {}

    @staticmethod
    def get_overlap(
        line_intervals: list[tuple[int, int]], line_nos: list[int]
    ) -> list[int]:
        """
        key property: line_intervals and line_nos are sorted
        """
        interval_idx = 0
        overlap_lines = []
        for num in line_nos:
            while (
                interval_idx < len(line_intervals)
                and line_intervals[interval_idx][1] < num
            ):
                interval_idx += 1
            if (
                interval_idx < len(line_intervals)
                and line_intervals[interval_idx][0]
                <= num
                <= line_intervals[interval_idx][1]
            ):
                overlap_lines.append(num)
        return overlap_lines

    def parse(self) -> None:
        for file_name, file_data in self.coverage_data["files"].items():
            if file_name not in self.diff_parser.additions:
                continue
            line_intervals: list[tuple[int, int]] = self.diff_parser.additions[
                file_name
            ]
            executed_line_nos: list[int] = file_data["executed_lines"]
            print(file_name)
            executed_overlap = CoverageParser.get_overlap(
                line_intervals, executed_line_nos
            )
            print(f"Executed: {len(executed_overlap)} lines")
            missed_line_nos: list[int] = file_data["missing_lines"]
            missed_overlap = CoverageParser.get_overlap(line_intervals, missed_line_nos)
            print(f"Missed: {len(missed_overlap)} lines")
            total_lines = len(executed_overlap) + len(missed_overlap)
            coverage_percent = len(executed_overlap) / total_lines
            print(f"Coverage: {coverage_percent * 100:.2f}%")
            self.output_data[file_name] = CoverageData(
                executed_overlap, missed_overlap, coverage_percent
            )
