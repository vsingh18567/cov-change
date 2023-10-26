# Cov Change
Cov change is a tool to help you find the changes in your code that are not covered by your tests. It uses `git diff` to find your changes, and `coverage` to find your test coverage.

## Installation
```bash
pip install --upgrade pip
pip install cov-change
```

## Usage
Assuming you've already run tests with `coverage` (e.g. `coverage run -m pytest`), you will have generated a `.coverage` file. To then use `cov-change`:

```bash
coverage json # generate a json file from the .coverage file
cov-change
```
By default, `cov-change` will compare your current branch to `origin/main`. The full usage is:

```bash
cov-change [diff_branch] [curr_branch] [--coverage-file COVERAGE_FILE]  [-o --output OUTPUT] [-v --verbose] [--diff_file DIFF_FILE] [--use-coverage-diff] [-h --help]
```

### Options
- `diff_branch` and `curr_branch` are the branches you want to compare. By default, `diff_branch` is `origin/main` and `curr_branch` is your current commit.
- `--coverage_file COVERAGE_FILE` is the path to the coverage file. By default, it is `coverage.json`.
-  `-o --output OUTPUT` is the path to the output JSON file. By default, it is `coverage_change.json`.
- `-v --verbose` will print out the missing lines for each file.
- `--diff_file DIFF_FILE` is the path to a pre-generated diff file. If this is not passed in, the `git diff` will be run within the `cov-change` command itself. It is recommended that you **do not** pass this argument in.
- `--use_coverage_diff` assumes that `cov-change` has already been run once, and that the coverage change file has been generated. It will then use that diff file to generate the output.
- `-f --format {cli,markdown}` is the format of the output. By default, it is `cli` and outputs a formatted table. If `markdown` is passed in, it will output a markdown table.

### Examples
```bash
cov-change # compare origin/main to current commit
cov-change origin/dev HEAD # compare origin/dev to the current commit
cov-change origin/dev HEAD --coverage_file my_coverage.json -v # compare origin/dev to the current commit, using my_coverage.json as the coverage file and printing out the missing lines
```

### `cov-change-check`
`cov-change-check` checks if the generated `coverage_change.json` file meets requirements. If it doesn't, it will exit with a non-zero exit code. This is useful for CI/CD pipelines. The full usage is:
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
