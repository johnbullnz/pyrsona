## Project Overview

**pyrsona** is a Python library for text data file validation and structure management using pydantic and parse packages. The core concept is defining file structure models that can parse structured text files with metadata sections and optional table sections.

### Key Architecture Components

- **BaseStructure class**: Core class in `pyrsona/__init__.py` that provides the foundation for all file structure models
- **Structure definitions**: String patterns that define the expected file format using parse package syntax
- **Pydantic models**: `meta_model` and `row_model` classes for data validation
- **Post-processors**: Optional `meta_postprocessor` and `table_postprocessor` methods for data transformation
- **Inheritance model**: Support for sub-models that extend parent structures for format evolution

## Common Development Commands

### Testing and Quality Assurance
```bash
# Run full test suite with coverage
./coverage.sh

# Run tests without coverage (using pytest directly)
pytest -v -m "not slow" tests

# Run specific test file
pytest tests/test_examples.py -v

# Run single test
pytest tests/test_examples.py::test_example_structure -v

# Code formatting and linting
black .
ruff check .
```

### Development Tools
```bash
# Install dependencies (Poetry-based project)
poetry install

# Run pre-commit hooks manually
pre-commit run --all-files
```

## Development Workflow

This project follows a GitHub-based development workflow:
1. Create issues for tracking work (`gh issue create`)
2. Create development branches (`gh issue develop $ISSUE_NUMBER -c`)
3. Make changes and run tests with `./coverage.sh`
4. Commit with pre-commit hooks running automatically
5. Create pull requests (`gh pr create`)
6. Version updates involve updating: `pyproject.toml`, `pyrsona/__init__.py`, and `tests/test_pyrsona.py`

## Code Patterns and Conventions

### Structure Model Definition
- Inherit from `BaseStructure`
- Define `structure` class attribute with parse pattern
- Create `meta_model` and `row_model` pydantic classes
- Optional post-processors for data transformation
- Sub-models inherit from parent models for format evolution

### File Structure Models
- Parent models are entry points (`ParentModel.read()`)
- Sub-models are checked first, then parent model
- Model names ending with underscore + hex (e.g., `_a4c15356`) indicate version variants
- `structure_id` returned from `read()` method identifies which model was used

### Key Methods
- `read(path)`: Main entry point for parsing files
- `parse(data)`: Parse string data directly
- `get_structures()`: Returns all available structure models in hierarchy
- Post-processors run after pydantic validation but before return

## Testing Strategy

- Examples in `examples/` directory demonstrate usage patterns
- Test data in `tests/data/` includes various file formats and encodings
- Coverage tracked with Coverage.py plugin
- Slow tests marked with `@pytest.mark.slow` and excluded from normal runs
- Tests validate both successful parsing and error handling

## Dependencies

- **Core**: pydantic v2, parse package, numpy
- **Async processing**: unsync for parallel table row validation
- **Performance**: psutil for CPU management during parallel processing
- **Development**: pytest, black, ruff, pre-commit

## File Organization

- `pyrsona/__init__.py`: Single module containing all core functionality
- `examples/`: Demonstration files and structure models
- `tests/`: Comprehensive test suite with test data
- `development.md`: Detailed development container and workflow instructions
