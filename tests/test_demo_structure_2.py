from pydantic import BaseModel, field_validator
from datetime import date, time, datetime

from pyrsona import BaseStructure


class DemoStructure2(BaseStructure):
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


class _e4f5de45(DemoStructure2):
    pass


class _89c2effb(DemoStructure2):
    structure = (
        "89c2effb\n"
        "operator name: {operator_name}\n"
        "date: {date}\n"
        "\n"
        "id,time,value\n"
    )

    class meta_model(BaseModel):
        operator_name: str
        date: str


class _4d41ccd5(DemoStructure2):
    structure = (
        "4d41ccd5\n"
        "operator name: {operator_name}\n"
        "date: {date}\n"
        "\n"
        "id,time,value\n"
    )

    class row_model(BaseModel):
        id: int
        time: str
        value: int


def test_demo_structure_2_e4f5de45_direct():
    meta, table_rows, structure_id = _e4f5de45.read(
        "tests/data/demo_structure_2_e4f5de45.txt"
    )
    assert meta == {"operator_name": "John Doe", "date": date(2020, 2, 27)}
    assert table_rows == [
        {"id": 1, "time": time(20, 4, 5), "value": 2098.0},
        {"id": 2, "time": time(20, 5), "value": 4328.0},
    ]
    assert structure_id == "e4f5de45"


def test_demo_structure_2_e4f5de45():
    meta, table_rows, structure_id = DemoStructure2.read(
        "tests/data/demo_structure_2_e4f5de45.txt"
    )
    assert meta == {"operator_name": "John Doe", "date": date(2020, 2, 27)}
    assert table_rows == [
        {"id": 1, "time": time(20, 4, 5), "value": 2098.0},
        {"id": 2, "time": time(20, 5), "value": 4328.0},
    ]
    assert structure_id == "e4f5de45"


def test_demo_structure_2_89c2effb():
    meta, table_rows, structure_id = DemoStructure2.read(
        "tests/data/demo_structure_2_89c2effb.txt"
    )
    assert meta == {"operator_name": "John Doe", "date": "27/2/2020"}
    assert table_rows == [
        {"id": 1, "time": time(20, 4, 5), "value": 2098.0},
        {"id": 2, "time": time(20, 5), "value": 4328.0},
    ]
    assert structure_id == "89c2effb"


def test_demo_structure_2_4d41ccd5():
    meta, table_rows, structure_id = DemoStructure2.read(
        "tests/data/demo_structure_2_4d41ccd5.txt"
    )
    assert meta == {"operator_name": "John Doe", "date": date(2020, 2, 27)}
    assert table_rows == [
        {"id": 1, "time": "20:04:05", "value": 2098.0},
        {"id": 2, "time": "20:05:00", "value": 4328.0},
    ]
    assert structure_id == "4d41ccd5"
