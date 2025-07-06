from decimal import Decimal
from typing import (
    Literal,
    Any,
    Mapping,
    Iterable,
    TextIO
)

import csv


def get_columns_rows_from_csv(
        file: TextIO
) -> tuple[list[str], list[list[str]]]:
    reader = csv.reader(file)
    columns: list[str] = next(reader)
    rows = list(reader)

    return columns, rows


def get_rows_filtered_by(
        sign: Literal[">", "<", "="],
        rows: Iterable[list[Any]],
        filter_condition: str,
        indices_columns: Mapping[str, int]
) -> list[list[Any]]:
    filtered_rows = []
    column_name, value_filter = filter_condition.split(sign)
    for row in rows:
        index_column = indices_columns[column_name]
        if sign == ">" and Decimal(row[index_column]) > Decimal(value_filter):
            filtered_rows.append(row)
        if sign == "<" and Decimal(row[index_column]) < Decimal(value_filter):
            filtered_rows.append(row)
        if sign == "=" and value_filter.isdigit() and Decimal(row[index_column]) == Decimal(value_filter):
            filtered_rows.append(row)
        elif sign == "=" and row[index_column] == value_filter:
            filtered_rows.append(row)
    return filtered_rows


def use_mode(
        column: str,
        mode_: Literal["max", "min"],
        rows_: Iterable[list[Any]],
        indices_columns: Mapping[str, int],
) -> tuple[list[list[Any]], list[str]]:
    modes_as_functions = {
        "min": min,
        "max": max
    }
    column_values = [
        Decimal(row[indices_columns[column]])
        for row in rows_
    ]
    filtered_rows = modes_as_functions[mode_](column_values)
    return [[filtered_rows]], [mode_]


