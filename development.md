# Development

## Starting the development container

1. Open VS Code
1. Inside the Command Palette (`Ctrl+Shift+P` or `F1`), enter `Remote-Containers: Clone Repository in Container Volume...`
1. From the dropdown menu select `GitHub`
1. If prompted, log in to your GitHub account
1. From the dropdown menu select this repository

VS Code will start a development container based on the instructions in the remote GitHub repository. Once the development container has been created VS Code will automatically attach to the development container.

**Building the development container for the first time may take several minutes.**

You can rebuild the container at any time by opening the Command Palette (`Ctrl+Shift+P` or `F1`) and entering `Remote-Containers: Rebuild Container`. Any uncommitted changes to the repository still will be present after the container is rebuilt.


## Running the test suite

The automated test suite is written using the [Pytest](https://pytest.org) framework. There are two ways to make use of the test suite, covered in the following sections.

### Coverage script

The repository includes a script called `coverage.sh` that runs the full test suite with the [Coverage.py](https://coverage.readthedocs.io/en/6.4.4/) plugin activated. This prints the test results in the terminal and saves a `cov.xml` file in the repository that can be used by the VS Code [Coverage Gutters](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters) extension.

Run the script in the VS Code terminal as follows:

```bash
./coverage.sh
```

### VS Code Testing panel

Select the VS Code Testing panel from the right sidebar. Here you can select which tests to run and whether to run in *Debug* mode.

Alternatively, you can open a test file and press the green play button to run specific test. Right click and select `Debug Test` to run the test in *Debug* mode.

When running tests in *Debug* mode the Python interpreter will pause at any breakpoints that have been set.

## Typical development workflow

The following steps should be taken when making changes to the Python codebase:

1. Use the `gh auth login` command to authenticate with GitHub.

1. Create a new issue in the GitHub repository to track the new functionality or bug fix (if one does not already exist):

   ```bash
   gh issue create  # follow the prompts
   ```

1. Create a new development branch for the issue:

   ```bash
   gh issue develop $ISSUE_NUMBER -c
   ```

1. Make the required changes to the Python codebase and run the test suite using the `coverage.sh` script to confirm all tests pass.

1. Commit the changes to the development branch:

   ```bash
   git add path/to/changed/files
   git commit -m 'brief description of changes'
   ```

   Pre-commit checks will run automatically when you commit changes. If any checks fail you will need to fix the issues and add any additional changes using `git add /path/to/changed/files` before you can commit the changes.

1. Create a new pull request:

   ```bash
   gh pr create  # follow the prompts
   ```

1. Assign the pull request to a reviewer and wait for the review to be completed.

1. Once the review is complete and the pull request has been approved, merge the changes into the `main` branch:

   ```bash
   gh pr merge  # follow the prompts
   ```

1. Update the package version numbers in the following files:
   - *pyproject.toml*
   - *project/__init__.py*
   - *tests/test_version.py*

1. Commit the version number changes to the `main` branch and tag the commit with the new version number. For example:

   ```bash
   git add pyproject.toml project/__init__.py tests/test_version.py
   git commit -m 'vX.Y.Z'
   git tag vX.Y.Z
   git push origin main vX.Y.Z
   ```

   The package will automatically be published to PyPI when a new version tag is pushed to GitHub.
