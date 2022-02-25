
from datetime import time


def test_example_structure():
    from examples import example_structure

    assert example_structure.meta == {'operator_name': 'Jane Smith', 'country': 'NZ'}
    assert example_structure.table_rows == [
        {'id': 1, 'time': time(20, 4, 5), 'duration_sec': 12.2, 'value': 2098.0},
        {'id': 2, 'time': time(20, 5), 'duration_sec': 2.35, 'value': 4328.0},
    ]
    assert example_structure.structure_id == "ExampleStructure"


def test_new_example_structure():
    from examples import new_example_structure

    assert new_example_structure.meta == {
        'operator_name': 'Jane Smith', 'country': 'NZ', "city": "Auckland",
    }
    assert new_example_structure.table_rows == [
        {'id': 1, 'time': time(20, 4, 5), 'duration_sec': 12.2, 'value': 2098.0},
        {'id': 2, 'time': time(20, 5), 'duration_sec': 2.35, 'value': 4328.0},
    ]
    assert new_example_structure.structure_id == "NewExampleStructure"
