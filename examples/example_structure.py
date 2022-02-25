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

    class row_model(BaseModel):
        id: int
        time: time
        duration_sec: float
        value: float


meta, table_rows, structure_id = ExampleStructure.read("examples/example.txt")

print(meta)
#> {'operator_name': 'Jane Smith', 'country': 'NZ'}

print(table_rows)
#> [{'id': 1, 'time': datetime.time(20, 4, 5), 'value': 2098.0}, {'id': 2, 'time': datetime.time(20, 5), 'value': 4328.0}]

print(structure_id)
#> 'ExampleStructure'