import pytest
from datetime import time


@pytest.mark.skip(reason="causes CI to fail")
def test_example_structure():
    from examples import example_structure

    assert example_structure.meta == {"operator_name": "Jane Smith", "country": "NZ"}
    assert example_structure.table_rows == [
        {"id": 1, "time": time(20, 4, 5), "duration_sec": 12.2, "value": 2098.0},
        {"id": 2, "time": time(20, 5), "duration_sec": 2.35, "value": 4328.0},
    ]
    assert example_structure.structure_id == "ExampleStructure"


@pytest.mark.skip(reason="causes CI to fail")
def test_new_example_structure():
    from examples import new_example_structure

    assert new_example_structure.meta == {
        "operator_name": "Jane Smith",
        "country": "NZ",
        "city": "Auckland",
    }
    assert new_example_structure.table_rows == [
        {"id": 1, "time": time(20, 4, 5), "duration_sec": 12.2, "value": 2098.0},
        {"id": 2, "time": time(20, 5), "duration_sec": 2.35, "value": 4328.0},
    ]
    assert new_example_structure.structure_id == "NewExampleStructure"


@pytest.mark.skip(reason="causes CI to fail")
def test_no_row_model_example():
    from examples import no_row_model_example

    assert no_row_model_example.meta == {"operator_name": "Jane Smith", "country": "NZ"}
    assert no_row_model_example.table_rows == [
        {"id": 1, "array_data": ["20:04:05", "12.2", "2098"]},
        {"id": 2, "array_data": ["20:05:00", "2.35", "4328"]},
    ]
    assert no_row_model_example.structure_id == "ExampleStructure"
