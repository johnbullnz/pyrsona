
from parse import Result
from pydantic import BaseModel, validator
import pytest
from datetime import date, time, datetime

from pyrsona import BaseStructure


class TestStructure(BaseStructure):

    structure = (
        "operator name: {operator_name}\n"
        "date: {date}\n"
        "\n"
        "id,time,value\n"
    )

    class meta_model(BaseModel):
        operator_name: str
        date: date

        @validator("date", pre=True)
        def parse_date(cls, value):
            return datetime.strptime(value, "%d/%m/%Y").date()

    class row_model(BaseModel):
        id: int
        time: time
        value: float


def test_parse_line_by_line_valid_structure():
    data = (
        "operator name: John Doe\n"
        "date: 27/2/2020\n"
        "\n"
        "id,time,value\n"
        "1,20:04:05,2098\n"
        "2,20:05:00,4328\n"
    )
    result = TestStructure.parse_line_by_line(data)

    assert len(result) == 5
    assert all((isinstance(rr["output"], Result) for rr in result))


def test_parse_line_by_line_invalid_structure_1():
    data = (
        "operator name: John Doe\n"
        "measurement date: 27/2/2020\n"
        "\n"
        "id,time,value\n"
        "1,20:04:05,2098\n"
        "2,20:05:00,4328\n"
    )
    result = TestStructure.parse_line_by_line(data)

    assert len(result) == 5
    assert result[1]["output"] is None
    assert all((isinstance(result[ii]["output"], Result) for ii in [0, 2, 3, 4]))


def test_parse_line_by_line_invalid_structure_2():
    data = (
        "operator name: John Doe\n"
        "date: 27/2/2020\n"
        "temperature: 22\n"
        "\n"
        "id,time,value\n"
        "1,20:04:05,2098\n"
        "2,20:05:00,4328\n"
    )
    result = TestStructure.parse_line_by_line(data)

    assert len(result) == 5
    assert all((result[ii]["output"] is None for ii in [2, 3]))
    assert all((isinstance(result[ii]["output"], Result) for ii in [0, 1, 4]))