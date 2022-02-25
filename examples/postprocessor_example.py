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

    @staticmethod
    def meta_postprocessor(meta):
        meta["version"] = 3
        return meta

    @staticmethod
    def table_postprocessor(table_rows, meta):
        # Add a cumulative total and delete the "id" field:
        total = 0
        for ii, row in enumerate(table_rows):
            total += row["value"]
            row["total"] = total
            del(row["id"])
            table_rows[ii] = row
        return table_rows


meta, table_rows, structure_id = ExampleStructure.read("examples/example.txt")


print(meta)
#> {'operator_name': 'Jane Smith', 'country': 'NZ', 'version': 3}

print(table_rows)
#> [{'time': datetime.time(20, 4, 5), 'duration_sec': 12.2, 'value': 2098.0, 'total': 2098.0}, {'time': datetime.time(20, 5), 'duration_sec': 2.35, 'value': 4328.0, 'total': 6426.0}]
