
from parse import parse

from pyrsona import BaseStructure


def test_derive_structure_pattern_rows_demo_structure_1():
    data = BaseStructure._read_data_from_file("tests/data/demo_structure_1.txt")
    structure_rows = BaseStructure._derive_structure_pattern_rows(data)
    assert structure_rows == [
        "operator name: {operator_name}\n",
        "date: {date}\n",
        "\n",
        "{}",
    ]
    assert parse("".join(structure_rows), data) is not None


def test_derive_structure_pattern_rows_demo_structure_2_4d41ccd5():
    data = BaseStructure._read_data_from_file("tests/data/demo_structure_2_4d41ccd5.txt")
    structure_rows = BaseStructure._derive_structure_pattern_rows(data)
    assert structure_rows == [
        "4d41ccd5\n",
        "operator name: {operator_name}\n",
        "date: {date}\n",
        "\n",
        "{}",
    ]
    assert parse("".join(structure_rows), data) is not None


def test_derive_structure_pattern_rows_demo_structure_3():
    data = BaseStructure._read_data_from_file("tests/data/demo_structure_3.txt")
    structure_rows = BaseStructure._derive_structure_pattern_rows(data)
    assert structure_rows == [
        "[GROUP 1]\n",
        "var 1 = {var_1}\n",
        "var 2 = {var_2}\n",
        "\n",
        "[GROUP 2]\n",
        "var_3 = {var_3}\n",
        "Var 4 = {var_4}",
    ]
    assert parse("".join(structure_rows), data) is not None


def test_derive_structure_pattern_rows_demo_structure_3_with_new_line_at_end():
    data = BaseStructure._read_data_from_file("tests/data/demo_structure_3.txt") + "\n"
    structure_rows = BaseStructure._derive_structure_pattern_rows(data)
    assert structure_rows == [
        "[GROUP 1]\n",
        "var 1 = {var_1}\n",
        "var 2 = {var_2}\n",
        "\n",
        "[GROUP 2]\n",
        "var_3 = {var_3}\n",
        "Var 4 = {var_4}\n",
    ]
    assert parse("".join(structure_rows), data) is not None
