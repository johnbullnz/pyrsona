
from pydantic import BaseModel

from pyrsona import BaseStructure


class DemoStructure3(BaseStructure):

    structure = (
        "[GROUP 1]\n"
        "var 1 = {var_1}\n"
        "var 2 = {var_2}\n"
        "\n"
        "[GROUP 2]\n"
        "var_3 = {var_3}\n"
        "Var 4 = {var_4}"
    )
    has_table_section = False
    
    class meta_model(BaseModel):
        var_1: int
        var_2: str
        var_3: str
        var_4: str


def test_demo_structure_3_no_table():
    meta, table_rows, structure_id = DemoStructure3.read("tests/data/demo_structure_3.txt")
    assert meta == {
        "var_1": 1,
        "var_2": "here",
        "var_3": "okay",
        "var_4": "11/2/23",
    }
    assert table_rows == []
    assert structure_id == "DemoStructure3"
