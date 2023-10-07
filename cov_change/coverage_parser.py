from cov_change.diff_parser import DiffParser
import json
from dataclasses import dataclass, asdict, is_dataclass
from typing import Any


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o: object) -> Any:
        if is_dataclass(o):
            return asdict(o)  # type: ignore
        return super().default(o)


@dataclass
class CoverageData:
    file_name: str
    executed_lines: list[int]
    missed_lines: list[int]
    coverage_percent: float
    missed_lines_str: str = ""

    def __post_init__(self) -> None:
        self.missed_lines.sort()
        previous_line = -2
        section_start = None
        for line in self.missed_lines:
            if section_start is None:
                section_start = line

            if line == previous_line + 1:
                previous_line = line
            else:
                if section_start == previous_line:
                    self.missed_lines_str += f"{section_start}, "
                elif previous_line >= 0:
                    self.missed_lines_str += f"{section_start}-{previous_line}, "
                section_start = line
                previous_line = line

        if section_start == previous_line:
            self.missed_lines_str += f"{section_start}, "
        elif previous_line >= 0:
            self.missed_lines_str += f"{section_start}-{previous_line}, "

        if len(self.missed_lines_str) > 0:
            self.missed_lines_str = self.missed_lines_str[:-2]


@dataclass
class CoverageSummary:
    total_coverage: float
    total_executed_lines: int
    total_missed_lines: int
    total_lines: int
    files: dict[str, CoverageData]


class CoverageParser:
    def __init__(self, file_name: str, diff_parser: DiffParser):
        with open(file_name, "r") as f:
            self.coverage_data = json.load(f)
        self.diff_parser: DiffParser = diff_parser
        self.files: dict[str, CoverageData] = {}
        self.summary: CoverageSummary | None = None

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
            if file_name not in self.diff_parser.additions or not file_name.endswith(
                ".py"
            ):
                continue
            line_intervals: list[tuple[int, int]] = self.diff_parser.additions[
                file_name
            ]
            executed_line_nos: list[int] = file_data["executed_lines"]

            executed_overlap = CoverageParser.get_overlap(
                line_intervals, executed_line_nos
            )
            missed_line_nos: list[int] = file_data["missing_lines"]
            missed_overlap = CoverageParser.get_overlap(line_intervals, missed_line_nos)
            total_lines = len(executed_overlap) + len(missed_overlap)
            coverage_percent = len(executed_overlap) / total_lines
            self.files[file_name] = CoverageData(
                file_name, executed_overlap, missed_overlap, coverage_percent * 100
            )

        # get overall coverage
        total_executed = 0
        total_missed = 0
        for file_name, file_data in self.files.items():
            total_executed += len(file_data.executed_lines)
            total_missed += len(file_data.missed_lines)
        total = total_executed + total_missed
        if total == 0:
            total_coverage_percent = 100.0
        else:
            total_coverage_percent = (
                total_executed / (total_executed + total_missed) * 100
            )
        self.summary = CoverageSummary(
            total_coverage_percent,
            total_executed,
            total_missed,
            total_executed + total_missed,
            self.files,
        )

    def json(self) -> str:
        return json.dumps(self.summary, indent=4, cls=DataclassJSONEncoder)
