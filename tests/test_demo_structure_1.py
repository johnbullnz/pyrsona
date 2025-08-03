from pydantic import BaseModel, field_validator
from datetime import date, time, datetime

from pyrsona import BaseStructure


class DemoStructure1(BaseStructure):
    structure = (
        "operator name: {operator_name}\n" "date: {date}\n" "\n" "id,time,value\n"
    )

    class meta_model(BaseModel):
        operator_name: str
        date: date

        @field_validator("date", mode="before")
        @classmethod
        def parse_date(cls, value):
            return datetime.strptime(value, "%d/%m/%Y").date()

    class row_model(BaseModel):
        id: int
        time: time
        value: float


def test_demo_structure_1_no_children():
    meta, table_rows, structure_id = DemoStructure1.read(
        "tests/data/demo_structure_1.txt"
    )
    assert meta == {"operator_name": "John Doe", "date": date(2020, 2, 27)}
    assert table_rows == [
        {"id": 1, "time": time(20, 4, 5), "value": 2098.0},
        {"id": 2, "time": time(20, 5), "value": 4328.0},
    ]
    assert structure_id == "DemoStructure1"
