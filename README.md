# pyrsona

Text data file validation and structure management using the [pydantic](https://pydantic-docs.helpmanual.io/) and [parse](https://github.com/r1chardj0n3s/parse) Python packages.


## Installation

Install using `pip install pyrsona`.


## A Simple Example

For the text file `example.txt`:

```
operator name: Jane Smith
country: NZ
year: 2022

ID,Time,Duration (sec),Reading
1,20:04:05,12.2,2098
2,20:05:00,2.35,4328
```

The following *pyrsona* file structure model can be defined:

```python
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
```

The `read()` method can then be used to read the file, parse its contents and validate the meta data and table rows:

```python
meta, table_rows, structure_id = ExampleStructure.read("example.txt")

print(meta)
#> {'operator_name': 'Jane Smith', 'country': 'NZ'}

print(table_rows)
#> [{'id': 1, 'time': datetime.time(20, 4, 5), 'value': 2098.0}, {'id': 2,
# 'time': datetime.time(20, 5), 'value': 4328.0}]

print(structure_id)
#> ExampleStructure
```

**What's going on here:**

- The `structure` class attribute contains a definition of the basic file structure. This definition includes the meta data lines and table header lines. Any variable text of interest is replaced with curly brackets and a field name, E.g. `'{operator_name}'`, while any variable text that should be ignored is replaced with empty curly brackets, E.g. `'{}'`. The `structure` definition must contain all spaces, tabs and new line characters in order for a file to successfully match it. The named fields in the `structure` definition will be passed to `meta_model`.

- `meta_model` is simply a [pydantic model](https://pydantic-docs.helpmanual.io/usage/models/) with field names that match the named fields in the `structure` definition. All values sent to `meta_model` will be strings and these will be converted to the field types defined in `meta_model`. Custom [pydantic validators](https://pydantic-docs.helpmanual.io/usage/validators/) can be included in the `meta_model` definition as per standard pydantic models.

- `row_model` is also a [pydantic model](https://pydantic-docs.helpmanual.io/usage/models/). This time the field names do not need to match the header line in the `structure` definition; however, the `row_model` fields do need to be provided in the **same order as the table columns**. This allows the table column names to be customised/standardised where the user does not control the file structure itself. Again, custom [pydantic validators](https://pydantic-docs.helpmanual.io/usage/validators/) can be included in the `row_model` definition if required.


## Another Example

Should the file structure change at some point in the future a new model can be created based on the original model. This is referred to as a *sub-model*, where the original model is the *parent* model.

Given the slightly modified file structure of `new_example.txt`:

```
operator name: Jane Smith
country: NZ
city: Auckland
year: 2022

ID,Time,Duration (sec),Reading
1,20:04:05,12.2,2098
2,20:05:00,2.35,4328
```

Attempting to parse this file using the original `ExampleStructure` model will raise a `PyrsonaError` due to the addition of the `'city: Auckland'` line. In order to successfully parse the file and capture the new `'city'` field the following *sub-model* should be defined.

```python
from pyrsona import BaseStructure
from pydantic import BaseModel
from datetime import time


class NewExampleStructure(ExampleStructure):

    structure = (
        "operator name: {operator_name}\n"
        "country: {country}\n"
        "city: {city}\n"
        "year: {}\n"
        "\n"
        "ID,Time,Duration (sec),Reading\n"
    )

    class meta_model(BaseModel):
        operator_name: str
        country: str
        city: str
```

`ExampleStructure` is still used as the entry point; however, *pyrsona* will attempt to parse the file using any *sub-models* that exist (in this case `NewExampleStructure`) before using `ExampleStructure` itself.

```python
meta, table_rows, structure_id = ExampleStructure.read("new_example.txt")

print(meta)
#> {'operator_name': 'Jane Smith', 'country': 'NZ', 'city': 'Auckland'}

print(table_rows)
#> [{'id': 1, 'time': datetime.time(20, 4, 5), 'value': 2098.0}, {'id': 2,
# 'time': datetime.time(20, 5), 'value': 4328.0}]

print(structure_id)
#> NewExampleStructure
```

**What's going on here:**

- A new *pyrsona* file structure model is defined based on the original `ExampleStructure` model. This mean that `structure`, `meta_model` and `row_model` will be inherited from `ExampleStructure`. This also provides a single entry point (I.e. `ExampleStructure.read()`) when attempting to read the different file versions.

- `structure` and `meta_model` are redefined to include the new `"city: Auckland"` meta data line. Alternatively, the original `meta_model` in `ExampleStructure` could have been updated to include an *optional* `city` field.


## Post-processors

It is sometimes necessary to modify some of the data following parsing by the `meta_model` and `row_model`. Two post-processing methods are available for this purpose.

Using the `ExampleStructure` class above, `meta_postprocessor` and `table_postprocessor` static methods are defined for post-processing the meta data and table_rows, respectively:

```python
class ExampleStructure(BaseStructure):

    # Lines omitted for brevity

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
```

The meta data and table_rows are now run through the post-processing stages before being returned:

 - A new *version* field is added to the meta data.
 - The *id* field is deleted from the table_rows and a cumulative total field is added.

```python
meta, table_rows, structure_id = ExampleStructure.read("example.txt")

print(meta)
#> {'operator_name': 'Jane Smith', 'country': 'NZ', 'version': 3}

print(table_rows)
#> [{'time': datetime.time(20, 4, 5), 'duration_sec': 12.2, 'value': 2098.0,
# 'total': 2098.0}, {'time': datetime.time(20, 5), 'duration_sec': 2.35, 'value': 4328.0,
# 'total': 6426.0}]

print(structure_id)
#> NewExampleStructure
```


## Extra details


### All meta lines MUST be included

While it is possible to effectively add a wildcard using `'{}'` in the structure definition to ignore several lines of the meta section of the file, this can cause a later named field to be included in the wildcard section. *pyrsona* therefore checks for the presence of a new line character `'\n'` in the named fields and fails if one is found.


### Sub-sub-models

Calling the `read()` method will first build a list of *pyrsona* file structure models from the *parent* model down. 

Any *sub-models* of the *parent* model will themselves be checked for *sub-models*, meaning that every model in the tree below the *parent* model will be used when attempting to parse a file.

Each branch of models will be ordered bottom-up so that the deepest nested model in a branch will be used first. The *parent* model will be the final model used if all others fail.

### Model names

The `read()` method returns a `structure_id` variable that matches the model name. This `structure_id` can be useful when creating automated tests that sit alongside the *pyrsona* models as it provide a mechanism for confirming that a text file was parsed using the expected *pyrsona* model where multiple *sub-models* exist.

As the number of *sub-models* grows a naming convention becomes more important. One option is to set the names of any `sub-models` to a random hexadecimal value prefixed with a single underscore (in case the value begins with a number), E.g. `'_a4c15356'`. The initial underscore will be removed from model name when returning the `structure_id` value.


### *parse* formats

The *parse* package allows format specifications to be included alongside the fields, E.g. `'{year:d}'`. While including these format types in the structure definition is valid, more complex format conversions can be made using `meta_model`. Keeping all format conversions in `meta_model` means that all conversions are defined in one place.