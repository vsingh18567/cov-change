from coverage_parser import CoverageParser
from diff_parser import DiffParser


if __name__ == "__main__":
    diff_parser = DiffParser("gdiff.diff")
    diff_parser.parse()
    coverage_parser = CoverageParser("coverage.json", diff_parser)
    coverage_parser.parse()