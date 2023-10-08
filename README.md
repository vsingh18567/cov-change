# Cov Change
Cov change is a tool to help you find the changes in your code that are not covered by your tests. It uses `git diff` to find your changes, and `coverage` to find your test coverage.

## Installation
```bash
pip install cov-change
```

## Usage
Assuming you've already run `pytest` with `coverage` (e.g. `python3 -m coverage pytest .`), you will have generated a `.coverage` file. To then use `cov-change`:

```bash
coverage json # generate a json file from the .coverage file
cov-change
```
By default, `cov-change` will compare your current branch to `origin/main`. The full usage is:

```bash
cov-change [branch1] [branch2] [--coverage-file COVERAGE_FILE]  [-o --output OUTPUT] [-v --verbose] [--diff-file DIFF_FILE] [--use-coverage-diff] [-h --help]
```

### Options
- `branch1` and `branch2` are the branches you want to compare. By default, `branch1` is `origin/main` and `branch2` is your current commit.
- `--coverage-file COVERAGE_FILE` is the path to the coverage file. By default, it is `coverage.json`.
- - `-o --output OUTPUT` is the path to the output JSON file. By default, it is `coverage_change.json`.
- `-v --verbose` will print out the missing lines for each file.
- `--diff-file DIFF_FILE` is the path to a pre-generated diff file. If this is not passed in, the `git diff` will be run within the `cov-change` command itself. It is recommended that you **do not** pass this argument in.
- `--use-coverage-diff` assumes that `cov-change` has already been run once, and that the coverage change file has been generated. It will then use that diff file to generate the output.

### Examples
```bash
cov-change # compare origin/main to current commit
cov-change origin/dev HEAD # compare origin/dev to the current commit
cov-change origin/dev HEAD --coverage-file my_coverage.json -v # compare origin/dev to the current commit, using my_coverage.json as the coverage file and printing out the missing lines
```

### `cov-change-check`
`cov-change-check` checks if the generated `coverage_change.json` file meets requirements. If it does, it will exit with a non-zero exit code. This is useful for CI/CD pipelines. The full usage is:
```bash
cov-change-check [coverage_change_file] [--total TOTAL] [--file FILE] [-h --help]
```

#### Options
- `coverage_change_file` is the path to the coverage change file. By default, it is `coverage_change.json`.
- `--total TOTAL` is the minimum total coverage change required. By default, it is 0.
- `--file FILE` is the minimum coverage change required in each file. By default, it is 0.

#### Examples
```bash
cov-change-check --total 80 --file 50 # check if the total coverage is at least 80%, and if each file has at least 50% coverage
```
