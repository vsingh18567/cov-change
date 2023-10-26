from cov_change.coverage_parser import CoverageSummary
from cov_change.utils import bcolors
from rich.console import Console
from rich.table import Table


def build_table_cli(json_data: CoverageSummary, verbose: bool) -> Table:
    """
    Build a rich table from the json data.
    """
    table = Table()
    columns = ["File", "Coverage", "# Executed", "# Missed"]
    if verbose:
        columns += ["Missed Lines"]

    for column in columns:
        table.add_column(column)
    for file in json_data.files.values():
        row = [
            file.file_name,
            f"{file.coverage_percent:.2f}%",
            str(len(file.executed_lines)),
            str(len(file.missed_lines)),
        ]
        if verbose:
            row.append(file.missed_lines_str)

        table.add_row(*row)

    return table


def build_table_markdown(summary: CoverageSummary, verbose: bool) -> str:
    """
    Build a markdown table from the json data.
    """
    table = "| File | Coverage | # Executed | # Missed |"
    if verbose:
        table += " Missed Lines |"
    table += "\n"
    table += "| ---- | -------- | ---------- | -------- |"
    if verbose:
        table += " ------------- |"
    table += "\n"
    for file in summary.files.values():
        row = [
            file.file_name,
            f"{file.coverage_percent:.2f}%",
            str(len(file.executed_lines)),
            str(len(file.missed_lines)),
        ]
        if verbose:
            row.append(file.missed_lines_str)

        table += "| " + " | ".join(row) + " |\n"

    return table


def print_output(summary: CoverageSummary, verbose: bool, format: str) -> None:
    if format == "cli":
        print(
            f"{bcolors.OKCYAN}{bcolors.BOLD}Coverage of changes{bcolors.ENDC}: {bcolors.OKCYAN}{summary.total_coverage:.2f}%{bcolors.ENDC}"
        )
        table = build_table_cli(summary, verbose)
        console = Console()
        console.print(table, overflow="fold")
    elif format == "markdown":
        table = build_table_markdown(summary, verbose)
        print(f"**Coverage of changes: {summary.total_coverage:.2f}%**\n\n")
        print(table)
    else:
        raise Exception(f"Unknown format {format}")
