__version__ = "0.2"

import os
import psutil

import numpy as np

from multiprocessing import cpu_count
from parse import parse
from pathlib import Path
from platform import system
from pydantic import BaseModel, ValidationError
from typing import Union, Optional, List
from unsync import unsync
from uuid import uuid4


CPU_COUNT = cpu_count()
OS = system()


class BaseStructure:

    structure = ""  # Data structure string (as per the "parse" package)

    class meta_model(BaseModel):
        """
        Meta data Pydantic model.
        """
        pass

    class row_model(BaseModel):
        """
        Table row Pydantic model.
        """
        pass

    @staticmethod
    def meta_postprocessor(meta: dict) -> dict:
        """
        Meta data postprocessor.
        This method is used to modify the meta data following parsing by `meta_model`. A
        possible use case is combining 'date' and 'time' meta data fields into a single 
        'datetime' field.
        """
        return meta

    @staticmethod
    def table_postprocessor(table_rows: List[dict], meta: dict = {}) -> List[dict]:
        """
        Table post-processor.
        This method is used as a final step before the table rows are returned. It allows
        modification of the table data when knowledge all of the table data and/or meta
        data is required. For changes to table rows that don't require knowledge of the
        full table use a custom validator attached to `row_model`.
        """
        return table_rows

    @classmethod
    def _extract_meta(cls, data: str) -> dict:
        """
        Extract the meta data from the data sting.
        The meta data is run through meta_postprocessor before being returned.
        """
        parsed = parse(cls.structure + "{}", data)
        if parsed is None:
            return None

        if any(("\n" in vv for vv in parsed.named.values())):
            return None

        return parsed.named

    @classmethod
    def _extract_table(
        cls, data: str, meta: Optional[dict] = None, parallel: bool = True,
    ) -> dict:
        """
        Extract the table rows from the data string.
        """
        parsed = parse(cls.structure + "{}", data)
        if parsed is None:
            return None

        # Extract table data from the last unnamed parameter in structure and
        # convert to list of dicts using the row_model fields as the keys:
        table_data = parsed.fixed[-1]
        table_data = [row.split(",") for row in tab_to_comma(table_data).split("\n")]
        table_rows = [dict(zip(cls.row_model.__fields__, row)) for row in table_data]

        return table_rows

    @classmethod
    def _validate_meta(cls, meta):
        """
        Validate the meta data using meta_model.
        """
        return cls.meta_model(**meta).dict(exclude_unset=True)

    @classmethod
    def _validate_table(cls, table_rows, parallel=True):
        """
        Validate the table rows using row_model.
        """
        return validate_table_rows(
            cls.row_model, table_rows, exclude_unset=True, parallel=parallel,
        )

    @classmethod
    @property
    def children(cls) -> list:
        """
        List of data structure classes derived from this parent class.
        """
        return cls.__subclasses__()

    @classmethod
    def get_structures(cls):
        """
        Return all parent and child pyrsona file structure models.
        """
        if len(cls.children) == 0:
            return [cls]
        temp = [cc.get_structures() for cc in cls.children]
        return [ii for ss in temp for ii in ss] + [cls]

    @classmethod
    @property
    def id(cls) -> str:
        """
        Data structure ID.
        """
        return cls.__name__.split("_")[-1]

    @staticmethod
    def _read_data_from_file(path: Union[str, Path]):
        with open(path, "r") as f:
            data = f.read()
        return data

    @classmethod
    def read(cls, path: Union[str, Path], parallel: bool = False):
        data = cls._read_data_from_file(path)

        # Loop over all data structure subclasses and attempt to parse data:
        for structure in cls.get_structures():
            meta = structure._extract_meta(data)
            if meta is None:
                continue

            # Validate and post-process meta:
            meta = structure._validate_meta(meta)
            meta = structure.meta_postprocessor(meta)

            table_rows = structure._extract_table(data, meta)
            try:
                table_rows = structure._validate_table(table_rows, parallel)
            except ValidationError:
                table_rows = None
                continue

            table_rows = structure.table_postprocessor(table_rows, meta)
            break

        # Raise DataStructureError if unable to parse:
        if (meta is None) or (table_rows is None):
            raise PyrsonaError(
                "Unable to parse data using an existing file structure model. You "
                "may need to add a structure model if one does not exist for the current "
                "file."
            )

        return (meta, table_rows, structure.id)


class PyrsonaError(Exception):
    pass


def unpack_results(tasks):
    return [rr for tt in tasks for rr in tt.result()]


def limit_cpu():
    p = psutil.Process(os.getpid())
    if OS == "Windows":
        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    else:
        p.nice(19)


@unsync(cpu_bound=True)
def call_row_model(row_model, rows, exclude_unset=False):
    limit_cpu()
    return [row_model(**row).dict(exclude_unset=exclude_unset) for row in rows]


@unsync(cpu_bound=True)
def call_row_preprocessor(row_preprocessor, rows):
    limit_cpu()
    return [row_preprocessor(row) for row in rows]


def validate_table_rows(row_model, table_rows, exclude_unset=False, parallel=True):
    if parallel:
        tasks = [
            call_row_model(row_model, rows.tolist(), exclude_unset)
            for rows in np.array_split(table_rows, CPU_COUNT)
        ]
        return unpack_results(tasks)
    return [row_model(**row).dict(exclude_unset=exclude_unset) for row in table_rows]


def preprocess_table_rows(row_preprocessor, table_rows, parallel=True):
    if parallel:
        tasks = [
            call_row_preprocessor(row_preprocessor, rows.tolist())
            for rows in np.array_split(table_rows, CPU_COUNT)
        ]
        return unpack_results(tasks)
    return [row_preprocessor(row) for row in table_rows]


def tab_to_comma(contents):
    return ",".join(contents.split("\t"))


def generate_hex():
    return uuid4().hex[:8]
