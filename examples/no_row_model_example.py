from pyrsona import BaseStructure
from pydantic import BaseModel
from datetime import time


class ExampleStructure(BaseStructure):

    structure = (
        "operator name: {operator_name}\n"
        "country: {country}\n"
        "year: {}\n"
        "\n"
        "ID,Time,Duration (sec),Reading\n"
    )

    class meta_model(BaseModel):
        operator_name: str
        country: str

    @staticmethod
    def table_postprocessor(table_rows, meta):

        class row_model(BaseModel):
            id: int
            array_data: list[str]

        ids = [row[0] for row in table_rows]
        array_data = [row[1:] for row in table_rows]

        table_rows = [
            row_model(id=row_id, array_data=row_array_data).dict()
            for row_id, row_array_data in zip(ids, array_data)
        ]

        return table_rows


meta, table_rows, structure_id = ExampleStructure.read("examples/example.txt")

print(table_rows)
#> [{'id': 1, 'array_data': ['20:04:05', '12.2', '2098']}, {'id': 2, 'array_data': ['20:05:00','2.35','4328']}]
