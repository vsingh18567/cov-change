import subprocess
import json
import traceback

from dacite import from_dict
from cov_change.coverage_parser import CoverageSummary
from cov_change.utils import print_error, bcolors


def run_test(
    test_name: str,
    coverage_file: str,
    diff_file: str = "diff.diff",
    expect_fail: bool = False,
) -> CoverageSummary | None:
    command = [
        "cov-change",
        "--coverage_file",
        f"tests/{coverage_file}",
        "--diff_file",
        f"tests/{diff_file}",
        "--output",
        "tests/coverage_change.json",
    ]

    print(
        f"Running {test_name}, coverage_file: {coverage_file}, diff_file: {diff_file}"
    )

    output = subprocess.run(command, capture_output=True, text=True)
    if expect_fail:
        if output.returncode == 0:
            raise Exception("Expected failure, but got success")
        else:
            return None
    elif output.returncode != 0:
        print(output.stderr)
        raise Exception("Expected success, but got failure")
    with open(f"tests/coverage_change.json", "r") as f:
        data = json.load(f)
        summary: CoverageSummary = from_dict(CoverageSummary, data)
    return summary


def test_empty() -> None:
    summary = run_test("test_empty", "cov_empty.json")
    assert len(summary.files) == 0, "Expected no files"
    assert summary.total_coverage == 100.0, "Expected 100% coverage"


def test_cov1() -> None:
    summary = run_test("test one file", "cov1.json")
    assert len(summary.files) == 1, "Expected one file"
    views_file = summary.files["homePage/views.py"]
    assert views_file.executed_lines == [
        24
    ], f"Expected one executed line, got {views_file.executed_lines}"
    assert (
        views_file.missed_lines == []
    ), "Missed lines should be empty as it doesn't intersect with diff"


def test_cov2() -> None:
    summary = run_test("test complex coverage", "cov2.json")
    assert len(summary.files) == 2, f"Expected two files, got {len(summary.files)}"
    user_data_file = summary.files["mainApp/user_data.py"]
    assert user_data_file.executed_lines == [
        243,
        244,
        245,
    ], f"Expected executed lines to be [243, 244, 245], actually got {user_data_file.executed_lines}"
    assert user_data_file.missed_lines == [
        246,
        247,
        248,
    ], f"Expected missed lines to be [246, 247, 248], actually got {user_data_file.missed_lines}"
    assert (
        user_data_file.missed_lines_str == "246-248"
    ), f"Expected missed lines to be compacted, actually got {user_data_file.missed_lines_str}"
    assert user_data_file.coverage_percent == 50.0, "Expected 50% coverage"
    assert round(summary.total_coverage) == 57.0, "Expected 57% coverage"


def main() -> None:
    tests = [test_empty, test_cov1, test_cov2]
    failed = False
    for test in tests:
        try:
            test()
            print(f"\t{test.__name__} passed")
        except Exception as e:
            print_error(f"\t{test.__name__} failed")
            traceback.print_exc()
            failed = True
    if failed:
        exit(1)
    else:
        print(f"{bcolors.OKGREEN}All tests passed{bcolors.ENDC}")


if __name__ == "__main__":
    main()
